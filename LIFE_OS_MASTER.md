# LIFE OS MASTER

> Canonical operating context and migration handoff for Life OS  
> Status date: 12 August 2026, Asia/Kolkata  
> Canonical local repository: `/Users/ari/Documents/life-os`  
> Canonical remote repository: `https://github.com/arindam-islam/life-os.git`  
> Production workspace: `/home/ubuntu/projects/n8n` on SSH alias `life-os-prod`

## 1. Purpose of this document

This is the single starting document for any local AI workspace or engineering
agent continuing Life OS. It records the product intent, operating model,
approval rules, architecture, environments, routines, completed work, current
working tree, production state, known risks, and exact restart conditions.

This document contains project-level instructions and user-approved operating
rules. It intentionally does **not** contain hidden provider prompts, raw secret
values, private-key contents, tokens, credentials, payment details, captured
personal content, or production database contents.

When information conflicts, use this order:

1. The product owner's latest explicit instruction.
2. `/Users/ari/Documents/life-os/AGENTS.md`.
3. A current task-specific approval or runbook.
4. This master document.
5. Component READMEs and repository history.
6. Old chats or handoff summaries.

Never treat an old plan as proof of current production state. Verify drift-prone
facts with read-only checks before changing production.

## 2. Product vision

Life OS is meant to become an observable, approval-controlled operating system
for Arindam's personal and professional goals. It should receive unstructured
inputs, clean and understand them, decide what should happen next, preserve
useful knowledge, and coordinate agents that carry out routine work.

The product owner should decide:

- what outcome matters;
- what to prioritize;
- acceptable cost and risk;
- whether sensitive, financial, public, destructive, or reputation-affecting
  actions may proceed.

The engineering system should independently handle:

- technical design;
- implementation;
- testing and review;
- safe deployment;
- validation and monitoring;
- rollback planning;
- concise outcome reporting.

The product owner should not be asked to inspect code, commands, container
configuration, or routine technical details.

### Long-term outcome

```text
Capture → clean → understand → decide → store or act → learn
                              │
                              └── human approval for consequential actions
```

The near-term business priorities are job/career outcomes and additional income
sources. A more general Jarvis-like agent system is a later goal, after those
primary outcomes start working reliably.

## 3. Product-owner communication style

- Be direct, candid, evidence-based, and willing to challenge bad assumptions.
- Do not act as a yes-man and do not use empty encouragement.
- Lead with the outcome, then explain only what the owner needs to decide.
- Use short, precise, nontechnical updates.
- Explain what is happening, where it is happening, and why it matters.
- Do not dump long command blocks on the product owner unless they explicitly
  ask to execute something themselves.
- Report four things: what changed, what works, what is blocked, and the next
  material decision.
- Never describe planned, prepared, or repository-only work as live.

## 4. Roles and operating model

| Layer | Responsibility |
|---|---|
| Product owner | Outcomes, priorities, cost, risk, sensitive approvals |
| CTO/architecture layer | Translate goals into design, challenge assumptions, review risk |
| Engineering agents | Implement, test, deploy approved changes, validate, roll back |
| GitHub | Versioned source of truth |
| Oracle production | The running 24x7 Life OS system |
| Control view | Truthful visibility into health, processing, work, blockers, and approvals |

Use multiple agents only when workstreams are genuinely independent and the
token/cost budget supports it. Parallelism previously accelerated delivery but
also exhausted the shared weekly agentic allowance. The new default is:

- one primary engineering lane for stateful production work;
- parallel agents only for bounded, independent, high-value work;
- no parallel agent merely to create the appearance of activity;
- pause one blocked lane and switch to another safe lane when useful;
- never let parallel agents change the same files or production surface without
  coordination.

## 5. Approval policy

The complete enforceable policy is in `AGENTS.md`. The following is its working
summary.

### Proceed without asking

Proceed autonomously with routine in-scope work:

- inspect repository files, history, configuration, and current changes;
- edit files required for the named task;
- run tests, validation, linting, builds, and static analysis;
- perform read-only production checks of health, status, logs, identities,
  networks, mounts, and non-secret metadata;
- complete technical steps, validation, and agreed rollback already contained
  in an explicitly approved named deployment.

