#!/usr/bin/env python3
"""
Life OS Permanent Release State Machine CLI & Engine (Hardened)
Gate Lifecycle: Dev -> Test -> Security -> Staging -> QA -> Production

Enforces strict role binding, exact git commit & clean worktree verification,
structured verification receipts, isolated staging verification with synthetic/sanitized data,
independent QA digest verification, post-deployment runtime verification, and
bounded, non-destructive rollback plans.
"""

import sys
import os
import json
import argparse
import datetime
import re
import subprocess
import hashlib

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "releases", "release_ledger.json")
SCHEMA_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "schemas", "release_schema.json")

GATE_ORDER = ["dev", "test", "security", "staging", "qa", "production"]

ALLOWED_ROLES_PER_GATE = {
    "dev": ["Engineering Agent"],
    "test": ["QA / Verification Agent", "Engineering Agent"],
    "security": ["Security & Reliability Reviewer"],
    "staging": ["CTO / Architecture Agent"],
    "qa": ["QA / Verification Agent"],
    "production": ["Orchestrator / Chief of Staff"]
}

VALID_STATUSES = ["NOT_STARTED", "IN_PROGRESS", "PASSED", "FAILED", "BLOCKED"]
VALID_RELEASE_STATUSES = ["DRAFT", "IN_PROGRESS", "BLOCKED", "PASSED", "INVALID"]

PROHIBITED_ROLLBACK_PATTERNS = [
    r"^\s*true\s*$",
    r"git\s+checkout\s+\.\s*$",
    r"git\s+checkout\s+HEAD\s+--\s+\.\s*$",
    r"git\s+reset",
    r"docker\s+compose\s+down",
    r"docker-compose\s+down",
    r"rm\s+-rf",
    r"docker\s+compose\s+up\s+-d\s+--build\s*$"
]


def load_ledger(path=LEDGER_PATH):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ledger(data, path=LEDGER_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def check_git_commit_and_worktree(commit_sha):
    """
    Verifies git invariants:
    1. Commit SHA exists in git history.
    2. Local HEAD matches commit SHA.
    3. Git worktree is completely clean.
    """
    errors = []
    try:
        res_verify = subprocess.run(
            ["git", "rev-parse", "--verify", f"{commit_sha}^{{commit}}"],
            cwd=WORKSPACE_ROOT, capture_output=True, text=True
        )
        if res_verify.returncode != 0:
            errors.append(f"Git commit {commit_sha} does not exist in local repository history.")

        res_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=WORKSPACE_ROOT, capture_output=True, text=True
        )
        current_head = res_head.stdout.strip()
        if current_head != commit_sha:
            errors.append(f"Repository HEAD ({current_head[:7]}) does not match candidate commit ({commit_sha[:7]}).")

        res_status = subprocess.run(
            ["git", "status", "--porcelain", "--", ":(exclude).life-os/", ":(exclude)staging/receipts/"],
            cwd=WORKSPACE_ROOT, capture_output=True, text=True
        )
        if res_status.stdout.strip():
            errors.append("Repository worktree has uncommitted code changes outside runtime state storage.")
    except Exception as ex:
        errors.append(f"Failed executing git verification: {ex}")

    return errors


def validate_rollback_plan(rollback_plan):
    errors = []
    if not isinstance(rollback_plan, dict):
        return ["rollback_plan must be an object."]

    for req_field in ["previous_version", "bounded_commands", "recovery_reference", "verification_steps", "safe_to_execute"]:
        if req_field not in rollback_plan:
            errors.append(f"rollback_plan missing required field: '{req_field}'.")

    if "previous_version" in rollback_plan and not str(rollback_plan["previous_version"]).strip():
        errors.append("rollback_plan.previous_version cannot be empty.")

    if "recovery_reference" in rollback_plan and not str(rollback_plan["recovery_reference"]).strip():
        errors.append("rollback_plan.recovery_reference cannot be empty.")

    if "safe_to_execute" in rollback_plan and not rollback_plan["safe_to_execute"]:
        errors.append("rollback_plan.safe_to_execute must be true.")

    commands = rollback_plan.get("bounded_commands", [])
    if not isinstance(commands, list) or len(commands) == 0:
        errors.append("rollback_plan.bounded_commands must be a non-empty array.")
    else:
        for cmd in commands:
            for pattern in PROHIBITED_ROLLBACK_PATTERNS:
                if re.search(pattern, str(cmd)):
                    errors.append(f"Prohibited/placeholder rollback command detected: '{cmd}'.")

    v_steps = rollback_plan.get("verification_steps", [])
    if not isinstance(v_steps, list) or len(v_steps) == 0:
        errors.append("rollback_plan.verification_steps must be a non-empty array.")

    return errors


