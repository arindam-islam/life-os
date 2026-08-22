#!/usr/bin/env python3
"""
Unit tests for Life OS Multi-Agent Slack Bot Workforce Integration.
"""

import os
import sys
import json
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from archive.prototypes.slack_workforce_agents import (
    qualify_b2b_lead,
    generate_content_package,
    analyze_dev_diagnostic,
    dispatch_slack_workforce_agent,
    LEADS_LEDGER_PATH
)


class TestSlackWorkforceAgents(unittest.TestCase):

    def test_qualify_b2b_lead_high_budget(self):
        res = qualify_b2b_lead("We need enterprise AI automation with $50k budget ASAP", user_id="U_TEST1")
        self.assertEqual(res["agent"], "b2b-lead-agent")
        self.assertEqual(res["lead_data"]["status"], "QUALIFIED")
        self.assertGreaterEqual(res["lead_data"]["score"], 70)
        self.assertEqual(res["lead_data"]["budget_estimate"], "High / Enterprise")
        self.assertIn("blocks", res["slack_response"])

    def test_qualify_b2b_lead_persistence(self):
        qualify_b2b_lead("Looking for custom dev quote", user_id="U_TEST2")
        self.assertTrue(LEADS_LEDGER_PATH.exists())
        with open(LEADS_LEDGER_PATH, "r", encoding="utf-8") as f:
            leads = json.load(f)
        self.assertGreater(len(leads), 0)

    def test_generate_content_package(self):
        res = generate_content_package("Faceless Video Generation")
        self.assertEqual(res["agent"], "content-agent")
        self.assertIn("Faceless Video Generation", res["linkedin_post"])
        self.assertEqual(len(res["twitter_thread"]), 5)
        self.assertIn("faceless_video_generator.py", res["slack_response"]["blocks"][4]["text"]["text"])

    def test_analyze_dev_diagnostic_valid(self):
        valid_code = "```python\ndef hello():\n    return 'world'\n```"
        res = analyze_dev_diagnostic(valid_code)
        self.assertEqual(res["agent"], "dev-agent")
        self.assertTrue(res["syntax_valid"])
        self.assertEqual(res["status"], "OK")

    def test_analyze_dev_diagnostic_invalid(self):
        invalid_code = "```python\ndef broken_func(\n```"
        res = analyze_dev_diagnostic(invalid_code)
        self.assertEqual(res["agent"], "dev-agent")
        self.assertFalse(res["syntax_valid"])
        self.assertEqual(res["status"], "SYNTAX_ERROR")

    def test_dispatch_slack_workforce_agent_routing(self):
        res_lead = dispatch_slack_workforce_agent("@b2b-lead-agent Client quote request")
        self.assertEqual(res_lead["agent"], "b2b-lead-agent")

        res_content = dispatch_slack_workforce_agent("@content-agent Post idea about AI")
        self.assertEqual(res_content["agent"], "content-agent")

        res_dev = dispatch_slack_workforce_agent("@dev-agent Fix syntax bug")
        self.assertEqual(res_dev["agent"], "dev-agent")

        res_fallback = dispatch_slack_workforce_agent("Hello team!")
        self.assertEqual(res_fallback["agent"], "workforce-orchestrator")


if __name__ == "__main__":
    unittest.main()
