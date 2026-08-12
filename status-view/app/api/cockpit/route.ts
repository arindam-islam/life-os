import {
  cockpitSnapshot,
  type CockpitSnapshot,
  type HealthState,
} from "../../cockpit-source";

export const dynamic = "force-dynamic";

type BridgeSystem = {
  id: string;
  name: string;
  state: string;
  checked_at: string;
  detail: string;
};

type BridgeExecution = {
  id: number;
  workflow: string;
  status: string;
  mode: string;
  started_at: string | null;
  stopped_at: string | null;
  duration_ms: number | null;
};

type BridgePayload = {
  schema_version: number;
  generated_at: string;
  overall: string;
  source: string;
  systems: BridgeSystem[];
  processing: {
    window_hours: number;
    total: number;
    succeeded: number;
    failed: number;
    running_or_waiting: number;
    success_rate: number | null;
    recent_executions: BridgeExecution[];
    active_workflows: Array<{ name: string; updated_at: string | null }>;
    unavailable_reason?: string;
  };
  privacy: {
    contains_execution_payloads: boolean;
    contains_credentials: boolean;
    contains_captured_content: boolean;
  };
};

const BRIDGE_TIMEOUT_MS = 5_000;

function fallbackSnapshot(message: string, servedAt: string): CockpitSnapshot {
  return {
    ...cockpitSnapshot,
    telemetry: {
      status: "fallback",
      label: "Reviewed source snapshot",
      message,
      generatedAt: null,
      lastAttemptAt: servedAt,
    },
  };
}

function isBridgePayload(value: unknown): value is BridgePayload {
  if (!value || typeof value !== "object") return false;
  const candidate = value as Partial<BridgePayload>;
  return (
    candidate.schema_version === 1 &&
    typeof candidate.generated_at === "string" &&
    typeof candidate.source === "string" &&
    Array.isArray(candidate.systems) &&
    Boolean(candidate.processing) &&
    Boolean(candidate.privacy) &&
    candidate.privacy?.contains_execution_payloads === false &&
    candidate.privacy?.contains_credentials === false &&
    candidate.privacy?.contains_captured_content === false
  );
}

function liveHealthState(state: string): HealthState {
  return state === "healthy" ? "healthy" : "disconnected";
}

function mergeBridge(snapshot: CockpitSnapshot, bridge: BridgePayload, servedAt: string): CockpitSnapshot {
  const systemById = new Map(bridge.systems.map((system) => [system.id, system]));
  const bridgeSource = {
    id: "oracle-telemetry",
    name: bridge.source,
    kind: "Authenticated read-only production feed",
    location: "Private Life OS status bridge",
    observedOn: bridge.generated_at,
    availability: "available" as const,
    note: "Contains component health and n8n execution metadata only; no payloads, credentials, or captured content.",
  };

  const components = snapshot.components.map((component) => {
    const live = systemById.get(component.id);
    if (live) {
      const state = liveHealthState(live.state);
      return {
        ...component,
        state,
        reading: state === "healthy" ? "Live healthy" : "Live check unavailable",
        observedOn: live.checked_at,
        freshness: "Live bridge check",
        sourceIds: ["oracle-telemetry"],
        detail: live.detail,
      };
    }
    if (component.id === "health-feed") {
      return {
        ...component,
        state: "healthy" as const,
        reading: "Live feed connected",
        observedOn: bridge.generated_at,
        freshness: "Current bridge response",
        sourceIds: ["oracle-telemetry"],
        detail: "Authenticated component health is available through the read-only bridge.",
      };
    }
    return component;
  });

  const database = systemById.get("n8n-database");
  const historyConnected = database?.state === "healthy" && !bridge.processing.unavailable_reason;
  const requiredFeeds = snapshot.requiredFeeds.map((feed) => {
    if (feed.id === "component-health") {
      return { ...feed, state: "connected" as const, blocker: "Authenticated read-only bridge connected." };
    }
    if (feed.id === "processing-history" && historyConnected) {
      return { ...feed, state: "connected" as const, blocker: "Read-only n8n execution metadata connected." };
    }
    return feed;
  });

  return {
    ...snapshot,
    mode: "live",
    asOf: bridge.generated_at,
    telemetry: {
      status: "live",
      label: bridge.overall === "operational" ? "Live production health" : "Live production health · degraded",
      message: "Component health and n8n execution metadata are coming from the authenticated read-only bridge.",
      generatedAt: bridge.generated_at,
      lastAttemptAt: servedAt,
    },
    processing: {
      source: historyConnected ? "live" : "unavailable",
      windowHours: bridge.processing.window_hours,
      total: historyConnected ? bridge.processing.total : null,
      succeeded: historyConnected ? bridge.processing.succeeded : null,
      failed: historyConnected ? bridge.processing.failed : null,
      runningOrWaiting: historyConnected ? bridge.processing.running_or_waiting : null,
      successRate: historyConnected ? bridge.processing.success_rate : null,
      recentExecutions: historyConnected
        ? bridge.processing.recent_executions.map((execution) => ({
            id: execution.id,
            workflow: execution.workflow,
            status: execution.status,
            mode: execution.mode,
            startedAt: execution.started_at,
            stoppedAt: execution.stopped_at,
            durationMs: execution.duration_ms,
          }))
        : [],
      activeWorkflows: historyConnected
        ? bridge.processing.active_workflows.map((workflow) => ({
            name: workflow.name,
            updatedAt: workflow.updated_at,
          }))
        : [],
      unavailableReason: historyConnected
        ? null
        : "The bridge is reachable, but workflow-history metadata is unavailable.",
    },
    components,
    requiredFeeds,
    sources: snapshot.sources.map((source) =>
      source.id === "oracle-telemetry" ? bridgeSource : source,
    ),
  };
}

