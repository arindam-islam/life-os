#!/usr/bin/env python3
"""
Unit test suite for Life OS Automated Career Ops (Tracker, Form-Filler & Feedback Loop).
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

from scripts import career_ops_tracker, career_ops_form_filler, career_ops_feedback
from scripts.career_ops_tracker import export_to_csv
from scripts.career_ops_form_filler import get_application_form_payload, generate_recruiter_email_draft
from scripts.career_ops_feedback import record_outcome, load_feedback_store


class TestCareerOpsFull(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.temp_csv_path = os.path.join(self.tmp_dir.name, "job_tracker.csv")
        self.temp_outreach_dir = os.path.join(self.tmp_dir.name, "outreach")
        self.temp_feedback_path = os.path.join(self.tmp_dir.name, "feedback_loop.json")

        self.patcher_csv = patch.object(career_ops_tracker, "CSV_TRACKER_PATH", self.temp_csv_path)
        self.patcher_outreach = patch.object(career_ops_form_filler, "OUTREACH_DIR", self.temp_outreach_dir)
        self.patcher_feedback = patch.object(career_ops_feedback, "FEEDBACK_STORE_PATH", self.temp_feedback_path)

        self.patcher_csv.start()
        self.patcher_outreach.start()
        self.patcher_feedback.start()

    def tearDown(self):
        self.patcher_csv.stop()
        self.patcher_outreach.stop()
        self.patcher_feedback.stop()
        self.tmp_dir.cleanup()

    def test_csv_export(self):
        path = export_to_csv()
        self.assertTrue(os.path.exists(path))
        self.assertEqual(path, self.temp_csv_path)

    def test_form_payload(self):
        job = {"job_id": "TEST-001", "company": "Test Co", "title": "Lead Ops"}
        payload = get_application_form_payload(job)
        self.assertEqual(payload["full_name"], "Arindam Islam")
        self.assertEqual(payload["expected_ctc_lpa"], 18.0)
        self.assertEqual(payload["min_ctc_lpa_floor"], 16.5)

    def test_recruiter_email_draft_creation(self):
        job = {"job_id": "TEST-001", "company": "Test Co", "title": "Lead Ops", "recruiter_details": {"name": "Test Recruiter"}}
        path, draft = generate_recruiter_email_draft(job)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.startswith(self.temp_outreach_dir))
        self.assertIn("Arindam Islam", draft)
        self.assertIn("Test Co", draft)

    def test_feedback_loop_learning(self):
        store = record_outcome("TEST-001", "Test Co", "REJECTED", "Strict degree requirement missing")
        self.assertGreater(store["total_applications"], 0)
        self.assertTrue(os.path.exists(self.temp_feedback_path))


if __name__ == "__main__":
    unittest.main()
