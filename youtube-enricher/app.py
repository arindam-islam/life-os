import json
import logging
import os
import shutil
import subprocess
from datetime import date, datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from urllib.parse import urlsplit

from flask import Flask, jsonify, request

SERVICE_NAME = "youtube-enricher"
SERVICE_VERSION = "1.0.0"
MAX_REQUEST_BYTES = 8 * 1024
DEFAULT_TIMEOUT_SECONDS = 60
MAX_TIMEOUT_SECONDS = 60
MAX_URL_LENGTH = 2_048
ALLOWED_YOUTUBE_HOSTS = frozenset(
    {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "youtu.be",
        "youtube-nocookie.com",
        "www.youtube-nocookie.com",
    }
)


def _configured_timeout() -> int:
    raw_value = os.getenv("YTDLP_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS))
    try:
        timeout = int(raw_value)
    except ValueError:
        return DEFAULT_TIMEOUT_SECONDS
    return min(max(timeout, 10), MAX_TIMEOUT_SECONDS)


YTDLP_TIMEOUT_SECONDS = _configured_timeout()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_BYTES
logger = logging.getLogger(SERVICE_NAME)


def _error_response(status: int, code: str, message: str):
    return jsonify({"ok": False, "error": {"code": code, "message": message}}), status


def _validate_youtube_url(value):
    if not isinstance(value, str) or not value.strip():
        return None, "url must be a non-empty string"

    candidate = value.strip()
    if len(candidate) > MAX_URL_LENGTH:
        return None, f"url must be at most {MAX_URL_LENGTH} characters"

    try:
        parsed = urlsplit(candidate)
        port = parsed.port
    except ValueError:
        return None, "url is not valid"

    if parsed.scheme != "https":
        return None, "url must use https"
    if parsed.username or parsed.password:
        return None, "url must not contain credentials"
    if parsed.hostname not in ALLOWED_YOUTUBE_HOSTS:
        return None, "url must point to YouTube"
    if port not in (None, 443):
        return None, "url must use the standard https port"
    if not parsed.path or parsed.path == "/":
        return None, "url must identify a YouTube video"

    return candidate, None


def _yt_dlp_command(url: str):
    return [
        "yt-dlp",
        "--ignore-config",
        "--dump-single-json",
        "--skip-download",
        "--no-playlist",
        "--no-progress",
        "--socket-timeout",
        "15",
        "--retries",
        "2",
        "--extractor-retries",
        "2",
        "--",
        url,
    ]


def _iso_date(value):
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(f"{value[:4]}-{value[4:6]}-{value[6:8]}").isoformat()
    except ValueError:
        return None


def _iso_timestamp(value):
    if not isinstance(value, (int, float)):
        return None
    try:
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )
    except (OverflowError, OSError, ValueError):
        return None


def _string_list(value):
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _caption_summary(value):
    if not isinstance(value, dict):
        return []

    tracks = []
    for language in sorted(value):
        formats = value.get(language)
        if not isinstance(formats, list):
            continue

        extensions = sorted(
            {
                item.get("ext")
                for item in formats
                if isinstance(item, dict) and isinstance(item.get("ext"), str)
            }
        )
        display_name = next(
            (
                item.get("name")
                for item in formats
                if isinstance(item, dict) and isinstance(item.get("name"), str)
            ),
            None,
        )
        tracks.append(
            {
                "language": language,
                "name": display_name,
                "formats": extensions,
            }
        )
    return tracks


def _chapter_summary(value):
    if not isinstance(value, list):
        return []

    chapters = []
    for item in value:
        if not isinstance(item, dict):
            continue
        chapters.append(
            {
                "title": item.get("title"),
                "start_seconds": item.get("start_time"),
                "end_seconds": item.get("end_time"),
            }
        )
    return chapters


