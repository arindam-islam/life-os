"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  cockpitSnapshot as embeddedSnapshot,
  type CockpitSnapshot,
  type HealthState,
} from "./cockpit-source";

type CockpitResponse = CockpitSnapshot & { servedAt?: string };
type HealthFilter = "all" | "healthy" | "attention" | "disconnected";

const healthFilters: Array<{ id: HealthFilter; label: string }> = [
  { id: "all", label: "All components" },
  { id: "healthy", label: "Healthy" },
  { id: "attention", label: "Reported / ready" },
  { id: "disconnected", label: "Missing feeds" },
];

const stateLabels: Record<HealthState, string> = {
  healthy: "Healthy",
  reported: "Reported",
  ready: "Ready",
  disconnected: "Disconnected",
  planned: "Planned",
};

function sourceById(snapshot: CockpitSnapshot, id: string) {
  return snapshot.sources.find((source) => source.id === id);
}

function formatServedAt(value?: string) {
  if (!value) return "Embedded source snapshot";
  return `Source snapshot checked ${new Intl.DateTimeFormat("en-IN", {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value))}`;
}

function formatTimestamp(value: string | null) {
  if (!value) return "—";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return new Intl.DateTimeFormat("en-IN", {
    day: "numeric",
    month: "short",
    hour: "numeric",
    minute: "2-digit",
  }).format(parsed);
}

function formatDuration(value: number | null) {
  if (value === null) return "—";
  if (value < 1_000) return `${value} ms`;
  if (value < 60_000) return `${(value / 1_000).toFixed(1)} s`;
  return `${Math.round(value / 60_000)} min`;
}

