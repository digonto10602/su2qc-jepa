---
id: reports/001
title: 'Conventions update: numbered artifacts and the Graphify code graph'
series: reports
created_utc: '2026-10-02T18:30:21Z'
author: planner
milestone: null
status: done
supersedes: null
superseded_by: null
---

# Conventions update: numbered artifacts and the Graphify code graph

**Milestone:** before M0 · **Prompt:** the user's request of 2 Oct 2026 (Cowork) · **Commit range:** not yet under git

## What was asked
Add to the plan that every prompt the planner creates goes into `prompts/` with a number, and the same for reports and other produced files; make Claude Code use Graphify to keep track of the codebase; include both in the starter package and deliver the updated package.

## Actions taken
1. Checked Graphify's current interface (PyPI `graphifyy` 0.9.74, command `graphify`) and tested it on a scratch copy: code-only rebuild with no LLM or API key; `graphify claude install` (adds a Graphify section to `CLAUDE.md` once and a hook in `.claude/settings.json` holding the absolute path of the binary); `graphify hook install` (background rebuild after each commit); determinism with `PYTHONHASHSEED=0`; path independence across clone names and locations.
2. Added `src/su2qc_jepa/repo/artifacts.py` + `scripts/new_artifact.py` (allocates numbers, writes front matter from `templates/`, handles `--supersedes`, regenerates `INDEX.md`) and `scripts/check_artifacts.py` (names, uniqueness, no gaps, front matter, cross-references, index freshness).
3. Added `src/su2qc_jepa/repo/graph.py`, `scripts/graph_stats.py`, `scripts/graph_update.sh` (rebuild, drop dated snapshots, save `evidence/graph/stats.json`; `--check` compares nodes and edges with the committed graph), `.graphifyignore`, git-ignore rules, the pinned dependency, an env-check entry and CI steps.
4. Restructured the tree: `plans/000` (1 Oct plan, superseded), `plans/001` (v2 plan, active, previously `docs/PLAN.md`), prompts renumbered `000`–`008` with front matter, `decisions/000` (conventions, previously ADR-0001), `decisions/001` (this change), `reports/000` (package build, replacing `SESSION_LOG.md`), empty `figures/`.
5. Rewrote `CLAUDE.md` §2 as a start/during/end session protocol using the graph and the artifact tool, and included Graphify's own section verbatim so the install leaves the file unchanged; rewrote `prompts/000` (bootstrap installs Graphify, builds and commits the first graph); added a protocol line to every prompt; pointed figures, the one-month note and convention changes at numbered artifacts; gave `prompts/001` a step that maps the SU2ZX code with Graphify outside this repository.
6. Plan `plans/001` amended (same number, no physics or gate changes): revision note, audit row 15, comparison row, §10 session mechanics, M0 and W8 steps, new §15.
7. Added `tests/test_repo_conventions.py` (7 tests: slug rule, repository conventions, one active plan and all milestone prompts, numbering/supersede/index, violation detection, graph helpers, committed-graph freshness by rebuilding in a copy).

## Results and what they mean
- `python -m pytest -q`: 26 passed (19 earlier + 7 new). `ruff`: clean. `scripts/check_artifacts.py`: OK. `scripts/graph_update.sh --check`: FRESH.
- Smoke pipeline unchanged: dataset checksum `d49e02a1990d` identical to 1 Oct; gate statuses at smoke scale identical (J0 PARTIAL in quick mode, J1 FAIL, J2 PARTIAL, J3 FAIL — expected for a 15-epoch smoke model).
- Bootstrap simulated in a scratch git copy: `CLAUDE.md` unchanged by `graphify claude install`; only `graphify-out/graph.json` and `GRAPH_REPORT.md` staged; `.claude/settings.json` ignored; working tree clean after commit.
- The freshness test caught a real stale graph when a test file was edited, which is the behaviour wanted from CI.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | none (Graphify not yet adopted) | 591 / 1,068 / 39, from 74 files (`evidence/graph/stats.json`) |
| hubs (`graphify god-nodes`) | — | `PlaquetteModel`, `j0_data.py`, `train.py`, `chain.py`, `plaquette.py`, `artifacts.py` |
| `graphify affected` checks | — | not applicable (new tooling only; physics untouched) |

## Problems and assumptions
- Graphify's git hooks are off by default because the post-commit rebuild leaves the tree dirty after every commit and writes dated snapshot folders; graph refresh is an explicit end-of-session step instead (`decisions/001`).
- Two defects of my own were found and fixed during this work: slugs truncated at 60 characters could end in `-` (now stripped, with a test); and in the freshness test an ignore pattern `data` also skipped the package folder `src/su2qc_jepa/data/`, which made the copied graph differ. Graphify itself was path-independent in every check.
- Machine records under `evidence/` keep UTC stamps rather than numbers (immutable, referenced by hash). If numbered evidence files are wanted too, that is a one-line change to the series list plus a decision record.
- `graphifyy` is pinned at 0.9.74; a different version on the desktop or in CI can change the graph and fail the freshness check — upgrade it deliberately, with a decision record and a rebuilt graph.

## Next action
First Claude Code session: `Read CLAUDE.md and prompts/000_bootstrap.md, then execute the bootstrap session.`
