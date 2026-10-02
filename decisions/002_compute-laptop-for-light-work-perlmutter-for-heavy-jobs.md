---
id: decisions/002
title: 'Compute: laptop for light work, Perlmutter for heavy jobs'
series: decisions
created_utc: '2026-10-02T19:30:21Z'
author: planner
milestone: M0
status: superseded
supersedes: null
superseded_by: decisions/003
---

# Compute: laptop for light work, Perlmutter for heavy jobs

## Decision
There is no desktop GPU in this project. Claude Code runs on the laptop (Dell G7 7588, 6-core i7-8750H), and everything there runs on the CPU with a CPU-only PyTorch in its own `su2qc-jepa` environment. Jobs estimated at more than one hour on the laptop run on NERSC Perlmutter: one A100 in the `shared` queue, submitted from the laptop with `scripts/perlmutter/submit.sh` and collected with `scripts/perlmutter/fetch.sh`. The rule and the machine settings live in `configs/compute.yaml`; `scripts/where_to_run.py` applies the rule from measured unit costs. Code selects its device with `su2qc_jepa.compute.pick_device()`, which falls back to the CPU when a GPU is present but unusable. The Perlmutter budget for the whole plan is capped at 50 node-hours.

## Why
- The RTX 3070 desktop assumed in `plans/001` (1 Oct) is not available.
- The laptop's GTX 1060 Max-Q is a Pascal card (compute capability 6.1). Current PyTorch CUDA builds do not include kernels for it, and installing a CUDA 13 PyTorch on the laptop also pulled in `cuda-bindings` 13, which broke `cuquantum-python-cu12` in the `coding` environment (reported by Digonto, 2 Oct 2026). CPU-only PyTorch in a separate environment avoids both problems.
- Measured on 2 Oct 2026 (2 cores): generating 2,000 trajectories took 11.7 s; one training epoch over 1,137 trajectories took 2.5 s; one 12-qubit density-matrix twin circuit at 4,000 shots takes 6–30 s. With a conservative 2× speed-up for 6 cores, the laptop needs about 3.7 h for the 5-seed main training run (about 7 h with the masked-coupling runs), 18–35 h for the ablation ladder, and about 1.2 h or more for a full twin day — and minutes for everything else.

## Alternatives considered
- *Everything on the laptop:* possible (overnight runs) but slow for the ablation ladder; kept as the fallback when Perlmutter is unreachable, with reduced seeds and a note in the report.
- *Everything on Perlmutter, including Claude Code:* rejected. NERSC's multi-factor login needs a person, login nodes are not for computation, and the IBM token should stay on one machine.
- *Perlmutter CPU nodes instead of GPU:* possible; the GPU queue was chosen because one shared A100 costs ¼ node-hour per hour and also accelerates the Aer twin.

## Consequences
- `CLAUDE.md` §5, `plans/001` (§16 and the compute rows), `README.md`, `environment.yml`, `STATE.json`, `prompts/002`, `003`, `005` were updated; `docs/PERLMUTTER.md` holds the one-time setup.
- Twin jobs on Perlmutter read a noise model built on the laptop and saved to a file (`--noise-model`), never `--backend`.
- Every Perlmutter job is recorded in `evidence/perlmutter/LEDGER.json`; session reports state node-hours used.
