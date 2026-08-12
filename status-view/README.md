# Life OS Operating Cockpit

A private, read-only operating view for Life OS. It brings together component
health and freshness, verified outcomes, attention and approval items,
engineering workstreams, and a visible source ledger.

## Source coverage

The current cockpit is source-backed but only partially live:

- Production acceptance evidence confirms n8n, OmniRoute, and YouTube Enricher
  health on 12 Aug 2026, including one real-video enrichment test.
- Repository evidence confirms the Capture Processor observation and the
  ready-but-inactive Slack Resource Inbox adapter.
- Current engineering handoff data supplies workstream priorities.
- When `LIFE_OS_STATUS_URL` and `LIFE_OS_STATUS_TOKEN` are configured for the
  hosted server, the dashboard proxy fetches component health and n8n execution
  metadata every 30 seconds through the authenticated read-only bridge.
- When the bridge is absent or unavailable, the UI visibly degrades to the
  reviewed source snapshot. Live agent runtime remains unconnected and
  engineering workstream status stays explicitly snapshot-based.

The same-origin `GET /api/cockpit` endpoint returns the reviewed, non-secret
source snapshot with private no-store caching. The bearer token is used only in
the server route and is never returned to the browser. The endpoint does not
accept writes. Production controls remain absent.

Hosted server configuration:

```text
LIFE_OS_STATUS_URL=https://<private-approved-route>/life-os/status
LIFE_OS_STATUS_TOKEN=<dedicated-status-token>
```

## Local use

Requires Node.js `>=22.13.0`.

```bash
npm install
npm run dev
```

Validation:

```bash
npm run build
npm run lint
npm test
```
