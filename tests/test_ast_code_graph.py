#!/usr/bin/env python3
"""
Unit test suite for Life OS Automated AST Code Graph & Memory Indexer.
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

import archive.prototypes.ast_code_graph as ast_module
from archive.prototypes.ast_code_graph import build_ast_graph, query_symbol


class TestASTCodeGraph(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.temp_ast_graph = os.path.join(self.tmp_dir.name, "ast_graph.json")
        self.patcher_graph = patch.object(ast_module, "AST_GRAPH_PATH", self.temp_ast_graph)
        self.patcher_graph.start()

    def tearDown(self):
        self.patcher_graph.stop()
        self.tmp_dir.cleanup()

    def test_ast_graph_build(self):
        graph = build_ast_graph()
        self.assertTrue(os.path.exists(self.temp_ast_graph))
        self.assertIn("files", graph)
        self.assertIn("symbol_index", graph)
        self.assertGreater(len(graph["files"]), 0)

    def test_ast_symbol_query(self):
        build_ast_graph()
        res = query_symbol("build_ast_graph")
        self.assertEqual(res["symbol"], "build_ast_graph")
        self.assertGreater(len(res["definitions"]), 0)


if __name__ == "__main__":
    unittest.main()
