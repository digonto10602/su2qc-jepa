---
id: decisions/004
title: 'Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs'
series: decisions
created_utc: '2026-10-02T20:26:48Z'
author: planner
milestone: M0
status: active
supersedes: decisions/003
superseded_by: null
---

# Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs

## Decision
1. **Two machines only.**
   - The **laptop** (64 GB RAM, i7-8750H with 6 cores / 12 threads, GTX 1060 Max-Q) runs Claude Code and light work.
   - **NERSC Perlmutter** (A100 GPUs) runs everything heavy.
   - There is no desktop worker.
   - The laptop GPU is not used. Current PyTorch CUDA builds have no kernels for its Pascal architecture (compute capability 6.1), and installing them broke the `coding` environment once; `prompts/009` repairs that. The project uses its own conda environment, `su2qc-jepa`, with CPU-only PyTorch.
2. **One entry point.** Every computation goes through `python scripts/run.py -- <command>` (`src/su2qc_jepa/localrun.py`), which works in four stages.
   - **Classify.** A command goes to Perlmutter if it needs a GPU, or if its estimated laptop time is above 20 minutes. The estimate comes from measured unit costs and, for training, the dataset manifest. A heavy command never runs on the laptop: the runner writes `jobs/NNN_*.yaml` (with a step that rebuilds the dataset on Perlmutter from the same seed) and, with `--push`, commits and pushes it.
   - **Admit.** A light command runs only if there is room *now*:
     - available memory minus the request stays above a reserve of 16 GB (at most 25% of total RAM, so the rule scales down on small machines);
     - the 1-minute load plus the requested threads leaves 2 logical CPUs free;
     - no other su2qc computation is running in any session (a lock file).
     
     Otherwise the runner waits up to 20 minutes, polling every 30 s, then queues the job for Perlmutter. A command that cannot be queued is not run (exit code 2).
   - **Cap.** The command runs at nice 19 and idle I/O priority, with 2 threads by default (4 at most) set for every maths library, and a wall-clock limit (40 min by default). Its memory ceiling is 4 GB by default and 16 GB at most:
     - a cgroup limit through `systemd-run --user --scope` (`MemoryMax`, no swap), used only when the memory controller is delegated to the user session;
     - otherwise an address-space limit of 3× the request (`prlimit`).
     
     The process also gets `oom_score_adj = 1000`, so under memory pressure the kernel kills this job first and never another session's process. If the runner itself is killed (for example, its Claude session is closed), the job receives a termination signal too, and the lock, which is a kernel file lock, is released, so nothing is left running unsupervised.
   - **Heal.**
     - A memory kill is retried once with twice the memory, if admission allows it; otherwise the job is queued for Perlmutter.
     - A timeout means the job is heavier than estimated, so it is queued for Perlmutter.
     - A program error is never retried. The log tail is shown and the bug is fixed in code.
     - Every attempt is written to `.local_runs/ledger.jsonl` (git-ignored), with its own log.
     - Exit codes: 0 done here, 10 queued, 1 failed, 2 not run.
3. **Perlmutter worker heals itself** (`scripts/worker/worker.py`, started by `scrontab` every 15 minutes).
   - **Resubmission.** Failed jobs are resubmitted automatically by `su2qc_jepa.jobs.retry_resources`, up to 3 attempts in all:
     - TIMEOUT: twice the wall-clock limit, capped at 48 h;
     - OUT_OF_MEMORY: twice the GPUs, and so twice the memory on the shared queue (cap 2);
     - NODE_FAIL, PREEMPTED, BOOT_FAIL, or LOST (Slurm has no record for 3 h): the same resources;
     - FAILED, which is a program error: never retried.
   - **Worker repair.**
     - A corrupted clone is deleted and re-cloned.
     - A crashed tick writes `tick_errors.log`, and the next tick runs normally.
     - If the worker's state file is lost, in-flight jobs are recovered from the `results` branch.
     - The worker pushes a heartbeat, `results/_worker/perlmutter.json`, which `scripts/jobs/status.py` reads to warn when the worker looks stopped.
4. The queue mechanics of `decisions/003` are unchanged: numbered job files on `main`, an allowlist of scripts, results only on the `results` branch, a deploy key, a 50 node-hour budget, and the laptop never connecting to Perlmutter.

## Why
- Digonto will run the project only on the laptop and Perlmutter, and other Claude sessions share the laptop. A fixed 2-thread / 3 GB cap (`decisions/003`) protected them, but it did not ask whether the machine had room *at that moment*, and it gave up instead of recovering. Admission control plus `oom_score_adj` protects the other sessions in both directions:
  - a su2qc job does not start when they are busy;
  - if memory runs out anyway, the kernel kills the su2qc job first.
- **Measured peaks of the laptop-side steps** (2 Oct 2026, 2 threads):

  | step | time | peak memory |
  |---|---|---|
  | tests | 34 s | 0.9 GB |
  | J0 gate | 10 s | 0.2 GB |
  | 20,000-trajectory dataset | 87 s | 0.2 GB |
  | training check | 46 s | 1.2 GB |
  | one 12-qubit twin circuit | 51 s | 0.5 GB |

  All of them fit the 4 GB default with a wide margin. The main training run (5 seeds × 200 epochs, with and without the masked-coupling task) is estimated at about 1,058 laptop-minutes, so it always goes to Perlmutter.
- **The GTX 1060 Max-Q.** It has 6 GB, Pascal architecture. It would need an old PyTorch (CUDA 11.8 / 12.1 builds) with its own driver constraints, for a speed-up that the A100 queue already gives. The risk of breaking another environment again is not worth it.
- **Self-healing was tested** with a real allocation above the ceiling: the 0.5 GB attempt failed, the retry with 1 GB succeeded (peak 3.28 GB of address space under the fallback limiter), and the ledger recorded `retry`, then `done`. A TIMEOUT resubmission was tested with stand-in `sbatch`/`sacct`: the second submission had twice the time limit, and both attempts were in the job's history.

## Alternatives considered
- *Keep `decisions/003` as it was* (fixed caps, optional desktop worker): simpler, but it starts jobs on a busy laptop and does not recover from a crash; the desktop is out of scope now.
- *Use the GTX 1060 with an old PyTorch build in its own environment:* possible, but fragile, and it was the root cause of the `coding` breakage; rejected.
- *Run every computation on Perlmutter:* safest for the laptop, but the queue adds 15–30 minutes of latency to tests and small checks, which would slow every session; rejected for light work.

## Consequences (what must be re-run or re-checked)
- **New:**
  - `src/su2qc_jepa/localrun.py` and `scripts/run.py`;
  - `tests/test_localrun.py` (5 tests, including a real capped run that hits the ceiling and retries, and a check that a job dies with its runner);
  - `jobs.retry_resources` and two new tests in `tests/test_jobs.py`;
  - the worker heartbeat and resubmission;
  - `prompts/009`, which repairs `coding` and creates `su2qc-jepa`.
- **Removed:** `scripts/worker/install_desktop.sh` and `scripts/where_to_run.py`. `WHERE` is now only `perlmutter`. `scripts/safe_run.sh` remains as a shim (`run.py --no-queue`).
- **Changed:** `configs/compute.yaml`, the `CLAUDE.md` §5 rules, `docs/PERLMUTTER.md`, `plans/001` §16, the README, and `STATE.json`.
- **Must be checked on the real laptop** (by `prompts/009`): which memory limiter is active (`cgroup` or `address-space`), and that all tests pass through the runner.
- **Must be checked on the real Perlmutter** (by `docs/PERLMUTTER.md`, step 4): the first tick, the heartbeat, and one completed job.
