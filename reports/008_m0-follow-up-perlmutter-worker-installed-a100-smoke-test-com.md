---
id: reports/008
title: 'M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED'
series: reports
created_utc: '2026-10-02T23:32:12Z'
author: claude-code
milestone: M0
status: done
supersedes: null
superseded_by: null
---

# M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED

**Milestone:** M0 (one-time Perlmutter setup, `docs/PERLMUTTER.md`) · **Prompt:** prompts/000 (same session; continued on Digonto's request) · **Commit range:** `74fbcc7^..` (from `73a1ae5` to this report)

## What was asked
After M0 (`reports/007`), Digonto asked whether Perlmutter had to be set up now. Answer: not for M1, but before `prompts/002`. Digonto then chose to set it up immediately and asked for the steps. Digonto ran every command on Perlmutter; this session read the pasted output, fixed what broke, set the account and ran the end-to-end test.

## Actions taken
1. Gave the steps from `docs/PERLMUTTER.md`. Digonto cloned the repository to `~/su2qc-setup` and ran `setup_env_perlmutter.sh m4135`. The environment was created in `/global/common/software/m4135/su2qc-jepa-env`. The script stopped at its final `pytest` with 2 failures (below), after everything was installed.
2. **Account.** Digonto's existing scrontab entries use `m4135_g`, the project's GPU account, while the software folder is `/global/common/software/m4135`. The installers used one name for both. Commit `73a1ae5`: both installers now use `${ACCOUNT%_g}` for the folder, with `SU2QC_ENV_PREFIX` as an override. `sbatch --test-only -C gpu -q shared --gpus 1` accepted both `m4135` and `m4135_g`; Digonto chose `m4135_g`.
3. **Test failure `test_worker_slurm_mode_resubmits_after_timeout`.** The fake job's log (`/tmp/pytest-of-digonto/pytest-3/.../wk/runs/000.log` on login34) said `EnvironmentLocationNotFound: Not a conda environment: /none`. So the real `conda` ran instead of the test's stand-in. On Perlmutter, the exported shell functions (`BASH_FUNC_module%%`, `BASH_FUNC_conda%%`, …) and `BASH_ENV` re-define `module` and `conda` inside every `bash`, and these shadow the stand-ins on `PATH`. My first guess, exported functions alone, was wrong: removing them by hand did not fix it. Commit `2b0ea41`: the test drops `BASH_FUNC_*`, `BASH_ENV` and `ENV` from the stand-in job's environment. The assertions are unchanged. I reproduced the failure on the laptop with a `BASH_ENV` file defining a failing `conda`: without the fix the test fails with the same log as on Perlmutter; with the fix it passes. On Perlmutter, after `git pull`: `1 passed`.
4. Digonto ran `install_perlmutter.sh m4135_g` and added the deploy key (with write access). `ssh -T git@github-su2qc` greeted `digonto10602/su2qc-jepa`. A manual `tick.sh` created the `results` branch, with heartbeat 2026-10-02T23:11:26Z. `scrontab_merge.sh add` backed up the old table (`~/.scrontab-backup-20261002T231146Z.txt`, 16 lines) and kept `skqd-ci-poll` and `trotter-ci-poll` unchanged.
5. Commit `80efb3d`: `configs/compute.yaml` `perlmutter.account: "m4135_g"` (the value Digonto installed with). `STATE.json` `compute.perlmutter`: `worker_installed: true`, account, env prefix, worker folder.
6. `python scripts/jobs/enqueue.py check "worker smoke test" --time 00:10:00 --step "python scripts/env_check.py" --output evidence/ENV.json --push` → `jobs/000`, commit `273f5cb`.
7. Waited with `scripts/jobs/status.py`, then ran `python scripts/jobs/fetch.py 000`.

## Results and what they mean
| check | result | evidence |
|---|---|---|
| worker picked up the job | SUBMITTED at 2026-10-02T23:15:41Z, Slurm id 59236367 | `evidence/jobs/000/status.json` |
| job ran | on `nid002212` (a GPU compute node), start 23:21:05Z, COMPLETED at 23:30:30Z (status written at the next tick) | `evidence/jobs/000/log.txt` |
| cost | 0.011 h elapsed, **0.003 node-hours** of the 50 node-hour budget | `evidence/jobs/000/status.json` |
| GPU | `NVIDIA A100-SXM4-40GB`, `torch 2.14.1+cu130`, `"torch_device_used": "cuda"` | `evidence/jobs/000/ENV.perlmutter.json` |
| code version | `git_head 80efb3d`, `git_dirty false`, graphify 0.9.74 | same |

The whole path works: the laptop queues a job, GitHub carries it, the scrontab worker submits it with Slurm on `m4135_g`, it runs on an A100, and the result comes back through the `results` branch. `docs/PERLMUTTER.md`'s smoke-test criterion (an A100 and `cuda`) is met. The `--test-only` estimate of a start around 2026-10-04 03:30 UTC was far too pessimistic: the job started about 5.5 min after submission.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 842 / 1615 / 64 (`reports/007`) | see `evidence/graph/stats.json` after the final `chore(graph)` commit (markdown reports add nodes) |
| new or changed hubs | – | none |
| `graphify affected` checks run | `install_perlmutter.sh`: no dependants | `test_jobs.py` and `test_compute.py` re-run after each change |

## Problems and assumptions
1. **`fetch.py` overwrote the laptop's `evidence/ENV.json`.** The smoke job's declared output has the same path as the laptop's committed environment record, and `fetch.py` copies outputs straight into the working tree. I moved the Perlmutter copy to `evidence/jobs/000/ENV.perlmutter.json` and restored the laptop file with `git checkout`. Suggestion for the doc (not done): give the smoke test an output path that does not collide, or have `fetch.py` refuse to overwrite tracked files.
2. **No GPU Qiskit simulator on Perlmutter.** `aer_devices` is `["CPU"]`. `setup_env_perlmutter.sh` installs `qiskit-aer-gpu` (0.15.1, the newest wheel pip found), and then the package's own dependency `qiskit-aer` 0.17.2 overwrites the same `qiskit_aer` module. In addition, 0.15.1 predates Qiskit 2.x. `TwinRunner` defaults to `device="CPU"`, so nothing breaks; any `--device GPU` run would fail. Suggestion: drop `qiskit-aer-gpu` from the setup script, or plan the twin runs as CPU.
3. **`test_run_py_retries_after_memory_limit` fails on Perlmutter login nodes.** It is expected: it tests the laptop runner's admission rule, and the login node had a load of 378 on 256 cores. The worker never uses the laptop runner. The test was not changed.
4. `setup_env_perlmutter.sh` uses `set -e`, so the test failures stopped it before its last `echo`. The environment was nevertheless complete; this was checked with `env_check.py` on the login node and then on the compute node.
5. `qiskit_ibm_runtime` and `mthree` are absent on Perlmutter by design: the setup installs `[ml,dev]`, and IBM work stays on the laptop.

## Next action
`prompts/001_physics-and-data.md` (M1, gate J0) — all of M1 runs on the laptop (`run.py --dry`: datasets 2.0 / 0.5 / 0.3 min estimated).
