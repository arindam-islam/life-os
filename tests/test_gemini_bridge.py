#!/usr/bin/env python3
"""
Unit test suite for Life OS Gemini <-> Antigravity 'agy' Keyword Activation Bridge.
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

from archive.prototypes.gemini_antigravity_bridge import dispatch_agy_command, load_json
import archive.prototypes.gemini_antigravity_bridge as bridge_module


class TestGeminiBridgeAGY(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.temp_notes_path = os.path.join(self.tmp_dir.name, "notes_index.json")
        self.temp_bridge_path = os.path.join(self.tmp_dir.name, "gemini_bridge_state.json")

        self.patcher_notes = patch.object(bridge_module, "NOTES_INDEX_PATH", self.temp_notes_path)
        self.patcher_bridge = patch.object(bridge_module, "BRIDGE_STATE_PATH", self.temp_bridge_path)

        self.patcher_notes.start()
        self.patcher_bridge.start()

    def tearDown(self):
        self.patcher_notes.stop()
        self.patcher_bridge.stop()
        self.tmp_dir.cleanup()

    def test_agy_make_note(self):
        record = dispatch_agy_command("agy make a note of this ideal faceless channel prompt setup")
        self.assertEqual(record["trigger"], "agy")
        self.assertEqual(record["intent"], "NOTE_SAVED")
        notes = load_json(bridge_module.NOTES_INDEX_PATH, default=[])
        self.assertGreater(len(notes), 0)
        self.assertEqual(notes[0]["content"], "ideal faceless channel prompt setup")

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
