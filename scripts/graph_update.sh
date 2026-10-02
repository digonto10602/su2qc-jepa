#!/usr/bin/env bash
# Keep the Graphify code graph current (decisions/001).  Code-only: local tree-sitter parsing, no LLM, no API key.
#   bash scripts/graph_update.sh            rebuild graphify-out/{graph.json,GRAPH_REPORT.md}, print stats, save evidence/graph/stats.json
#   bash scripts/graph_update.sh --check    rebuild and report FRESH/STALE against the committed graph (exit 1 if stale)
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v graphify >/dev/null 2>&1; then
  echo "graphify not found: pip install 'graphifyy==0.9.74'  (PyPI name has two y's; the command is 'graphify')"; exit 2
fi
export PYTHONHASHSEED=0            # makes the clustering, and hence graph.json, reproducible run to run
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
[ -f graphify-out/graph.json ] && cp graphify-out/graph.json "$TMP/committed.json"
# always rebuild from source with an empty cache: an incremental update can keep stale nodes that a fresh clone
# (e.g. CI) would not produce, which would make the freshness check machine-dependent
rm -rf graphify-out/cache graphify-out/graph.json graphify-out/manifest.json graphify-out/.graphify_* 2>/dev/null || true
graphify update . --force >"$TMP/update.log" 2>&1 || { cat "$TMP/update.log"; exit 1; }
grep -E "Rebuilt|nodes" "$TMP/update.log" | head -2 || true
rm -rf graphify-out/20[0-9][0-9]-*/ 2>/dev/null || true   # dated snapshots are never kept
python scripts/graph_stats.py --save evidence/graph/stats.json --top 8
if [ "${1:-}" = "--check" ]; then
  if [ ! -f "$TMP/committed.json" ]; then echo "graph structure: STALE (no committed graph)"; exit 1; fi
  python scripts/graph_stats.py --compare "$TMP/committed.json" graphify-out/graph.json
fi
