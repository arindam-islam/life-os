#!/usr/bin/env python3
"""
Unit test suite for Life OS Automated AST Code Graph & Memory Indexer.
"""

import unittest
import os
import sys

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

from archive.prototypes.ast_code_graph import build_ast_graph, query_symbol, AST_GRAPH_PATH


class TestASTCodeGraph(unittest.TestCase):

    def test_ast_graph_build(self):
        graph = build_ast_graph()
        self.assertTrue(os.path.exists(AST_GRAPH_PATH))
        self.assertIn("files", graph)
        self.assertIn("symbol_index", graph)
        self.assertGreater(len(graph["files"]), 0)

    def test_ast_symbol_query(self):
        res = query_symbol("build_ast_graph")
        self.assertEqual(res["symbol"], "build_ast_graph")
        self.assertGreater(len(res["definitions"]), 0)


if __name__ == "__main__":
    unittest.main()
