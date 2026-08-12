# Approval-gated production plan

## Verified production shape

Read-only checks on 2026-08-12 established the following without exporting
workflow bodies, pinned data, credentials, or secret values:

- **Life OS - Capture Processor** is active.
- Its entry point is `POST /webhook/life-os/capture` with Header Auth.
- It responds through a Respond to Webhook node.
- Its observed input fields are `raw_input`, `normalized_input`, `content`,
  `source_type`, `source_url`, `title`, and `type`.
- Production contains zero Slack credentials and zero Slack Trigger nodes.

The adapter therefore calls
`http://127.0.0.1:5678/webhook/life-os/capture`. Loopback keeps the handoff inside
the existing n8n container. The Header Auth secret remains in n8n's credential
store and is never copied into this package.

## Approval gates

Do not perform any item below until the product owner approves this Slack Inbox
production addition. The approval must cover the Slack access and production
workflow changes.

1. Create or select a dedicated Life OS Slack app, grant only
   `message.groups` / `groups:history`, configure its signing secret, install it
   to Arindam Labs, and add it to private channel `C0BPQBNTK8R`.
2. Create the n8n Slack credential in the production credential store. Do not
   print or export the token or signing secret.
3. Import `workflow.json` as an inactive workflow. Bind the Slack credential to
   **Watch Private Resource Inbox**.
4. Bind the existing Capture Processor Header Auth credential to **Forward to
   Authenticated Capture Webhook**. Reuse the credential reference; never copy
   the header name or value into the node.
5. Configure the Slack app Event Subscriptions request URL from the imported
   trigger. Do not overwrite another endpoint. The current n8n inventory has no
   Slack Trigger, but the Slack app configuration must still be checked live.
6. Run the acceptance test below. Activation requires every check to pass.
7. Activate only the Slack Resource Inbox adapter. Do not restart or recreate
   n8n or OmniRoute.

## Acceptance test while inactive

Use one harmless public documentation URL and no personal or confidential text.

1. Record the active state and workflow revision of the Capture Processor.
2. In n8n test mode, listen for one Slack event and post the harmless URL once
   in `life-os-resource-inbox`.
3. Confirm the adapter accepts the correct channel, creates
   `source=slack_resource_inbox`, and calls the loopback webhook with Header
   Auth. Confirm no credential value appears in execution output.
4. Confirm exactly one Capture Processor execution succeeds and exactly one
   durable capture is created. Confirm the existing Truthful/Saved outcome is
   still produced.
5. Replay the same normalized test event once. If a second durable capture is
   created, stop: idempotency is not proven and activation is blocked. Adding a
   persistent uniqueness guard is a separate production change.
6. Confirm Capture Processor remains active and unchanged, and n8n and
   OmniRoute container identities and health are unchanged.

The test creates a production capture. Keep it labelled as a harmless test
record. Deleting it is a separate destructive action and is not part of this
plan.

## Rollback

If the adapter fails after activation:

1. Deactivate only **Life OS - Slack Resource Inbox Adapter**.
2. Confirm no new adapter executions start and the existing Capture Processor
   remains active and healthy.
3. Confirm n8n and OmniRoute identities, mounts, and shared network are
   unchanged. Do not run Compose recreation, `docker compose down`, or
   `--remove-orphans`.
4. Leave the Slack credential in the credential store and the test capture in
   durable storage. Removing the Slack app, credential, channel membership, or
   capture requires separate access-control or destructive approval.
5. Diagnose from the adapter execution only. Do not modify the Capture
   Processor unless a separate change is approved.
