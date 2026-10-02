# Heavy jobs: the job queue and the Perlmutter worker

Living document. Policy: `decisions/004` (the queue was introduced in `decisions/003`); settings: `configs/compute.yaml`; plan: `plans/001` §16.

**How it works.** Claude Code on the laptop never connects to Perlmutter. When `scripts/run.py` finds a job too heavy for the laptop (or it needs a GPU, or the laptop has no room, or a laptop attempt hit its limits), it writes a numbered job request `jobs/NNN_<slug>.yaml` (what to run, at which commit, which files to send back) and pushes it to `main`. On Perlmutter, `scrontab` (NERSC's scheduled-job tool, which replaced cron) starts a *worker tick* every 15 minutes. The tick pulls `main`, submits new jobs addressed to `perlmutter` with Slurm (NERSC's batch scheduler) on one A100, and, when they finish, pushes their status, log tail and declared outputs to a separate `results` branch. The laptop reads that branch with `scripts/jobs/status.py` and copies outputs in with `scripts/jobs/fetch.py`. This is the same "Claude updates GitHub, Perlmutter runs what it finds" pattern used before, made explicit and checked.

```
laptop (Claude Code)                     GitHub                         Perlmutter
 code commit ── push ─────────────►  main  ◄──── pull every 15 min ── worker tick (scrontab, cron QOS)
 jobs/NNN.yaml ── push ─────────►   main                                │ sbatch (shared QOS, 1 A100)
 status.py / fetch.py ◄── fetch ──  results ◄──── push ──────────────── │ status.json, log.txt, outputs/
```

Guarantees built into the worker (`scripts/worker/worker.py`): it only runs jobs whose commit is on `main`; every step must be `python scripts/<allowlisted>.py ...` (no shell commands, no hardware submission); it never pushes to `main`; one tick at a time (lock file); at most 2 new submissions per tick; it refuses jobs that would exceed the node-hour budget (50); outputs above 50 MB or `.npz` files are not published (listed as skipped).

## One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub)

1. **Environment and checkout.** Log in to Perlmutter as usual, then:

   ```bash
   git clone https://github.com/digonto10602/su2qc-jepa.git ~/su2qc-setup
   bash ~/su2qc-setup/scripts/worker/setup_env_perlmutter.sh m1234          # your NERSC project
   ```

   This creates the conda environment in `/global/common/software/m1234/su2qc-jepa-env` (NERSC's recommended place for environments used by jobs), installs CUDA PyTorch and `qiskit-aer-gpu`, and runs the tests.

2. **Worker.**

   ```bash
   bash ~/su2qc-setup/scripts/worker/install_perlmutter.sh m1234
   ```

   It creates an SSH *deploy key* (a key that can only access this one repository) and prints its public half. Add it on GitHub: repository → Settings → Deploy keys → Add deploy key, tick **Allow write access**. Then, as the script prints:

   ```bash
   ssh -T git@github-su2qc                       # should greet digonto10602/su2qc-jepa
   bash $SCRATCH/su2qc-worker/tick.sh            # one tick by hand: creates the results branch
   bash $SCRATCH/su2qc-worker/scrontab_merge.sh add $SCRATCH/su2qc-worker/scrontab.txt   # every 15 min from now on (UTC)
   scrontab -l                                   # your other entries + the su2qc-jepa block between its markers
   ```

   **Your other scrontab entries are kept.** `scrontab <file>` would *replace* your whole table and `scrontab -r` would *delete* all of it, so never use them for this worker. `scrontab_merge.sh` backs up the current table to `~/.scrontab-backup-<UTC>.txt`, changes only the lines between `# >>> su2qc-jepa worker >>>` and `# <<< su2qc-jepa worker <<<`, and restores the backup if any other line changed. To stop only this worker: `bash $SCRATCH/su2qc-worker/scrontab_merge.sh remove`.

3. **Tell the repository.** Put the project id into `configs/compute.yaml` (`perlmutter.account`) and commit. Claude Code never fills this in.

4. **First real test.** On the laptop (or ask Claude Code):

   ```bash
   python scripts/jobs/enqueue.py check "worker smoke test" --time 00:10:00 \
     --step "python scripts/env_check.py" --output evidence/ENV.json --push   # a GPU check must run there
   python scripts/jobs/status.py        # QUEUED -> SUBMITTED -> COMPLETED within ~30 min
   python scripts/jobs/fetch.py NNN
   ```

   The fetched `evidence/ENV.json` should show an A100 and `"torch_device_used": "cuda"`.

There is no daily step: the worker runs under your account on Perlmutter, so NERSC's multi-factor login is only needed when you log in yourself.

## Self-healing

- **Automatic resubmission** (up to 3 attempts, `su2qc_jepa.jobs.retry_resources`): TIMEOUT → twice the wall-clock limit (cap 48 h); OUT_OF_MEMORY → twice the GPUs, and so twice the memory on the shared queue (cap 2 GPUs); NODE_FAIL, PREEMPTED, BOOT_FAIL, LOST (Slurm has no record for 3 h) → same resources. FAILED (a program error) is never retried. The status keeps every attempt in `history`.
- **Worker repair:** a corrupted clone is deleted and re-cloned. A crashed tick writes `tick_errors.log` and the next tick simply runs again. If `state.json` is lost, in-flight jobs are recovered from the `results` branch. A lock file prevents overlapping ticks.
- **Heartbeat:** the worker pushes `results/_worker/perlmutter.json` at most hourly while work is pending, and every 12 h otherwise. `scripts/jobs/status.py` shows its age and warns when the worker looks stopped.

## Costs and limits

`shared` QOS: one A100 = ¼ node-hour per hour, up to 48 h. Whole-plan estimate 15–40 node-hours; the worker stops at 50 (`--budget-node-hours`). The `cron` QOS ticks are short (well under a minute when idle). `$SCRATCH` is purged after a period of inactivity; everything that matters is pushed to the `results` branch by the worker.

## When something is wrong

| Symptom | Meaning | What to do |
|---|---|---|
| job stays QUEUED > 1 h | no tick is running | on Perlmutter: `scrontab -l`; read `$SCRATCH/su2qc-worker/tick-*.log` |
| state REFUSED | invalid job, commit not on `main`, or budget | read `reason` in the status; queue a corrected job (new number) |
| state FAILED / TIMEOUT | the job ran and failed | `git show origin/results:NNN/log.txt`; fix, push, queue a new job |
| `ssh -T git@github-su2qc` fails | deploy key missing or read-only | re-add it with write access |
