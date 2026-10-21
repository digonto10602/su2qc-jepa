# Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use

Policy: `decisions/006` (amends `decisions/004`). The desktop is a second worker on the same job queue as Perlmutter: the laptop session writes a numbered job file `jobs/NNN_*.yaml` with `where: desktop` and pushes it to `main`; the desktop's worker picks it up, runs it on the GPU at exactly that commit, and pushes status, log and outputs to the `results` branch. Nobody works *on* the desktop; nothing is pushed from it to `main`.

## One-time setup (on the desktop, Linux, about 20 minutes)
1. Get the code (this copy is only used to build the environment; the worker keeps its own copy):
   ```
   git clone https://github.com/digonto10602/su2qc-jepa.git ~/su2qc-setup
   ```
2. Build the environment and check the GPU (CUDA build of PyTorch, the package, the fast tests including the CUDA case):
   ```
   bash ~/su2qc-setup/scripts/worker/setup_env_desktop.sh
   ```
   It must end with `GPU ok: NVIDIA GeForce RTX 3070 sm_86 …` and the test summary without failures. If it says the driver is too old for the PyTorch CUDA build, update the NVIDIA driver and re-run.
3. Install the worker (deploy key, tick script, systemd user timer):
   ```
   bash ~/su2qc-setup/scripts/worker/install_desktop.sh
   ```
   then follow the four steps it prints:
   - add the printed public key on GitHub (repository → Settings → Deploy keys → Add, title `desktop worker`, **Allow write access**; the key can write only to this repository);
   - `ssh -T git@github-su2qc-desktop` must greet `digonto10602/su2qc-jepa`;
   - run one tick by hand: `bash ~/su2qc-worker/tick.sh` (it writes a heartbeat to the `results` branch; the laptop sees it in `python scripts/jobs/status.py`);
   - start the timer: `systemctl --user enable --now su2qc-worker.timer`, and `sudo loginctl enable-linger $USER` so it also runs when you are not logged in.

## Daily use
- **Switching the desktop on is all that is needed.** The timer runs a tick 3 minutes after boot and then 15 minutes after each tick ends; every tick fetches GitHub itself, so queued jobs start without any `git pull`.
- `git -C ~/su2qc-setup pull` is only needed when the dependencies changed (a commit touching `pyproject.toml`); then re-run step 2.
- **Switching it off during a job is safe.** The next tick after boot finds the interrupted job and runs it again (up to 3 runs in all; after that it is recorded `LOST`). The results branch shows `RUNNING` while a job runs.
- One job runs at a time, at low CPU priority (`nice 10`), with `SU2QC_DEVICE=cuda`, so a job fails loudly if the GPU is not usable instead of silently running on the CPU.

## From the laptop
- Queue: `python scripts/run.py --push --where desktop -- python scripts/train_jepa.py …` (or `scripts/jobs/enqueue.py … --where desktop --push`). The commit must already be pushed.
- Follow: `python scripts/jobs/status.py` (one heartbeat line per worker; it warns about the desktop only when jobs are waiting for it).
- Fetch: `python scripts/jobs/fetch.py NNN` (a local file that differs, e.g. a dataset manifest, is kept; the job's copy goes to `evidence/jobs/NNN/outputs/`).
- Datasets are rebuilt on the desktop from their manifest and seed; compare a rebuild with the preregistered reference using `scripts/compare_fingerprints.py` (equivalence rule in `docs/PREREGISTRATION.md` §2).

## Troubleshooting (on the desktop)
| symptom | check |
|---|---|
| no heartbeat on the laptop | `systemctl --user list-timers su2qc-worker.timer`; `journalctl --user -u su2qc-worker -n 50`; `cat ~/su2qc-worker/tick_errors.log` |
| push refused | the deploy key lacks write access, or `ssh -T git@github-su2qc-desktop` fails |
| job FAILED with a CUDA error | `nvidia-smi`; re-run step 2 (driver vs PyTorch CUDA build) |
| stop the worker | `systemctl --user disable --now su2qc-worker.timer` |