### Stop and request approval

Approval is required before:

- accessing, using, transmitting, or disclosing sensitive personal data beyond
  what is necessary for an approved action;
- payments, subscriptions, purchases, billing changes, API credits, or spend;
- applications, cold email, public communication, external outreach, or any
  reputation-affecting action;
- destructive or difficult-to-recover changes;
- authentication, authorization, permission, access-control, membership, or
  secret-rotation changes;
- exposing, printing, copying, transmitting, or committing a real secret;
- a production action materially different from the named approval;
- increasing cost, external impact, or production risk materially;
- bypassing a human approval gate, CAPTCHA, access control, subscription, or
  service entitlement.

### Scope of an approval

An explicit approval covers all necessary in-scope implementation, deployment,
validation, and rollback steps for that named action during the current task.
Do not repeatedly ask about routine substeps unless scope, cost, external
impact, or production risk changes materially.

A later explicit **stop** overrides an earlier approval. After a stop, do not
resume the paused action until the owner explicitly says to resume it.

## 6. Secret and data-handling rules

- Never print or commit real `.env` values, tokens, keys, credential exports,
  cookies, signing secrets, payment data, or private captured content.
- Keep secrets in their existing secret or credential stores.
- Prefer credential references over copied values.
- The SSH key is configured locally as `~/.ssh/life-os-prod`; never copy its
  contents into this repository or an AI prompt.
- Use the SSH alias `life-os-prod`; do not ask the owner to retype the host,
  username, or key path.
- Production data under `data/` and `files/` is untracked and sensitive.
- Dashboard telemetry may expose operational metadata only. It must not expose
  workflow payloads, credentials, captured content, or personal data.
- Slack file ingestion may retain minimal file metadata but must not copy
  private Slack download URLs or automatically download files.
- Job-search records, résumés, contacts, salaries, sponsorship status, and
  application status must remain truthful. Inference must never be presented as
  verification.

## 7. Canonical environments

### Local Mac workspace

- Canonical repository: `/Users/ari/Documents/life-os`
- Branch: `main`
- Current committed HEAD: `4713b2782b54f4c624e38551f4f527b79cc4545b`
- Current origin: `https://github.com/arindam-islam/life-os.git`
- The ChatGPT project mirror under `.codex/.chatgpt-projects/...` is reference
  context, not the canonical code workspace.

Open the actual Life OS repository as the Codex/Claude/local-agent workspace.
Doing so avoids repeated operating-system permission prompts caused by starting
in the ChatGPT project mirror and then accessing an external folder.

### Production Oracle server

- SSH alias: `life-os-prod`
- Remote user: `ubuntu`
- Project path: `/home/ubuntu/projects/n8n`
- Shared Docker network: external `n8n_default`
- Reverse proxy: Caddy
- Existing public n8n host: `arindam-n8n.duckdns.org`
- Existing Slack incident action handler: local controller on
  `127.0.0.1:8787`, routed only at `/slack/actions`

Do not store the underlying IP address or SSH private key in project files when
the alias is sufficient.

### Git and deployment rule

Production pulls approved commits from GitHub. Do not deploy uncommitted local
changes. Before any production action:

1. inspect the working tree;
2. validate the exact change;
3. commit only intended files;
4. push the intended revision;
5. record affected container identities and current health;
6. target only the named service;
7. validate the outcome and unchanged dependencies;
8. use only the approved rollback if needed.

## 8. System architecture

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

## 9. Production components

### n8n

- Image pinned in Compose: `docker.n8n.io/n8nio/n8n:2.31.6`
- Container name: `n8n`
- Host binding: `127.0.0.1:5678`
- Persistent n8n state: `./data:/home/node/.n8n`
- Shared files: `./files:/files`
- File access restriction: `/files`
- Health endpoint: `http://127.0.0.1:5678/healthz`
- Latest confirmed status on 12 August 2026: healthy

Active workflows observed on production:

- `Life OS - Capture Processor`
- `Slack Incident Actions`

The Capture Processor entry point is:

- `POST /webhook/life-os/capture`
- Header Auth
- observed fields: `raw_input`, `normalized_input`, `content`, `source_type`,
  `source_url`, `title`, and `type`

