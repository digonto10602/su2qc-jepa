---
id: reports/015
title: Desktop GPU worker online; v1_final trained; preregistered J2 FAIL (on-family passes, strong coupling fails)
series: reports
created_utc: '2026-10-21T20:30:59Z'
author: claude-code
milestone: M3
status: done
supersedes: null
superseded_by: null
---

# Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)

**Milestone:** M3 (with the J2 gate of M4a, run as soon as its preregistered input existed) · **Prompts:** prompts/003, prompts/010 · **Commit range:** `bc7ba86..` (desktop worker) to the final `chore(graph)` commit · **Gates:** J2 **FAIL** (`evidence/J2_forecast/20261021T201507Z.json`); J1 on `v1_final` FAIL, information only (`evidence/J1_training/20261021T203007Z.json`) · **Previous report:** `reports/014`

## What was asked
Digonto, 21 Oct 2026:
1. Run the heavy work on his desktop (Linux, RTX 3070, sometimes switched off) instead of the stopped Perlmutter worker: "go with option A", with a deploy key.
2. Fix the preregistration's dataset-equivalence rule with a decision record ("Decision record").
3. Run the dataset equivalence check, and then gates J1 and J2, on the desktop as well, because the laptop was saturated by another session.

## Actions taken
1. **Desktop worker** (`decisions/006`; commits `bc7ba86`, `f2498e3`):
   - jobs may now say `where: desktop`; `run.py --where`, and `queue.default_where = desktop`;
   - local worker mode: publishes a RUNNING status; a job interrupted by a power-off is rerun (up to 3 runs in all) or recorded LOST;
   - `status.py` shows one heartbeat per worker;
   - new `setup_env_desktop.sh` and `install_desktop.sh`, and `docs/DESKTOP.md`;
   - 3 new tests.
2. **Fixes found while setting the desktop up:**
   - pinned qiskit 2.5.x and qiskit-aer 0.17.x, because qiskit-aer 0.18.0 fails to load next to PyTorch in CI (`09f931e` and before);
   - the graph-freshness test now uses the environment's own `graphify` (the desktop shell found an older `~/.local/bin/graphify` first);
   - the installer survives a missing user session bus and offers a cron schedule. Digonto used cron.
3. **Desktop checks:**
   - `ssh` deploy key OK; first heartbeat at 16:38 UTC;
   - GPU check `jobs/018` COMPLETED on the RTX 3070 (`sm_86`, PyTorch 2.14.1 with CUDA 13.0);
   - the desktop's `gpu_smoke` rebuild is bit-identical to Perlmutter's.
4. **Preregistration deviation** (`decisions/007`, approved by Digonto). The equivalence rule's bound "$\le10^{-12}$ per trajectory sum" contradicted the rebuild quoted in the same row ($5.7\times10^{-12}$, rounding only). It is corrected to: inputs bit-identical; targets $\le10^{-12}$ per value and $\le10^{-10}$ per trajectory sum. Recorded in §7 of `docs/PREREGISTRATION.md`, and made before `v1_final` existed. `compare_fingerprints.py` now prints the verdict, with a test.
5. **`v1_final`** (`jobs/019`): exactly the command in §3 of the preregistration (master seed 27182818, $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$, 5 seeds, 200 epochs, masked). Run on the desktop: 1.156 h, COMPLETED.
6. **Equivalence check** (`jobs/020`, desktop): **EQUIVALENT**.
7. **Gates** run on the desktop, because the laptop was at load 13–15 for hours:
   - J2 (`jobs/021`) and J1 (`jobs/022`);
   - inputs: byte-identical copies of `runs/v1_final` committed as `evidence/runs/v1_final/`. This is the only difference from the preregistered command, which names `runs/v1_final/…`;
   - the two gate records were appended to the local `evidence/GATE_LEDGER.md` after checking that each job's ledger is the local one plus exactly one block.

## Results and what they mean

### Dataset used by `v1_final` (`evidence/J0_data/fingerprint_compare_main_laptop_vs_desktop_v1_final.json`)
- Inputs `ctx`, `act` and `valid` are bit-identical to the reference `73fff8e5a7b7`.
- Targets differ by at most $1.9\times10^{-13}$ per value and $5.7\times10^{-12}$ per trajectory sum.
- Verdict under `decisions/007`: **EQUIVALENT**.

### J2: preregistered forecasting gate, **FAIL** (`evidence/J2_forecast/20261021T201507Z.json`)
MAE at $+4$ / $+8$ steps after the context step, for $P_{\text{baryonic}}$ / $P_{\text{meson}}$ / $C_{\text{string}}$, mean of 5 seeds, on the held-out split:

| family (trajectories) | model | +4 | +8 |
|---|---|---|---|
| on-family (2,935) | **JEPA** | 0.032 / 0.014 / 0.020 | 0.049 / 0.020 / 0.027 |
| | ridge | 0.060 / 0.019 / 0.030 | 0.144 / 0.030 / 0.136 |
| | autoregressive | 0.030 / 0.011 / 0.014 | 0.404 / 0.188 / 1.135 |
| | supervised MLP (reported, not gated) | 0.022 / 0.010 / 0.012 | 0.048 / 0.020 / 0.024 |
| | JEPA, couplings masked | 0.058 / 0.015 / 0.034 | 0.091 / 0.022 / 0.059 |
| | ridge, couplings masked | 0.063 / 0.020 / 0.031 | 0.458 / 0.048 / 0.264 |
| strong coupling (3,134) | **JEPA** | 0.105 / 0.016 / 0.048 | 0.123 / 0.021 / 0.061 |
| | ridge | 0.085 / 0.014 / 0.038 | 0.185 / 0.024 / 0.248 |
| | autoregressive | 0.128 / 0.015 / 0.054 | 0.367 / 0.077 / 0.237 |
| | supervised MLP (reported, not gated) | 0.109 / 0.013 / 0.046 | 0.153 / 0.018 / 0.068 |
| | JEPA, couplings masked | 0.087 / 0.013 / 0.039 | 0.137 / 0.018 / 0.066 |
| | ridge, couplings masked | 0.091 / 0.014 / 0.038 | 0.195 / 0.024 / 0.275 |

Gate rows:
- **on-family:** MAE ≤ 0.05 PASS at +4 (0.032) and at +8 (0.049); ridge non-inferiority PASS at both; autoregressive non-inferiority **FAIL at +4** (1/3), PASS at +8.
- **strong coupling:** MAE ≤ 0.05 **FAIL** at +4 (0.105) and at +8 (0.123), from $P_{\text{baryonic}}$ in both; ridge non-inferiority **FAIL at +4** (0/3), PASS at +8; autoregressive PASS at both.

**What it means.**
- H2 is not met. On-family, JEPA meets the error bound and beats ridge at both horizons. At strong coupling, $P_{\text{baryonic}}$ is off by more than twice the bound.
- JEPA's advantage grows with horizon: at +8 it beats ridge and the autoregressive model on every target in both families.
- The supervised MLP, which is reported but not gated, is about as good as JEPA. So these numbers support parity, not superiority, which is the plan's own expectation.
- With couplings masked, JEPA's error is 2–5× lower than masked ridge's at +8.
- Per the plan (§9), the forecasting claim is reported as mixed. J3 becomes the paper's primary outcome.

### J1 on `v1_final`, information only (`evidence/J1_training/20261021T203007Z.json`)
- Rank per seed 8.67, 8.65, 8.90, 8.55, **7.97**, so the row FAILs by 0.03 on one seed.
- Semigroup residual max $8.6\times10^{-4}$ (PASS); all grounding rows PASS (energy 0.898).
- H1 was already recorded as not met before the preregistration; this run confirms the configuration sits on the edge of the J1 rows.

### Cost
The desktop needs no node-hours: `v1_final` took 1.16 h on the RTX 3070, compared with 2.09 h for the same work on an A100. Perlmutter use is unchanged at 4.318 of 50 node-hours, and its worker has been silent since 8 Oct.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 1108 / 2014 / 102 (`reports/014`) | 1158 / 2091 / 101 before this report; final numbers in `evidence/graph/stats.json` of the closing commit |
| new or changed | – | `jobs.WHERE`, `ALLOWED_SCRIPTS`; `Worker.run_one_local`, `Worker.recover_local`; `status.py`; `run.py --where`; desktop scripts; `compare_fingerprints.py` verdict |
| `graphify affected` checks | `validate_job` → `worker.eligible`, `check_artifacts`, `tests/test_jobs.py`, `tests/test_repo_conventions.py`; `Worker` → `worker.main` | all run in the full suite: 61 passed, 1 skipped (CUDA case; it passed on the desktop); CI green |

## Problems and assumptions
1. **J2 FAIL** is the preregistered result and is reported as such. No threshold, target or horizon was changed.
2. **Preregistration deviation** (`decisions/007`): the error was in my draft of the rule. The correction was made before `v1_final` existed and is listed in §7 of the preregistration.
3. **Path deviation:** the gates read byte-identical copies under `evidence/runs/v1_final/`, not `runs/v1_final/`, so that the desktop could read them.
4. **Gate jobs appear as "FAILED" in `status.py`,** because a failing gate exits with code 1. The logs show complete gate runs, not program errors.
5. **The laptop was saturated** (load 13–15) by another session for hours. No work bypassed the runner; the light gate work was moved to the desktop instead.
6. **Perlmutter worker still stopped.** Not needed while the desktop is available; `queue.default_where = desktop`.
7. **The supervised MLP baseline matches JEPA,** which weakens any "JEPA is better" reading even on-family.

## Next action
M3 continues (`prompts/003`): the twin calibration and hardware dry run, which run on the laptop or the desktop; the μ* estimator; figures F1/F2. Since J2 has failed, J3 (hardware) is the primary outcome. The pilot QPU cap discrepancy (90 s vs 120 s) must be settled before the pilot.
