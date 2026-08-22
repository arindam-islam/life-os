#!/usr/bin/env python3
"""
Unit test suite for Life OS Automated Career Ops (Tracker, Form-Filler & Feedback Loop).
"""

import unittest
import os
import sys

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

from scripts.career_ops_tracker import export_to_csv, CSV_TRACKER_PATH
from scripts.career_ops_form_filler import get_application_form_payload, generate_recruiter_email_draft
from scripts.career_ops_feedback import record_outcome, load_feedback_store


class TestCareerOpsFull(unittest.TestCase):

    def test_csv_export(self):
        path = export_to_csv()
        self.assertTrue(os.path.exists(path))

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
        self.assertIn("Arindam Islam", draft)
        self.assertIn("Test Co", draft)

    def test_feedback_loop_learning(self):
        store = record_outcome("TEST-001", "Test Co", "REJECTED", "Strict degree requirement missing")
        self.assertGreater(store["total_applications"], 0)


if __name__ == "__main__":
    unittest.main()
