---
id: reports/010
title: 'M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling R2 0.914)'
series: reports
created_utc: '2026-10-05T17:43:03Z'
author: claude-code
milestone: M2
status: done
supersedes: null
superseded_by: null
---

# M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)

**Milestone:** M2 · **Prompt:** prompts/002 (session M2a) · **Commit range:** `0a76800..` (model code to the final graph refresh) · **Gate:** J1 **NOT RUN** (the 5-seed runs are still on Perlmutter)

## What was asked
Digonto: "Read ~/.claude/CLAUDE.md, CLAUDE.md and prompts/002_model-and-prereg.md, then execute the M2 session." `prompts/002` has two sessions. **M2a** (model health): a 10-epoch laptop check; the 5-seed, 200-epoch baseline on Perlmutter; gate J1; the ablation ladder (SIGReg weight, latent 32, EMA target, grounding weight 3, horizon curriculum); a diagnostics figure; `docs/MODEL_CARD.md`. **M2b** (preregistration, dated 16 Oct): freeze `configs/gates.yaml`, write `docs/PREREGISTRATION.md`, tag `prereg-2026-10-16`. This session did M2a up to the queued runs and stopped on a `CLAUDE.md` §2 stop condition (below). M2b was not started: it is dated 16 Oct and needs the chosen configuration and Digonto's decision on the energy row.

## Actions taken
1. **Session start:** `scripts/env_check.py` (CPU, torch 2.14.1+cpu, IBM account saved); `bash scripts/graph_update.sh --check` → FRESH (893 nodes, 1697 edges, 64 communities); fast tests 53 passed (exit 0, 75 s). Oriented with `graphify explain JEPAConfig`, `graphify query` on training and on the runner's job writing, then `graphify affected` for `GaugeJEPA`, `train_jepa`, `TrainConfig`, `JEPAConfig` (all lead to `train.py`, `scripts/train_jepa.py`, `gates/j1_training.py` and `tests/test_pipeline.py::test_jepa_trains_one_epoch`).
2. **Model code for the ladder** (commit `0a76800`, pushed):
   - `JEPAConfig.ema_target: float | None` (`src/su2qc_jepa/models/jepa.py`). When set, the prediction target is the clean observation encoded by an exponential-moving-average (EMA) copy of the encoder, with no gradient through it ("stop-gradient"). EMA means the copy's weights follow the trained encoder slowly: $\theta_{\text{tgt}}\leftarrow\tau\,\theta_{\text{tgt}}+(1-\tau)\,\theta$ after every optimiser step. With EMA on, SIGReg (the regulariser that pushes the latent distribution towards a standard Gaussian) acts on the context latent only, as the prompt says. Grounding (the linear heads that read energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag) acts on the context latent and on the *online* encoder's clean latent, the same latent that J1 scores.
   - `TrainConfig.curriculum_epochs` (`models/train.py`): the first $n$ epochs use horizons (1, 2) only, then all of (1, 2, 4, 8).
   - `scripts/train_jepa.py`: new flags `--w-ground`, `--ema-target`, `--curriculum-epochs`, `--master-seed`; writes `runs/<name>/args.json`.
   - **Seed fix.** The training seeds were the integers 0..4, and the shuffle of epoch $e$ used seed $s+e$, so seed 0 epoch 1 had the same batch order as seed 1 epoch 0. `CLAUDE.md` §5 forbids adjacent integer seeds. Seeds are now spawned from `numpy.random.SeedSequence(20261005)`, with one shuffle stream per run. They are recorded in `args.json` and `forecast_eval.json`.
   - New test `tests/test_pipeline.py::test_jepa_ema_target_and_curriculum` checks four things: the EMA copy starts equal to the encoder; it has no gradient; one EMA step equals $\tau\,\theta_{\text{tgt}}+(1-\tau)\,\theta$ to $10^{-7}$; and the curriculum changes the prediction loss.
