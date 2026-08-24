#!/usr/bin/env python3
"""
Life OS Automated AST Code Graph & Memory Indexer
Parses all Python codebase files, extracts functions, classes, imports, call chains,
and updates machine-readable knowledge index at .life-os/knowledge/ast_graph.json.
Runs 100% locally in background under Antigravity. Zero external apps required.
"""

import os
import sys
import json
import ast
import datetime

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AST_GRAPH_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "knowledge", "ast_graph.json")


class CodebaseVisitor(ast.NodeVisitor):
    def __init__(self, rel_path):
        self.rel_path = rel_path
        self.functions = []
        self.classes = []
        self.imports = []
        self.calls = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({"name": alias.name, "as": alias.asname, "line": node.lineno})
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for alias in node.names:
            self.imports.append({"name": f"{module}.{alias.name}", "as": alias.asname, "line": node.lineno})
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        args = [arg.arg for arg in node.args.args]
        self.functions.append({
            "name": node.name,
            "args": args,
            "line_start": node.lineno,
            "line_end": getattr(node, "end_lineno", node.lineno),
            "docstring": ast.get_docstring(node)
        })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        self.classes.append({
            "name": node.name,
            "bases": bases,
            "line_start": node.lineno,
            "line_end": getattr(node, "end_lineno", node.lineno),
            "docstring": ast.get_docstring(node)
        })
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append({"name": node.func.id, "line": node.lineno})
        elif isinstance(node.func, ast.Attribute):
            self.calls.append({"name": node.func.attr, "line": node.lineno})
        self.generic_visit(node)


def build_ast_graph():
    graph = {
        "updated_at": datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(),
        "files": {},
        "symbol_index": {}
    }

    for root, dirs, files in os.walk(WORKSPACE_ROOT):
        # Exclude venv, .git, node_modules
        dirs[:] = [d for d in dirs if d not in (".git", "venv", "node_modules", ".next", "__pycache__")]
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, WORKSPACE_ROOT)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        source = f.read()
                    tree = ast.parse(source, filename=rel_path)
                    visitor = CodebaseVisitor(rel_path)
                    visitor.visit(tree)

                    file_entry = {
                        "path": rel_path,
                        "functions": visitor.functions,
                        "classes": visitor.classes,
                        "imports": visitor.imports,
                        "calls": visitor.calls
                    }
                    graph["files"][rel_path] = file_entry

                    for fn in visitor.functions:
                        symbol = fn["name"]
                        if symbol not in graph["symbol_index"]:
                            graph["symbol_index"][symbol] = []
                        graph["symbol_index"][symbol].append({"type": "function", "file": rel_path, "line": fn["line_start"]})

                    for cl in visitor.classes:
                        symbol = cl["name"]
                        if symbol not in graph["symbol_index"]:
                            graph["symbol_index"][symbol] = []
                        graph["symbol_index"][symbol].append({"type": "class", "file": rel_path, "line": cl["line_start"]})

                except Exception as e:
                    pass

    os.makedirs(os.path.dirname(AST_GRAPH_PATH), exist_ok=True)
    with open(AST_GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)

    return graph


def query_symbol(symbol):
    if not os.path.exists(AST_GRAPH_PATH):
        build_ast_graph()

    with open(AST_GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)

    results = graph["symbol_index"].get(symbol, [])
    callers = []

    for rel_path, file_data in graph["files"].items():
        for c in file_data.get("calls", []):
            if c["name"] == symbol:
                callers.append({"file": rel_path, "line": c["line"]})

    return {"symbol": symbol, "definitions": results, "callers": callers}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        if len(sys.argv) < 3:
            print("Usage: python3 scripts/ast_code_graph.py query <symbol_name>")
            sys.exit(1)
        res = query_symbol(sys.argv[2])
        print(json.dumps(res, indent=2))
    else:
        graph = build_ast_graph()
        total_files = len(graph["files"])
        total_symbols = len(graph["symbol_index"])
        print(f"✅ Life OS AST Code Graph Index built successfully.")
        print(f"   Indexed {total_files} Python files, {total_symbols} unique code symbols.")
        print(f"   Graph output: {AST_GRAPH_PATH}")


if __name__ == "__main__":
    main()
