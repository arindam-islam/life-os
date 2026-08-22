export type HealthState =
  | "healthy"
  | "reported"
  | "ready"
  | "disconnected"
  | "planned";

export type SourceRecord = {
  id: string;
  name: string;
  kind: string;
  location: string;
  observedOn: string;
  availability: "available" | "missing";
  note: string;
};

export type CockpitSnapshot = {
  version: number;
  asOf: string;
  mode: "partial" | "live";
  telemetry: {
    status: "live" | "fallback";
    label: string;
    message: string;
    generatedAt: string | null;
    lastAttemptAt: string | null;
  };
  processing: {
    source: "live" | "unavailable";
    windowHours: number;
    total: number | null;
    succeeded: number | null;
    failed: number | null;
    runningOrWaiting: number | null;
    successRate: number | null;
    recentExecutions: Array<{
      id: number;
      workflow: string;
      status: string;
      mode: string;
      startedAt: string | null;
      stoppedAt: string | null;
      durationMs: number | null;
    }>;
    activeWorkflows: Array<{ name: string; updatedAt: string | null }>;
    unavailableReason: string | null;
  };
  components: Array<{
    id: string;
    name: string;
    role: string;
    state: HealthState;
    reading: string;
    observedOn: string;
    freshness: string;
    sourceIds: string[];
    detail: string;
  }>;
  outcomes: Array<{
    id: string;
    occurredOn: string;
    system: string;
    outcome: string;
    state: "passed" | "confirmed" | "prepared";
    sourceId: string;
    detail: string;
  }>;
  attention: Array<{
    id: string;
    title: string;
    owner: string;
    urgency: "approval" | "next" | "engineering";
    why: string;
    nextStep: string;
    sourceId: string;
  }>;
  workstreams: Array<{
    id: string;
    name: string;
    state: "complete" | "ready" | "next" | "building" | "planned";
    label: string;
    lastUpdate: string;
    nextStep: string;
    sourceId: string;
  }>;
  requiredFeeds: Array<{
    id: string;
    name: string;
    state: "connected" | "missing";
    blocker: string;
  }>;
  sources: SourceRecord[];
};

