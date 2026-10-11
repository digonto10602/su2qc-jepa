---
id: reports/013
title: 'M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model w_sigreg 3, w_semigroup 10'
series: reports
created_utc: '2026-10-08T21:00:46Z'
author: claude-code
milestone: M2
status: done
supersedes: null
superseded_by: null
---

# M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$

**Milestone:** M2 (session M2a, continued) · **Prompts:** prompts/002, prompts/010 · **Commit range:** `5a934f7..` (after `reports/011`) to the final `chore(graph)` commit · **Gate:** J1 **FAIL** (`evidence/GATE_LEDGER.md`, last row `v1_confirm`) · **Previous report:** `reports/010` (M2a start), with overviews in `reports/011` and `reports/012`

## What was asked
Digonto, in order:
1. "fix the gpu bug and continue";
2. a full project report for download (`reports/012`, written by a Sonnet subagent);
3. on 6 Oct, when every configuration had failed J1: "Two more runs";
4. when $(w_{\text{sigreg}},w_{\text{semigroup}})=(3,10)$ passed on its selection seeds: "Two points + confirm", i.e. call J1 PASS only if a fresh-seed confirmation run also passes;
5. after the confirmation failed: "J1 FAIL, continue". Record J1 FAIL with the diagnosis, take the $(3,10)$ configuration as the working model for M3, and write the figure, model card and session report.

## Actions taken
1. **GPU bug** (commit `3fd0a65`). `baseline_autoregressive` built its network on the CPU while the data were on CUDA. `baseline_supervised_mlp` kept its inputs and network on the CPU while the targets were on CUDA. Both now use the data's device. Every Perlmutter training job before the fix (002–008) crashed after training, in these baselines. Their models and `history.json` were saved, so J1 was unaffected, but no `forecast_eval.json` was written. New test `test_training_and_baselines_run_on_device`: the CPU case runs everywhere and the CUDA case wherever a GPU exists. Verified end to end on an A100 by `jobs/009` (tiny dataset `gpu_smoke`, 2 epochs, masked, all baselines): COMPLETED, 0.003 node-hours.
2. **Dataset reproducibility** (commit `ade81b0`, `jobs/010`):
   - `dataset_fingerprint` stores per-trajectory sums at full precision plus 2,000 fixed sampled values per array;
   - `make_dataset` now writes `fingerprint.json`;
   - `scripts/compare_fingerprints.py` compares two builds without moving the data arrays, which the worker never publishes.
3. **`fetch.py`** (commit `3010090`). Fetching a job no longer overwrites a different local file; the job's copy goes to `evidence/jobs/NNN/outputs/`. A test was extended for this.
4. **`--w-semigroup` flag** added to `scripts/train_jepa.py` (default 0.1, unchanged).
5. **Fourteen configurations trained on Perlmutter** (jobs 002–008 and 011–017), 5 seeds × 200 epochs each. Each was fetched and gated once with `python scripts/run.py --no-queue --threads 1 --name J1_<run> -- python scripts/run_gate.py J1 --runs runs/<run>/seed0 … seed4` (unmasked seeds only).
6. **Figures** with `scripts/plot_j1_diagnostics.py`. Data sidecars now go to `evidence/figures/`, because `figures/` holds images only and the artifact check enforces that.
   - `figures/000`: the plan's ablation ladder;
   - `figures/001`: the semigroup-weight series and the confirmation run.
7. **matplotlib** was missing from the project environment and from the declared dependencies. It was added to the `ml` extra in `pyproject.toml` and installed into `su2qc-jepa`: matplotlib 3.11.2 plus 6 new dependencies, nothing upgraded, `pip check` clean.
8. **`docs/MODEL_CARD.md`** written.

## Results and what they mean

### J1 (validation split, final epoch; every row is in `evidence/GATE_LEDGER.md`)
| # | configuration | rank, min (≥ 8) | semigroup, max (< 1e-3) | other | J1 |
|---|---|---|---|---|---|
| 1 | `v1_base` ($w_{\text{sigreg}}$ 0.5, $w_{\text{sg}}$ 0.1) | 5.16 | 3.29e-3 | | FAIL |
| 2 | `v1_wsigreg2` | 8.26 | 5.34e-3 | | FAIL |
| 3 | `v1_wsigreg5` | 10.53 | 8.47e-3 | | FAIL |
| 4 | `v1_latent32` | 6.12 | 4.72e-3 | | FAIL |
| 5 | `v1_ema` ($\tau$ 0.996) | 13.09 | 2.21e-2 | $P_{\text{meson}}$ 0.915 | FAIL |
| 6 | `v1_wground3` | 5.63 | 6.94e-3 | | FAIL |
| 7 | `v1_curriculum` | 6.18 | 2.86e-3 | | FAIL |
| 8 | `v1_wsemigroup1` | 4.94 | 1.72e-3 | | FAIL |
| 9 | `v1_wsig2_wsg1` | 8.56 | 5.57e-3 | | FAIL |
| 10 | `v1_wsig2_wsg3` | 8.07 | 1.17e-3 | | FAIL |
| 11 | `v1_wsig2_wsg5` | 7.80 | 1.01e-3 | | FAIL |
| 12 | `v1_wsig2_wsg10` | 7.42 | 9.2e-4 | | FAIL |
| 13 | `v1_wsig3_wsg10` | 8.26 | 7.8e-4 | | PASS (selection seeds) |
| 14 | `v1_confirm` (= 13, master seed 31415926) | 8.45 | **1.48e-3** (seed 3; others 3.2–7.3e-4) | | **FAIL** |

