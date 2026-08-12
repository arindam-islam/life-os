# Life OS

> Observable, approval-controlled operating system for personal and professional goal execution.
> Local workspace: `/Users/ari/Documents/life-os`
> Remote repository: `https://github.com/arindam-islam/life-os.git`
> Production host: SSH alias `life-os-prod` (`/home/ubuntu/projects/n8n`)

---

## 1. Product Vision & Architecture

Life OS ingests unstructured personal and professional inputs, cleans and understands them via AI services, enforces strict human approval boundaries, preserves durable knowledge, and coordinates agents to perform routine work.

```text
Inputs
├── iPhone capture                         LIVE
├── Slack Resource Inbox                   PREPARED, NOT CONFIRMED LIVE
└── Future connectors                      PLANNED
        │
        ▼
n8n Capture Processor                      LIVE
├── normalize / clean
├── AI understanding through OmniRoute
├── decision and approval boundaries
└── durable storage
        │
        ├── YouTube Enricher               LIVE
        ├── future Knowledge Engine        PLANNED
        ├── Career Ops                     PAUSED FOR OWNER BRIEF
        └── future action agents           PLANNED

Observability
├── Life OS Control View                   OLD PRIVATE PROTOTYPE DEPLOYED
├── new Operating Cockpit code             LOCAL, UNCOMMITTED
└── read-only Status Bridge                LOCAL, UNCOMMITTED, NOT DEPLOYED
```

### Core Operating Principle

- **Product Owner (User):** Decides desired outcomes, priorities, cost tolerance, risk parameters, and approval-gated actions.
- **Engineering System (AI Agents):** Owns technical design, implementation, automated testing, safe deployment, runtime validation, rollback planning, and concise outcome reporting.
- **Primary Focus:** Near-term business priorities are job/career outcomes (Career Ops) and income generation. General autonomous agent features follow primary loop stability.

---

## 2. Canonical Environments

| Environment | Host / Path | Purpose | System of Record |
|---|---|---|---|
| **Local Mac** | `/Users/ari/Documents/life-os` (branch `main`) | Development, local validation, code editing | Primary local workspace |
| **GitHub** | `https://github.com/arindam-islam/life-os.git` | Version control & release target | Git System of Record for production |
| **Production Server** | Oracle Server via SSH alias `life-os-prod` (`/home/ubuntu/projects/n8n`) | 24x7 running production runtime | Live production environment |

---

## 3. Production Services & Infrastructure

### n8n Workflow Engine

- **Compose Image:** `docker.n8n.io/n8nio/n8n:2.31.6` (Container: `n8n`)
- **Host Binding:** `127.0.0.1:5678` (Loopback only)
- **Shared Network:** External Docker network `n8n_default`
- **Durable Mounts:** `./data:/home/node/.n8n` (workflows, credentials, SQLite DB, encryption key) and `./files:/files`
- **Active Workflows:** `Life OS - Capture Processor` (`POST /webhook/life-os/capture`) and `Slack Incident Actions`
- **Health Endpoint:** `http://127.0.0.1:5678/healthz` (Status: Healthy)

### OmniRoute AI Router

- **Container Name:** `omniroute` (Host binding `127.0.0.1:20128`, attached to `n8n_default`)
- **Purpose:** Central model routing layer for AI decision-making.
- **Entitlement Rule:** OmniRoute models routing logic but does not provide free provider credits. Upstream routes must use funded provider accounts or valid credentials.

### YouTube Enricher v1

- **Container Name:** `youtube-enricher` (`http://youtube-enricher:8080` on Docker network, no host port published)
- **Endpoints:** `GET /health` (runtime checks yt-dlp & Deno), `POST /enrich` (JSON: `{"url": "https://..."}`)
- **Security & Operation:** Non-root container, Deno runtime, `--skip-download` & `--no-playlist`. Extracts metadata without downloading video files or storing temporary signed URLs.
- **Status:** Live & Healthy in production.

### Status Bridge (`status-bridge/`)

- **Service:** Read-only Python microservice bound to `127.0.0.1:8788`.
- **Purpose:** Exposes telemetry (service health, 24-hour execution counts, execution status/timestamps) to the cockpit dashboard via a read-only n8n database mount.
- **Privacy Boundary:** Excludes execution payloads, credentials, captured content, and personal data.
- **Status:** Prepared local code; **Not deployed to production** (awaiting `APPROVE LIVE DASHBOARD CONNECTION`).

### Operating Cockpit (`status-view/`)

- **Service:** Next.js dashboard UI providing observable monitoring, approval queues, component health, and snapshot-based workstream status.
- **Security:** Uses server-side token injection (`LIFE_OS_STATUS_TOKEN`); falls back visibly to snapshot mode if bridge is unavailable.
- **Status:** Prepared local code; **Not deployed** (awaiting `APPROVE LIVE DASHBOARD CONNECTION`).

---

## 4. Subsystems & Active Workstreams

### Slack Resource Inbox (`slack-resource-inbox/`)

