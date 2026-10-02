---
id: prompts/006
title: M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions)
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M6
status: active
supersedes: null
superseded_by: null
---

# M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions)

**Session protocol:** `CLAUDE.md` §2 — start with `scripts/env_check.py` and `bash scripts/graph_update.sh --check` (read the first screen of `graphify-out/GRAPH_REPORT.md`); use `graphify query/explain/affected` before broad searches; end with tests, the gate, `bash scripts/graph_update.sh`, a numbered session report (`python scripts/new_artifact.py reports "M6: <result>" --milestone M6`), `scripts/check_artifacts.py` OK, `STATE.json`, and a final `chore(graph):` commit. Any new prompt you write for a later session goes into `prompts/` via `scripts/new_artifact.py prompts ...`; every figure via `scripts/new_artifact.py figures ... --ext .png`.

1. Day 3 exactly as M5.
2. `residual_eval.py` over all three days (`--records` merged; add `--merge` support or concatenate records.json files), shots levels 0/512/256; `python scripts/run.py -- python scripts/run_gate.py J3 --eval evidence/hardware/residual_eval_all.json` (13 Nov).
3. Day-separation AUROC (day with the worst calibration vs the best) — report even if null.
4. $\mu^*$ from hardware (strong family): fit over the four masses at $t=20$; compare with 3/8; evidence `evidence/J3_hardware/resonance_hw.json`.
5. Error-budget table (`docs/ERROR_BUDGET.md`): truncation ($j_{\max}=1$ reference), Krylov, Trotter, shot, device (post-selected), twin mismatch (`raw_twin`), model — each with its evidence path.
6. Draft the "Results: hardware" section in `docs/PAPER_OUTLINE.md`.

## Expected
J3 PASS or PARTIAL (non-inferiority met). Either way the hardware dataset is released with checksums.