Energy, $C_{\text{string}}$ and $P_{\text{baryonic}}$ pass in all 14 configurations, and $P_{\text{meson}}$ in all but `v1_ema`.

**What it means.** The latent does not collapse: every grounding row passes, and the rank reaches 8–13 once SIGReg is strong enough. What fails is the predictor's consistency.
- The semigroup residual rises as the latent spreads out (rank up → residual up) and falls with the semigroup weight (rank down).
- It varies about 5× between seeds, so the row, scored as the worst of 5 seeds, depends on one unlucky seed.
- With the couplings hidden (masked runs) it is about $2\times10^{-5}$, so the inconsistency comes from how the predictor uses the coupling inputs.
- Setting 13 was picked by searching on the same split that J1 scores. The confirmation run (14), on 5 fresh seeds, shows that its pass was partly selection luck. Under the rule agreed before that run, **J1 = FAIL**.
- The plan's "PARTIAL" fallback is written for rank staying below 8, which is not this case, so the status stays FAIL, as Digonto decided.

### Working model
$(w_{\text{sigreg}}, w_{\text{semigroup}}) = (3, 10)$; models in `runs/v1_confirm` (plain and masked, `jobs/017` at commit `600197b`). Details are in `docs/MODEL_CARD.md`.

### Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`; not a J2 result)
MAE at $+8$ steps, $P_{\text{baryonic}}$ / $P_{\text{meson}}$ / $C_{\text{string}}$:

| family | JEPA | ridge | supervised MLP |
|---|---|---|---|
| on-family | 0.046 / 0.021 / 0.027 | 0.144 / 0.030 / 0.136 | 0.048 / 0.020 / 0.024 |
| strong coupling | **0.133** / 0.020 / **0.069** | 0.185 / 0.024 / 0.248 | 0.153 / 0.018 / 0.068 |

On-family, the JEPA is within J2's 0.05 bound and beats ridge. On the strong-coupling family it is above 0.05 for two targets. This is flagged now as a J2 risk for M3/M4.

### Dataset reproducibility (`evidence/J0_data/fingerprint_compare_*.json`)
- The noisy inputs `ctx` (including every simulated shot), the actions `act` and the masks `valid` are **bit-identical** between the laptop and Perlmutter builds of `data/main`.
- The exact targets `tgt` and `energy` differ only by floating-point rounding: at most $5.7\times10^{-14}$ and $1.9\times10^{-13}$ per sampled value, and $5.7\times10^{-12}$ per trajectory sum. That is why the checksums differ (`73fff8e5a7b7` laptop, `76f4c9055591` Perlmutter).
- The small test dataset `gpu_smoke` shows the same pattern.

### Cost
Perlmutter: 4.32 of 50 node-hours used in all. A 5-seed, 200-epoch run takes about 1.1 h and 0.27 node-hours; with the masked runs, about 2.1 h and 0.52 node-hours.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 931 / 1775 / 80 (`070238d`, `reports/010`) | 1078 / 1970 / 96 before this report's commit; final numbers in `evidence/graph/stats.json` of the closing `chore(graph)` commit |
| new or changed hubs | – | `dataset_fingerprint` (new); `baseline_autoregressive`, `baseline_supervised_mlp` (changed) |
| `graphify affected` checks run | `baseline_autoregressive` → only mentions in reports (its caller `scripts/train_jepa.py` is not linked to the symbol in the graph); `baseline_supervised_mlp` → none; `generate_dataset` → 5 tests in `tests/test_pipeline.py` | all named tests run in the full suite |

## Problems and assumptions
1. **J1 FAIL**, as above. M3 proceeds with a model that is not J1-validated. This must be stated in the preregistration (M2b, 16 Oct) and in the paper.
2. **Process errors of mine, both corrected before commit:**
   - a retry loop treated the J1 gate's own FAIL exit code as "laptop busy" and re-ran the `v1_base` gate 10 times. The 10 identical duplicate records were removed and one kept;
   - the runner once turned a gate run into a Perlmutter job file (`jobs/013`) while the laptop was busy. It was never committed or pushed and was deleted. The number 013 was later used by a real job.
3. **The laptop was shared** with another session at load 13–20 for hours. Several test and gate runs were refused (runner exit 2) and retried. No work ran outside the runner.
4. **Environment change:** matplotlib was installed into `su2qc-jepa`. The Perlmutter environment does not need it (no plotting there).
5. **Selection effect:** 13 configurations were searched on the validation split that J1 scores. Only `v1_confirm` is free of that selection.
6. **Source disagreements** found by the `reports/012` subagent (§10.3 there), still open:
   - the pilot QPU cap is 90 s in `prompts/004` and 120 s in `configs/hardware_budget.yaml`;
   - the plan calls the on-family mass dependence "monotone", but the recomputed values are not (0.628, 0.635, 0.625, 0.596, 0.531);
   - `docs/CLAIMS.md` C6 promises `evidence/J0_data/mass_dependence.json`, which does not exist.

## Next action
M2b (16 Oct, `prompts/002` items 6–8): freeze `configs/gates.yaml`, write `docs/PREREGISTRATION.md` with J1 FAIL, the working configuration and the reference dataset checksum, then tag `prereg-2026-10-16`. M3 (`prompts/003`) uses `runs/v1_confirm`.