def _structured_metadata(data, requested_url: str):
    subtitles = _caption_summary(data.get("subtitles"))
    automatic_captions = _caption_summary(data.get("automatic_captions"))

    return {
        "ok": True,
        "source": "youtube",
        "video": {
            "id": data.get("id"),
            "title": data.get("title"),
            "description": data.get("description"),
            "requested_url": requested_url,
            "webpage_url": data.get("webpage_url") or requested_url,
            "duration_seconds": data.get("duration"),
            "duration_text": data.get("duration_string"),
            "thumbnail_url": data.get("thumbnail"),
            "availability": data.get("availability"),
            "age_limit": data.get("age_limit"),
            "language": data.get("language"),
            "live_status": data.get("live_status"),
            "is_live": bool(data.get("is_live")),
            "was_live": bool(data.get("was_live")),
            "tags": _string_list(data.get("tags")),
            "categories": _string_list(data.get("categories")),
        },
        "channel": {
            "id": data.get("channel_id"),
            "name": data.get("channel") or data.get("uploader"),
            "url": data.get("channel_url") or data.get("uploader_url"),
            "follower_count": data.get("channel_follower_count"),
        },
        "published": {
            "upload_date": _iso_date(data.get("upload_date")),
            "release_date": _iso_date(data.get("release_date")),
            "timestamp": _iso_timestamp(data.get("timestamp")),
            "release_timestamp": _iso_timestamp(data.get("release_timestamp")),
        },
        "engagement": {
            "view_count": data.get("view_count"),
            "like_count": data.get("like_count"),
            "comment_count": data.get("comment_count"),
        },
        "captions": {
            "subtitles": subtitles,
            "automatic": automatic_captions,
            "has_subtitles": bool(subtitles),
            "has_automatic_captions": bool(automatic_captions),
        },
        "chapters": _chapter_summary(data.get("chapters")),
        "extractor": {
            "name": data.get("extractor"),
            "key": data.get("extractor_key"),
        },
    }


@app.get("/health")
def health():
    try:
        yt_dlp_version = version("yt-dlp")
    except PackageNotFoundError:
        yt_dlp_version = None

    yt_dlp_available = shutil.which("yt-dlp") is not None
    deno_available = shutil.which("deno") is not None
    healthy = bool(yt_dlp_version and yt_dlp_available and deno_available)
    payload = {
        "ok": healthy,
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "dependencies": {
            "yt_dlp": {
                "available": yt_dlp_available,
                "version": yt_dlp_version,
            },
            "deno": {"available": deno_available},
        },
    }
    return jsonify(payload), 200 if healthy else 503


@app.post("/enrich")
def enrich():
    if not request.is_json:
        return _error_response(
            415, "unsupported_media_type", "content type must be application/json"
        )

    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return _error_response(400, "invalid_json", "request body must be a JSON object")

    url, validation_error = _validate_youtube_url(body.get("url"))
    if validation_error:
        return _error_response(400, "invalid_url", validation_error)

    try:
        result = subprocess.run(
            _yt_dlp_command(url),
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
            timeout=YTDLP_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        logger.warning("yt-dlp timed out after %s seconds", YTDLP_TIMEOUT_SECONDS)
        return _error_response(
            504, "extraction_timeout", "YouTube metadata extraction timed out"
        )
    except OSError:
        logger.exception("yt-dlp could not be started")
        return _error_response(
            503, "dependency_unavailable", "yt-dlp is unavailable in this service"
        )

    if result.returncode != 0:
        logger.warning("yt-dlp failed with exit code %s", result.returncode)
        return _error_response(
            502, "extraction_failed", "yt-dlp could not retrieve metadata for this video"
        )

    try:
        data = json.loads(result.stdout)
    except (json.JSONDecodeError, TypeError):
        logger.warning("yt-dlp returned invalid JSON")
        return _error_response(
            502, "invalid_extractor_response", "yt-dlp returned an invalid response"
        )

    if not isinstance(data, dict) or not data.get("id"):
        logger.warning("yt-dlp response did not contain a video id")
        return _error_response(
            502, "incomplete_extractor_response", "yt-dlp returned incomplete metadata"
        )

    return jsonify(_structured_metadata(data, url))


@app.errorhandler(413)
def request_too_large(_error):
    return _error_response(
        413,
        "request_too_large",
        f"request body must be at most {MAX_REQUEST_BYTES} bytes",
    )