export default function Home() {
  const [snapshot, setSnapshot] = useState<CockpitResponse>(embeddedSnapshot);
  const [filter, setFilter] = useState<HealthFilter>("all");
  const [refreshing, setRefreshing] = useState(false);
  const [refreshError, setRefreshError] = useState(false);

  const refresh = useCallback(async () => {
    setRefreshing(true);
    try {
      const response = await fetch("/api/cockpit", { cache: "no-store" });
      if (!response.ok) throw new Error("Cockpit source request failed");
      const next = (await response.json()) as CockpitResponse;
      setSnapshot(next);
      setRefreshError(false);
    } catch {
      setRefreshError(true);
    } finally {
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    const initialTimer = window.setTimeout(() => void refresh(), 0);
    const timer = window.setInterval(() => void refresh(), 30 * 1000);
    return () => {
      window.clearTimeout(initialTimer);
      window.clearInterval(timer);
    };
  }, [refresh]);

  const filteredComponents = useMemo(
    () =>
      snapshot.components.filter((component) => {
        if (filter === "all") return true;
        if (filter === "healthy") return component.state === "healthy";
        if (filter === "attention")
          return component.state === "reported" || component.state === "ready";
        return component.state === "disconnected";
      }),
    [filter, snapshot.components],
  );

  const verifiedHealthy = snapshot.components.filter(
    (component) => component.state === "healthy",
  ).length;
  const connectedFeeds = snapshot.requiredFeeds.filter(
    (feed) => feed.state === "connected",
  ).length;

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Life OS cockpit home">
          <span className="brand-mark">L</span>
          <span>Life OS</span>
        </a>
        <nav aria-label="Cockpit sections">
          <a href="#health">Health</a>
          <a href="#attention">Attention</a>
          <a href="#work">Work</a>
          <a href="#processing">Processing</a>
          <a href="#history">History</a>
          <a href="#sources">Sources</a>
        </nav>
        <div className="top-actions">
          <span className={`mode-chip mode-${snapshot.telemetry.status}`}>
            <span />{snapshot.telemetry.label}
          </span>
          <button className="refresh-button" onClick={() => void refresh()} disabled={refreshing}>
            {refreshing ? "Checking…" : "Refresh"}
          </button>
        </div>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow">Private operating cockpit</p>
          <h1>What is working.<br />What needs attention.</h1>
          <p className="hero-note">
            A read-only view of verified system health, real outcomes, approval gates, and engineering work.
          </p>
        </div>
        <aside className={`source-state telemetry-${snapshot.telemetry.status}`} aria-label="Dashboard source state">
          <div className="source-state-top">
            <span className="source-state-icon">{snapshot.telemetry.status === "live" ? "✓" : "!"}</span>
            <div>
              <strong>{snapshot.telemetry.label}</strong>
              <p>{snapshot.telemetry.message}</p>
            </div>
          </div>
          <div className="snapshot-time">
            <span>{formatServedAt(snapshot.servedAt)}</span>
            <span>
              {snapshot.telemetry.generatedAt
                ? `Bridge generated ${formatTimestamp(snapshot.telemetry.generatedAt)}`
                : "Evidence as of 12 Aug 2026"}
            </span>
          </div>
          <small className="refresh-cadence">Checks again automatically every 30 seconds.</small>
          {refreshError && <p className="refresh-error" role="status">Refresh failed. Showing the last embedded source snapshot.</p>}
        </aside>
      </section>

      <section className="metric-strip" aria-label="Operating summary">
        <article className="metric-card metric-green">
          <span>Verified healthy</span>
          <strong>{verifiedHealthy}</strong>
          <small>Production components</small>
        </article>
        <article className="metric-card metric-blue">
          <span>Workflow runs · last {snapshot.processing.windowHours}h</span>
          <strong>{snapshot.processing.total ?? "—"}</strong>
          <small>
            {snapshot.processing.source === "live"
              ? `${snapshot.processing.succeeded} succeeded · ${snapshot.processing.failed} failed`
              : "Live execution history unavailable"}
          </small>
        </article>
        <article className="metric-card metric-amber">
          <span>Open attention items</span>
          <strong>{snapshot.attention.length}</strong>
          <small>Approval + engineering actions</small>
        </article>
        <article className="metric-card metric-red">
          <span>Live feeds connected</span>
          <strong>{connectedFeeds}<em>/{snapshot.requiredFeeds.length}</em></strong>
          <small>Health, history, agents</small>
        </article>
        <article className="priority-card">
          <span>Next operating priority</span>
          <strong>Career Ops pilot</strong>
          <small>Prepare the pilot; keep applications and external messages approval-gated.</small>
        </article>
      </section>

      <section className="section" id="health" aria-labelledby="health-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Component health + freshness</p>
            <h2 id="health-title">System readings</h2>
          </div>
          <div className="filters" aria-label="Filter component readings">
            {healthFilters.map((item) => (
              <button
                key={item.id}
                className={filter === item.id ? "active" : ""}
                onClick={() => setFilter(item.id)}
                aria-pressed={filter === item.id}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        <div className="health-table" role="table" aria-label="Life OS component health">
          <div className="health-row health-header" role="row">
            <span role="columnheader">Component</span>
            <span role="columnheader">Current reading</span>
            <span role="columnheader">Freshness</span>
            <span role="columnheader">Source</span>
          </div>
          {filteredComponents.map((component) => {
            const primarySource = sourceById(snapshot, component.sourceIds[0]);
            return (
              <div className="health-row" role="row" key={component.id}>
                <div className="component-name" role="cell">
                  <span
                    className={`component-mark state-${component.state}`}
                    aria-label={stateLabels[component.state]}
                    title={stateLabels[component.state]}
                  >
                    {component.name.slice(0, 1)}
                  </span>
                  <div><strong>{component.name}</strong><small>{component.role}</small></div>
                </div>
                <div className="reading-cell" role="cell">
                  <span className={`status status-${component.state}`}><span />{component.reading}</span>
                  <small>{component.detail}</small>
                </div>
                <div className="freshness-cell" role="cell">
                  <strong>{component.freshness}</strong>
                  <small>{component.observedOn}</small>
                </div>
                <div className="source-cell" role="cell">
                  <strong>{primarySource?.name ?? "Source unavailable"}</strong>
                  <small>{primarySource?.kind ?? "Missing source"}</small>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <div className="two-column">
        <section className="section attention-panel" id="attention" aria-labelledby="attention-title">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Attention + approvals</p>
              <h2 id="attention-title">What needs a decision</h2>
            </div>
          </div>
          <div className="attention-list">
            {snapshot.attention.map((item, index) => (
              <article key={item.id}>
                <div className={`attention-number urgency-${item.urgency}`}>{String(index + 1).padStart(2, "0")}</div>
                <div>
                  <div className="item-heading">
                    <h3>{item.title}</h3>
                    <span>{item.owner}</span>
                  </div>
                  <p>{item.why}</p>
                  <div className="next-step"><strong>Next:</strong> {item.nextStep}</div>
                  <small className="inline-source">Source: {sourceById(snapshot, item.sourceId)?.name}</small>
                </div>
              </article>
            ))}
          </div>
        </section>

        <aside className="section feed-panel" aria-labelledby="feed-title">
          <div>
            <p className="eyebrow">Coverage gap</p>
            <h2 id="feed-title">What is not live yet</h2>
            <p className="panel-copy">These feeds are required before this can become a real-time operating dashboard.</p>
          </div>
          <div className="feed-list">
            {snapshot.requiredFeeds.map((feed) => (
              <article key={feed.id}>
                <span className="feed-off">×</span>
                <div><strong>{feed.name}</strong><p>{feed.blocker}</p></div>
              </article>
            ))}
          </div>
          <div className="controls-locked">
            <span>×</span>
            <div><strong>Production controls remain disabled</strong><p>This cockpit is read-only. It cannot restart services, activate workflows, send messages, or approve external actions.</p></div>
          </div>
        </aside>
      </div>

      <section className="section" id="work" aria-labelledby="work-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Agent + work status</p>
            <h2 id="work-title">Engineering workstreams</h2>
          </div>
          <span className="quiet-pill">Handoff status · not live agent telemetry</span>
        </div>
        <div className="work-grid">
          {snapshot.workstreams.map((work) => (
            <article className="work-card" key={work.id}>
              <div className="work-card-top">
                <span className={`work-status work-${work.state}`}>{work.label}</span>
                <small>{work.lastUpdate}</small>
              </div>
              <h3>{work.name}</h3>
              <p>{work.nextStep}</p>
              <small className="inline-source">Source: {sourceById(snapshot, work.sourceId)?.name}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="section processing-panel" id="processing" aria-labelledby="processing-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Processing outcomes</p>
            <h2 id="processing-title">Workflow activity</h2>
          </div>
          <span className={`quiet-pill ${snapshot.processing.source === "live" ? "live-pill" : "warning-pill"}`}>
            {snapshot.processing.source === "live"
              ? `Live metadata · last ${snapshot.processing.windowHours} hours`
              : "Live execution history unavailable"}
          </span>
        </div>
        {snapshot.processing.source === "live" ? (
          <>
            <div className="processing-summary" aria-label="Workflow execution summary">
              <article><span>Total runs</span><strong>{snapshot.processing.total}</strong></article>
              <article><span>Succeeded</span><strong>{snapshot.processing.succeeded}</strong></article>
              <article><span>Failed</span><strong>{snapshot.processing.failed}</strong></article>
              <article><span>Running / waiting</span><strong>{snapshot.processing.runningOrWaiting}</strong></article>
              <article>
                <span>Success rate</span>
                <strong>{snapshot.processing.successRate === null ? "—" : `${Math.round(snapshot.processing.successRate * 100)}%`}</strong>
              </article>
              <article><span>Active workflows</span><strong>{snapshot.processing.activeWorkflows.length}</strong></article>
            </div>
            <div className="execution-table" role="table" aria-label="Recent workflow executions">
              <div className="execution-row execution-header" role="row">
                <span role="columnheader">Workflow</span>
                <span role="columnheader">Outcome</span>
                <span role="columnheader">Started</span>
                <span role="columnheader">Duration</span>
              </div>
              {snapshot.processing.recentExecutions.length > 0 ? (
                snapshot.processing.recentExecutions.map((execution) => (
                  <div className="execution-row" role="row" key={execution.id}>
                    <div role="cell"><strong>{execution.workflow}</strong><small>{execution.mode}</small></div>
                    <div role="cell"><span className={`execution-status execution-${execution.status}`}>{execution.status}</span></div>
                    <time role="cell">{formatTimestamp(execution.startedAt)}</time>
                    <span role="cell">{formatDuration(execution.durationMs)}</span>
                  </div>
                ))
              ) : (
                <div className="empty-row">No recent executions were returned by the live bridge.</div>
              )}
            </div>
            <p className="privacy-note">Metadata only: workflow name, outcome, mode, time, and duration. No execution payloads or captured content.</p>
          </>
        ) : (
          <div className="processing-empty">
            <span>×</span>
            <div>
              <strong>Processing history is not available</strong>
              <p>{snapshot.processing.unavailableReason}</p>
            </div>
          </div>
        )}
      </section>

      <section className="section history-panel" id="history" aria-labelledby="history-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Verified outcomes + history</p>
            <h2 id="history-title">Evidence we can stand behind</h2>
          </div>
          <span className="quiet-pill warning-pill">Partial history · n8n execution feed missing</span>
        </div>
        <div className="history-list" role="list">
          {snapshot.outcomes.map((outcome) => (
            <article role="listitem" key={outcome.id}>
              <span className={`outcome-mark outcome-${outcome.state}`}>
                {outcome.state === "passed" || outcome.state === "confirmed" ? "✓" : "•"}
              </span>
              <time>{outcome.occurredOn}</time>
              <div><strong>{outcome.outcome}</strong><p>{outcome.system} · {outcome.detail}</p></div>
              <span className="history-source">{sourceById(snapshot, outcome.sourceId)?.name}</span>
            </article>
          ))}
        </div>
      </section>

      <section className="section sources-panel" id="sources" aria-labelledby="sources-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Source ledger</p>
            <h2 id="sources-title">Where every claim comes from</h2>
          </div>
          <span className="quiet-pill">No secrets or personal data</span>
        </div>
        <div className="sources-grid">
          {snapshot.sources.map((source) => (
            <details key={source.id} className={source.availability === "missing" ? "source-missing" : ""}>
              <summary>
                <span className={`source-dot source-${source.availability}`} />
                <span><strong>{source.name}</strong><small>{source.kind}</small></span>
                <time>{source.observedOn}</time>
              </summary>
              <div className="source-detail">
                <span>{source.location}</span>
                <p>{source.note}</p>
              </div>
            </details>
          ))}
        </div>
      </section>

      <footer>
        <span>Life OS Operating Cockpit · read-only v1</span>
        <span>
          {snapshot.telemetry.status === "live" ? "Production health connected" : "Reviewed source snapshot"}
          {" · private access unchanged"}
        </span>
      </footer>
    </main>
  );
}
