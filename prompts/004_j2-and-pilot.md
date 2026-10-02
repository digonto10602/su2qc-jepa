---
id: prompts/004
title: M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M4
status: active
supersedes: null
superseded_by: null
---

# M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.

**Session protocol:** `CLAUDE.md` §2 — start with `scripts/env_check.py` and `bash scripts/graph_update.sh --check` (read the first screen of `graphify-out/GRAPH_REPORT.md`); use `graphify query/explain/affected` before broad searches; end with tests, the gate, `bash scripts/graph_update.sh`, a numbered session report (`python scripts/new_artifact.py reports "M4: <result>" --milestone M4`), `scripts/check_artifacts.py` OK, `STATE.json`, and a final `chore(graph):` commit. Any new prompt you write for a later session goes into `prompts/` via `scripts/new_artifact.py prompts ...`; every figure via `scripts/new_artifact.py figures ... --ext .png`.

**Read first:** `CLAUDE.md` §4, `plans/001_gauge-jepa-p-v2.md` §8–§10 (W4), `configs/hardware_budget.yaml`.

## Session M4a — J2 (30 Oct)
1. `python scripts/run.py -- python scripts/run_gate.py J2 --eval runs/v1_final/forecast_eval.json`.
2. Ablation table (`evidence/J2_forecast/ablations.json`): no SIGReg / no grounding / no semigroup / EMA target / latent 8 and 32 — forecasting MAE per family, 3 seeds each.
3. Figure F3 (baseline comparison, both tasks) via `scripts/new_artifact.py figures`. Write the "Results: forecasting" section draft into `docs/PAPER_OUTLINE.md` with the numbers and their evidence paths.

## Session M4b — pilot (one job)
4. Re-run the dry run for the pilot on the day's calibration (line may change). Post the manifest hash and estimate in the session report and STOP until Digonto has set `approved: true`, the hash and the caps in `configs/hardware_budget.yaml` (max_qpu_seconds 90, max_jobs 1, max_cz_per_circuit 200, shots 4000).
5. `python scripts/hw_submit.py submit --dry-run-dir evidence/hardware/pilot --confirm` → job id. Poll with `gh`-style patience (`job.status()` every 5 min; do not resubmit).
6. `python scripts/hw_submit.py collect --job-id <id>`; measured QPU seconds → update the `shots_per_second` prior in `hardware/ibm.py` (no decision record needed; record the number in `STATE.json`).
7. Pilot analysis `scripts/pilot_analysis.py` (figures via `scripts/new_artifact.py figures`): flag rates per circuit; post-selected populations vs ideal circuit; X-setting coherence sanity ($\langle X_kX_{k'}\rangle$ symmetric, within [-1,1]); bit-order check (the $r=1$ Z-populations must peak on qubit 0). Compare with the day's twin (same line). Figure F4.
8. Stop/go review in the session report: go if post-selected $r=1$ populations are within 0.03 of the ideal circuit and the flag rate at $r=8$ is below 0.7.

## Expected
QPU time 40–90 s; flag rate 0.2–0.6; populations within 0.03 at $r=1$. One-month deliverable: J0–J2 passed, twin rehearsal, pilot figure — write the one-month note as a numbered report (`scripts/new_artifact.py reports "One-month note: simulator, twin and pilot"`, ≤ 4 pages) if the project stops here.
