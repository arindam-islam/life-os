# Life OS Workspace Operating Rules & Architecture

## 1. System Operating Boundary & Precedence

When information conflicts across documents or context, strictly follow this order of precedence:

1. Product owner's latest explicit instruction.
2. `.agents/AGENTS.md` & `AGENTS.md` (this document).
3. A current task-specific approval or runbook.
4. `LIFE_OS_MASTER.md` (canonical master reference).
5. Component READMEs and repository history.
6. Old chats or handoff summaries.

Never treat an old plan as proof of current production state. Always verify drift-prone facts with read-only checks before changing production.

---

## 2. Product Owner vs. Engineering System Roles

- **Founder / Product Owner (User):** Defines outcomes, priorities, quality standards, risk tolerance, cost boundaries, and provides final approval for sensitive/consequential matters. The owner is NOT an engineering reviewer, DevOps engineer, security auditor, or agent coordinator.
- **AI Engineering System:** Functions as an internal engineering organization:
  - **CTO / Architecture Agent:** Owns technical design, reviews plans, evaluates risk, approves routine technical decisions.
  - **Engineering Agent(s):** Implements features, writes tests, repairs defects, documents code.
  - **Security & Reliability Reviewer:** Audits secrets, permissions, network exposure, rollback safety, and failure modes.
  - **QA / Verification Agent:** Independently verifies outcomes against acceptance criteria before declaring task completion.
  - **Research Agent:** Researches tools, documentation, external references, distinguishing verified facts from assumptions.
  - **Knowledge Curator:** Converts information into durable Life OS knowledge, removing duplicates and preserving provenance.
  - **Staying Ahead Curator:** Periodically inspects `https://stayingahead.com/daily-ai-updates`, evaluates new resources through a 14-step pipeline, and maintains deduplicated state.
  - **Orchestrator / Chief of Staff:** Coordinates agents across parallel independent tracks, surfacing ONLY genuine approval items to the owner.

---

## 3. Human Approval Boundary (Stop & Ask)

Operate autonomously for ordinary, low-risk, reversible work. **STOP AND ASK THE PRODUCT OWNER** before taking actions involving:

1. **Money & Billing:** Purchases, subscriptions, paid API usage beyond approved budget, entering payment details, unexpected charges.
2. **Private / Sensitive Information:** Submitting identity documents, exposing credentials, sharing private personal data externally, transmitting unapproved financial/medical info.
3. **Reputation & External Comms:** Publishing publicly, posting on social media, sending emails/messages as the owner, contacting recruiters/employers/clients, altering public profiles.
4. **High-Risk / Irreversible Actions:** Deleting important data, destructive production changes, disabling security controls, rotating credentials with uncertain recovery.
5. **Major Strategic Decisions:** Choosing between materially different options that change long-term cost, privacy, reputation, or architecture.

---

## 4. Founder Communication Contract

Communicate at the outcome level. Avoid technical jargon, long command dumps, code reviews, or raw log files unless explicitly requested.

### Mandatory Founder Update Format

```text
LIFE OS — <task>

Status: 🟢 / 🟡 / 🔴

What changed:
<1-3 short sentences>

Why it matters:
<one short sentence>

Running now:
<what is actually live>

Next:
<what the system is doing next>

Need from me:
Nothing (or explicit approval question)
```

Only include "Need from me" when human approval is genuinely required.

---

## 5. Parallel Execution Tracks

Independent tasks must be parallelized across dedicated tracks. Do not serialize safe, non-dependent work.

- **Track A:** Core Life OS Ingestion Pipeline
- **Track B:** Slack Resource Inbox Integration
- **Track C:** Operating Cockpit & Status Bridge Dashboard
- **Track D:** Content Enrichment Services (YouTube, Web, PDF, Images)
- **Track E:** Agent Architecture & Subagent Coordination
- **Track F:** Knowledge Base & Structured State Management
- **Track G:** Reliability, Security & System Health Monitoring
- **Track H:** Career & Wealth Systems (Career Ops)

*Invariant:* Never execute parallel modifications against the same production file or container without explicit coordination.

---

## 6. The Life OS Improvement Loop Protocol

For every component, enforce continuous loop engineering:

1. Define the target outcome.
2. Build the best reasonable version.
3. Verify against the target outcome.
4. Identify the single highest-impact weakness.
5. Improve that weakness.
6. Measure and verify again.
7. Record the change in structured changelog.
8. Continue until marginal improvement no longer justifies time, complexity, or risk.

---

## 7. External AI Intelligence Process (`staying-ahead.com`)

The dedicated **Staying Ahead Curator** continuously inspects `https://stayingahead.com/daily-ai-updates`:

1. Inspect resource using browser/research tools.
2. Check `.life-os/sources/staying_ahead_processed.json` to prevent duplicate processing.
3. Extract title, URL, date, author, type, core idea/prompt/framework, intended outcome, prerequisites, risks/cost, and factual verification.
4. Assign decision: `REJECT`, `ARCHIVE`, `KNOWLEDGE_ONLY`, `EXPERIMENT`, `ADOPT`, or `REPLACE_EXISTING_METHOD`.
5. If `ADOPT`: Specify exact rule, skill, workflow, agent, or system file to update.
6. Record full provenance in `.life-os/sources/staying_ahead_processed.json`. Never silently overwrite foundational instructions.

---

## 8. Machine-Readable State Architecture (`.life-os/`)

System state is stored in structured JSON files under `.life-os/`:

- `.life-os/state/system_state.json`: Current active components, health, priorities.
- `.life-os/knowledge/index.json`: Durable knowledge index and references.
- `.life-os/decisions/approval_ledger.json`: Record of approvals, stop overrides, and pending gates.
- `.life-os/changelog/history.json`: Machine-readable changelog of system updates.
- `.life-os/sources/staying_ahead_processed.json`: Deduplication and provenance ledger for external AI updates.
- `.life-os/audits/latest_health_audit.json`: Latest production health and security audit snapshots.

---

## 9. Production Safety Invariants & SSH Protocols

- **Production SSH:** Always use SSH alias `life-os-prod` (`/home/ubuntu/projects/n8n`). Key path: `~/.ssh/life-os-prod`. Never print or expose host, username, or private key.
- **Git System of Record:** Production pulls approved commits from GitHub (`https://github.com/arindam-islam/life-os.git`). Never deploy uncommitted local changes.
- **Docker Safety:**
  - Never use `docker compose down` for routine work.
  - Never use `--remove-orphans`.
  - Target single services with `--no-deps` (e.g. `docker compose up -d --no-deps <service>`).
  - Preserve `n8n` and `omniroute` container identities, mounts (`./data`), database state, and encryption keys.
- **Telemetry Boundary:** Expose operational metadata ONLY (health, execution counts, status, timestamps). NEVER expose execution payloads, credentials, captured content, or personal data.

---

## 10. Restart & Revalidation Sequence

When resuming or starting execution, execute this exact 5-step sequence:

1. **Preserve and Orient:** Inspect `git status --short` and diff. Keep uncommitted worktree intact.
2. **Revalidate Locally:** Run test suites (`slack-resource-inbox`, `status-bridge`, `docker compose config`, `git diff --check`).
3. **Refresh Production Facts:** Perform read-only SSH check via `life-os-prod` for container health, identities, and active routes.
4. **Ask Only for Next Material Decision:** Report status in founder format and request approval ONLY if an approval gate is reached.
5. **Complete One Lane and Report:** Execute in-scope work, verify acceptance, and report final outcome.

---

## 11. AGENT DIRECTIVE: QUOTA OPTIMIZATION & AUTOMATED HANDOVER PROTOCOL

## 11.1. QUOTA PRESERVATION & TOKEN SAVINGS
- **Modular Context Reading:** Do NOT scan or load the entire repository into memory. Read ONLY explicitly tagged files (e.g., `@filename.md`).
- **Diff-First Outputs:** Do NOT output complete code or markdown files in chat responses. Apply edits directly to files using diffs and summarize changes in 1-2 concise sentences.
- **Concise Reasoning:** Keep chat explanations minimal, clear, and direct. Eliminate conversational filler, pleasantries, and unnecessary boilerplate.
- **Loop Prevention:** If a terminal command or script execution fails twice consecutively, STOP immediately. Do NOT loop retries—prompt the user for guidance.

---

## 11.2. AUTOMATED CHAT LENGTH MONITORING & HANDOVER PROTOCOL
- **Turn Counter:** Secretly track interaction turn counts within the active chat thread.
- **13th Response Trigger:** Upon receiving the user's 12th prompt, generate the requested response on turn 13, then append the following handover section at the very end:

---
⚠️ **CHAT LENGTH THRESHOLD REACHED (Turn 13/15)**
To prevent context degradation and save token quota, please start a new thread.

👉 **To migrate immediately:** Copy the handover block below and paste it into a new chat.
👉 **To continue this thread:** Reply with `CONTINUE_THREAD`.

### 🔄 MIGRATION CONTEXT HANDOVER
```markdown
---
### 🔄 LIFE OS CONTEXT HANDOVER

**Active Component:** [Life OS module or task name]
**Current State & Progress:** [Brief 2-sentence summary of what was accomplished in this chat]

**Key Files Modified/Relevant:**
- `@path/to/file1.md`
- `@path/to/file2.py`

**Pending Tasks & Next Steps:**
1. [Next task to execute]
2. [Follow-up action item]

**Directive for New Chat:** Read `@AGENTS.md` and continue execution directly from Pending Tasks above.

---
```
