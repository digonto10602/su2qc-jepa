"""Numbered-artifact conventions and code-graph helpers (decisions/001)."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from su2qc_jepa.repo.artifacts import SERIES, check_artifacts, new_artifact, read_front_matter, write_index
from su2qc_jepa.repo.graph import graph_stats, same_structure

ROOT = Path(__file__).resolve().parents[1]


def test_repository_follows_artifact_conventions():
    problems = check_artifacts(ROOT)
    assert problems == [], "\n".join(problems)


def test_exactly_one_active_plan_and_milestone_prompts_present():
    plans = [read_front_matter(p)[0] for p in sorted((ROOT / "plans").glob("[0-9][0-9][0-9]_*.md"))]
    assert sum(1 for m in plans if m["status"] == "active") == 1
    prompts = {read_front_matter(p)[0].get("milestone") for p in (ROOT / "prompts").glob("[0-9][0-9][0-9]_*.md")}
    assert {f"M{i}" for i in range(9)} <= prompts


def _scaffold(tmp: Path) -> Path:
    for s in SERIES:
        (tmp / s).mkdir(parents=True)
    shutil.copytree(ROOT / "templates", tmp / "templates")
    for s in SERIES:
        write_index(tmp, s)
    return tmp


def test_new_artifact_numbering_supersede_and_index(tmp_path):
    root = _scaffold(tmp_path)
    p0 = new_artifact(root, "prompts", "M2 repair: rank collapse", milestone="M2")
    p1 = new_artifact(root, "prompts", "M2 repair v2", milestone="M2", supersedes="prompts/000")
    assert p0.name == "000_m2-repair-rank-collapse.md" and p1.name.startswith("001_")
    m0 = read_front_matter(p0)[0]
    assert m0["status"] == "superseded" and m0["superseded_by"] == "prompts/001"
    assert read_front_matter(p1)[0]["supersedes"] == "prompts/000"
    r = new_artifact(root, "reports", "M2: J1 pass", milestone="M2")
    assert "## What was asked" in r.read_text() and "## Code graph" in r.read_text()
    f = new_artifact(root, "figures", "J2 forecast vs exact", ext=".png")
    assert f.name == "000_j2-forecast-vs-exact.png" and not f.exists()
    f.write_bytes(b"\x89PNG")
    write_index(root, "figures")
    assert check_artifacts(root) == []


def test_check_detects_violations(tmp_path):
    root = _scaffold(tmp_path)
    new_artifact(root, "reports", "first")
    (root / "reports" / "005_skipped.md").write_text("---\nid: reports/005\n---\nx")
    (root / "reports" / "notes.md").write_text("unnumbered")
    probs = "\n".join(check_artifacts(root))
    assert "gaps in numbering" in probs and "NNN_slug" in probs and "INDEX.md is stale" in probs and "lacks 'title'" in probs
    with pytest.raises(ValueError):
        new_artifact(root, "prompts", "x", supersedes="prompts/042")


def test_graph_helpers():
    g = {"nodes": [{"id": "a", "label": "A", "community": 0, "source_file": "x.py"}, {"id": "b", "label": "B", "community": 1, "source_file": "y.py"},
                   {"id": "c", "label": "C", "community": 1, "source_file": "y.py"}],
         "links": [{"source": "a", "target": "b", "relation": "calls"}, {"source": "a", "target": "c", "relation": "calls"}],
         "built_at_commit": "abc"}
    st = graph_stats(g)
    assert (st["nodes"], st["edges"], st["communities"], st["files"]) == (3, 2, 2, 2)
    assert st["god_nodes"][0]["label"] == "A"
    h = json.loads(json.dumps(g))
    h["built_at_commit"] = "def"
    h["nodes"][0]["community"] = 7
    assert same_structure(g, h)[0], "commit stamp and community numbering are not structure"
    h["links"].append({"source": "b", "target": "c", "relation": "calls"})
    same, diff = same_structure(g, h)
    assert not same and diff["edges_only_in_rebuild"] == 1


@pytest.mark.skipif(shutil.which("graphify") is None, reason="graphify not installed")
def test_committed_graph_is_fresh(tmp_path):
    """Rebuild the graph in a copy of the repository and compare structure with the committed graph."""
    committed = ROOT / "graphify-out" / "graph.json"
    if not committed.exists():
        pytest.skip("no committed graph yet (run bash scripts/graph_update.sh)")
    dst = tmp_path / "repo"
    def ignore(directory, names):
        skip = {"__pycache__", ".pytest_cache", ".ruff_cache"} | {n for n in names if n.endswith(".egg-info")}
        if Path(directory).resolve() == ROOT:  # top-level only: src/su2qc_jepa/data is a package and must be copied
            skip |= {".git", "data", "runs", "graphify-out"}
        return [n for n in names if n in skip]

    shutil.copytree(ROOT, dst, ignore=ignore)
    subprocess.run(["graphify", "update", ".", "--force"], cwd=dst, check=True, capture_output=True, env={**__import__("os").environ, "PYTHONHASHSEED": "0"})
    same, diff = same_structure(json.loads(committed.read_text()), json.loads((dst / "graphify-out" / "graph.json").read_text()))
    assert same, f"committed code graph is stale: {diff} — run bash scripts/graph_update.sh and commit"


def test_slugify_never_ends_with_dash():
    from su2qc_jepa.repo.artifacts import slugify

    s = slugify("Conventions update: numbered artifacts and the Graphify code graph")
    assert not s.endswith("-") and len(s) <= 60
    assert slugify("  M2: J1 pass!! ") == "m2-j1-pass"