### OmniRoute

- Independently managed container: `omniroute`
- Host binding: `127.0.0.1:20128`
- Attached to `n8n_default` in addition to its original network
- Latest confirmed status on 12 August 2026: healthy
- Purpose: route Life OS model requests to configured AI providers

OmniRoute does not provide free model access. Every upstream route must have a
legitimate entitlement, API key, local model, or funded provider account. Its
Anthropic-compatible proxy behavior must be validated before pointing Claude
Code at it.

### YouTube Enricher v1

- Container name: `youtube-enricher`
- Internal address: `http://youtube-enricher:8080`
- No host port is published
- Endpoints: `GET /health`, `POST /enrich`
- Non-root container, bounded timeouts, log rotation, health check
- Uses `yt-dlp` and Deno to extract structured metadata without downloading the
  video or copying temporary signed caption URLs
- Latest confirmed status on 12 August 2026: live and healthy
- Real YouTube production test: passed

### Caddy

The existing host routes `/slack/actions` to the local incident controller and
all other requests to n8n. The proposed `/life-os/status` route is **not
confirmed active** and must not be assumed to exist.

### Durable state

Existing workflows, credentials, SQLite data, and encryption configuration are
under `/home/node/.n8n` inside the n8n container, backed by the production
`./data` mount. Preserve these mounts and the existing encryption state.

## 10. Completed production work

### YouTube Enrichment v1

Completed:

- rebuilt and hardened the service;
- isolated deployment to only `youtube-enricher`;
- kept n8n and OmniRoute untouched during the initial rollout;
- confirmed health from n8n over the shared Docker network;
- ran a real-video acceptance test successfully;
- confirmed n8n and OmniRoute remained healthy.

Never repeat the first rollout with blanket `docker compose up -d --build`.
Target the named service with `--no-deps`.

### Approved production repair

The owner explicitly approved a production repair after the initial rollout.
That repair:

- corrected production URL variables and the `/files` restriction in `.env`;
- cleared pinned workflow test data that contained an authentication token;
- recreated only n8n under the approved repair scope;
- kept OmniRoute and YouTube Enricher identities unchanged;
- preserved active workflows, credentials, database state, and mounts;
- produced backup
  `/home/ubuntu/projects/n8n/.life-os-backups/production-repair-20260812T093644Z`.

Capture-token rotation was deliberately not performed because the dependent
iPhone capture configuration could not be updated safely at the same time.
Treat rotation as a separate future access-control change.

## 11. Current worktree: preserve before migration

The committed `main` branch is clean only through commit `4713b27`. The working
tree contains important **uncommitted** work. Do not reset, discard, overwrite,
or recreate it.

Modified tracked files:

- `.env.example`
- `README.md`
- `docker-compose.yml`
- `slack-resource-inbox/DEPLOYMENT.md`
- `slack-resource-inbox/README.md`
- `slack-resource-inbox/tests/test_package.py`
- `slack-resource-inbox/workflow.json`
- `status-view/README.md`
- `status-view/app/globals.css`
- `status-view/app/layout.tsx`
- `status-view/app/page.tsx`
- `status-view/tests/rendered-html.test.mjs`

New untracked work:

- `slack-resource-inbox/APPROVAL.md`
- `slack-resource-inbox/activation-manifest.json`
- `status-bridge/`
- `status-view/app/api/`
- `status-view/app/cockpit-source.ts`
- this `LIFE_OS_MASTER.md`

Before continuing implementation, run `git status --short`, review the diff,
and create a preservation branch or intentional commit after validation. Do not
commit generated caches, real runtime data, or secrets.

## 12. Slack Resource Inbox

### Desired behavior

Resources posted to the private Slack inbox should enter the same Life OS
capture, cleaning, decision, and durable-storage pipeline as iPhone captures.
Capturing a resource must never itself trigger an application, email, payment,
public message, or other consequential action.

### Known Slack surface

- Workspace: `Arindam Labs`
- Workspace ID: `T0BLLQ18E5C`
- Existing private channel: `#life-os-resource-inbox`
- Channel ID: `C0BPQBNTK8R`
- Channel existed before this work; no duplicate channel was created