- **Purpose:** Captures links and resource posts from private Slack channel `#life-os-resource-inbox` (`C0BPQBNTK8R`) into the Capture Processor.
- **Adapter Logic:** Credential-free n8n workflow (`workflow.json`), filters noise/bots/edits, deduplicates using n8n Remove Duplicates v2 (10,000 key history), and forwards to Capture Processor with 3 HTTP retries.
- **Status:** Prepared. 11 local unit tests passed. Production deployment is **Paused** pending explicit `RESUME SLACK RESOURCE INBOX CONNECTION` instruction.

### Career Ops

- **Purpose:** Continuous job discovery, capability/schema validation, location/authorization filtering, deduplication, fit scoring, and truthful document drafting.
- **Candidate Context:** Bangalore-based Indian citizen authorized in India (Target roles: Product Operations Lead, Technical Product Ops Lead, APM, Product Analyst; target compensation: ~16.5–18+ LPA).
- **Approval Boundaries:** Separate approval gates required per job (`APPROVE APPLY [JOB ID]`, `APPROVE EMAIL [JOB ID]`). No automated email/submission is permitted without human consent.
- **Status:** **Paused** pending owner explanation of desired workflow.

---

## 5. System Rules & Governance

All engineering operations are governed by [AGENTS.md](file:///Users/ari/Documents/life-os/AGENTS.md). Key rules include:

1. **Order of Precedence:** Product Owner instruction > `AGENTS.md` > Task Runbook > `LIFE_OS_MASTER.md` > Component READMEs > Old logs.
2. **Approval Policy:**
   - **Proceed Without Asking:** Repository inspection, code edits, local builds/tests, read-only production health/log checks, executing explicitly approved deployments.
   - **Stop and Request Approval:** Sensitive data handling, payments/spend, job applications/cold emails, destructive actions, access-control/secret changes, production changes beyond scope.
3. **Secrets & Production SSH:**
   - Never print or commit real secrets or `.env` values.
   - Production SSH must use alias `life-os-prod` and local key path `~/.ssh/life-os-prod`. Never copy private keys into prompts or repository files.
4. **Production Safety Invariants:**
   - Git system of record: Production pulls approved commits from GitHub.
   - Never run `docker compose down` or `--remove-orphans`.
   - Target single services with `--no-deps` (e.g., `docker compose up -d --no-deps youtube-enricher`).
   - Preserve existing n8n and OmniRoute container identities, mounts, credentials, and database state.

---

## 6. Development, Testing & Validation Routines

Run the following test commands to validate the workspace before committing or deploying:

```sh
# 1. Slack Resource Inbox tests
python3 -m unittest discover -s slack-resource-inbox/tests -v

# 2. Status Bridge unit tests
python3 -m unittest discover -s status-bridge/tests -v

# 3. Docker Compose configuration syntax check
N8N_ENV_FILE=.env.example docker compose --env-file .env.example config --quiet

# 4. Operating Cockpit build, lint, and test suite
cd status-view && npm run build && npm run lint && npm test && cd ..

# 5. Git whitespace & secret sanity check
git diff --check
```

---

## 7. Single-Service Deployment & Rollback Protocol

When deploying an approved single service to production via `life-os-prod`:

1. **Local Verification:** Ensure all unit tests pass locally and git status is clean for intended files.
2. **Commit & Push:** Commit intended changes to `main` and push to GitHub.
3. **Pre-Deployment Audit:** SSH to `life-os-prod`, inspect container identities (`docker ps`), and verify health of running services (`n8n`, `omniroute`, `youtube-enricher`).
4. **Targeted Deployment:** Pull latest commit and build/up only the target service:
   ```sh
   ssh life-os-prod "cd /home/ubuntu/projects/n8n && git pull origin main && docker compose build <service-name> && docker compose up -d --no-deps <service-name>"
   ```
5. **Post-Deployment Audit:** Re-verify health endpoints and confirm existing container identities remained unchanged.
6. **Rollback Execution:** If post-deployment validation fails, execute the pre-planned, narrow rollback targeting only the newly introduced container/configuration.

---

## 8. Active System Status & Next Steps

### Current System Snapshot (12 August 2026)

- **Git HEAD:** `4713b2782b54f4c624e38551f4f527b79cc4545b`
- **Live Production Services:** `n8n` (Healthy), `omniroute` (Healthy), `youtube-enricher` (Healthy).
- **Prepared / Uncommitted Work:**
  - `slack-resource-inbox/` (Prepared adapter & unit tests passed; paused pending `RESUME SLACK RESOURCE INBOX CONNECTION`)
  - `status-bridge/` & `status-view/` (Prepared cockpit dashboard & telemetry bridge; paused pending `APPROVE LIVE DASHBOARD CONNECTION`)
  - `LIFE_OS_MASTER.md` (Canonical master documentation reference)

### Next Actionable Priorities

1. **Preserve Workspace:** Keep local uncommitted working tree intact.
2. **Slack Connection Audit & Resume:** Complete read-only Slack audit, then request `RESUME SLACK RESOURCE INBOX CONNECTION`.
3. **Operating Cockpit Validation:** Finish local build/lint/test cycle for `status-view` and request `APPROVE LIVE DASHBOARD CONNECTION`.
4. **Career Ops Briefing:** Await product owner's workflow explanation before initiating the 20-job pilot phase.
