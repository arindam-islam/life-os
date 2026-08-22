#!/usr/bin/env python3
"""
Unit tests for Life OS Autonomous Faceless AI Video & Reels Generator Engine.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.faceless_video_generator import (
    generate_video_script,
    format_srt_time,
    create_srt_file,
    synthesize_audio,
    build_ffmpeg_command,
    render_faceless_video
)


class TestFacelessVideoGenerator(unittest.TestCase):

    def test_generate_video_script(self):
        script = generate_video_script("Automation Tools", duration_sec=30.0)
        self.assertEqual(script["topic"], "Automation Tools")
        self.assertGreaterEqual(script["duration"], 30.0)
        self.assertIn("Automation Tools", script["segments"][0]["text"])
        self.assertEqual(len(script["segments"]), 5)

    def test_format_srt_time(self):
        self.assertEqual(format_srt_time(0.0), "00:00:00,000")
        self.assertEqual(format_srt_time(5.5), "00:00:05,500")
        self.assertEqual(format_srt_time(65.123), "00:01:05,123")

    def test_create_srt_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            srt_path = os.path.join(tmpdir, "test.srt")
            segments = [
                {"id": 1, "start": 0.0, "end": 2.5, "text": "Hello world"},
                {"id": 2, "start": 2.5, "end": 5.0, "text": "Subtitles test"}
            ]
            res_path = create_srt_file(segments, srt_path)
            self.assertTrue(os.path.exists(res_path))
            with open(res_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("00:00:00,000 --> 00:00:02,500", content)
            self.assertIn("Hello world", content)

    def test_synthesize_audio_fallback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "narration.wav")
            res_path = synthesize_audio("Test audio narration synthesis", audio_path)
            self.assertTrue(os.path.exists(res_path))
            self.assertGreater(os.path.getsize(res_path), 0)

    def test_build_ffmpeg_command(self):
        cmd = build_ffmpeg_command("audio.wav", "sub.srt", "out.mp4", aspect="9:16", duration=30.0)
        cmd_str = " ".join(cmd)
        self.assertIn("1080x1920", cmd_str)
        self.assertIn("subtitles=", cmd_str)
        self.assertIn("out.mp4", cmd_str)

    def test_render_faceless_video_dry_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "reel.mp4")
            res = render_faceless_video("3 AI Tools", aspect="9:16", duration=30.0, output_path=out_file, dry_run=True)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertTrue(os.path.exists(res["srt_path"]))
            self.assertTrue(os.path.exists(res["audio_path"]))
            self.assertIn("ffmpeg", res["ffmpeg_cmd"])


if __name__ == "__main__":
    unittest.main()