### Prepared adapter

`slack-resource-inbox/workflow.json` is an inactive, credential-free n8n
workflow that:

- watches only the exact private channel;
- drops bots, edits, deletes, join/leave notices, wrong-channel events, and
  empty messages;
- extracts unique links and minimal file metadata;
- assigns a stable key based on workspace, channel, and Slack message timestamp;
- uses n8n Remove Duplicates v2 with a 10,000-key cross-execution history;
- forwards only kept events to the existing authenticated Capture Processor;
- retries the internal HTTP handoff three times;
- contains no token, secret, or credential binding.

### Important delivery semantics

The duplicate key is recorded before the HTTP side effect. If all three HTTP
attempts fail, the adapter fails closed and the original Slack message needs
manual recovery. This provides at-most-once behavior during persistent
downstream failure. Never silently claim the resource was saved, and never clear
the entire deduplication history automatically.

### Validation completed

- 11 local package tests passed.
- Three JSON files parsed successfully.
- Six synthetic events passed in the installed production Node runtime without
  running or modifying a production n8n workflow.
- Production read-only inspection found no existing n8n Slack credential and no
  Slack Trigger node.

### Approval and stop status

The owner explicitly said:

`APPROVE SLACK RESOURCE INBOX CONNECTION`

That approval covered the bounded steps in
`slack-resource-inbox/APPROVAL.md`. Shortly afterward, the owner said to stop
everything because only 10% of the shared weekly allowance remained. All agents
were interrupted. Completion was **not confirmed**.

Therefore:

- do not claim the Slack app exists;
- do not claim credentials were created or bound;
- do not claim the workflow was imported or activated;
- do not claim an acceptance capture was created;
- audit current Slack and n8n state read-only before resuming;
- wait for an explicit `RESUME SLACK RESOURCE INBOX CONNECTION` instruction.

On resume, follow `slack-resource-inbox/DEPLOYMENT.md` exactly. If browser OAuth
or Slack admin consent requires the owner, stop only at that exact interaction
and continue other safe work where possible.

## 13. Life OS Control View / Operating Cockpit

### Why it exists

The dashboard is not a decorative project-status website. It is the product
owner's observable operating cockpit. It must answer:

1. Is Life OS working now?
2. What arrived and moved through the pipeline?
3. What succeeded, failed, is waiting, or is stale?
4. What are agents and engineering workstreams doing?
5. What needs owner attention or approval?
6. What happened recently, and what source proves it?

Its value is visibility, accountability, control, trust, and focus. A manually
maintained status page does not satisfy this requirement.

### Old deployed prototype

- Private Sites URL:
  `https://life-os-control-view.arindambevan04.chatgpt.site`
- Sites project ID: `appgprj_6a7c405c9294819186c9c715a12c83a9`
- Access mode last verified: owner-only custom access, one allowed user, no
  groups, no external visitors

The owner rejected the deployed version because it was static and not
informative. Treat it only as an obsolete visual prototype.

### New local cockpit work

The uncommitted dashboard now includes:

- component health and freshness;
- source-labelled outcomes;
- approval and attention queue;
- engineering workstream status explicitly labelled as snapshot-based;
- a source ledger;
- manual refresh and planned 30-second automatic refresh;
- live/fallback modes;
- current n8n execution counts and recent execution metadata when the bridge is
  available;
- no production write controls.

The server-side `/api/cockpit` route uses `LIFE_OS_STATUS_URL` and
`LIFE_OS_STATUS_TOKEN` and never returns the token to the browser. If the live
source is absent, unauthorized, invalid, unsafe, or slower than five seconds,
the UI falls back visibly to a reviewed snapshot.

This new dashboard revision was interrupted before a final complete
build/lint/test/publish cycle. It is **not deployed**.

### Read-only status bridge

The uncommitted `status-bridge/` service is designed to expose only:

- n8n, YouTube Enricher, and OmniRoute health;
- workflow success/failure counts for the last 24 hours;
- recent execution metadata: workflow, status, mode, timestamps, duration;
- active workflow names and freshness.

It explicitly excludes execution payloads, credentials, captured content, and
personal data. It is bearer-authenticated, read-only, non-root, has a read-only
filesystem, receives a read-only n8n database mount, and has no Docker socket.

