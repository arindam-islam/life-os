"use client";

import { useState } from "react";

type SystemState = "healthy" | "reported" | "ready" | "priority" | "planned";

const systems: Array<{
  name: string;
  role: string;
  state: SystemState;
  label: string;
  source: string;
  mark: string;
}> = [
  {
    name: "n8n",
    role: "Runs Life OS workflows",
    state: "healthy",
    label: "Production healthy",
    source: "Verified during the safe rollout · this view does not poll it",
    mark: "N",
  },
  {
    name: "OmniRoute",
    role: "Routes work to the right AI model",
    state: "healthy",
    label: "Production healthy",
    source: "Verified during the safe rollout · this view does not poll it",
    mark: "O",
  },
  {
    name: "Capture API",
    role: "Receives new ideas and resources",
    state: "reported",
    label: "Reported healthy",
    source: "Latest reported production handoff · this view does not poll it",
    mark: "C",
  },
  {
    name: "Durable storage",
    role: "Keeps approved, cleaned information",
    state: "reported",
    label: "Reported healthy",
    source: "Latest reported production handoff · this view does not poll it",
    mark: "D",
  },
  {
    name: "YouTube Enricher",
    role: "Turns videos into useful knowledge",
    state: "healthy",
    label: "Live and healthy",
    source: "Production deployment + real-video test passed · this view does not poll it",
    mark: "Y",
  },
  {
    name: "Slack Resource Inbox",
    role: "Captures links dropped in Slack",
    state: "ready",
    label: "Ready, not connected",
    source: "Channel + inactive adapter ready · Slack connection is still off",
    mark: "S",
  },
  {
    name: "Career Ops pilot",
    role: "Tests the job-search workflow safely",
    state: "planned",
    label: "Paused by owner",
    source: "Held until the next product review · pilot is not running",
    mark: "P",
  },
  {
    name: "Knowledge Engine",
    role: "Connects and recalls what matters",
    state: "planned",
    label: "Planned",
    source: "Not deployed",
    mark: "K",
  },
  {
    name: "Agents",
    role: "Completes approved work across Life OS",
    state: "planned",
    label: "Planned",
    source: "Not deployed",
    mark: "A",
  },
];

const stateFilters: Array<{ key: "all" | SystemState; label: string }> = [
  { key: "all", label: "All systems" },
  { key: "healthy", label: "Production healthy" },
  { key: "reported", label: "Reported healthy" },
  { key: "ready", label: "Ready" },
  { key: "priority", label: "Next priority" },
  { key: "planned", label: "Planned" },
];

const rollout = [
  { title: "Prepare safely", detail: "Code reviewed and deployment isolated", status: "done" },
  { title: "Deploy only the new service", detail: "n8n and OmniRoute left intact", status: "done" },
  { title: "Confirm service health", detail: "Production health check passed", status: "done" },
  { title: "Test a real video", detail: "A production enrichment completed successfully", status: "done" },
  { title: "Protect the existing system", detail: "n8n and OmniRoute remained healthy", status: "done" },
];