async function loadCockpit(): Promise<CockpitSnapshot> {
  const servedAt = new Date().toISOString();
  const bridgeUrl = process.env.LIFE_OS_STATUS_URL?.trim();
  const bridgeToken = process.env.LIFE_OS_STATUS_TOKEN?.trim();

  if (!bridgeUrl || !bridgeToken || bridgeToken.length < 32) {
    return fallbackSnapshot(
      "The live bridge is not configured for this dashboard runtime. Showing the reviewed source snapshot.",
      servedAt,
    );
  }

  try {
    if (new URL(bridgeUrl).protocol !== "https:") {
      return fallbackSnapshot(
        "The live bridge URL is not using the required secure connection. Showing the reviewed source snapshot.",
        servedAt,
      );
    }
  } catch {
    return fallbackSnapshot(
      "The live bridge URL is invalid. Showing the reviewed source snapshot.",
      servedAt,
    );
  }

  try {
    const response = await fetch(bridgeUrl, {
      method: "GET",
      headers: {
        accept: "application/json",
        authorization: `Bearer ${bridgeToken}`,
      },
      cache: "no-store",
      signal: AbortSignal.timeout(BRIDGE_TIMEOUT_MS),
    });
    if (!response.ok) {
      return fallbackSnapshot(
        response.status === 401 || response.status === 403
          ? "The live bridge rejected dashboard authorization. Showing the reviewed source snapshot."
          : "The live bridge returned an unavailable response. Showing the reviewed source snapshot.",
        servedAt,
      );
    }

    const payload: unknown = await response.json();
    if (!isBridgePayload(payload)) {
      return fallbackSnapshot(
        "The live bridge returned an unexpected safe-data shape. Showing the reviewed source snapshot.",
        servedAt,
      );
    }
    return mergeBridge(cockpitSnapshot, payload, servedAt);
  } catch {
    return fallbackSnapshot(
      "The live bridge could not be reached within five seconds. Showing the reviewed source snapshot.",
      servedAt,
    );
  }
}

export async function GET() {
  const servedAt = new Date().toISOString();
  const snapshot = await loadCockpit();
  return Response.json(
    { ...snapshot, servedAt },
    { headers: { "cache-control": "private, no-store, max-age=0" } },
  );
}
