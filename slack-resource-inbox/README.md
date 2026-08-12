# Slack Resource Inbox adapter

## Current status

- Slack workspace: `Arindam Labs` (`T0BLLQ18E5C`)
- Private channel: `life-os-resource-inbox` (`C0BPQBNTK8R`)
- The channel already existed, so this work did not create a duplicate.
- No message was posted and nobody was invited.
- `workflow.json` is an inactive, importable n8n adapter with no credential IDs,
  tokens, or secret values.
- It is **not live**. Both required credential bindings are deliberately absent.
- A read-only production check on 2026-08-12 confirmed that **Life OS - Capture
  Processor** is active and begins with a `POST` Webhook at `life-os/capture`
  using Header Auth. It does not support Execute Sub-workflow input.
- Production currently has no n8n Slack credential and no Slack Trigger node.
- The normalizer was executed against six synthetic events in the installed
  production Node.js runtime; link cleanup, channel/bot/edit guards, and minimal
  file handling passed. This did not execute or modify any n8n workflow.

## What the adapter does

1. Watches only the private resource inbox for new message events.
2. Drops bot messages, edits, deletions, join/leave notices, messages from other
   channels, and empty events.
3. Keeps the message text, extracts unique links, and records only minimal Slack
   file metadata. It does not download files or copy private download URLs.
4. Produces a stable event envelope with a Slack message deduplication key.
5. Uses n8n's persistent Remove Duplicates node to discard a Slack message key
   already processed by an earlier adapter execution.
6. Sends a loopback-only HTTP request to the existing authenticated Capture
   Processor webhook. This reuses its ingestion, cleaning, decision, and
   durable-save stages without exposing the webhook on a new network path.

The exact envelope is defined by `event-envelope.schema.json`.

The adapter translates its envelope to the Capture Processor's observed webhook
contract: `raw_input`, `normalized_input`, `content`, `source_type`,
`source_url`, `title`, and `type`. Extra provenance fields are forwarded but
must not be assumed to persist until the acceptance test proves that behavior.

See `DEPLOYMENT.md` for the approval gates, acceptance test, and rollback plan.
`activation-manifest.json` is the machine-readable checklist of the exact
channel, credential types, handoff, deduplication policy, and invariants.

Slack posts should not trigger applications, emails, payments, public messages,
or other reputation-affecting actions without the existing human approval gate.
The existing Capture Processor does not reference `deduplication_key`, so the
adapter owns duplicate suppression. The HTTP handoff retries up to three times.
If all attempts fail after the key is recorded, the execution fails closed and
an engineer must recover the capture from the original Slack message; the
adapter must never silently claim it was saved.

## Local verification

No dependencies or credentials are required:

```sh
python3 -m unittest discover -s slack-resource-inbox/tests -v
```
