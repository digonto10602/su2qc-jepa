---
id: decisions/001
title: Numbered artifacts and the Graphify code graph
series: decisions
created_utc: '2026-10-02T18:19:55Z'
author: planner
milestone: M0
status: active
supersedes: null
superseded_by: null
---

# Numbered artifacts and the Graphify code graph

## Decision

**1. Every produced artifact is numbered and append-only.** Plans go in `plans/`, prompts in `prompts/`, reports in `reports/`, decision records in `decisions/`, figures in `figures/`, each named `NNN_<slug>.<ext>` with a three-digit number allocated only by `scripts/new_artifact.py`. This applies to prompts written by the planner (Claude in Cowork) and to prompts Claude Code writes for later sessions (repair, escalation, follow-up). Markdown artifacts carry YAML front matter (`id`, `title`, `series`, `created_utc`, `author`, `milestone`, `status`, `supersedes`, `superseded_by`). A revision is a new number with `supersedes:` set; the old file's only permitted edit is `status: superseded` + `superseded_by:`. Numbers are never deleted or reused (`status: withdrawn` instead). Each folder has a generated `INDEX.md`. `scripts/check_artifacts.py` enforces all of this and runs in the test suite and in CI.

Not numbered: living documents edited in place and versioned by git (`README.md`, `CLAUDE.md`, `docs/*.md`, `configs/*`, `STATE.json`), and machine records (`evidence/**/*.json`, raw hardware counts), which keep UTC stamps and job ids because they are immutable and referenced by hash.

**2. Claude Code tracks the codebase with Graphify.** Graphify (PyPI `graphifyy==0.9.74`, command `graphify`) parses the repository locally with tree-sitter into a graph of files, classes, functions, calls, imports and Markdown headings — code-only mode needs no LLM and no API key. `graphify-out/graph.json` and `graphify-out/GRAPH_REPORT.md` are committed; the cache, HTML view, manifest, labels and dated snapshots are not. Every session starts with `bash scripts/graph_update.sh --check` and reads the first screen of `GRAPH_REPORT.md`; uses `graphify query / explain / path / affected` before broad searching; runs `graphify affected "<function>"` before changing a function and runs the tests of what it lists; ends with `bash scripts/graph_update.sh` and a separate `chore(graph):` commit. Each session report records nodes/edges/communities before and after. CI rebuilds the graph and fails if the committed graph is structurally stale.

## Why

- Prompts and reports accumulate quickly (the SU2ZX campaign reached v0.6.3 in a week). Numbers give an unambiguous order and a citable id (`prompts/004`) and make "which prompt produced this result" answerable from the front matter.
- The v0.6.3 Hermes session found that the generated code documentation covered a different package than the one under gate, which let the twin-seed defect through review. A code graph rebuilt from the actual tree every session, with CI failing when it is stale, closes that gap mechanically. A code graph is navigation, not a scientific review, and is never cited as one.
- Code-only Graphify is deterministic with `PYTHONHASHSEED=0` (verified 2 Oct 2026: two rebuilds byte-identical), uses relative paths, and rebuilds this repository in about 2 s.

## Alternatives considered

- *Graphify git hooks* (`graphify hook install`): rejected as the default. The post-commit hook rebuilds in the background, leaves the working tree dirty after every commit and creates dated snapshot folders under `graphify-out/` (verified 2 Oct 2026). Optional for interactive work on the laptop.
- *Committing `.claude/settings.json` from `graphify claude install`*: rejected; it contains the absolute path of the local `graphify` binary. The install runs once per machine (bootstrap) and the file is ignored.
- *Timestamps instead of numbers*: unambiguous but unreadable in conversation; numbers plus `created_utc` give both.
- *LLM community labels* (`graphify label`): off by default (cost, non-determinism); placeholder labels are acceptable.

## Consequences

- Prompts were renumbered `00_…` → `000_…` before first use; the plan moved from `docs/PLAN.md` to `plans/001`; the 1 Oct plan is kept as `plans/000` (superseded); ADR-0001 became `decisions/000`; `SESSION_LOG.md` was replaced by numbered session reports.
- The bootstrap session installs Graphify, runs `graphify claude install`, builds the first graph and commits it.
- `graphifyy` is pinned; upgrading it is a decision record of its own (the graph is rebuilt and committed in the same change).