def validate_schema_hardened(candidate):
    errors = []
    if not isinstance(candidate, dict):
        return ["Candidate must be a JSON object."]

    for req in ["release_id", "commit_sha", "target_track", "release_status", "rollback_plan", "gates"]:
        if req not in candidate:
            errors.append(f"Missing required top-level field: '{req}'.")

    if "commit_sha" in candidate and not re.match(r"^[a-f0-9]{40}$", candidate["commit_sha"]):
        errors.append(f"Invalid 40-character commit_sha: '{candidate.get('commit_sha')}'")

    if "release_status" in candidate and candidate["release_status"] not in VALID_RELEASE_STATUSES:
        errors.append(f"Invalid release_status: '{candidate.get('release_status')}'")

    if "rollback_plan" in candidate:
        errors.extend(validate_rollback_plan(candidate["rollback_plan"]))

    if "gates" in candidate:
        gates = candidate["gates"]
        if not isinstance(gates, dict):
            errors.append("gates must be an object.")
        else:
            for g_name in GATE_ORDER:
                if g_name not in gates:
                    errors.append(f"Missing gate in gates object: '{g_name}'.")
                    continue
                gate = gates[g_name]
                if not isinstance(gate, dict):
                    errors.append(f"Gate '{g_name}' must be an object.")
                    continue
                for g_field in ["status", "timestamp", "responsible_role", "evidence", "notes"]:
                    if g_field not in gate:
                        errors.append(f"Gate '{g_name}' missing field: '{g_field}'.")

                role = gate.get("responsible_role")
                if role == "Product Owner" or role == "Founder":
                    errors.append(f"REJECTED: Product Owner / Founder cannot act as technical role for gate '{g_name}'.")

                allowed_roles = ALLOWED_ROLES_PER_GATE.get(g_name, [])
                if role not in allowed_roles:
                    errors.append(f"REJECTED: Role '{role}' is not permitted for gate '{g_name}'. Must be one of {allowed_roles}.")

    return errors