3. **Laptop check:** `python scripts/run.py -- python scripts/train_jepa.py --data data/main --name v1_check --epochs 10 --seeds 1` → exit 0, 765 s total, of which training took 175 s (17.5 s per epoch on 2 threads) and the baselines the rest; peak 0.98 GB; no NaN.
4. **Queued on Perlmutter** with `python scripts/run.py --push --prompt prompts/002 --name <run> -- python scripts/train_jepa.py --data data/main --epochs 200 --seeds 5 --name <run> <flag>`. Every job is at commit `0a76800` and first rebuilds `data/main` from its manifest (seed 20261005).

   | job | run | change vs base | Slurm limit |
   |---|---|---|---|
   | `jobs/002` | `v1_base` | none; also `--masked` | 08:28 |
   | `jobs/003` | `v1_wsigreg2` | `--w-sigreg 2` | 04:14 |
   | `jobs/004` | `v1_wsigreg5` | `--w-sigreg 5` | 04:14 |
   | `jobs/005` | `v1_latent32` | `--latent 32` | 04:14 |
   | `jobs/006` | `v1_ema` | `--ema-target 0.996` | 04:14 |
   | `jobs/007` | `v1_wground3` | `--w-ground 3` | 04:14 |
   | `jobs/008` | `v1_curriculum` | `--curriculum-epochs 50` | 04:14 |

   The rung "`--w-sigreg` 0.5" is the base itself, since `train_jepa.py`'s default is 0.5. (`JEPAConfig`'s own default is 0.05, but the script always passes 0.5.) At the last check (`scripts/jobs/status.py`, ≈17:40 UTC), jobs 002–007 were SUBMITTED to Slurm and 008 was QUEUED, with the worker heartbeat 0.5 h old.
5. **Ceiling analysis** (my addition; `scripts/j1_ceiling.py`, run as `python scripts/run.py --est-minutes 15 --timeout-min 45 -- python scripts/j1_ceiling.py --data data/main --out evidence/J1_training/ceiling_main.json`, 625 s). The 10-epoch energy $R^2$ (0.895) looked like an information limit rather than a training problem, so I measured how well *any* regressor predicts each grounding target from one clean observation. The regressors are fit on the training split and scored on the validation split, the split J1 uses: ridge (linear), 5-nearest-neighbours, gradient-boosted trees and an MLP. Each is run with the observation alone and with the step's couplings $(c_M,c_H,c_B)$ appended. Regressor seeds come from `SeedSequence(20261005)`. The JSON records HEAD `63065dd` (a job-queue commit whose code equals `0a76800`); the script itself was committed afterwards in this session, unchanged from the version that ran. A first attempt with a larger MLP was too slow on 2 threads and was stopped by me; nothing from it was used.
6. Wrote `scripts/plot_j1_diagnostics.py` (effective rank, four grounding $R^2$ and the semigroup residual vs epoch, per rung, with a JSON sidecar). It is not run yet, because it needs the fetched runs. Wrote the follow-up prompt `prompts/010`.

## Results and what they mean

### Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split)
| quantity | epoch 10 | J1 threshold |
|---|---|---|
| effective rank | 3.93 / 16 | ≥ 8 |
| grounding $R^2$ energy | 0.895 | ≥ 0.99 |
| grounding $R^2$ $C_{\text{string}}$ | 0.997 | ≥ 0.99 |
| grounding $R^2$ $P_{\text{meson}}$ | 0.964 | ≥ 0.95 |
| grounding $R^2$ $P_{\text{baryonic}}$ | 0.996 | ≥ 0.98 |
| semigroup residual | $2.5\times10^{-4}$ | $<10^{-3}$ |
| isotropy (min/max latent variance) | 0.022 | (recorded only) |

This is a code-path check, not a gate run. It confirms the smoke-run picture of the plan (rank 4–6). Three of the four grounding rows and the semigroup row already pass after 10 epochs; rank and energy do not. The forecast MAE values are in `runs/v1_check/forecast_eval.json`. For example, on-family at +8 steps, $P_{\text{baryonic}}$ MAE is 0.072 for the JEPA, 0.144 for ridge and 0.048 for the supervised MLP. That file is for M3, not J1.

### The energy row cannot pass with this encoder (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows; training split 126,824 rows; `data/main` `73fff8e5a7b7`)
| target | best $R^2$ from the observation | best $R^2$ with couplings added | J1 threshold |
|---|---|---|---|
| energy | **0.914** (MLP; ridge 0.887, trees 0.890, kNN 0.851) | 0.994 (MLP; trees 0.985) | 0.99 |
| $C_{\text{string}}$ | 1.000 | 1.000 | 0.99 |
| $P_{\text{meson}}$ | 1.000 | 1.000 | 0.95 |
| $P_{\text{baryonic}}$ | 1.000 | 1.000 | 0.98 |

