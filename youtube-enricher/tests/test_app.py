import json
import subprocess
import unittest
from unittest.mock import patch

import app as enricher

VALID_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class EnricherApiTests(unittest.TestCase):
    def setUp(self):
        enricher.app.config.update(TESTING=True)
        self.client = enricher.app.test_client()

    def test_timeout_configuration_is_bounded(self):
        with patch.dict(enricher.os.environ, {"YTDLP_TIMEOUT_SECONDS": "999"}):
            self.assertEqual(enricher._configured_timeout(), 60)
        with patch.dict(enricher.os.environ, {"YTDLP_TIMEOUT_SECONDS": "1"}):
            self.assertEqual(enricher._configured_timeout(), 10)
        with patch.dict(enricher.os.environ, {"YTDLP_TIMEOUT_SECONDS": "invalid"}):
            self.assertEqual(enricher._configured_timeout(), 60)

    @patch("app.shutil.which", return_value="/usr/local/bin/dependency")
    def test_health(self, _which):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["ok"])
        self.assertEqual(response.get_json()["service"], "youtube-enricher")

    @patch("app.shutil.which", return_value=None)
    def test_health_fails_when_runtime_dependencies_are_missing(self, _which):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 503)
        self.assertFalse(response.get_json()["ok"])

    def test_enrich_requires_json_content_type(self):
        response = self.client.post("/enrich", data="url=not-json")

        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_json()["error"]["code"], "unsupported_media_type")

    def test_enrich_requires_an_object(self):
        response = self.client.post("/enrich", json=[{"url": VALID_URL}])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"]["code"], "invalid_json")

    def test_enrich_rejects_oversized_request(self):
        response = self.client.post(
            "/enrich",
            json={"url": "https://www.youtube.com/watch?v=" + ("a" * 9_000)},
        )

        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.get_json()["error"]["code"], "request_too_large")

    def test_enrich_rejects_non_youtube_url(self):
        response = self.client.post(
            "/enrich", json={"url": "https://example.com/video"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"]["code"], "invalid_url")

    def test_enrich_rejects_http_url(self):
        response = self.client.post(
            "/enrich", json={"url": "http://www.youtube.com/watch?v=abc"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"]["code"], "invalid_url")

    @patch("app.subprocess.run")
    def test_enrich_returns_structured_metadata_without_download_flags(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=json.dumps(
                {
                    "id": "dQw4w9WgXcQ",
                    "title": "Example title",
                    "description": "Example description",
                    "webpage_url": VALID_URL,
                    "duration": 213,
                    "duration_string": "3:33",
                    "thumbnail": "https://i.ytimg.com/example.jpg",
                    "channel_id": "channel-id",
                    "channel": "Example channel",
                    "channel_url": "https://www.youtube.com/channel/channel-id",
                    "channel_follower_count": 10,
                    "upload_date": "20260812",
                    "timestamp": 1786501800,
                    "view_count": 100,
                    "like_count": 5,
                    "comment_count": 2,
                    "tags": ["one", "two"],
                    "categories": ["Education"],
                    "subtitles": {"en": [{"ext": "vtt", "name": "English"}]},
                    "automatic_captions": {
                        "hi": [
                            {"ext": "json3", "name": "Hindi"},
                            {"ext": "vtt", "name": "Hindi"},
                        ]
                    },
                    "chapters": [
                        {"title": "Intro", "start_time": 0, "end_time": 30}
                    ],
                    "extractor": "youtube",
                    "extractor_key": "Youtube",
                }
            ),
            stderr="",
        )

        response = self.client.post("/enrich", json={"url": VALID_URL})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["video"]["id"], "dQw4w9WgXcQ")
        self.assertEqual(payload["published"]["upload_date"], "2026-08-12")
        self.assertEqual(payload["captions"]["subtitles"][0]["language"], "en")
        self.assertEqual(
            payload["captions"]["automatic"][0]["formats"], ["json3", "vtt"]
        )
        self.assertEqual(payload["chapters"][0]["start_seconds"], 0)

        command = run.call_args.args[0]
        self.assertIn("--skip-download", command)
        self.assertIn("--no-playlist", command)
        self.assertNotIn("--write-subs", command)
        self.assertNotIn("--write-auto-subs", command)
        self.assertEqual(command[-2:], ["--", VALID_URL])
        self.assertEqual(
            run.call_args.kwargs["timeout"], enricher.YTDLP_TIMEOUT_SECONDS
        )

    @patch("app.subprocess.run", side_effect=subprocess.TimeoutExpired("yt-dlp", 60))
    def test_enrich_handles_timeout(self, _run):
        response = self.client.post("/enrich", json={"url": VALID_URL})

        self.assertEqual(response.status_code, 504)
        self.assertEqual(response.get_json()["error"]["code"], "extraction_timeout")

    @patch("app.subprocess.run", side_effect=OSError("executable missing"))
    def test_enrich_handles_missing_yt_dlp(self, _run):
        response = self.client.post("/enrich", json={"url": VALID_URL})

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.get_json()["error"]["code"], "dependency_unavailable"
        )

    @patch("app.subprocess.run")
    def test_enrich_does_not_return_yt_dlp_stderr(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="sensitive upstream details",
        )

        response = self.client.post("/enrich", json={"url": VALID_URL})

        self.assertEqual(response.status_code, 502)
        self.assertNotIn("sensitive", response.get_data(as_text=True))
        self.assertEqual(response.get_json()["error"]["code"], "extraction_failed")

    @patch("app.subprocess.run")
    def test_enrich_handles_invalid_yt_dlp_json(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="not-json", stderr=""
        )

        response = self.client.post("/enrich", json={"url": VALID_URL})

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.get_json()["error"]["code"], "invalid_extractor_response"
        )


if __name__ == "__main__":
    unittest.main()
