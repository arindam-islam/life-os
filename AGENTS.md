# Life OS engineering operating boundaries

## Roles and communication

- The user is the product owner. Ask them to decide outcomes, priorities, cost,
  risk tolerance, and approval-gated actions; do not make them review routine
  implementation details.
- The engineering system owns implementation, technical review, testing,
  rollback planning, and concise outcome reporting.
- Keep progress updates short and nontechnical. State what changed, what is
  working, what is blocked, and the next material decision.

## Approval required before acting

Stop and ask the user before any action that involves:

- personal, private, or sensitive details beyond what is strictly required;
- payments, purchases, subscriptions, billing changes, or new spend;
- public communication, external outreach, applications, or anything that can
  affect the user's reputation;
- deletion, destructive changes, access-control changes, secret rotation, or a
  materially risky production change;
- bypassing an existing human approval gate.

Approval for one action does not authorize later actions in the same category.

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
