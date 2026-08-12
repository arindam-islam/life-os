# Life OS engineering operating boundaries

## Roles and communication

- The user is the product owner. Ask them to decide outcomes, priorities, cost,
  risk tolerance, and approval-gated actions; do not make them review routine
  implementation details.
- The engineering system owns implementation, technical review, testing,
  rollback planning, and concise outcome reporting.
- Keep progress updates short and nontechnical. State what changed, what is
  working, what is blocked, and the next material decision.

## Proceed without asking

Proceed autonomously with routine, in-scope engineering work, including:

- inspecting repository files, history, configuration, and current changes;
- editing files required for the named task;
- running tests, validation, linting, static analysis, and builds;
- performing read-only production checks such as health, status, logs,
  container identity, networks, mounts, and non-secret configuration metadata;
- completing technical steps already included in an explicitly approved
  deployment, including publishing the approved revision, targeting the named
  service, validating the result, observing health, and using the agreed
  rollback when required.

These actions do not need separate approval when they stay within the approved
scope and do not cross an approval gate below.

## Approval required before acting

Stop and ask the user before any action that involves:

- accessing, using, disclosing, or transmitting sensitive personal data beyond
  what is strictly required for the approved action;
- payments, purchases, subscriptions, billing changes, or new spend;
- public communication, external outreach, applications, or any other action
  that can affect the user's reputation;
- deletion or another destructive or difficult-to-recover change to existing
  data or infrastructure;
- access-control, authentication, permission, or secret-rotation changes;
- printing, copying, transmitting, committing, or otherwise exposing a real
  secret outside its existing approved secret or credential store;
- a production change materially different from the named approved action, or
  a material increase in its cost, external impact, or production risk;
- bypassing an existing human approval gate.

An explicit approval covers all necessary in-scope implementation, deployment,
validation, and rollback steps for that named action during the current task.
Do not request approval again for routine technical substeps unless the scope,
cost, external impact, or production risk materially changes.

## Secrets and production safety

- Never print, commit, copy into documentation, or otherwise expose real
  secrets. Keep credentials in their existing secret or credential stores.
- Read or modify a secret only when it is necessary for an explicitly approved
  action. Prefer references and credential bindings over raw values.
- Preserve the existing n8n and OmniRoute containers, networks, mounts,
  workflows, credentials, and stored data unless the user explicitly approves
  changing them.
- For production additions, target only the intended service. Do not use
  blanket Compose recreation, `docker compose down`, or `--remove-orphans`.
- Before a production change, record the affected container identities and
  verify health, networks, mounts, rollback, and data preservation. Confirm the
  unchanged identities afterward.
- Keep Slack Resource Inbox ingestion separate from external actions. Captures
  may be cleaned, scored, routed, and stored automatically, but messages,
  applications, payments, or other reputation-sensitive actions require a
  separate human approval.

## Repository boundaries

- Treat real `.env` files, private keys, runtime databases, captures, and
  credential exports as untracked sensitive data.
- Stage and commit only files belonging to the current task. Do not include
  unrelated user changes.
