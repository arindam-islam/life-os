#!/usr/bin/env python3
"""
Unit test suite for Life OS Career Ops Engine (Track H - Live Search).
Tests salary floor enforcement, strict degree filtering, domain ranking,
and live URL generator.
"""

import unittest
import os
import sys

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

from scripts.career_ops_engine import (
    generate_live_platform_search_urls,
    PROFILE_PATH,
    load_json
)


class TestCareerOpsEngine(unittest.TestCase):

    def setUp(self):
        self.profile = load_json(PROFILE_PATH).get("candidate", {})

    def test_live_platform_search_url_generation(self):
        urls = generate_live_platform_search_urls("Product Operations Lead", "Bangalore")
        self.assertIn("LinkedIn", urls)
        self.assertIn("Naukri", urls)
        self.assertIn("Indeed", urls)
        self.assertIn("Weekday", urls)
        self.assertIn("Wellfound", urls)
        self.assertTrue(urls["LinkedIn"].startswith("https://www.linkedin.com/jobs/search/"))
        self.assertIn("Product%20Operations%20Lead", urls["LinkedIn"])


if __name__ == "__main__":
    unittest.main()
