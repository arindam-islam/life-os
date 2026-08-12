"""Read-only telemetry bridge for the Life OS control view.

The bridge deliberately exposes operational metadata only. It never reads n8n
execution payloads, credential tables, environment files, or captured content.
"""

from __future__ import annotations

import hmac
import json
import os
import sqlite3
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


DEFAULT_DB_PATH = "/n8n-data/database.sqlite"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8788
DEFAULT_N8N_HEALTH_URL = "http://n8n:5678/healthz"
DEFAULT_YOUTUBE_HEALTH_URL = "http://youtube-enricher:8080/health"
DEFAULT_OMNIROUTE_HEALTH_URL = "http://omniroute:20128/"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime | None = None) -> str:
    current = value or utc_now()
    return current.astimezone(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def parse_sqlite_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class BridgeConfig:
    token: str
    database_path: str = DEFAULT_DB_PATH
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    n8n_health_url: str = DEFAULT_N8N_HEALTH_URL
    youtube_health_url: str = DEFAULT_YOUTUBE_HEALTH_URL
    omniroute_health_url: str = DEFAULT_OMNIROUTE_HEALTH_URL

    @classmethod
    def from_environment(cls) -> "BridgeConfig":
        token = os.environ.get("LIFE_OS_STATUS_TOKEN", "")
        if len(token) < 32:
            raise RuntimeError("LIFE_OS_STATUS_TOKEN must contain at least 32 characters")
        return cls(
            token=token,
            database_path=os.environ.get("LIFE_OS_N8N_DB", DEFAULT_DB_PATH),
            host=os.environ.get("LIFE_OS_STATUS_HOST", DEFAULT_HOST),
            port=int(os.environ.get("LIFE_OS_STATUS_PORT", str(DEFAULT_PORT))),
            n8n_health_url=os.environ.get(
                "LIFE_OS_N8N_HEALTH_URL", DEFAULT_N8N_HEALTH_URL
            ),
            youtube_health_url=os.environ.get(
                "LIFE_OS_YOUTUBE_HEALTH_URL", DEFAULT_YOUTUBE_HEALTH_URL
            ),
            omniroute_health_url=os.environ.get(
                "LIFE_OS_OMNIROUTE_HEALTH_URL", DEFAULT_OMNIROUTE_HEALTH_URL
            ),
        )


def http_health(url: str, timeout: float = 2.0) -> dict[str, Any]:
    checked_at = iso_utc()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            response.read(2048)
            healthy = 200 <= response.status < 300
            return {
                "state": "healthy" if healthy else "unavailable",
                "checked_at": checked_at,
                "detail": "Health check passed" if healthy else f"HTTP {response.status}",
            }
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {
            "state": "unavailable",
            "checked_at": checked_at,
            "detail": type(exc).__name__,
        }


def _connect_read_only(database_path: str) -> sqlite3.Connection:
    path = Path(database_path)
    if not path.is_file():
        raise FileNotFoundError(database_path)
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=2)
    connection.row_factory = sqlite3.Row
    return connection