Why: the grounding target is $E=\langle\psi|H(c_M,c_H,c_B)|\psi\rangle$ in units of $g_E$, with $H/g_E=c_E\mathcal{E}+c_M\mathcal{M}+2c_H\mathcal{T}+c_B\mathcal{B}$ (`data/trajectories.py` line 184). The observation holds the configuration-basis (diagonal) quantities only: vertex occupations, link Casimirs, channel weights and $C_{\text{string}}$. The hopping term $\langle\mathcal{T}\rangle$ and the plaquette term $\langle\mathcal{B}\rangle$ are off-diagonal, so they are not in it. The couplings that weight every term differ between trajectories, and the encoder never sees them (they enter the model only through the actions). Four regressor families agree that one observation explains at most about 91% of the energy variance, and adding the couplings closes most of the gap. The JEPA's 0.895 at epoch 10 is already within 0.02 of this ceiling. So the energy row is a property of the gate definition, not a sign of collapse, and no ladder rung can fix it. This is the `CLAUDE.md` §2 stop condition "a gate threshold would have to change to pass". I have not changed `configs/gates.yaml`.

The other rows are reachable. The other three grounding targets have ceiling 1.000. The clean observations themselves have effective rank 11.2 (standardised; 9.1 raw), with 14 nonzero variance directions out of 18 (four linear constraints among the probabilities). So a latent rank of ≥ 8 is attainable in principle, and that is what the ladder tests.

### Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration)
- **A.** Keep the threshold. J1 is then PARTIAL at best, with this diagnosis. The plan already allows that.
- **B.** Let the energy head see the couplings: ground energy from (latent, $c_M,c_H,c_B$). The ceiling becomes 0.994, so it passes only narrowly, and it changes what the row tests.
- **C.** Set the energy threshold relative to the measured ceiling (e.g. $R^2\ge0.97\times0.914\approx0.89$), recorded with this evidence file.
- **D.** Report energy $R^2$ but take it out of the pass/fail rows, keeping $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, rank and semigroup.

My recommendation is C or D. Both keep the row honest without rewarding a design change made just to pass.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 893 / 1697 / 64 (`5b9277e`) | 931 / 1775 / 80 at `070238d` (all code changes in); the final numbers, including this report, are in `evidence/graph/stats.json` of the `chore(graph)` commit |
| new or changed hubs | – | none expected: two new scripts; `GaugeJEPA` gains `encode_target`/`update_target` |
| `graphify affected` checks run | `GaugeJEPA`, `train_jepa`, `TrainConfig`, `JEPAConfig` | tests covering what they list: `tests/test_pipeline.py` (both JEPA tests), `tests/test_localrun.py`, `tests/test_compute.py` (CLI classification of `train_jepa.py`) — all in the full suite, full suite 54 passed, 0 failed at the end (`.local_runs/logs/20261005T181257Z-4ad6cd_pytest_a1.log`; 53 at the start). Two earlier end-of-session attempts were refused by the runner for lack of free cores (exit 2, not run); the third ran with 1 thread |

## Problems and assumptions
1. **J1 energy row is unreachable as defined** (above). This is the reason the session stops here.
2. **The prompt's J1 command `--runs runs/v1_base/seed*` also matches `seed*_masked`** (the `--masked` run writes those folders), so 10 runs would be gated. `prompts/010` names `seed0`…`seed4` explicitly.
3. **My choices** where the prompt was silent: EMA decay $\tau=0.996$ (the I-JEPA starting value); with EMA, grounding uses the online clean latent, so that J1 measures what is trained; ladder rungs run without `--masked` (J1 does not use it, and it halves the cost); curriculum = 50 epochs on (1, 2).
4. **Seeds changed** (seed fix above). v1 runs are not seed-comparable with the starter smoke runs. Nothing gated before used the old seeds.
5. **`status.py` warned "worker looks stopped"** at a heartbeat age of 8.4 h. As in report 009, that was a false alarm: the worker picked up jobs 002–007 at its 17:00 UTC tick. So the prompt's fallback (1 laptop seed, 30 epochs) was not needed.
6. **Perlmutter cost is not yet known.** Slurm limits sum to 33.9 h (8:28 + 6 × 4:14) on quarter-node (1-GPU shared) allocations. If every job ran to its limit, that is ≈ 8.5 node-hours of the 50. A small model with batch 64 may not gain much from an A100, so a TIMEOUT followed by the worker's automatic resubmission (twice the time) is possible.
7. **The laptop was shared:** the runner waited for free cores several times (load up to 13.6 of 12).
8. **M2b not done:** it is dated 16 Oct and depends on the chosen configuration and on the decision above.

## Next action
Digonto decides the energy row (A–D). Then run `prompts/010` once `python scripts/jobs/status.py` shows jobs 002–008 COMPLETED.
