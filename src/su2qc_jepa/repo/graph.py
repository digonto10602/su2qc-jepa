"""Helpers around the Graphify code graph (graphify-out/graph.json).

Graphify (PyPI package `graphifyy`, command `graphify`) parses the repository locally with
tree-sitter — no LLM, no API key in code-only mode — into a graph of files, classes, functions,
imports, calls and Markdown headings, clusters it into communities and writes
`graphify-out/graph.json` and `graphify-out/GRAPH_REPORT.md`.  This module only *reads* those
files: it counts nodes/edges/communities, lists the most connected nodes, and decides whether a
committed graph is structurally identical to a fresh rebuild (ignoring the commit stamp and the
community assignment, which are not structure).
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

__all__ = ["load_graph", "graph_stats", "structure_signature", "same_structure"]


def load_graph(path: str | Path = "graphify-out/graph.json") -> dict:
    return json.loads(Path(path).read_text())


def _edges(g: dict) -> list[dict]:
    return g.get("links", g.get("edges", []))


def graph_stats(g: dict, top: int = 10) -> dict:
    nodes = g.get("nodes", [])
    edges = _edges(g)
    deg: Counter = Counter()
    for e in edges:
        deg[e.get("source")] += 1
        deg[e.get("target")] += 1
    label = {n["id"]: n.get("label", n["id"]) for n in nodes}
    files = {n.get("source_file") for n in nodes if n.get("source_file")}
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "communities": len({n.get("community") for n in nodes if n.get("community") is not None}),
        "files": len(files),
        "built_at_commit": g.get("built_at_commit"),
        "god_nodes": [{"id": k, "label": label.get(k, k), "degree": v} for k, v in deg.most_common(top)],
    }


def structure_signature(g: dict) -> tuple[frozenset, frozenset]:
    nodes = frozenset((n["id"], n.get("source_file"), n.get("source_location")) for n in g.get("nodes", []))
    edges = frozenset((e.get("source"), e.get("target"), e.get("relation", e.get("type"))) for e in _edges(g))
    return nodes, edges


def same_structure(a: dict, b: dict) -> tuple[bool, dict]:
    na, ea = structure_signature(a)
    nb, eb = structure_signature(b)
    diff = {"nodes_only_in_committed": len(na - nb), "nodes_only_in_rebuild": len(nb - na),
            "edges_only_in_committed": len(ea - eb), "edges_only_in_rebuild": len(eb - ea)}
    return (na == nb and ea == eb), diff
