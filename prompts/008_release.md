---
id: prompts/008
title: M8 — Paper assembly, release, replication (W8, 2 sessions)
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M8
status: active
supersedes: null
superseded_by: null
---

# M8 — Paper assembly, release, replication (W8, 2 sessions)

**Session protocol:** `CLAUDE.md` §2 — start with `scripts/env_check.py` and `bash scripts/graph_update.sh --check` (read the first screen of `graphify-out/GRAPH_REPORT.md`); use `graphify query/explain/affected` before broad searches; end with tests, the gate, `bash scripts/graph_update.sh`, a numbered session report (`python scripts/new_artifact.py reports "M8: <result>" --milestone M8`), `scripts/check_artifacts.py` OK, `STATE.json`, and a final `chore(graph):` commit. Any new prompt you write for a later session goes into `prompts/` via `scripts/new_artifact.py prompts ...`; every figure via `scripts/new_artifact.py figures ... --ext .png`.

1. Assemble `paper/` (LaTeX, PRD/Quantum template) from `docs/PAPER_OUTLINE.md`: every number carries an evidence path in a comment; the claims table (PLAN §11) is a table in the paper; the error budget (`docs/ERROR_BUDGET.md`) is a table.
2. Release: `data/` checksums (`evidence/RELEASE_MANIFEST.json`), models (`runs/v1_final/seed*/model.pt` → GitHub release assets), hardware raw records already in `evidence/hardware/`.
3. `scripts/replicate.sh`: from a clean clone, re-run J0 (quick), J1 (from released histories), J2 (from released eval), J3 (from released residual eval) and the physics tests; it must print PASS/FAIL per gate identically to the ledger.
4. `CITATION.cff` version bump; tag `v1.0.0-preprint`.
5. Preprint checklist in the session report: advisor sign-off on scope vs Sufian's report; no forbidden phrases (CLAUDE.md §6); figures have evidence paths.
