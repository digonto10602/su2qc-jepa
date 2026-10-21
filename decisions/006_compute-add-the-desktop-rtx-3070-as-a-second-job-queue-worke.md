---
id: decisions/006
title: 'Compute: add the desktop RTX 3070 as a second job-queue worker'
series: decisions
created_utc: '2026-10-21T14:52:06Z'
author: claude-code
milestone: M3
status: active
supersedes: null
superseded_by: null
---

# Compute: add the desktop RTX 3070 as a second job-queue worker

**Decided by:** Digonto, 2026-10-21 ("linux, dedicated but i occasionally turn it off … use a deploy key — go with option A"). **Amends** `decisions/004` (which stays in force for everything not changed here). **Drafted by:** claude-code.

## Decision
1. **A third machine.** Digonto's Linux desktop with a dedicated NVIDIA RTX 3070 (8 GB, compute capability `sm_86`) runs heavy and GPU jobs. Like Perlmutter, it is a *worker on the job queue*: nobody works on it, and it never pushes to `main`.
2. **Same queue, new destination.** Job files may now say `where: desktop` (`su2qc_jepa.jobs.WHERE = ("perlmutter", "desktop")`). `scripts/run.py --where desktop` and `scripts/jobs/enqueue.py --where desktop` address it. `configs/compute.yaml: queue.default_where` decides where a heavy job goes when `--where` is not given; it is set to `desktop` from 21 Oct 2026 because the Perlmutter worker has been stopped since 8 Oct.
3. **The worker.** `scripts/worker/worker.py --name desktop --mode local`, started by a systemd *user* timer: 3 minutes after boot, then 15 minutes after each tick ends (`scripts/worker/install_desktop.sh`). Each tick:
   - fetches GitHub itself, so switching the machine on is enough;
   - runs at most one job, at `nice 10`, with `SU2QC_DEVICE=cuda`, so a job fails loudly instead of falling back to the CPU;
   - pushes status, log tail and declared outputs (≤ 50 MB, never `.npz`) to the `results` branch.
4. **Interruptions heal themselves.** The desktop is sometimes switched off. A local job still marked running when a tick starts was interrupted; the tick's lock proves nothing else is running. The job is rerun, up to `MAX_ATTEMPTS` = 3 runs in all, and then recorded `LOST`. While a job runs, the results branch shows `RUNNING`. Every attempt is kept in the job's `history`.
5. **Credentials.** A deploy key with write access to this repository only (`~/.ssh/su2qc_deploy_desktop`, SSH host alias `github-su2qc-desktop`). No personal GitHub login and no IBM token on the desktop. The hardware-submission script stays off the worker allowlist.
6. **Environment.** `scripts/worker/setup_env_desktop.sh`: Python 3.12 (conda prefix, or a venv if there is no conda) at `~/.su2qc-jepa-env`, PyPI's CUDA build of PyTorch, `pip install -e ".[ml,dev]"`. Before the worker is installed, it checks that PyTorch has kernels for the GPU's architecture and runs the fast tests, including the CUDA case of `test_training_and_baselines_run_on_device`.

## Why
- The Perlmutter worker has been silent since 2026-10-08 (no heartbeat), and the preregistered J2 run `v1_final` (5 seeds, 200 epochs, masked) needs about 2 GPU-hours. On the laptop it would take about 10 h, beyond the runner's 20-minute rule. J2 is due 30 Oct.
- The desktop is dedicated, so it needs no admission control. The queue gives every result the same record as a Perlmutter job (commit, machine, log, outputs) and keeps one writer of `main`, the laptop session. The local worker mode already existed and was tested end to end; it only lacked recovery from power-off, now added with a regression test (`tests/test_jobs.py::test_worker_recovers_interrupted_local_jobs`).
- The preregistration fixes the configuration, seed and analysis, not the machine. A dataset rebuilt on the desktop is checked against the preregistered reference with the fingerprint equivalence rule (`docs/PREREGISTRATION.md` §2), and the GPU model and driver are recorded in each job's log.

## Alternatives considered
- **A Claude Code session on the desktop running a prompt (option B):** more moving parts. The runner would refuse heavy or GPU work there without a new machine profile, two sessions would push to `main`, and `runs/` outputs would need their own path back. Rejected.
- **Wait for Perlmutter:** an unknown delay against the 30 Oct J2 date. Perlmutter stays available as `where: perlmutter` once its worker is restarted.
- **Train `v1_final` on the laptop:** about 10 h at 2 threads on a shared machine, against the laptop rules. Rejected.

## Consequences (what must be re-run or re-checked)
- Code: `src/su2qc_jepa/jobs.py` (WHERE), `scripts/jobs/enqueue.py` and `scripts/run.py` (`--where`), `scripts/worker/worker.py` (local recovery, RUNNING status), `scripts/jobs/status.py` (one heartbeat per worker). New: `scripts/worker/setup_env_desktop.sh`, `scripts/worker/install_desktop.sh`, `docs/DESKTOP.md`. Tests: `test_job_destinations`, `test_worker_recovers_interrupted_local_jobs`.
- `CLAUDE.md` §5 and `configs/compute.yaml` updated to name the desktop. `decisions/004` is not edited.
- First use: the GPU check of `setup_env_desktop.sh` must pass, and the first job's dataset rebuild is compared with the reference by fingerprint before its results are used.