Local validation completed before interruption:

- five bridge unit tests passed;
- Python compilation passed using a temporary bytecode cache;
- rendered Compose configuration passed with the example environment;
- diff whitespace validation passed.

### Dashboard activation approval

The requested phrase was:

`APPROVE LIVE DASHBOARD CONNECTION`

The owner did **not** provide this approval before stopping work. Do not deploy
the bridge, generate/store its production token, alter Caddy, configure the
Sites secret, or publish the new dashboard without a fresh explicit approval.

If approved, the scope is limited to:

- deploying only `status-bridge` without dependencies;
- generating a dedicated token directly in approved secret stores without
  printing it;
- adding only `/life-os/status` before Caddy's existing catch-all;
- connecting the owner-only Sites runtime server-side;
- validating unauthenticated rejection, metadata-only output, live refresh,
  and unchanged n8n/OmniRoute/YouTube identities;
- rolling back only the new route, bridge, and token if validation fails.

## 14. Career Ops

Career Ops is a priority because the job hunt should eventually run continuously
for discovery and preparation. It is currently paused because the owner said
they would explain the desired workflow before work continues.

Do not resume until the owner provides that explanation.

### Known candidate and targeting context

- Bangalore-based Indian citizen authorized to work in India.
- Initial target roles include Product Operations Lead/Manager, Technical
  Product Operations Lead, Associate Product Manager, and related
  resume-supported product, program, business-operations, and product-analyst
  roles.
- Prior compensation context: INR 12.1 LPA.
- Initial India target: approximately INR 16.5-18 LPA or higher, subject to the
  actual role and market.
- Treat location eligibility as three separate categories:
  - Bangalore office/hybrid;
  - remote explicitly eligible for India;
  - another Indian city requiring a relocation decision.
- International roles require explicit visa sponsorship, relocation support, or
  clearly verified India-remote eligibility.

### Required Career Ops pipeline

```text
Source discovery
→ live capability/schema validation
→ eligibility validation
→ deduplication
→ fit scoring
→ shortlist
→ truthful tailored resume/cover-letter/outreach drafts
→ explicit human approval
→ permitted submission or manual checklist
→ tracking ledger
```

### Career Ops approval commands

- `APPROVE APPLY [JOB ID]`
- `APPROVE EMAIL [JOB ID]`
- `APPROVE BOTH [JOB ID]`
- `REVISE [JOB ID]: [instructions]`
- `REJECT [JOB ID]`

Application and email approval are separate gates. Never guess a hiring
manager's email and present it as verified. Never bypass CAPTCHAs, access
controls, platform restrictions, or job-site terms.

### Adoption order

1. Validate the real connected tool inventory and live Apify Actor schemas.
2. Pilot roughly 20 jobs with a tracking ledger.
3. Assess relevance, eligibility accuracy, and document quality.
4. Only then automate unattended discovery through n8n or another scheduler.
5. Keep submissions and outreach individually approved.

No paid source, API spend, application, email, or public action is approved.

## 15. Current validation and production evidence

### Repository validation already completed

- YouTube Enricher: 13 tests, lint, compilation, server configuration,
  dependency checks, Compose invariants, required-variable failures, ignore and
  diff checks passed before rollout.
- YouTube production: health check and real-video enrichment passed.
- Slack package: 11 tests plus six synthetic runtime cases passed.
- Status bridge: five unit tests, compilation, Compose rendering, and diff
  checks passed.
- The newest Operating Cockpit revision needs a fresh complete build, lint, and
  test run because work was interrupted before final validation.

### Last read-only execution snapshot

During dashboard source validation on 12 August 2026:

- execution IDs were unique;
- timestamps and statuses used by the dashboard were populated and valid;
- the latest 24-hour window contained 22 executions: 17 success and 5 error;
- all 22 were from the Capture Processor;
- the errors were clustered in earlier build/test activity, followed by later
  successful runs;
- the latest observed execution was successful;
- two active workflows were present.

This was a point-in-time read-only snapshot, not a live dashboard. Re-query
before using these numbers operationally.

## 16. Production safety invariants

