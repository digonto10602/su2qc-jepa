---
id: prompts/000
title: M0 — Bootstrap (first Claude Code invocation, ~30 min)
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M0
status: active
supersedes: null
superseded_by: null
---

# M0 — Bootstrap (first Claude Code invocation, ~45 min)

**Before this session:** `prompts/009` must have run (the `su2qc-jepa` environment exists and is active; check `STATE.json` → `compute.laptop.laptop_env_ready`). If it has not, stop and say so.

**Read first:** `~/.claude/CLAUDE.md` (user-level instructions), then `CLAUDE.md` (all of it — §2 is the session protocol you will follow from now on), `README.md`, `plans/001_gauge-jepa-p-v2.md` §0–§2, §10 and §11, `decisions/001`.

## Context
This is the first session. The package was built and verified outside Claude Code (`reports/000`–`reports/002`; compute policy in `decisions/002`). Nothing has been pushed yet and no code graph has been committed from this machine. This session runs entirely on the laptop; Perlmutter is not needed until `prompts/002` (one-time setup: `docs/PERLMUTTER.md`).

## Tasks
1. `python scripts/env_check.py` — records the environment in `evidence/ENV.json`; expect `"torch_device_used": "cpu"`. If anything is missing, the environment session (`prompts/009`) did not finish: stop and say so (do not install into any other environment).
2. `python scripts/run.py -- python -m pytest -q` — all fast tests must pass. If a physics test fails, STOP: copy the failure verbatim into the session report; do not patch physics to make a test pass.
3. `python scripts/check_artifacts.py` — must print `OK`.
4. `gh auth status` — if not logged in, STOP and ask Digonto to run `gh auth login` (this session cannot do it).
5. `bash scripts/bootstrap_repo.sh digonto10602/su2qc-jepa` — this (a) installs Graphify if needed, (b) runs `graphify claude install` (registers Graphify's hook in the machine-local, git-ignored `.claude/settings.json`; `CLAUDE.md` already contains the Graphify section), (c) builds the code graph with `scripts/graph_update.sh`, (d) commits and creates the **public** repository, (e) pushes `main`. You are explicitly authorised to create and push this repository. Do not set `GRAPHIFY_HOOKS=1` (decisions/001 explains why the git hooks are off).
6. Try the graph once so the report can show it works: `graphify query "where is the Krylov chain circuit built"` and `graphify affected "lanczos"`; paste the first lines of each into the report.
7. CI: `gh run list --limit 1`, wait for completion. CI runs lint, the artifact check, the tests and `scripts/graph_update.sh --check`. If CI fails on the graph check only, rebuild locally with `bash scripts/graph_update.sh`, commit `chore(graph): refresh code graph`, push, and record the cause in the report (most likely a different `graphifyy` version).
8. Session report: `python scripts/new_artifact.py reports "M0: repository created, CI green, code graph committed" --milestone M0`; fill it (template order), `status: done`. Update `STATE.json` (`M0.status: PASS`, repo URL, commit hash, report id, graph node/edge counts). Commit `docs: M0 session report`, then `chore(graph): refresh code graph`; push.

## Definition of done
- `https://github.com/digonto10602/su2qc-jepa` exists, is public, CI is green (all five steps).
- `graphify-out/graph.json` and `graphify-out/GRAPH_REPORT.md` are committed; `bash scripts/graph_update.sh --check` prints FRESH.
- the M0 session report (the next free number in `reports/`) exists with `status: done`; `scripts/check_artifacts.py` prints OK.

## Out of scope
- No datasets, no training, no twin runs.
- Do not touch `configs/hardware_budget.yaml`.
