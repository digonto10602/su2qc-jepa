#!/usr/bin/env python
"""Print (and optionally save) code-graph statistics; compare a committed graph with a rebuild.
  python scripts/graph_stats.py                                    # stats of graphify-out/graph.json
  python scripts/graph_stats.py --save evidence/graph/stats.json   # also write JSON (used in session reports)
  python scripts/graph_stats.py --compare old.json new.json        # exit 1 if the structure differs
"""
import argparse
import json
import sys
from pathlib import Path

from su2qc_jepa.repo.graph import graph_stats, load_graph, same_structure

p = argparse.ArgumentParser()
p.add_argument("--graph", default="graphify-out/graph.json")
p.add_argument("--save")
p.add_argument("--top", type=int, default=10)
p.add_argument("--compare", nargs=2, metavar=("COMMITTED", "REBUILT"))
a = p.parse_args()

if a.compare:
    same, diff = same_structure(load_graph(a.compare[0]), load_graph(a.compare[1]))
    print("graph structure:", "FRESH" if same else "STALE", json.dumps(diff))
    sys.exit(0 if same else 1)
if not Path(a.graph).exists():
    print("no graph at", a.graph, "- run: bash scripts/graph_update.sh")
    sys.exit(1)
st = graph_stats(load_graph(a.graph), a.top)
if a.save:  # save first, so a closed output pipe cannot skip it
    Path(a.save).parent.mkdir(parents=True, exist_ok=True)
    Path(a.save).write_text(json.dumps(st, indent=2))
print(f"nodes {st['nodes']}  edges {st['edges']}  communities {st['communities']}  files {st['files']}  built_at_commit {st['built_at_commit']}")
for g in st["god_nodes"]:
    print(f"  {g['degree']:4d}  {g['label']}")
