---
id: reports/002
title: 'Compute update: laptop for light work, Perlmutter for heavy jobs'
series: reports
created_utc: '2026-10-02T19:32:02Z'
author: planner
milestone: null
status: done
supersedes: null
superseded_by: null
---

# Compute update: laptop for light work, Perlmutter for heavy jobs

**Milestone:** before M0 · **Prompt:** Digonto's message of 2 Oct 2026 (Cowork) · **Commit range:** not yet under git

## What was asked
The RTX 3070 desktop cannot be used. Jobs that need a powerful GPU should run on NERSC Perlmutter; everything else on the laptop. Digonto also reported a pip conflict after installing the package: a CUDA 13 PyTorch was installed and `cuda-bindings` 13 broke `cuquantum-python-cu12`.

## Actions taken
1. Measured unit costs on 2 CPU cores: 2,000 trajectories generated in 11.7 s; one training epoch over 1,137 trajectories in 2.5 s; twin circuits 6–30 s each (from `plans/001` App. B).
2. Added `src/su2qc_jepa/compute.py`: `pick_device()` (CPU fallback when a GPU exists but the installed PyTorch has no kernels for it, verified by a tiny kernel; `SU2QC_DEVICE` override) and a routing rule; `configs/compute.yaml`; `scripts/where_to_run.py`.
3. Added `scripts/perlmutter/{setup_env.sh, submit.sh, fetch.sh}` and `scripts/slurm/{train.sbatch, twin.sbatch}`; `train_jepa.py` now uses `pick_device()` and has `--threads`; `env_check.py` reports the device actually used.
4. Updated `CLAUDE.md` §5, `plans/001` (§16 and the compute rows), `README.md` (laptop install with CPU-only PyTorch in its own environment), `environment.yml`, `STATE.json`, `prompts/000`, `002`, `003`, `005`; wrote `docs/PERLMUTTER.md` and `decisions/002`.
5. Added `tests/test_compute.py` (3 tests).

## Results and what they mean
- Routing with the measured costs: 5-seed main training ≈ 3.7 laptop-hours → Perlmutter; full twin day (≈ 480 circuits) ≈ 1.2 h → Perlmutter; 20,000-trajectory dataset ≈ 1–2 min, 1-seed checks and pilot-size twin runs → laptop. Whole-plan Perlmutter estimate 15–40 node-hours (cap 50), down from the 200 in `plans/000`.
- `submit.sh` and `fetch.sh` were exercised end to end against a stand-in `ssh`/`sbatch`/`sacct` and a local git remote: the dataset is shipped (or regenerated with the preregistered settings when absent), the exact commit is checked out, `sbatch` receives `-A <project>`, the queue and the script arguments, and the ledger records the job and its accounting.
- `python -m pytest -q`: 29 passed. `ruff`: clean. `scripts/check_artifacts.py`: OK. Code graph rebuilt and FRESH.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 591 / 1,068 / 39 (`reports/001`) | see `evidence/graph/stats.json` |
| `graphify affected` checks | — | `scripts/train_jepa.py` (device argument) — covered by `tests/test_pipeline.py::test_jepa_trains_one_epoch` and the smoke pipeline |

## Problems and assumptions
- Not tested against the real Perlmutter: needs Digonto's NERSC project id, user name and an `sshproxy` key. `docs/PERLMUTTER.md` step 5 is the first real test (30-minute debug queue).
- The laptop's speed-up over the 2-core measurement machine is assumed to be 2× (conservative); the first laptop session should record real timings in its report.
- `reports/000` and `reports/001` still mention the RTX 3070; they are append-only records of what was true then. This report and `decisions/002` supersede that assumption.
- The environment Digonto installed into (it contains `cuquantum-python-cu12`, so most likely `coding`) needs a repair; the steps are in the chat reply of 2 Oct 2026 and in `README.md`.

## Next action
Repair the environment, create the separate `su2qc-jepa` environment with CPU PyTorch, then `prompts/000` in Claude Code on the laptop.
