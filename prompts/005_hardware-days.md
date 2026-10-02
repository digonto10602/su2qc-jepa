---
id: prompts/005
title: M5 — Hardware days 1 and 2 (W5, one session per day)
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M5
status: active
supersedes: null
superseded_by: null
---

# M5 — Hardware days 1 and 2 (W5, one session per day)

**Session protocol:** `CLAUDE.md` §2 — start with `scripts/env_check.py` and `bash scripts/graph_update.sh --check` (read the first screen of `graphify-out/GRAPH_REPORT.md`); use `graphify query/explain/affected` before broad searches; end with tests, the gate, `bash scripts/graph_update.sh`, a numbered session report (`python scripts/new_artifact.py reports "M5: <result>" --milestone M5`), `scripts/check_artifacts.py` OK, `STATE.json`, and a final `chore(graph):` commit. Any new prompt you write for a later session goes into `prompts/` via `scripts/new_artifact.py prompts ...`; every figure via `scripts/new_artifact.py figures ... --ext .png`.

**Read first:** `CLAUDE.md` §4, `plans/001_gauge-jepa-p-v2.md` §8, §10 (W5).

Per day (define the day by the calibration snapshot hash, not the calendar):
1. Snapshot calibration and save the day's noise model on the laptop (see `prompts/003` step 6), commit and push it; queue the twin of the day: `python scripts/jobs/enqueue.py twin "dayN twin" --prompt prompts/005 --time 06:00:00 --step "python scripts/run_twin.py --name dayN --noise-model evidence/twin/dayN/noise_model.json --seeds 5" --step "python scripts/residual_eval.py ..." --output evidence/twin/dayN/residual_eval.json --push` (both families, both arms), then `fetch.py`. The QPU submission itself always runs from the laptop.
2. Dry run of the day's design (full or minimum, per the remaining budget in `evidence/hardware/QPU_LEDGER.json`): on-family KC-Trotter $r\in\{1,2,4,8\}$ at $g_E\in\{1.3,1.75,2.0\}$ + KC-prep at the same times; strong family KC-prep $\mu\in\{0.3,0.375,0.42,0.5\}$ at $t\in\{10,15,20\}$; settings Z, X; 4,000 shots. Two jobs: arm A (plain), arm B (`--dd --twirl`).
3. STOP for approval (two approvals, one per job); submit; collect; immutable raw records.
4. `scripts/hw_analysis.py` (write in day 1): converts raw counts into the `records.json` schema used by `residual_eval.py` (`hw_est`, `ideal_circuit`, `exact`, flags), per point; then `residual_eval.py --source hardware --reference evidence/twin/dayN/records.json`.
5. Day figures (each via `scripts/new_artifact.py figures ... --ext .png`): depth ladder (post-selected observables vs ideal, both arms); strong-family resonance (breaking fraction vs $\mu$ at the three times, hardware vs exact); R4 panel (forecast of $t=3$ from $r\le2$ vs direct $r=8$).
6. Day 2 extra: if the window allows, the on-family block on a second Open-plan QPU (cross-backend).

## Expected
Depth ladder error 0.03 → 0.1–0.3; KC-prep within 0.05; resonance contrast visible at $t=20/g_E$ (≈ 0.25 vs < 0.1); R4: forecast error ≤ 0.05 vs direct 0.1–0.3. Budget: ≤ 5 min/day.