def validate_release_candidate(candidate, check_git=False):
    errors = validate_schema_hardened(candidate)
    if errors:
        return errors

    commit_sha = candidate["commit_sha"]
    gates = candidate["gates"]

    # Invariant 1: Sequential Gate Dependencies
    passed_so_far = True
    for idx, g_name in enumerate(GATE_ORDER):
        gate = gates[g_name]
        status = gate["status"]

        if status == "PASSED":
            if not passed_so_far:
                prev_name = GATE_ORDER[idx - 1]
                errors.append(f"FAIL-CLOSED: Gate '{g_name}' is PASSED, but preceding gate '{prev_name}' is not PASSED.")

            # Hardened Evidence Check for PASSED gates
            ev = gate.get("evidence", {})
            if g_name == "test":
                t_receipt = ev.get("test_receipt", {})
                if not t_receipt.get("command") or not t_receipt.get("result") or t_receipt.get("commit_sha") != commit_sha:
                    errors.append("FAIL-CLOSED: Test gate PASSED requires valid test_receipt matching commit SHA.")
            elif g_name == "security":
                s_receipt = ev.get("security_receipt", {})
                if not s_receipt.get("check_identity") or s_receipt.get("secret_scan") != "CLEAN" or s_receipt.get("commit_sha") != commit_sha:
                    errors.append("FAIL-CLOSED: Security gate PASSED requires valid security_receipt with secret_scan=CLEAN matching commit SHA.")
            elif g_name == "staging":
                env_id = ev.get("environment_id")
                syn_data = ev.get("synthetic_data")
                san_data = ev.get("sanitized_data")
                acc_receipt = ev.get("acceptance_receipt", {})
                if not env_id or env_id == "NONE" or not syn_data or not san_data or not acc_receipt.get("commit_sha"):
                    errors.append("FAIL-CLOSED: Staging gate PASSED requires verified isolated environment_id, synthetic_data=true, sanitized_data=true, and acceptance_receipt.")
            elif g_name == "qa":
                staged_digest = gates["staging"].get("evidence", {}).get("acceptance_receipt", {}).get("artifact_digest")
                qa_digest = ev.get("staged_artifact_digest")
                qa_receipt = ev.get("verification_receipt", {})
                if not qa_digest or (staged_digest and qa_digest != staged_digest) or ev.get("commit_sha") != commit_sha or not qa_receipt:
                    errors.append("FAIL-CLOSED: QA gate PASSED requires independent verification_receipt matching staged_artifact_digest and commit SHA.")
            elif g_name == "production":
                rt_receipt = ev.get("post_deployment_runtime_receipt", {})
                qa_digest = gates["qa"].get("evidence", {}).get("staged_artifact_digest")
                if not rt_receipt or rt_receipt.get("runtime_health") != "HEALTHY" or rt_receipt.get("commit_sha") != commit_sha or (qa_digest and rt_receipt.get("artifact_digest") != qa_digest):
                    errors.append("FAIL-CLOSED: Production gate PASSED requires post_deployment_runtime_receipt with runtime_health=HEALTHY matching QA artifact digest and commit SHA.")

        elif status in ["FAILED", "BLOCKED", "NOT_STARTED", "IN_PROGRESS"]:
            passed_so_far = False

    # Optional Git Worktree Enforcement for Test and later gates
    if check_git:
        any_test_or_later = any(gates[g]["status"] == "PASSED" for g in ["test", "security", "staging", "qa", "production"])
        if any_test_or_later:
            git_errs = check_git_commit_and_worktree(commit_sha)
            errors.extend(git_errs)

    return errors


