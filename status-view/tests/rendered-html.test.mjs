import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the Life OS control view", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>Life OS Control View<\/title>/i);
  assert.match(html, /Founder command center/);
  assert.match(html, /YouTube Enricher/);
  assert.match(html, /Live and healthy/);
  assert.match(html, /real-video test passed/i);
  assert.match(html, /Slack Resource Inbox/);
  assert.match(html, /Ready, not connected/);
  assert.match(html, /Career Ops pilot/);
  assert.match(html, /Paused by owner/);
  assert.match(html, /Production repair completed/);
  assert.match(html, /Knowledge Engine/);
  assert.match(html, /This is not live telemetry yet/);
  assert.match(html, /Live controls are locked/);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton/i);
});

test("removes starter-only preview assets and metadata", async () => {
  const [page, layout, packageJson] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/layout.tsx", import.meta.url), "utf8"),
    readFile(new URL("../package.json", import.meta.url), "utf8"),
  ]);

  assert.match(page, /Reported snapshot/);
  assert.match(page, /this view does not poll it/);
  assert.match(page, /Slack connection is still off/);
  assert.match(page, /pilot is not running/);
  assert.match(layout, /title: "Life OS Control View"/);
  assert.doesNotMatch(page + layout + packageJson, /codex-preview|react-loading-skeleton/i);
  await assert.rejects(access(new URL("app/_sites-preview", projectRoot)));
});