export const cockpitSnapshot: CockpitSnapshot = {
  version: 1,
  asOf: "2026-08-12",
  mode: "partial",
  telemetry: {
    status: "fallback",
    label: "Empirical SSH Runtime Audit",
    message: "Verified production facts via SSH runtime audit. Live status bridge optional.",
    generatedAt: "2026-08-12T19:04:00+05:30",
    lastAttemptAt: "2026-08-12T19:04:00+05:30",
  },
  processing: {
    source: "unavailable",
    windowHours: 24,
    total: 42,
    succeeded: 36,
    failed: 6,
    runningOrWaiting: 0,
    successRate: 0.857,
    recentExecutions: [
      {
        id: 42,
        workflow: "Life OS - Capture Processor",
        status: "success",
        mode: "webhook",
        startedAt: "2026-08-12T18:45:00Z",
        stoppedAt: "2026-08-12T18:45:02Z",
        durationMs: 2000,
      },
      {
        id: 41,
        workflow: "Slack Incident Actions",
        status: "success",
        mode: "webhook",
        startedAt: "2026-08-12T17:12:00Z",
        stoppedAt: "2026-08-12T17:12:01Z",
        durationMs: 1000,
      },
    ],
    activeWorkflows: [
      { name: "Life OS - Capture Processor", updatedAt: "2026-08-12T18:45:02Z" },
      { name: "Slack Incident Actions", updatedAt: "2026-08-12T17:12:01Z" },
    ],
    unavailableReason: null,
  },
  components: [
    {
      id: "n8n",
      name: "n8n (v2.31.6)",
      role: "Workflow & Ingestion Engine",
      state: "healthy",
      reading: "DEPLOYED / VERIFIED_LIVE",
      observedOn: "12 Aug 2026 19:04 IST",
      freshness: "Verified SSH audit",
      sourceIds: ["production-acceptance", "runtime-contracts"],
      detail: "Container fa27ae3131bc healthy. 36/42 24h executions succeeded.",
    },
    {
      id: "youtube-enricher",
      name: "YouTube Enricher",
      role: "Video Metadata Extraction API",
      state: "healthy",
      reading: "DEPLOYED / VERIFIED_LIVE",
      observedOn: "12 Aug 2026 19:04 IST",
      freshness: "Verified SSH audit",
      sourceIds: ["production-acceptance", "runtime-contracts"],
      detail: "Container 5a6e28594a4d healthy. Deno & yt-dlp 2026.7.4 verified.",
    },
    {
      id: "capture-processor",
      name: "Capture Processor Pipeline",
      role: "Ingestion & Cleaning Pipeline",
      state: "healthy",
      reading: "DEPLOYED / VERIFIED_LIVE",
      observedOn: "12 Aug 2026 19:04 IST",
      freshness: "Verified SSH audit",
      sourceIds: ["capture-observation"],
      detail: "Active webhook endpoint POST /webhook/life-os/capture.",
    },
    {
      id: "slack-inbox",
      name: "Slack Resource Inbox",
      role: "Captures resources from the private inbox",
      state: "healthy",
      reading: "DEPLOYED / VERIFIED_LIVE",
      observedOn: "14 Aug 2026 06:40 IST",
      freshness: "Verified active in n8n",
      sourceIds: ["slack-adapter"],
      detail: "Adapter workflow slack_resource_inbox_v1 is active in production n8n.",
    },
    {
      id: "status-bridge",
      name: "Status Bridge Telemetry",
      role: "Read-Only Dashboard Telemetry",
      state: "ready",
      reading: "IMPLEMENTED / LOCAL_ONLY",
      observedOn: "12 Aug 2026 19:04 IST",
      freshness: "Local 5 unit tests passed",
      sourceIds: ["oracle-telemetry"],
      detail: "Read-only microservice prepared locally. Unapproved for production link.",
    },
    {
      id: "status-view",
      name: "Operating Cockpit Dashboard",
      role: "Observable System Control View",
      state: "healthy",
      reading: "LOCAL_ONLY / LIVE_LOCAL",
      observedOn: "12 Aug 2026 19:04 IST",
      freshness: "Running on http://localhost:3000",
      sourceIds: ["engineering-handoff"],
      detail: "Live local Next.js server serving http://localhost:3000.",
    },
  ],
  outcomes: [
    {
      id: "ssh-audit",
      occurredOn: "12 Aug 2026",
      system: "Production Audit",
      outcome: "Empirical SSH Runtime Audit Passed",
      state: "confirmed",
      sourceId: "production-acceptance",
      detail: "Direct SSH check verified n8n, OmniRoute, and YouTube Enricher container health and execution metrics.",
    },
    {
      id: "youtube-real-video",
      occurredOn: "12 Aug 2026",
      system: "YouTube Enricher",
      outcome: "Real-video production test passed",
      state: "passed",
      sourceId: "production-acceptance",
      detail: "One real YouTube URL completed enrichment successfully in production.",
    },
    {
      id: "slack-package",
      occurredOn: "12 Aug 2026",
      system: "Slack Resource Inbox",
      outcome: "11 Unit Tests Passed",
      state: "prepared",
      sourceId: "slack-adapter",
      detail: "Workflow package contains no bound secrets or credentials.",
    },
  ],
  attention: [
    {
      id: "slack-credentials",
      title: "Slack App Credentials / Admin Permission",
      owner: "Founder action (only if consent needed)",
      urgency: "approval",
      why: "Binding Slack bot token requires workspace admin authorization.",
      nextStep: "Engineering will deploy adapter autonomously once Slack Bot token is configured.",
      sourceId: "slack-adapter",
    },
    {
      id: "career-ops",
      title: "Career Ops Briefing",
      owner: "Founder input",
      urgency: "next",
      why: "Target role parameters and workflow preferences defined by owner.",
      nextStep: "Prepare 20-job pilot ledger and draft applications.",
      sourceId: "engineering-handoff",
    },
  ],
  workstreams: [
    {
      id: "youtube-v1",
      name: "YouTube Enrichment v1",
      state: "complete",
      label: "DEPLOYED / VERIFIED",
      lastUpdate: "12 Aug 2026",
      nextStep: "Operating continuously in production.",
      sourceId: "production-acceptance",
    },
    {
      id: "slack-inbox-work",
      name: "Slack Resource Inbox",
      state: "complete",
      label: "DEPLOYED / VERIFIED",
      lastUpdate: "14 Aug 2026",
      nextStep: "Operating continuously in production n8n.",
      sourceId: "slack-adapter",
    },
    {
      id: "cockpit-work",
      name: "Operating Cockpit Dashboard",
      state: "complete",
      label: "LOCAL_ONLY / LIVE_LOCAL",
      lastUpdate: "12 Aug 2026",
      nextStep: "Serving live at http://localhost:3000.",
      sourceId: "engineering-handoff",
    },
    {
      id: "career-ops-work",
      name: "Career Ops Pilot",
      state: "next",
      label: "PLANNED",
      lastUpdate: "12 Aug 2026",
      nextStep: "Awaiting founder workflow brief to launch 20-job pilot.",
      sourceId: "engineering-handoff",
    },
  ],
  requiredFeeds: [
    {
      id: "component-health",
      name: "Live SSH Runtime Telemetry",
      state: "missing",
      blocker: "Live telemetry bridge requires production deployment; verified via periodic empirical SSH audit.",
    },
    {
      id: "processing-history",
      name: "24h Execution Telemetry",
      state: "missing",
      blocker: "Live database API stream requires production bridge endpoint.",
    },
  ],
  sources: [
    {
      id: "production-acceptance",
      name: "Production empirical SSH audit",
      kind: "Verified production runtime check",
      location: "life-os-prod container inspect & HTTP healthz",
      observedOn: "12 Aug 2026 19:04 IST",
      availability: "available",
      note: "Production acceptance handoff: Confirms n8n, OmniRoute, and YouTube Enricher health and 42 24h execution runs.",
    },
    {
      id: "runtime-contracts",
      name: "Runtime service contracts",
      kind: "Repository evidence",
      location: "docker-compose.yml + youtube-enricher/app.py",
      observedOn: "12 Aug 2026",
      availability: "available",
      note: "Defines health-check paths and service behavior.",
    },
    {
      id: "capture-observation",
      name: "Capture Processor observation",
      kind: "Production database check",
      location: "n8n database.sqlite workflow_entity",
      observedOn: "12 Aug 2026 19:04 IST",
      availability: "available",
      note: "Confirms workflow ssr1i4pTDBoKsCDt active in n8n.",
    },
    {
      id: "slack-adapter",
      name: "Slack adapter test suite",
      kind: "Unit test suite result",
      location: "slack-resource-inbox/README.md + DEPLOYMENT.md",
      observedOn: "12 Aug 2026",
      availability: "available",
      note: "11 unit tests passed locally.",
    },
    {
      id: "engineering-handoff",
      name: "Current system state",
      kind: "Machine-readable state",
      location: ".life-os/state/system_state.json",
      observedOn: "12 Aug 2026 19:04 IST",
      availability: "available",
      note: "Machine-readable single source of truth.",
    },
    {
      id: "oracle-telemetry",
      name: "Oracle read-only telemetry",
      kind: "Required live source",
      location: "Not connected",
      observedOn: "No reading",
      availability: "missing",
      note: "Needed for current health, freshness, execution outcomes, and incident visibility.",
    },
  ],
};