- Never use `docker compose down` for routine Life OS work.
- Never use `--remove-orphans`.
- Never run blanket `docker compose up -d --build` for an isolated addition.
- Target only the named service with `--no-deps` where applicable.
- Treat `n8n_default` as an existing external network.
- Preserve n8n and OmniRoute identities unless a named approval explicitly
  allows recreation.
- Preserve n8n mounts, database, workflows, credentials, and encryption state.
- Record container identities and health before and after production changes.
- Keep rollback narrower than or equal to the new change.
- Do not delete test captures, credentials, Slack memberships, apps, or backup
  data without separate destructive or access-control approval.

## 17. Current approval and pause ledger

| Action | Approval | Current state |
|---|---|---|
| Deploy YouTube Enrichment v1 | Approved | Completed and validated |
| Production repair | Approved | Completed and validated |
| Connect Slack Resource Inbox | Approved, then globally stopped | Paused; completion unconfirmed; must audit and receive resume instruction |
| Connect live dashboard bridge | Not approved | Local code only; do not deploy |
| Career Ops | Explicitly held pending explanation | Paused |
| Applications or cold emails | Not approved | Never send |
| Paid API/model credits or subscriptions | Not approved | Do not purchase or configure billing |
| Public communication | Not approved | Do not send or publish publicly |
| Destructive cleanup or credential rotation | Not approved | Do not perform |

## 18. Resource-limit incident and new execution strategy

On 12 August 2026, ChatGPT/Codex reported approximately 10% weekly agentic usage
remaining, with the next reset shown as 19 August at 12:54. The owner instructed
all work to stop. Dashboard, Slack, and Career Ops agents were interrupted.

The shared allowance was consumed faster because multiple long-running agents
were active in parallel. Future operation should use:

- smaller tasks with explicit completion criteria;
- a clean local repository workspace to reduce repeated context and permission
  overhead;
- one stateful production lane at a time;
- selective lower-cost models for routine work;
- concise handoffs instead of repeatedly reloading the entire chat;
- `LIFE_OS_MASTER.md` plus component docs as durable context;
- parallel agents only when the expected time benefit justifies the extra
  usage;
- periodic checkpoints and intentional commits before switching tools.

## 19. Local-agent and Claude migration guidance

The repository, not a vendor conversation, is the transferable system of
record. A new local agent should start by reading:

1. `LIFE_OS_MASTER.md`
2. `AGENTS.md`
3. `git status --short` and the current diff
4. the README/runbook for the selected workstream
5. current read-only production state if production is involved

### Claude Cowork

Claude Cowork officially requires an eligible paid Claude plan. Do not attempt
to unlock it through a developer-mode hack, browser manipulation, shared
session, leaked credential, entitlement bypass, or other unsupported method.

### Claude Code through OmniRoute

A legitimate alternative is possible without Claude Pro:

```text
Local Life OS repository
→ Claude Code or another local coding agent
→ OmniRoute or a compatible local proxy
→ legitimately funded Anthropic API, another provider API, or a permitted local model
```

Before using this path:

1. verify that OmniRoute supports the client protocol and required model/tool
   behavior;
2. choose a legitimate upstream provider;
3. obtain explicit approval for API credits, payment details, and spending cap;
4. keep auto-reload disabled unless separately approved;
5. store the API key only in the appropriate local or production secret store;
6. test on a non-production repository task;
7. add cost and failure telemetry;
8. reserve CTO review and production approvals for the strongest available
   model.

OmniRoute provides routing and potential failover; it does not remove provider
costs, provider limits, or service entitlements.

## 20. Restart protocol

When the owner says to resume work, use this sequence.

### Step 1: Preserve and orient

- Open `/Users/ari/Documents/life-os` as the workspace.
- Read this file and `AGENTS.md`.
- Inspect `git status --short` and the complete diff.
- Do not reset or discard current changes.
- Create a preservation branch or intentional commit only after validation.

### Step 2: Revalidate locally

Run the workstream-specific tests:

```sh
python3 -m unittest discover -s slack-resource-inbox/tests -v
python3 -m unittest discover -s status-bridge/tests -v
N8N_ENV_FILE=.env.example docker compose --env-file .env.example config --quiet
cd status-view && npm run build && npm run lint && npm test
```

