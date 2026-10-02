---
id: reports/004
title: 'Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners'
series: reports
created_utc: '2026-10-02T20:26:49Z'
author: planner
milestone: null
status: done
supersedes: null
superseded_by: null
---

# Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners

**Milestone:** before M0 · **Prompt:** Digonto's message of 2 Oct 2026 (Cowork) · **Commit range:** not yet under git

## What was asked
1. A prompt for `claude --dangerously-skip-permissions` that repairs the `coding` conda environment, which `pip install -e ".[ml,ibm,dev]"` broke, and creates a separate laptop environment for su2qc-jepa.
2. Set the package up for two machines only: the laptop (64 GB RAM, GTX 1060 Max-Q) and NERSC Perlmutter.
   - Heavy GPU or CPU work always goes to Perlmutter through the `scrontab` worker and GitHub pushes.
   - Light work runs on the laptop only if the resources are there, with limits, so that other Claude sessions are never crashed.
   - A crashed job fixes itself.

## Actions taken
1. **`prompts/009` — laptop environment repair and setup** (planner, M0). It has four phases and eight absolute safety rules (the rules are summarised in "Problems and assumptions").
   - **A. Backup and inventory.** The prompt saves:
     - the conda explicit list and export;
     - the pip freeze, list and check;
     - the conda history;
     - an import test of the GPU stack (cuQuantum, `cuda.bindings`, CUDA-Q, Aer, CuPy, PyTorch).
     
     It also classifies every package from the bad install as *new*, *replaced conda package* or *replaced pip package*. This matters because the freeze is taken after the damage, so it does not hold the old versions.
   - **B. Repair `coding`, only if no process is using it.**
     1. A reverse-dependency check.
     2. Removal of only the new packages: the su2qc-jepa package, the CUDA-13 PyTorch/triton, the CUDA-13 runtime wheels without a `-cu12` suffix, Graphify and tree-sitter, `mthree` and `runningman`.
     3. Restoration of `cuda-bindings` to 12.x (`>=12.9.4,<13`, which `cuquantum-python-cu12` requires) and of any replaced conda or pip package.
     4. A check after each group, with a rollback on any regression.
   - **C. Create `su2qc-jepa`.** Python 3.12, CPU PyTorch installed *first*, then `pip install -e ".[ml,ibm,dev]"`. It then checks that no `nvidia-*` packages are present and verifies through the project's own runner, including which memory limiter is active.
   - **D. Report.** A numbered report and the `STATE.json` update.
2. **`src/su2qc_jepa/localrun.py` and `scripts/run.py`** — the only way to compute. They classify, admit, run capped and heal, as recorded in `decisions/004`. `scripts/safe_run.sh` is now a shim that calls `run.py --no-queue`.
3. **Worker self-healing** (`scripts/worker/worker.py`, `su2qc_jepa.jobs.retry_resources`).
   - Automatic resubmission after TIMEOUT, OUT_OF_MEMORY, NODE_FAIL, PREEMPTED, BOOT_FAIL or LOST, up to 3 attempts.
   - Re-clone of a corrupted checkout.
   - `tick_errors.log` for a crashed tick.
   - Recovery of in-flight jobs from the `results` branch.
   - A heartbeat that `scripts/jobs/status.py` reads.
4. **Removed the desktop path:** `install_desktop.sh`, `where_to_run.py`, and `--where desktop|any`.
5. **Rewrote the compute documents:**
   - `configs/compute.yaml`;
   - `CLAUDE.md` §5;
   - `docs/PERLMUTTER.md` (also fixed the config key it named: `perlmutter.account`);
   - `plans/001` §16;
   - the README (first two sessions; the tour now goes through `run.py`; correct test count);
   - `STATE.json` (milestone `M-env`, `jobs` series);
   - prompts 001–006, so every computing command goes through `run.py`. Prompt 003 no longer calls the removed `where_to_run.py`.
6. Wrote `decisions/004` (supersedes `decisions/003`) and regenerated every `INDEX.md`.

## Results and what they mean
- **Tests:** 45 fast tests pass through the runner, in 46 s with a peak of 1.9 GB. A slow test exists but was not re-run; physics is unchanged. New tests:
  - `tests/test_localrun.py` (5);
  - `tests/test_jobs.py`: 2 new (the retry rule; a Slurm-mode TIMEOUT that is resubmitted with twice the time and then completes, both attempts in its history).
