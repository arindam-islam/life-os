# Life OS Control View

A single-page, nontechnical status board for Life OS. It shows the system map,
the completed YouTube Enrichment rollout, recent engineering activity, and the
approval gates that remain with the founder.

## Data truth

This version is a visibility prototype. It does not connect to production or
claim live telemetry. The dashboard distinguishes production-verified health,
the latest reported handoff, ready-but-unconnected work, and future plans. Live
health checks and authenticated controls are future work.

## Local use

Requires Node.js `>=22.13.0`.

```bash
npm install
npm run dev
```

Validation:

```bash
npm run build
npm test
npm run lint
```