Run `git diff --check` and confirm that no secret or generated runtime data is
staged.

### Step 3: Refresh production facts

Use read-only checks through `life-os-prod` to confirm:

- n8n, OmniRoute, and YouTube Enricher health;
- container identities and shared network;
- active workflow names;
- whether a Slack credential, Slack Trigger, imported adapter, or status bridge
  now exists;
- whether Caddy has `/life-os/status`;
- whether the existing Capture Processor is unchanged.

Do not print workflow bodies, credential values, environment secrets, pinned
data, or execution payloads.

### Step 4: Ask only for the next material decision

- Slack: request `RESUME SLACK RESOURCE INBOX CONNECTION` only after reporting
  the read-only audit.
- Dashboard: request `APPROVE LIVE DASHBOARD CONNECTION` only after local tests
  pass and the exact deployment remains within the documented boundary.
- Career Ops: wait for the owner's explanation; do not infer the workflow.
- API/model migration: present cost options and request payment/spend approval
  before configuring credits or a key.

### Step 5: Complete one lane and report

For each lane, report:

- outcome;
- live versus prepared state;
- acceptance evidence;
- unchanged protected systems;
- remaining blocker or next material decision.

## 21. Recommended next priorities

The correct sequence after an explicit resume is:

1. Preserve and validate the uncommitted worktree.
2. Audit whether any part of the approved Slack connection occurred before the
   stop.
3. Finish Slack only after a resume instruction and required Slack consent.
4. Finish local Operating Cockpit validation.
5. Obtain explicit live-dashboard connection approval.
6. Deploy and validate only the read-only telemetry bridge and owner-only
   cockpit.
7. Receive the owner's Career Ops explanation.
8. Run the approximately 20-job Career Ops pilot before unattended automation.
9. Plan the Knowledge Engine and broader agent/Jarvis layer only after the
   primary job/income loops show measurable value.

## 22. Definition of done by workstream

### Slack Resource Inbox is done only when

- the dedicated read-only Slack app is legitimate and scoped to the exact
  private channel;
- credentials exist only in n8n's credential store;
- the adapter is imported inactive first;
- one harmless URL creates exactly one durable capture;
- duplicate replay creates no second capture;
- Capture Processor, n8n, and OmniRoute remain unchanged and healthy;
- only the adapter is activated;
- the dashboard reports it as live only after these checks.

### Operating Cockpit is done only when

- the owner-only dashboard refreshes real production health and execution
  metadata at the agreed interval;
- every live metric has a source and timestamp;
- stale or failed sources show visibly degraded state;
- snapshot-only engineering and agent status is labelled honestly;
- secrets, payloads, and captured content cannot reach the browser;
- no production write control exists in v1;
- build, lint, tests, private publish, and live acceptance checks pass.

### Career Ops pilot is done only when

- roughly 20 jobs have been discovered through verified sources;
- location and work-authorization eligibility is checked truthfully;
- duplicates are removed;
- fit scores and reasons are inspectable;
- tailored material contains no invented claims;
- a tracking ledger exists;
- no application or email is sent without its specific approval;
- pilot quality is reviewed before adding schedules or API spend.

## 23. Glossary

- **Prepared:** code or configuration exists locally but is not active.
- **Deployed:** code is running in production; this alone does not mean it
  passed acceptance.
- **Live:** deployed, reachable, accepted, and currently reporting a fresh
  reading.
- **Reported healthy:** a previous handoff said healthy; not current telemetry.
- **Approval gate:** a point requiring the product owner's explicit consent.
- **Rollback:** the pre-planned, narrow reversal of the newly introduced
  change.
- **OmniRoute:** model-routing layer; not a source of free provider capacity.
- **Capture Processor:** the existing authenticated n8n ingestion pipeline.
- **Status bridge:** proposed read-only metadata source for the cockpit.

## 24. Final handoff rule

The next agent must preserve truth over momentum. If a state cannot be verified,
label it unknown or prepared. If approval is missing, keep the item ready and
move to another safe task. Never make the product owner responsible for routine
engineering execution, and never trade away security, reputation, or financial
control merely to avoid an interruption.
