import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);

async function request(path = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}-${path}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request(`http://localhost${path}`, { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the source-backed Life OS cockpit", async () => {
  const response = await request();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>Life OS Control View<\/title>/i);
  assert.match(html, /Private operating cockpit/);
  assert.match(html, /Component health \+ freshness/);
  assert.match(html, /Real-video production test passed/);
  assert.match(html, /Attention \+ approvals/);
  assert.match(html, /Agent \+ work status/);
  assert.match(html, /Source ledger/);
  assert.match(html, /Reviewed source snapshot/);
  assert.match(html, /Checks again automatically every 30 seconds/);
  assert.match(html, /Processing outcomes/);
  assert.match(html, /Production controls remain disabled/);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton/i);
});

test("serves the reviewed cockpit snapshot through a read-only endpoint", async () => {
  const response = await request("/api/cockpit");
  assert.equal(response.status, 200);
  assert.match(response.headers.get("cache-control") ?? "", /private/);
  assert.match(response.headers.get("cache-control") ?? "", /no-store/);

  const payload = await response.json();
  assert.equal(payload.mode, "partial");
  assert.equal(payload.telemetry.status, "fallback");
  assert.equal(payload.asOf, "2026-08-12");
  assert.equal(payload.components.find((item) => item.id === "youtube-enricher").state, "healthy");
  assert.equal(payload.components.find((item) => item.id === "slack-inbox").state, "ready");
  assert.equal(payload.requiredFeeds.every((feed) => feed.state === "missing"), true);
  assert.equal(payload.processing.source, "unavailable");
  assert.equal(typeof payload.servedAt, "string");

  const sourceIds = new Set(payload.sources.map((source) => source.id));
  const allReferences = [
    ...payload.components.flatMap((component) => component.sourceIds),
    ...payload.outcomes.map((outcome) => outcome.sourceId),
    ...payload.attention.map((item) => item.sourceId),
    ...payload.workstreams.map((work) => work.sourceId),
  ];
  assert.equal(allReferences.every((id) => sourceIds.has(id)), true);
  assert.equal(new Set(payload.components.map((item) => item.id)).size, payload.components.length);
  assert.equal(new Set(payload.sources.map((item) => item.id)).size, payload.sources.length);
});

test("keeps provenance explicit and removes starter-only assets", async () => {
  const [page, data, layout, packageJson] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/cockpit-source.ts", import.meta.url), "utf8"),
    readFile(new URL("../app/layout.tsx", import.meta.url), "utf8"),
    readFile(new URL("../package.json", import.meta.url), "utf8"),
  ]);

  assert.match(page, /\/api\/cockpit/);
  assert.match(page, /30 \* 1000/);
  assert.match(data, /Production acceptance handoff/);
  assert.match(data, /slack-resource-inbox\/README\.md \+ DEPLOYMENT\.md/);
  assert.match(data, /Required live source/);
  assert.match(layout, /title: "Life OS Control View"/);
  assert.doesNotMatch(page + data + layout + packageJson, /codex-preview|react-loading-skeleton/i);
  assert.doesNotMatch(page + data, /LIFE_OS_STATUS_TOKEN|authorization: `Bearer/);
  await assert.rejects(access(new URL("app/_sites-preview", projectRoot)));
});

test("keeps bridge authentication server-side", async () => {
  const route = await readFile(new URL("../app/api/cockpit/route.ts", import.meta.url), "utf8");
  assert.match(route, /process\.env\.LIFE_OS_STATUS_URL/);
  assert.match(route, /process\.env\.LIFE_OS_STATUS_TOKEN/);
  assert.match(route, /authorization: `Bearer \$\{bridgeToken\}`/);
  assert.match(route, /cache: "no-store"/);
  assert.match(route, /AbortSignal\.timeout\(BRIDGE_TIMEOUT_MS\)/);
  assert.match(route, /contains_execution_payloads === false/);
  assert.match(route, /contains_credentials === false/);
  assert.match(route, /contains_captured_content === false/);
});
