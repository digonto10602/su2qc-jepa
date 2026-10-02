---
id: reports/003
title: 'Compute update 2: safe laptop and a pull-based job queue for Perlmutter'
series: reports
created_utc: '2026-10-02T19:54:59Z'
author: planner
milestone: null
status: done
supersedes: null
superseded_by: null
---

# Compute update 2: safe laptop and a pull-based job queue for Perlmutter

**Milestone:** before M0 · **Prompt:** Digonto's message of 2 Oct 2026 (Cowork) · **Commit range:** not yet under git

## What was asked
Other Claude sessions may be running on the laptop, so this project must not crash it. Digonto's earlier Perlmutter workflow was pull-based: Claude updates GitHub, a cron job on Perlmutter runs what it finds. Question: what should be done, or is it better to run everything on the RTX 3070 desktop?

## Actions taken
1. Measured the time and peak memory of every laptop-side step on 2 CPU cores. Tests: 34 s / 0.9 GB. J0 gate: 10 s / 0.2 GB. 20,000-trajectory dataset: 87 s / 0.2 GB. Training check: 46 s / 1.2 GB. One 12-qubit twin circuit: 51 s / 0.5 GB.
2. Checked NERSC's documentation: cron is replaced by `scrontab` (`-q cron -C cron`, UTC times); `shared` GPU queue at ¼ node-hour per GPU-hour.
3. Added `scripts/safe_run.sh`, which runs a command at lowest CPU/I/O priority, with 2 threads and a 3 GB memory ceiling. The ceiling uses a cgroup via `systemd-run --user`; the fallback is an address-space limit of 3×, verified to work with PyTorch while a 1× limit aborts. `train_jepa.py` honours `SU2QC_THREADS`.
4. Added the job queue:
   - a numbered `jobs/` series validated by `check_artifacts`;
   - `src/su2qc_jepa/jobs.py` (format, validation, script allowlist);
   - `scripts/jobs/{enqueue,status,fetch}.py`;
   - `scripts/worker/worker.py` (lock, sync, eligibility, Slurm submit/poll, local mode, size-capped publishing, budget, push with rebase-on-conflict, explicit git identity);
   - installers for Perlmutter (deploy key, tick script, scrontab entry) and for an optional desktop worker (systemd user timer with CPU/memory caps).
5. Removed the SSH-push scripts. Rewrote `CLAUDE.md` §5, `docs/PERLMUTTER.md`, `plans/001` §16, the README, `configs/compute.yaml`, `STATE.json` and prompts 002/003/005. Wrote `decisions/003`, which supersedes `decisions/002`.
6. Added `tests/test_jobs.py` (9 tests, including one end-to-end worker tick against a local git remote).

## Results and what they mean
- End-to-end runs against a local stand-in for GitHub:
  - A desktop-mode job and a Slurm-mode job (with stand-in `sbatch`/`sacct`) each ran at the pushed commit, published outputs to `results` and were fetched on the laptop without a merge.
  - The allowlist refused a job calling `hw_submit.py`.
  - Only the laptop committed to `main`.
  - Two workers pushing at once were serialised by the rebase-and-retry path.
- **Bugs found and fixed.**
  - `.gitignore` and `.graphifyignore` used `data/`, which also matched the package folder `src/su2qc_jepa/data/`. The GitHub repository would have lacked part of the package, so CI and every worker job would have failed; the code graph was also missing those files. Both are now root-anchored (`/data/`, `/runs/`). The graph grew from 636 to 722 nodes.
  - The committed code graph kept two stale nodes from that period because Graphify's update reuses its local cache. A fresh clone (as in CI) builds without them, so CI would have reported the graph as stale. `scripts/graph_update.sh` now always rebuilds with an empty cache.
  - Worker commits could take the identity from a user's `GIT_AUTHOR_*` variables. They now always use `su2qc-worker-<name>`.
- Routing at 2 threads: main training ≈ 7 h and a full twin day ≈ 2.4 h → queued. Datasets, training checks of ≤ 30 epochs and pilot twin runs → laptop.
- Desktop answer: the RTX 3070 could run everything, roughly 1–2 h for the heaviest job, and would be the simplest option if it can be dedicated to this. Since it cannot, it is an optional second worker on the same queue, and the plan does not depend on it.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 636 / 1,120 / 42 (`reports/002`, data package missing) | see `evidence/graph/stats.json` |
| `graphify affected` checks | — | `train_jepa.py`, `artifacts.py` (jobs series) → covered by `tests/test_pipeline.py`, `tests/test_repo_conventions.py`, `tests/test_jobs.py` |

## Problems and assumptions
- Not yet run on the real Perlmutter. The one-time setup and the first real test are in `docs/PERLMUTTER.md` and need Digonto's NERSC project and a deploy key. Whether `scrontab`'s cron nodes can reach GitHub over SSH is assumed (the earlier cron workflow did); `install_perlmutter.sh` step 3, one tick by hand, checks it.
- `--noise-model` for `run_twin.py` is specified in `prompts/003` but not yet implemented (a task for that session).
- Datasets are regenerated on the worker; NumPy/SciPy version differences could change checksums slightly, and each job report compares them.
- `reports/000`–`002` describe earlier states (RTX 3070, then SSH push); they are append-only. `decisions/003` is the current policy.

## Next action
On the laptop: create the `su2qc-jepa` environment (CPU PyTorch), run `prompts/000`; before week 2, follow `docs/PERLMUTTER.md`.
