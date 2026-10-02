---
id: decisions/003
title: 'Compute: a safe laptop and a pull-based job queue for Perlmutter'
series: decisions
created_utc: '2026-10-02T19:51:53Z'
author: planner
milestone: M0
status: superseded
supersedes: decisions/002
superseded_by: decisions/004
---

# Compute: a safe laptop and a pull-based job queue for Perlmutter

## Decision
1. **Laptop (shared with other Claude sessions).** Claude Code runs on the laptop and does only light work there, always through `scripts/safe_run.sh`: lowest CPU and I/O priority, 2 CPU threads, a 3 GB memory ceiling (a cgroup limit via `systemd-run --user` where available, otherwise an address-space limit of 3× that, which PyTorch tolerates). One computing command at a time, no background jobs. Work estimated above 15 minutes at 2 threads is queued.
2. **Job queue instead of SSH.** Heavy work is written as a numbered job request `jobs/NNN_<slug>.yaml` on `main` (`scripts/jobs/enqueue.py`). A pull-based worker (`scripts/worker/worker.py`), started every 15 minutes on Perlmutter by `scrontab`, runs the jobs addressed to it with Slurm on one A100 at the exact commit named in the request, and pushes status, a log tail and the declared outputs to the `results` branch, which the laptop reads (`scripts/jobs/status.py`, `scripts/jobs/fetch.py`). The worker authenticates to GitHub with a deploy key limited to this repository.
3. **Desktop optional.** The same worker can run on the RTX 3070 desktop in local mode (systemd user timer) for jobs queued with `--where desktop|any`. The plan does not depend on it.

Supersedes `decisions/002` (which sent jobs by SSH from the laptop and needed a daily NERSC login key).

## Why
- Other Claude sessions run on the laptop; an uncapped training run or a 12-thread NumPy job could starve them. Measured peaks of every laptop-side step fit easily inside 2 threads and 3 GB (tests 0.9 GB / 35 s; training check 1.2 GB / 46 s; dataset of 20,000 trajectories 0.2 GB / 90 s; one twin circuit 0.5 GB / 51 s).
- Digonto's earlier Perlmutter workflow was pull-based (GitHub updated by Claude, a scheduled job on Perlmutter runs what it finds). NERSC has replaced cron with `scrontab` (`-q cron -C cron`, times in UTC), so the pattern maps onto a supported tool.
- No SSH from the laptop: no daily multi-factor login, no NERSC credentials anywhere near an agent.
- Tested on 2 Oct 2026 with a local stand-in for GitHub and stand-ins for `sbatch`/`sacct`: a desktop-mode job and a Slurm-mode job ran at the pushed commit, status and outputs arrived on `results`, the laptop fetched them without merging, the allowlist refused a job calling the hardware-submission script, and only the laptop committed to `main`.

## Alternatives considered
- *Everything on the desktop (RTX 3070, Claude Code there too):* computationally sufficient — the heaviest job (5 seeds × 200 epochs) would take roughly 1–2 h on its GPU and a twin day well under an hour — and the simplest setup. Not chosen as the default because Digonto cannot dedicate the desktop to this project; kept available as an optional worker.
- *SSH push from the laptop (`decisions/002`):* needs a fresh NERSC key every 24 hours and gives an agent a shell on Perlmutter.
- *GitHub Actions self-hosted runner on Perlmutter:* NERSC login nodes are not for long-lived services; rejected.

## Consequences
- New: `jobs/` series (numbered YAML, enforced by `scripts/check_artifacts.py`), `src/su2qc_jepa/jobs.py` (format, validation, allowlist), `scripts/jobs/{enqueue,status,fetch}.py`, `scripts/worker/{worker.py, install_perlmutter.sh, install_desktop.sh, setup_env_perlmutter.sh}`, `scripts/safe_run.sh`.
- Removed: `scripts/perlmutter/submit.sh`, `fetch.sh`, `scripts/slurm/*.sbatch`.
- `.gitignore` and `.graphifyignore` now anchor `/data/` and `/runs/` to the repository root. Before this, they also matched the package folder `src/su2qc_jepa/data/`, which would have been left out of the GitHub repository and out of the code graph (found by the queue test).
- Datasets are regenerated on the worker from the same seed; reports compare the fetched checksum with the laptop's.