def cmd_init(args):
    ledger = load_ledger()
    commit_sha = args.sha
    if not re.match(r"^[a-f0-9]{40}$", commit_sha):
        print(f"Error: Invalid 40-character commit SHA '{commit_sha}'", file=sys.stderr)
        sys.exit(1)

    release_id = args.release_id or f"REL-{datetime.datetime.now().strftime('%Y%m%d')}-{commit_sha[:7]}"

    for entry in ledger:
        if entry["release_id"] == release_id:
            print(f"Error: Release ID '{release_id}' already exists.", file=sys.stderr)
            sys.exit(1)

    now_iso = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

    new_release = {
        "release_id": release_id,
        "commit_sha": commit_sha,
        "target_track": args.track,
        "release_status": "DRAFT",
        "rollback_plan": {
            "previous_version": args.prev_version or commit_sha,
            "bounded_commands": [args.rollback_command] if args.rollback_command else [f"docker compose up -d --no-deps service"],
            "recovery_reference": args.recovery_ref or f"/home/ubuntu/projects/n8n/.life-os-backups/backup-{commit_sha[:7]}",
            "verification_steps": [args.verify_step] if args.verify_step else ["python3 scripts/release_state_machine.py validate"],
            "safe_to_execute": True
        },
        "gates": {
            "dev": {
                "status": "IN_PROGRESS",
                "timestamp": now_iso,
                "responsible_role": "Engineering Agent",
                "evidence": {"commit_sha": commit_sha, "track": args.track},
                "notes": "Development candidate initialized in DRAFT state."
            },
            "test": {
                "status": "NOT_STARTED",
                "timestamp": None,
                "responsible_role": "QA / Verification Agent",
                "evidence": {},
                "notes": ""
            },
            "security": {
                "status": "NOT_STARTED",
                "timestamp": None,
                "responsible_role": "Security & Reliability Reviewer",
                "evidence": {},
                "notes": ""
            },
            "staging": {
                "status": "BLOCKED",
                "timestamp": now_iso,
                "responsible_role": "CTO / Architecture Agent",
                "evidence": {"environment_id": "NONE", "synthetic_data": False, "sanitized_data": False},
                "notes": "No isolated staging environment provisioned. Fail-closed per policy."
            },
            "qa": {
                "status": "NOT_STARTED",
                "timestamp": None,
                "responsible_role": "QA / Verification Agent",
                "evidence": {},
                "notes": ""
            },
            "production": {
                "status": "NOT_STARTED",
                "timestamp": None,
                "responsible_role": "Orchestrator / Chief of Staff",
                "evidence": {},
                "notes": ""
            }
        }
    }

    errs = validate_release_candidate(new_release)
    if errs:
        print("Initialization failed state validation:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    ledger.append(new_release)
    save_ledger(ledger)
    print(f"Successfully initialized release candidate: {release_id} (Status: DRAFT)")


def cmd_advance(args):
    ledger = load_ledger()
    target = None
    for entry in ledger:
        if entry["release_id"] == args.release_id:
            target = entry
            break

    if not target:
        print(f"Error: Release ID '{args.release_id}' not found.", file=sys.stderr)
        sys.exit(1)

    gate_name = args.gate.lower()
    if gate_name not in GATE_ORDER:
        print(f"Error: Invalid gate name '{args.gate}'. Must be one of {GATE_ORDER}", file=sys.stderr)
        sys.exit(1)

    target_status = args.status.upper()
    if target_status not in VALID_STATUSES:
        print(f"Error: Invalid status '{args.status}'. Must be one of {VALID_STATUSES}", file=sys.stderr)
        sys.exit(1)

    allowed_roles = ALLOWED_ROLES_PER_GATE.get(gate_name, [])
    if args.role not in allowed_roles:
        print(
            f"REJECTED: Role '{args.role}' is not authorized to transition gate '{gate_name}'. Authorized roles: {allowed_roles}",
            file=sys.stderr
        )
        sys.exit(1)

    # Parse evidence
    evidence = {}
    if args.evidence:
        if os.path.exists(args.evidence):
            with open(args.evidence, "r", encoding="utf-8") as ef:
                evidence = json.load(ef)
        else:
            try:
                evidence = json.loads(args.evidence)
            except Exception as e:
                print(f"Error parsing evidence JSON: {e}", file=sys.stderr)
                sys.exit(1)

    # Git commit and worktree check for Test and later gates
    if target_status == "PASSED" and gate_name in ["test", "security", "staging", "qa", "production"]:
        git_errs = check_git_commit_and_worktree(target["commit_sha"])
        if git_errs:
            print(f"FAIL-CLOSED REJECTION for gate '{gate_name}': Git commit/worktree check failed:", file=sys.stderr)
            for ge in git_errs:
                print(f"  - {ge}", file=sys.stderr)
            sys.exit(1)

    now_iso = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

    target["gates"][gate_name] = {
        "status": target_status,
        "timestamp": now_iso,
        "responsible_role": args.role,
        "evidence": evidence,
        "notes": args.notes or ""
    }

    # Update overall release status
    if any(target["gates"][g]["status"] in ["FAILED", "BLOCKED"] for g in GATE_ORDER):
        target["release_status"] = "BLOCKED"
    elif all(target["gates"][g]["status"] == "PASSED" for g in GATE_ORDER):
        target["release_status"] = "PASSED"
    elif target["gates"]["dev"]["status"] == "PASSED":
        target["release_status"] = "IN_PROGRESS"
    else:
        target["release_status"] = "DRAFT"

    errs = validate_release_candidate(target)
    if errs:
        print(f"Gate transition rejected by state machine for release '{args.release_id}':", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    save_ledger(ledger)
    print(f"Successfully updated release '{args.release_id}' gate '{gate_name}' -> {target_status}")


def cmd_validate(args):
    ledger = load_ledger()
    if not ledger:
        print("Release ledger is empty.")
        return

    total_errs = 0
    selected = ledger
    if args.release_id:
        selected = [e for e in ledger if e["release_id"] == args.release_id]
        if not selected:
            print(f"Error: Release ID '{args.release_id}' not found.", file=sys.stderr)
            sys.exit(1)

    for entry in selected:
        rel_id = entry.get("release_id", "UNKNOWN")
        errs = validate_release_candidate(entry, check_git=args.check_git)
        if errs:
            total_errs += len(errs)
            print(f"❌ INVALID RELEASE: {rel_id} (Status: {entry.get('release_status', 'UNKNOWN')})")
            for e in errs:
                print(f"   - {e}")
        else:
            print(f"✅ VALID RELEASE RECORD: {rel_id} (Status: {entry.get('release_status')}, Commit: {entry['commit_sha'][:7]})")

    if total_errs > 0:
        print(f"\nValidation failed with {total_errs} total error(s).", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nAll release ledger entries validated successfully.")


def cmd_status(args):
    ledger = load_ledger()
    if not ledger:
        print("No releases found in ledger.")
        return

    print("=" * 115)
    print(f"{'RELEASE ID':<42} | {'STATE':<10} | {'COMMIT SHA':<10} | {'GATES SUMMARY'}")
    print("=" * 115)

    status_symbols = {
        "PASSED": "🟢",
        "IN_PROGRESS": "🟡",
        "FAILED": "🔴",
        "BLOCKED": "⛔",
        "NOT_STARTED": "⚪"
    }

    for entry in ledger:
        if args.release_id and entry["release_id"] != args.release_id:
            continue
        rel_id = entry["release_id"]
        rel_state = entry.get("release_status", "UNKNOWN")[:10]
        sha = entry.get("commit_sha", "")[:7]

        gate_str_parts = []
        for g_name in GATE_ORDER:
            st = entry["gates"][g_name]["status"]
            sym = status_symbols.get(st, "❓")
            gate_str_parts.append(f"{g_name.capitalize()}:{sym}")

        gate_summary = " ".join(gate_str_parts)
        print(f"{rel_id:<42} | {rel_state:<10} | {sha:<10} | {gate_summary}")

    print("=" * 115)
    print("Legend: 🟢 PASSED | 🟡 IN_PROGRESS | 🔴 FAILED | ⛔ BLOCKED | ⚪ NOT_STARTED")
    print("Sequential Order: Dev → Test → Security → Staging → QA → Production")


def main():
    parser = argparse.ArgumentParser(description="Life OS Release State Machine Engine (Hardened)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init command
    p_init = subparsers.add_parser("init", help="Initialize a new release candidate")
    p_init.add_argument("--sha", required=True, help="40-character Git commit SHA")
    p_init.add_argument("--track", required=True, help="Target execution track")
    p_init.add_argument("--release-id", help="Optional explicit Release ID")
    p_init.add_argument("--prev-version", help="Previous known good version commit or release ID")
    p_init.add_argument("--rollback-command", help="Explicit bounded rollback command")
    p_init.add_argument("--recovery-ref", help="Recovery backup reference path or URI")
    p_init.add_argument("--verify-step", help="Post-rollback verification command")
    p_init.set_defaults(func=cmd_init)

    # Advance command
    p_adv = subparsers.add_parser("advance", help="Advance or set gate status")
    p_adv.add_argument("--release-id", required=True, help="Release ID")
    p_adv.add_argument("--gate", required=True, help="Gate name (dev, test, security, staging, qa, production)")
    p_adv.add_argument("--status", required=True, help="Gate status (PASSED, FAILED, BLOCKED, IN_PROGRESS, NOT_STARTED)")
    p_adv.add_argument("--role", required=True, help="Responsible role")
    p_adv.add_argument("--evidence", help="JSON string or path to JSON file containing evidence")
    p_adv.add_argument("--notes", help="Gate notes or description")
    p_adv.set_defaults(func=cmd_advance)

    # Validate command
    p_val = subparsers.add_parser("validate", help="Validate release ledger against fail-closed state machine rules")
    p_val.add_argument("--release-id", help="Optional specific Release ID to validate")
    p_val.add_argument("--check-git", action="store_true", help="Perform live git commit and clean worktree checks")
    p_val.set_defaults(func=cmd_validate)

    # Status command
    p_stat = subparsers.add_parser("status", help="Show release state machine status")
    p_stat.add_argument("--release-id", help="Optional specific Release ID")
    p_stat.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
