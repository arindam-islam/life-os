#!/usr/bin/env python3
"""
Adversarial Unit & Regression Test Suite for Life OS Release State Machine (Hardened).
Verifies strict role enforcement, git/worktree verification, structured verification receipts,
staging isolation, independent QA digest checking, post-deployment runtime receipts, and rollback safety.
"""

import unittest
import copy
import json
import os
import sys

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

from scripts.release_state_machine import (
    validate_schema_hardened,
    validate_release_candidate,
    validate_rollback_plan,
    GATE_ORDER
)


class TestReleaseStateMachineHardened(unittest.TestCase):

    def setUp(self):
        self.valid_candidate = {
            "release_id": "REL-20260812-a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
            "commit_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
            "target_track": "Track G (Security & Audit)",
            "release_status": "PASSED",
            "rollback_plan": {
                "previous_version": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
                "bounded_commands": ["docker compose up -d --no-deps youtube-enricher"],
                "recovery_reference": "/home/ubuntu/projects/n8n/.life-os-backups/backup-a1b2c3d",
                "verification_steps": ["curl -f http://127.0.0.1:8080/health"],
                "safe_to_execute": True
            },
            "gates": {
                "dev": {
                    "status": "PASSED",
                    "timestamp": "2026-08-12T10:00:00+00:00",
                    "responsible_role": "Engineering Agent",
                    "evidence": {"commit_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"},
                    "notes": "Dev completed"
                },
                "test": {
                    "status": "PASSED",
                    "timestamp": "2026-08-12T10:05:00+00:00",
                    "responsible_role": "QA / Verification Agent",
                    "evidence": {
                        "test_receipt": {
                            "command": "python3 -m unittest discover -s tests -v",
                            "result": "PASSED",
                            "commit_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
                            "timestamp": "2026-08-12T10:05:00+00:00",
                            "artifact_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                        }
                    },
                    "notes": "Tests passed"
                },
                "security": {
                    "status": "PASSED",
                    "timestamp": "2026-08-12T10:10:00+00:00",
                    "responsible_role": "Security & Reliability Reviewer",
                    "evidence": {
                        "security_receipt": {
                            "check_identity": "secret_leak_and_saif_audit",
                            "result": "PASSED",
                            "secret_scan": "CLEAN",
                            "commit_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
                            "timestamp": "2026-08-12T10:10:00+00:00"
                        }
                    },
                    "notes": "Security clean"
                },
                "staging": {
                    "status": "PASSED",
                    "timestamp": "2026-08-12T10:15:00+00:00",
                    "responsible_role": "CTO / Architecture Agent",
                    "evidence": {
                        "environment_id": "staging-isolated-01",
                        "synthetic_data": True,
                        "sanitized_data": True,
                        "acceptance_receipt": {
                            "command": "run_staging_acceptance.sh",
                            "result": "PASSED",
                            "commit_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
                            "artifact_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                        }
                    },
                    "notes": "Staging isolated test passed"
                },
                "qa": {
                    "status": "PASSED",
                    "timestamp": "2026-08-12T10:20:00+00:00",
                    "responsible_role": "QA / Verification Agent",
                    "evidence": {
                        "commit_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
                        "staged_artifact_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                        "verification_receipt": {
                            "acceptance_verification": "VERIFIED_CORRECT",
                            "timestamp": "2026-08-12T10:20:00+00:00"
                        }
                    },
                    "notes": "QA approved"
                },
                "production": {
                    "status": "PASSED",
                    "timestamp": "2026-08-12T10:25:00+00:00",
                    "responsible_role": "Orchestrator / Chief of Staff",
                    "evidence": {
                        "post_deployment_runtime_receipt": {
                            "runtime_health": "HEALTHY",
                            "commit_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
                            "artifact_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                            "timestamp": "2026-08-12T10:25:00+00:00"
                        }
                    },
                    "notes": "Deployed and verified live"
                }
            }
        }

    def test_valid_candidate_passes_all_checks(self):
        errs = validate_release_candidate(self.valid_candidate)
        self.assertEqual(errs, [], f"Valid candidate failed validation: {errs}")

    def test_adversarial_product_owner_passing_technical_gates_rejection(self):
        roles_to_test = [("security", "Product Owner"), ("qa", "Product Owner"), ("staging", "Founder")]
        for g_name, po_role in roles_to_test:
            cand = copy.deepcopy(self.valid_candidate)
            cand["gates"][g_name]["responsible_role"] = po_role
            errs = validate_release_candidate(cand)
            self.assertTrue(
                any("Product Owner" in e or "not permitted" in e for e in errs),
                f"State machine must reject Product Owner / Founder passing technical gate '{g_name}'"
            )

    def test_adversarial_placeholder_rollback_rejection(self):
        bad_commands = [
            ["true"],
            ["git checkout ."],
            ["git checkout HEAD -- ."],
            ["git reset --hard"],
            ["docker compose down"],
            ["docker-compose down"],
            ["rm -rf /"],
            ["docker compose up -d --build"]
        ]
        for bad_cmd in bad_commands:
            rb = {
                "previous_version": "v1.0",
                "bounded_commands": bad_cmd,
                "recovery_reference": "ref",
                "verification_steps": ["curl"],
                "safe_to_execute": True
            }
            errs = validate_rollback_plan(rb)
            self.assertTrue(
                len(errs) > 0,
                f"State machine must reject prohibited/placeholder rollback command: {bad_cmd}"
            )

    def test_adversarial_staging_without_isolated_env_or_synthetic_data_rejection(self):
        cand = copy.deepcopy(self.valid_candidate)
        cand["gates"]["staging"]["evidence"]["environment_id"] = "NONE"
        errs = validate_release_candidate(cand)
        self.assertTrue(
            any("verified isolated environment_id" in e for e in errs),
            "Staging gate must reject environment_id='NONE'"
        )

        cand2 = copy.deepcopy(self.valid_candidate)
        cand2["gates"]["staging"]["evidence"]["synthetic_data"] = False
        errs2 = validate_release_candidate(cand2)
        self.assertTrue(
            any("synthetic_data=true" in e for e in errs2),
            "Staging gate must reject synthetic_data=false"
        )

    def test_adversarial_qa_without_independent_receipt_or_digest_mismatch_rejection(self):
        cand = copy.deepcopy(self.valid_candidate)
        cand["gates"]["qa"]["evidence"]["staged_artifact_digest"] = "mismatched_digest_12345"
        errs = validate_release_candidate(cand)
        self.assertTrue(
            any("matching staged_artifact_digest" in e for e in errs),
            "QA gate must reject mismatched staged_artifact_digest"
        )

        cand2 = copy.deepcopy(self.valid_candidate)
        cand2["gates"]["qa"]["evidence"].pop("verification_receipt")
        errs2 = validate_release_candidate(cand2)
        self.assertTrue(
            any("verification_receipt" in e for e in errs2),
            "QA gate must reject missing verification_receipt"
        )

    def test_adversarial_production_without_runtime_receipt_rejection(self):
        cand = copy.deepcopy(self.valid_candidate)
        cand["gates"]["production"]["evidence"]["post_deployment_runtime_receipt"]["runtime_health"] = "UNHEALTHY"
        errs = validate_release_candidate(cand)
        self.assertTrue(
            any("runtime_health=HEALTHY" in e for e in errs),
            "Production gate must reject post-deployment receipt with runtime_health!=HEALTHY"
        )


if __name__ == "__main__":
    unittest.main()
