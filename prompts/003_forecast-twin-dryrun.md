---
id: prompts/003
title: M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M3
status: active
supersedes: null
superseded_by: null
---

# M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)

**Session protocol:** `CLAUDE.md` §2 — start with `scripts/env_check.py` and `bash scripts/graph_update.sh --check` (read the first screen of `graphify-out/GRAPH_REPORT.md`); use `graphify query/explain/affected` before broad searches; end with tests, the gate, `bash scripts/graph_update.sh`, a numbered session report (`python scripts/new_artifact.py reports "M3: <result>" --milestone M3`), `scripts/check_artifacts.py` OK, `STATE.json`, and a final `chore(graph):` commit. Any new prompt you write for a later session goes into `prompts/` via `scripts/new_artifact.py prompts ...`; every figure via `scripts/new_artifact.py figures ... --ext .png`.

**Read first:** `CLAUDE.md` §2 and §4 (hardware rules), `plans/001_gauge-jepa-p-v2.md` §5–§8, §10 (W3).

## Session M3a — forecasting
1. If not already run, queue the final training job with the M2 configuration (`python scripts/jobs/enqueue.py train "v1_final" --prompt prompts/003 --time 06:00:00 --step "python scripts/make_dataset.py --name main --n-traj 20000 --out data/main" --step "python scripts/train_jepa.py --data data/main --name v1_final --epochs 200 --seeds 5 --masked" --output runs/v1_final --output data/main/manifest.json --push`), then `fetch.py`; `runs/v1_final/forecast_eval.json`.
2. $\mu^*$ estimator (strong family): write `scripts/resonance_eval.py` — for each held-out $\mu$, forecast the breaking fraction at $t=20,30,50/g_E$ from the context at $t=8/g_E$; fit a Lorentzian/parabola over $\mu$ to the forecast and to the exact curve; report both maxima and their difference. Evidence `evidence/J2_forecast/resonance.json`.
3. Figures F1 (held-out $g_E$ forecasts vs exact, all baselines), F2 (resonance curve forecast vs exact), saved under `evidence/J2_forecast/`.
4. Cross-carrier check: encode `data/chain_onfam` and `data/main` records of the same states and report the latent distance distribution (should be comparable to the shot-noise scale).

## Session M3b — twin and dry run
5. Save the IBM account if needed (`QiskitRuntimeService.save_account(...)` — ask Digonto for the token; never paste it into a file under git). `python scripts/hw_list_backends.py` (write it: list Open-plan backends, qubit counts, median CZ error, queue). Choose the backend; record in `STATE.json`.
6. Calibrated twin: extend `twin/noise.py` use in `scripts/run_twin.py` with `--backend <name>` (NoiseModel.from_backend + the chosen line); queue the full campaign (`python scripts/run.py --dry -- python scripts/run_twin.py --name day0 --K 12 --seeds 5` shows it is heavy, so it is queued): `python scripts/jobs/enqueue.py twin "day0 twin campaign" --time 06:00:00 --step "python scripts/run_twin.py --name day0 --K 12 --seeds 5 --noise-model evidence/twin/day0/noise_model.json" --step "python scripts/residual_eval.py ..." --output evidence/twin/day0/residual_eval.json --push` for both families (add the strong-family KC-prep points to `run_twin.py`: `--family strong --times 10 15 20`). The IBM token stays on the laptop: build the calibrated noise model there (`NoiseModel.from_backend(backend)`), save it with `json.dump(noise_model.to_dict(serializable=True), ...)` to `evidence/twin/<name>/noise_model.json` together with the chosen qubit line, commit and push it, and add a `--noise-model <file>` option to `run_twin.py` that loads it with `NoiseModel.from_dict`; queued jobs use that option, never `--backend`. Fetch the results with `python scripts/jobs/fetch.py NNN` (raw twin records are large: publish `residual_eval.json` and summaries, not `records.json`).
7. `python scripts/run.py -- python scripts/residual_eval.py --model runs/v1_final/seed0/model.pt --records evidence/twin/day0/records.json --out evidence/twin/day0/residual_eval.json --shots-levels 0 512 256`; `python scripts/run.py -- python scripts/run_gate.py J3 --eval evidence/twin/day0/residual_eval.json` — this is a REHEARSAL (label the ledger row "twin rehearsal"), not a J3 pass.
8. Dry run on the live backend: `python scripts/run.py -- python scripts/hw_dry_run.py --backend <name> --K 12 --depths 1 8 --masses 0.375 --settings Z X --out evidence/hardware/pilot` (pilot design: $g_E=2$ only, $r\in\{1,8\}$, KC-Trotter and KC-prep, Z and X — add a `--prep` flag to include KC-prep circuits). Report the manifest hash and the estimate in the session report. DO NOT SUBMIT.

## Expected
Rehearsal: `jepa_twin` Spearman ≥ `raw_twin` − 0.05 at 512 shots; AUROC(arm B) ≥ 0.9. Dry run: 8–12 circuits, est. 30–60 QPU-s, 12-qubit line with summed CZ error < 0.05.