def execution_metrics(database_path: str, window_hours: int = 24) -> dict[str, Any]:
    with _connect_read_only(database_path) as connection:
        counts = connection.execute(
            """
            SELECT status, COUNT(*) AS count
            FROM execution_entity
            WHERE startedAt >= datetime('now', ?)
              AND deletedAt IS NULL
            GROUP BY status
            """,
            (f"-{window_hours} hours",),
        ).fetchall()
        by_status = {str(row["status"]): int(row["count"]) for row in counts}

        recent = connection.execute(
            """
            SELECT e.id, w.name AS workflow, e.status, e.mode,
                   e.startedAt, e.stoppedAt
            FROM execution_entity e
            LEFT JOIN workflow_entity w ON w.id = e.workflowId
            WHERE e.deletedAt IS NULL
            ORDER BY e.id DESC
            LIMIT 12
            """
        ).fetchall()

        active = connection.execute(
            """
            SELECT name, updatedAt
            FROM workflow_entity
            WHERE active = 1 AND isArchived = 0
            ORDER BY name
            """
        ).fetchall()

    succeeded = by_status.get("success", 0)
    failed = by_status.get("error", 0) + by_status.get("crashed", 0)
    running = by_status.get("running", 0) + by_status.get("waiting", 0)
    finished = succeeded + failed

    recent_rows: list[dict[str, Any]] = []
    for row in recent:
        started = parse_sqlite_timestamp(row["startedAt"])
        stopped = parse_sqlite_timestamp(row["stoppedAt"])
        duration_ms = None
        if started and stopped:
            duration_ms = max(0, round((stopped - started).total_seconds() * 1000))
        recent_rows.append(
            {
                "id": int(row["id"]),
                "workflow": row["workflow"] or "Deleted workflow",
                "status": row["status"],
                "mode": row["mode"],
                "started_at": iso_utc(started) if started else None,
                "stopped_at": iso_utc(stopped) if stopped else None,
                "duration_ms": duration_ms,
            }
        )

    return {
        "window_hours": window_hours,
        "total": sum(by_status.values()),
        "succeeded": succeeded,
        "failed": failed,
        "running_or_waiting": running,
        "success_rate": round(succeeded / finished, 4) if finished else None,
        "by_status": by_status,
        "recent_executions": recent_rows,
        "active_workflows": [
            {"name": row["name"], "updated_at": row["updatedAt"]} for row in active
        ],
    }


def build_status(
    config: BridgeConfig,
) -> dict[str, Any]:
    generated_at = iso_utc()
    systems: list[dict[str, Any]] = []

    n8n = http_health(config.n8n_health_url)
    systems.append({"id": "n8n", "name": "Automation engine", **n8n})

    for system_id, display_name, health_url in (
        ("youtube-enricher", "YouTube enrichment", config.youtube_health_url),
        ("omniroute", "AI model routing", config.omniroute_health_url),
    ):
        state = http_health(health_url)
        systems.append({"id": system_id, "name": display_name, **state})

    try:
        processing = execution_metrics(config.database_path)
        database_state = {
            "id": "n8n-database",
            "name": "Workflow history",
            "state": "healthy",
            "checked_at": iso_utc(),
            "detail": "Read-only metadata query passed",
        }
    except (OSError, sqlite3.Error, ValueError) as exc:
        processing = {
            "window_hours": 24,
            "total": 0,
            "succeeded": 0,
            "failed": 0,
            "running_or_waiting": 0,
            "success_rate": None,
            "by_status": {},
            "recent_executions": [],
            "active_workflows": [],
            "unavailable_reason": type(exc).__name__,
        }
        database_state = {
            "id": "n8n-database",
            "name": "Workflow history",
            "state": "unavailable",
            "checked_at": iso_utc(),
            "detail": "Read-only metadata query failed",
        }
    systems.append(database_state)

    unavailable = sum(system["state"] != "healthy" for system in systems)
    overall = "operational" if unavailable == 0 else "degraded"

    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "overall": overall,
        "source": "Live read-only production telemetry",
        "systems": systems,
        "processing": processing,
        "privacy": {
            "contains_execution_payloads": False,
            "contains_credentials": False,
            "contains_captured_content": False,
        },
    }


def make_handler(config: BridgeConfig) -> type[BaseHTTPRequestHandler]:
    class StatusHandler(BaseHTTPRequestHandler):
        server_version = "LifeOSStatusBridge/1.0"

        def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def _authorized(self) -> bool:
            supplied = self.headers.get("Authorization", "")
            expected = f"Bearer {config.token}"
            return hmac.compare_digest(supplied, expected)

        def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
            if self.path == "/healthz":
                self._send_json(HTTPStatus.OK, {"ok": True, "service": "status-bridge"})
                return
            if self.path != "/life-os/status":
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                return
            if not self._authorized():
                self._send_json(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
                return
            self._send_json(HTTPStatus.OK, build_status(config))

        def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
            self._send_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "read_only"})

        def log_message(self, format: str, *args: Any) -> None:
            # BaseHTTPRequestHandler logs method/path/status only; headers and
            # bearer tokens are never included.
            super().log_message(format, *args)

    return StatusHandler


def main() -> None:
    config = BridgeConfig.from_environment()
    server = ThreadingHTTPServer((config.host, config.port), make_handler(config))
    server.serve_forever()


if __name__ == "__main__":
    main()
