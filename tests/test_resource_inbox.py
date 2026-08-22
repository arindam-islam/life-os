#!/usr/bin/env python3
"""
Unit tests for Life OS Multimodal Resource Inbox & Verification Wall Engine.
"""

import os
import sys
import json
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.resource_inbox_router import (
    clean_social_fluff,
    run_authenticity_verification_wall,
    classify_area_domain,
    process_inbox_resource
)

from scripts.domain_distribution_engine import (
    distribute_resource_to_area,
    AREAS_MAP,
    AREAS_DIR
)


class TestResourceInboxEngine(unittest.TestCase):

    def test_clean_social_fluff(self):
        raw = "Check out this AI hack! Comment YES to get DM link! Follow for more tips and save this reel!"
        cleaned = clean_social_fluff(raw)
        self.assertNotIn("Comment YES to get DM link", cleaned)
        self.assertNotIn("Follow for more tips", cleaned)
        self.assertNotIn("save this reel", cleaned)

    def test_authenticity_verification_wall_authentic(self):
        title = "Circadian Rhythms & Energy Protocol"
        text = "Viewing early morning light sets the suprachiasmatic nucleus master clock."
        status, score, rationale = run_authenticity_verification_wall(title, text, "Dr. Andrew Huberman")
        self.assertEqual(status, "VERIFIED_AUTHENTIC")
        self.assertGreaterEqual(score, 85)
        self.assertIn("Passed Authenticity Wall", rationale)

    def test_authenticity_verification_wall_unauthentic(self):
        title = "Make 100k overnight"
        text = "Guaranteed 100x return in 2 days zero effort"
        status, score, rationale = run_authenticity_verification_wall(title, text, "Scam Channel")
        self.assertEqual(status, "REJECTED_UNAUTHENTIC")
        self.assertEqual(score, 20)
        self.assertIn("Failed Authenticity Wall", rationale)

    def test_classify_area_domain(self):
        self.assertEqual(classify_area_domain("nutrition workout body sleep habits"), "HEALTH_WELLNESS")
        self.assertEqual(classify_area_domain("podcast conversation confession lyrics music"), "CREATIVE_CONVERSATIONS")
        self.assertEqual(classify_area_domain("productivity workflow time management hack"), "PRODUCTIVITY_HACKS")
        self.assertEqual(classify_area_domain("saas revenue monetization business strategy wealth"), "CAREER_WEALTH")
        self.assertEqual(classify_area_domain("custom python llm agent pipeline"), "AI_AUTOMATION")

    def test_distribute_resource_to_area_resources_folder(self):
        sample = {
            "title": "Sleep & Nutrition Optimization Protocol",
            "domain": "HEALTH_WELLNESS",
            "resource_type": "PDF_DOCUMENT",
            "url_or_path": "circadian_guide.pdf",
            "uploader": "Dr. Wellness",
            "summary_5min": "Simple 5-minute summary explaining light exposure timing.",
            "trust_score": 90,
            "verification_status": "VERIFIED_AUTHENTIC",
            "verification_rationale": "Verified peer-reviewed evidence.",
            "concept_explanation": "Viewing morning light sets the master clock.",
            "current_state_context": "Dim indoor light delays sleep phase shift.",
            "solution_and_how_to": "Go outside 10 minutes every morning.",
            "measurement_metrics": "Track wakefulness score.",
            "long_term_growth_wealth": "High physical energy fuels sustained execution.",
            "key_deliverables": ["1. Morning Light Protocol Checklist", "2. Faceless Reel Script"],
            "reel_script": {
                "topic": "Sleep & Nutrition Optimization Protocol",
                "duration": 30.0,
                "segments": [{"id": 1, "start": 0.0, "end": 5.0, "type": "HOOK", "text": "Do this every morning!"}]
            }
        }

        res = distribute_resource_to_area(sample)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["area"], "health_wellness")
        self.assertTrue(os.path.exists(res["dossier_path"]))
        self.assertIn("/areas/health_wellness/resources/", res["dossier_path"])

        # Verify dossier contents
        with open(res["dossier_path"], "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("# 📚 Sleep & Nutrition Optimization Protocol", content)
        self.assertIn("VERIFIED_AUTHENTIC", content)
        self.assertIn("5-Minute Executive Summary", content)
        self.assertIn("Long-Term Wealth & Growth Scale Strategy", content)

    def test_process_inbox_resource_end_to_end(self):
        res = process_inbox_resource("Simple direct note on daily mindfulness and vitamin practices")
        self.assertEqual(res["status"], "PROCESSED")
        self.assertEqual(res["domain"], "HEALTH_WELLNESS")
        self.assertEqual(res["verification_status"], "VERIFIED_AUTHENTIC")
        self.assertTrue(os.path.exists(res["dossier_path"]))
        self.assertIn("/resources/", res["dossier_path"])


if __name__ == "__main__":
    unittest.main()