export default function Home() {
  const [filter, setFilter] = useState<(typeof stateFilters)[number]["key"]>("all");
  const visibleSystems = systems.filter((system) => filter === "all" || system.state === filter);

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Life OS command center home">
          <span className="brand-mark">L</span>
          <span>Life OS</span>
        </a>
        <nav aria-label="Dashboard sections">
          <a href="#systems">Systems</a>
          <a href="#rollout">Rollout</a>
          <a href="#activity">Activity</a>
        </nav>
        <div className="snapshot-chip"><span /> Reported snapshot</div>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow">Founder command center</p>
          <h1>See what is working.<br />See what happens next.</h1>
          <p className="hero-note">
            One nontechnical view of Life OS health, current engineering work, and the decisions that stay with you.
          </p>
        </div>
        <aside className="truth-card" aria-label="Data status">
          <div className="truth-icon">i</div>
          <div>
            <strong>This is not live telemetry yet</strong>
            <p>Health labels reflect the latest production verification and reported handoff. This page does not poll services or enable controls.</p>
          </div>
        </aside>
      </section>

      <section className="summary-grid" aria-label="System summary">
        <article className="summary-card accent-green">
          <span>Production healthy</span>
          <strong>3</strong>
          <small>n8n, OmniRoute + YouTube</small>
        </article>
        <article className="summary-card accent-amber">
          <span>Reported healthy</span>
          <strong>2</strong>
          <small>Capture + storage</small>
        </article>
        <article className="summary-card accent-grey">
          <span>Ready, not connected</span>
          <strong>1</strong>
          <small>Slack Resource Inbox</small>
        </article>
        <article className="summary-card summary-wide">
          <span>Current priority</span>
          <strong className="priority-text">Connect Slack Resource Inbox safely</strong>
          <small>Adapter ready · reusable Slack credential still required</small>
        </article>
      </section>

      <section className="pipeline" aria-labelledby="pipeline-title">
        <div className="section-heading compact-heading">
          <div>
            <p className="eyebrow">How Life OS moves information</p>
            <h2 id="pipeline-title">Capture → understand → decide → remember</h2>
          </div>
          <span className="label-pill">Founder approval protects sensitive actions</span>
        </div>
        <div className="pipeline-rail">
          {[
            ["01", "Capture", "iPhone live · Slack ready"],
            ["02", "Clean", "Remove noise"],
            ["03", "Understand", "Find meaning"],
            ["04", "Decide", "Choose next action"],
            ["05", "Store / Act", "With approval"],
          ].map(([number, title, detail], index) => (
            <div className="pipeline-step" key={title}>
              <span className="step-number">{number}</span>
              <strong>{title}</strong>
              <small>{detail}</small>
              {index < 4 && <span className="rail-arrow" aria-hidden="true">→</span>}
            </div>
          ))}
        </div>
      </section>

      <section className="section" id="systems" aria-labelledby="systems-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">System map</p>
            <h2 id="systems-title">Every part of Life OS</h2>
          </div>
          <div className="filters" aria-label="Filter systems">
            {stateFilters.map((item) => (
              <button
                className={filter === item.key ? "active" : ""}
                key={item.key}
                onClick={() => setFilter(item.key)}
                aria-pressed={filter === item.key}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
        <div className="systems-grid">
          {visibleSystems.map((system) => (
            <article className="system-card" key={system.name}>
              <div className={`system-mark state-${system.state}`}>{system.mark}</div>
              <div className="system-main">
                <h3>{system.name}</h3>
                <p>{system.role}</p>
              </div>
              <div className={`status status-${system.state}`}><span />{system.label}</div>
              <small className="source-label">{system.source}</small>
            </article>
          ))}
        </div>
      </section>

      <div className="split-layout">
        <section className="section panel" id="rollout" aria-labelledby="rollout-title">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Engineering rollout</p>
              <h2 id="rollout-title">YouTube Enrichment v1</h2>
            </div>
            <span className="status status-healthy"><span />Live and tested</span>
          </div>
          <ol className="rollout-list">
            {rollout.map((item, index) => (
              <li className={item.status} key={item.title}>
                <div className="rollout-marker">{item.status === "done" ? "✓" : index + 1}</div>
                <div>
                  <strong>{item.title}</strong>
                  <p>{item.detail}</p>
                </div>
                <span className="rollout-label">
                  {item.status === "done" ? "Complete" : "Queued"}
                </span>
              </li>
            ))}
          </ol>
        </section>

        <aside className="section panel guardrail-panel" aria-labelledby="guardrails-title">
          <div>
            <p className="eyebrow">Your control boundary</p>
            <h2 id="guardrails-title">You approve what can affect you</h2>
            <p className="panel-copy">Engineering can proceed independently until work reaches one of these gates.</p>
          </div>
          <ul className="guardrail-list">
            <li><span>01</span><strong>Personal or sensitive details</strong></li>
            <li><span>02</span><strong>Payments or new spend</strong></li>
            <li><span>03</span><strong>Public or reputation-sensitive actions</strong></li>
            <li><span>04</span><strong>Destructive or materially risky production changes</strong></li>
          </ul>
          <div className="controls-locked">
            <span className="lock-mark">×</span>
            <div><strong>Live controls are locked</strong><p>Controls will activate only after authenticated health checks are safely connected.</p></div>
          </div>
          <div className="control-actions">
            <button disabled>Run live health check</button>
            <button disabled>Pause automations</button>
          </div>
        </aside>
      </div>

      <section className="section activity-panel" id="activity" aria-labelledby="activity-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Recent activity</p>
            <h2 id="activity-title">What the engineering system is doing</h2>
          </div>
          <span className="label-pill">Reported events · not a live feed</span>
        </div>
        <div className="activity-list" role="list">
          <article role="listitem">
            <span className="activity-mark green">✓</span>
            <div><strong>YouTube Enricher is live</strong><p>Production deployment and the health check completed successfully.</p></div>
            <time>Live</time>
          </article>
          <article role="listitem">
            <span className="activity-mark green">✓</span>
            <div><strong>Real-video test passed</strong><p>A real video completed the production enrichment flow successfully.</p></div>
            <time>Verified</time>
          </article>
          <article role="listitem">
            <span className="activity-mark blue">S</span>
            <div><strong>Slack Resource Inbox is ready</strong><p>The channel and inactive adapter are prepared; the Slack connection remains off.</p></div>
            <time>Not connected</time>
          </article>
          <article role="listitem">
            <span className="activity-mark green">✓</span>
            <div><strong>Production repair completed</strong><p>n8n file access was corrected and exposed pinned test data was cleared.</p></div>
            <time>Verified</time>
          </article>
          <article role="listitem">
            <span className="activity-mark amber">P</span>
            <div><strong>Career Ops pilot paused</strong><p>The owner asked to resume this work together after lunch.</p></div>
            <time>On hold</time>
          </article>
        </div>
      </section>

      <footer>
        <span>Life OS Control View · v0.1</span>
        <span>Visibility first. Live telemetry and controls come next.</span>
      </footer>
    </main>
  );
}