- **The laptop runner, tested for real** (sandbox with 2 CPUs and about 8 GB, address-space limiter):
  - An allocation above a 0.5 GB ceiling failed; the runner retried once with 1 GB and succeeded. The ledger recorded `retry`, then `done`, with the limit each attempt actually ran under.
  - A job over its time limit was stopped.
  - When the runner was killed with `SIGKILL`, its job died with it.
- **Routing:**
  - The main training run (5 seeds × 200 epochs, plus the masked-coupling runs) is estimated at about 1,058 laptop-minutes, so it goes to Perlmutter.
  - A 20,000-trajectory dataset is estimated at about 2 minutes, so it runs on the laptop.
  - A GPU request always goes to Perlmutter.
- **What it means.** On the laptop, an su2qc job now starts only when there is room. It runs at the lowest priority under hard ceilings. If memory runs out, the kernel picks the su2qc job first. It cannot outlive the session that started it. On Perlmutter, the common failure modes resubmit themselves, and the laptop can see whether the worker is alive.

### Bugs found and fixed while doing this
1. The runner's ledger recorded the *next* attempt's memory limit for the current attempt, because the heal step raised it before the entry was written. It now records the limit actually used, and the test checks it.
2. A cgroup memory limit through `systemd-run --user --scope` is accepted but **not enforced** when the memory controller is not delegated to the user session. The runner now uses the cgroup only when `memory` is listed in the user manager's `cgroup.controllers`, and otherwise falls back to the address-space limit.
3. A job could outlive a killed runner (it runs in its own session, and the lock disappears with the runner), so two su2qc jobs could then overlap. The job now receives a parent-death signal.
4. Prompt 009 originally compared `pip check` with a baseline taken *after* the damage, which already contained the `cuda-bindings` conflict. The goal is now stated as "no conflict involving the CUDA/cuQuantum/CUDA-Q/PyTorch stack or the installed list". Upgrades of existing packages are restored, not deleted.
5. `jobs/INDEX.md` still named the removed desktop worker (caught by `check_artifacts`); the indexes were regenerated.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 722 / – / – (`reports/003`) | 812 / 1,574 / 59 (`evidence/graph/stats.json`) |
| new hubs | – | `localrun.py` (33 edges) |
| `graphify affected` checks | – | `jobs.retry_resources`, `worker.poll_slurm` → `tests/test_jobs.py`; `localrun.*`, `scripts/run.py` → `tests/test_localrun.py`; `compute.py` → `tests/test_compute.py` |

## Problems and assumptions
- **Not yet run on the real laptop or the real Perlmutter.**
  - On the laptop, `prompts/009` reports which memory limiter is active and runs all tests through the runner.
  - On Perlmutter, setup step 4 of `docs/PERLMUTTER.md` runs the first job.
- **Laptop CPU.** The i7-8750H (6 cores / 12 threads) is taken from Digonto's recorded hardware; the runner probes the real count at run time, so a different CPU only changes the thresholds.
- **Admission is conservative.** With other sessions busy (a load above 8 on 12 threads, or less than about 20 GB available), light jobs wait up to 20 minutes and then go to Perlmutter. That costs latency (15–30 minutes per queued job), never stability. A command that cannot be queued (for example, ad-hoc Python) is not run; exit code 2.
- **Prompt 009 cannot know whether a pip-installed PyTorch was used in `coding` before the bad install.** It removes the CUDA-13 build, which cannot use the GTX 1060 anyway, and lists the command to reinstall a CPU build or a Pascal-capable CUDA 12.x build (checked with `torch.cuda.get_arch_list()` containing `sm_61`).
- **Safety rules in prompt 009:**
  - it touches only `coding` and creates only `su2qc-jepa`;
  - no `sudo`, no environment removal, and no shell start-up file changes;
  - pip only by absolute path;
  - an environment with running processes is not touched, and other processes are never killed;
  - backup first, with a rollback on regression;
  - no `git push` and no `gh`.
- `reports/000`–`003` and `decisions/002`–`003` describe earlier states and are append-only.

## Next action
On the laptop: `cd su2qc-jepa && claude --dangerously-skip-permissions`, then *"Read prompts/009_laptop-environment-repair-and-setup.md and execute it."*; after that, `prompts/000`.
