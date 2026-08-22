#!/usr/bin/env python3
"""
Unit test suite for Life OS Gemini <-> Antigravity 'agy' Keyword Activation Bridge.
"""

import unittest
import os
import sys

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

from archive.prototypes.gemini_antigravity_bridge import dispatch_agy_command, BRIDGE_STATE_PATH, NOTES_INDEX_PATH, load_json


class TestGeminiBridgeAGY(unittest.TestCase):

    def test_agy_make_note(self):
        record = dispatch_agy_command("agy make a note of this ideal faceless channel prompt setup")
        self.assertEqual(record["trigger"], "agy")
        self.assertEqual(record["intent"], "NOTE_SAVED")
        notes = load_json(NOTES_INDEX_PATH, default=[])
        self.assertGreater(len(notes), 0)

    def test_agy_tasks_left(self):
        record = dispatch_agy_command("agy what are todays tasks left")
        self.assertEqual(record["intent"], "TASKS_QUERIED")
        self.assertIn("Active Life OS Tracks", record["response"])

    def test_agy_evaluate_idea(self):
        record = dispatch_agy_command("agy what do you think about this strategy")
        self.assertEqual(record["intent"], "IDEA_EVALUATED")

    def test_agy_general_instruction(self):
        record = dispatch_agy_command("agy scan LinkedIn for product ops roles")
        self.assertEqual(record["intent"], "INSTRUCTION_DISPATCHED")


if __name__ == "__main__":
    unittest.main()
