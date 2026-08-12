from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("life_os_status_bridge", MODULE_PATH)
assert SPEC and SPEC.loader
app = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = app
SPEC.loader.exec_module(app)


class StatusBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = str(Path(self.temp_dir.name) / "database.sqlite")
        connection = sqlite3.connect(self.database_path)
        connection.executescript(
            """
            CREATE TABLE workflow_entity (
                id TEXT PRIMARY KEY,
                name TEXT,
                active INTEGER,
                isArchived INTEGER,
                updatedAt TEXT
            );
            CREATE TABLE execution_entity (
                id INTEGER PRIMARY KEY,
                workflowId TEXT,
                status TEXT,
                mode TEXT,
                startedAt TEXT,
                stoppedAt TEXT,
                deletedAt TEXT
            );
            INSERT INTO workflow_entity VALUES
                ('capture', 'Life OS - Capture Processor', 1, 0, '2026-08-12 09:00:00');
            INSERT INTO execution_entity VALUES
                (1, 'capture', 'success', 'webhook', datetime('now', '-5 minutes'), datetime('now', '-4 minutes'), NULL),
                (2, 'capture', 'error', 'webhook', datetime('now', '-3 minutes'), datetime('now', '-2 minutes'), NULL);
            """
        )
        connection.commit()
        connection.close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_execution_metrics_are_metadata_only(self):
        metrics = app.execution_metrics(self.database_path)
        self.assertEqual(metrics["total"], 2)
        self.assertEqual(metrics["succeeded"], 1)
        self.assertEqual(metrics["failed"], 1)
        self.assertEqual(metrics["success_rate"], 0.5)
        self.assertEqual(metrics["recent_executions"][0]["workflow"], "Life OS - Capture Processor")
        self.assertNotIn("data", metrics["recent_executions"][0])

    def test_configuration_requires_strong_token(self):
        with mock.patch.dict(app.os.environ, {"LIFE_OS_STATUS_TOKEN": "short"}, clear=True):
            with self.assertRaises(RuntimeError):
                app.BridgeConfig.from_environment()

    def test_http_endpoint_rejects_missing_token_and_all_writes(self):
        config = app.BridgeConfig(token="x" * 32, database_path=self.database_path, port=0)
        server = app.ThreadingHTTPServer(("127.0.0.1", 0), app.make_handler(config))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with self.assertRaises(urllib.error.HTTPError) as missing_auth:
                urllib.request.urlopen(f"{base}/life-os/status", timeout=2)
            self.assertEqual(missing_auth.exception.code, 401)

            request = urllib.request.Request(f"{base}/life-os/status", method="POST")
            with self.assertRaises(urllib.error.HTTPError) as post_error:
                urllib.request.urlopen(request, timeout=2)
            self.assertEqual(post_error.exception.code, 405)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_health_endpoint_is_minimal(self):
        config = app.BridgeConfig(token="x" * 32, database_path=self.database_path, port=0)
        server = app.ThreadingHTTPServer(("127.0.0.1", 0), app.make_handler(config))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urllib.request.urlopen(
                f"http://127.0.0.1:{server.server_port}/healthz", timeout=2
            ) as response:
                payload = json.loads(response.read())
            self.assertEqual(payload, {"ok": True, "service": "status-bridge"})
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_status_payload_declares_privacy_boundaries(self):
        config = app.BridgeConfig(token="x" * 32, database_path=self.database_path)
        healthy = {
            "state": "healthy",
            "checked_at": "2026-08-12T10:00:00Z",
            "detail": "Health check passed",
        }
        with mock.patch.object(app, "http_health", return_value=healthy):
            payload = app.build_status(config)
        self.assertEqual(payload["overall"], "operational")
        self.assertFalse(payload["privacy"]["contains_execution_payloads"])
        self.assertFalse(payload["privacy"]["contains_credentials"])
        self.assertFalse(payload["privacy"]["contains_captured_content"])


if __name__ == "__main__":
    unittest.main()
