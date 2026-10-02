---
id: reports/006
title: 'Laptop environments: coding repaired, su2qc-jepa created'
series: reports
created_utc: '2026-10-02T21:41:10Z'
author: claude-code
milestone: M0
status: done
supersedes: null
superseded_by: null
---

# Laptop environments: coding repaired, su2qc-jepa created

**Milestone:** M0 (environment step `M-env`) · **Prompt:** prompts/009 · **Commit range:** none — the folder is not a git repository yet (prompts/009 runs before the repository exists) · **Backup and evidence folder:** `~/env-repair-20261002-1507/`

## What was asked
Digonto asked for `prompts/009_laptop-environment-repair-and-setup.md` to be carried out, with phases A (inventory and backup) and C (create the `su2qc-jepa` environment) already done earlier the same day; their records are in `~/env-repair-20261002-1507/`. So this session did phase B (repair the conda environment `coding`, damaged when `pip install -e ".[ml,ibm,dev]"` was run inside it), re-ran the phase C checks, and wrote this report (phase D).

## Actions taken
Phase A (earlier, records only): `coding-conda-explicit.txt`, `coding-env.yml`, `coding-pip-freeze-before.txt`, `coding-pip-list-before.json`, `coding-pip-check-before.txt`, `coding-conda-history.txt`, `du-before.txt`, `system-before.txt`, `import_test.py` → `import-before.json`, `changed-by-install.md` (A5), `reverse-deps.md` (B2).

Phase C (earlier; logs in the backup folder): `nice -n 10 conda env create -f environment.yml` (`su2-env-create.log`); `nice -n 10 $SU2/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu` (`su2-torch-cpu.log`, torch 2.14.1+cpu); `nice -n 10 $SU2/bin/python -m pip install -e ".[ml,ibm,dev]"` (`su2-pip-install-e.log`). Here `SU2=/home/digimonk/anaconda3/envs/su2qc-jepa`.

Phase B (this session), with `CODING=/home/digimonk/anaconda3/envs/coding`. Every pip call used `$CODING/bin/python -m pip`, and that path was printed before each change.
1. Rule 4 check: `pgrep -af "$CODING/bin/python"` and `pgrep -af "$CODING/"` were both empty (re-checked before every group), so `coding` was idle.
2. Guard (my addition): `record_overlap.py` checked whether any file listed in the `RECORD` (pip's list of installed files) of a package to be removed also belongs to a package that stays, since pip would delete that shared file. Result: `shared files: 0` (`record-overlap.txt`).
3. B3, each group followed by `step_check.sh` (import test plus `pip check`, compared with `import-before.json`):
   1. `nice -n 10 $CODING/bin/python -m pip uninstall -y su2qc-jepa` (`b3-1-uninstall.log`);
   2. `… uninstall -y torch triton` (`b3-2-uninstall.log`). After step 1, nothing required `torch`;
   3. `… uninstall -y cuda-toolkit nvidia-cublas nvidia-cuda-cupti nvidia-cuda-nvrtc nvidia-cuda-runtime nvidia-cudnn-cu13 nvidia-cufft nvidia-cufile nvidia-curand nvidia-cusolver nvidia-cusparse nvidia-cusparselt-cu13 nvidia-nccl-cu13 nvidia-nvjitlink nvidia-nvshmem-cu13 nvidia-nvtx` (16 packages, `b3-3-uninstall.log`). Their only remaining dependants were optional extras that are not installed (`nvmath-python[cu13]`, `cuda-bindings[all]`). No `*-cu12` package was touched;
   4. `… uninstall -y graphifyy mthree runningman tree-sitter` plus the 25 `tree-sitter-<language>` packages (29 removed, `b3-4-uninstall.log`).
4. B4: `nice -n 10 $CODING/bin/python -m pip install --dry-run "cuda-bindings>=12.9.4,<13"` showed it would change only `cuda-bindings`. Then `nice -n 10 $CODING/bin/python -m pip install "cuda-bindings>=12.9.4,<13"` replaced 13.4.3 with **12.9.9** (`b4-cuda-bindings.log`). No conda restore was needed: A5 found that conda had never managed any of the affected packages. `cuda-python` is not installed, so there was no `cuda-python` mismatch to fix.
5. B5 skipped: no package that predates the bad install requires `torch`.
6. B6 verification: `import-after.json`, `coding-pip-check-after.txt`, `coding-pip-freeze-after.txt`, `du-after.txt`, `smoke_test.py` → `smoke-test-after.txt`.

Phase C re-check (this session): `su2-checks.txt`, `su2-env-check.txt` (writes `evidence/ENV.json`), `su2-pytest-2.log`, `su2-pytest-3.log`, `su2-dry-run.txt`, `su2-check-artifacts.txt`. `STATE.json` updated (see Next action). No source file was changed.

## Results and what they mean

### `coding`: imports before and after (`import-before.json` → `import-after.json`)
| module | before (after the bad install) | after the repair |
|---|---|---|
| numpy / scipy / matplotlib / pandas | ok 2.5.2 / 1.18.0 / 3.11.1 / 3.0.5 | ok, same versions |
| qiskit / qiskit_aer / qiskit_ibm_runtime | ok 2.5.2 / 0.17.2 / 0.49.0 | ok, same |
| `AerSimulator().available_devices()` | `['CPU']` | `['CPU']` |
| cuquantum (+ `bindings.custatevec`, `bindings.cutensornet`, `tensornet`) | ok 26.3.2 | ok 26.3.2 |
| `cuquantum.custatevec`, `cuquantum.cutensornet` | ModuleNotFoundError | ModuleNotFoundError (unchanged; since cuquantum-python 24 these modules live under `cuquantum.bindings`, which imports) |
| cuda.bindings | ok **13.4.3** (breaks cuQuantum's requirement) | ok **12.9.9** |
| cudaq | ok 0.15.1, target `qpp-cpu` | ok, same |
| cupy | ok 13.6.0 | ok 13.6.0 |
| torch | ok 2.14.1+cu130 (added by the bad install) | not installed (removed on purpose) |
| pennylane / jax / tensorflow | not installed | not installed |

Every module that imported before the bad install still imports. The only module that went from ok to missing is `torch`, which the bad install had added (`changed-by-install.md`).

**Smoke test** (`smoke-test-after.txt`): `cuInit` = `CUDA_SUCCESS`; 1 device, compute capability 6.1 (Pascal); `custatevec` library version 11301 and `cutensornet` 21202 load; a CUDA‑Q Bell-state circuit on `qpp-cpu` with 1000 shots gave `{'00': 499, '11': 501}` (the ideal outcome is 50/50 between `00` and `11`, with a binomial standard deviation of about $\sqrt{1000\cdot 0.25}\approx 16$ counts); `cupy` summed `[0,1,2,3]` on the GPU to 6.0.

### `pip check`
- Before: `cuquantum-python-cu12 26.3.2 has requirement cuda-bindings<13.0.0,>=12.9.4, but you have cuda-bindings 13.4.3.` (`coding-pip-check-before.txt`)
- After: `No broken requirements found.` (`coding-pip-check-after.txt`)

No CUDA‑13 package, `torch`, `triton` or `cuda-toolkit` remains (`pip list` filter in this session).

### Disk
`du -sh $CODING`: 14G before (`du-before.txt`) → 8.3G after (`du-after.txt`). About 5–6 GiB were freed; `du -sh` rounds the "before" figure, hence the ±0.5 GiB range.

### `su2qc-jepa` environment
| check | result | evidence |
|---|---|---|
| Python, torch | 3.12.14; `torch 2.14.1+cpu`, `torch.version.cuda = None` | `su2-checks.txt` |
| no `nvidia-*`, no `cuda-bindings` | none | `su2-checks.txt` |
| `pip check` | No broken requirements found | `su2-checks.txt` |
| `$SU2/bin/graphify --help` | works; graphifyy 0.9.74 (the pinned version) | `su2-checks.txt` |
| `scripts/env_check.py` | `"torch_device_used": "cpu"`, `cuda: false`, qiskit 2.5.2, qiskit_aer 0.17.2 (`aer_devices: ["CPU"]`), graphify 0.9.74 | `evidence/ENV.json`, `su2-env-check.txt` |
| test suite via `scripts/run.py` | **47 passed**, exit 0, 59 s, peak 0.77 GB, limiter `cgroup` (with `$SU2/bin` first on `PATH`; see Problems) | `su2-pytest-3.log`, `.local_runs/logs/20261002T213954Z-9bcd5b_pytest_a1.log` |
| memory limiter | `cgroup`: the systemd user manager has the memory controller, so the runner's memory ceiling is exact | `su2-checks.txt` |
| `run.py --dry -- python scripts/train_jepa.py … --epochs 200 --seeds 5 --masked` | `"heavy": true`, `est_minutes: 1058.0`, so it goes to Perlmutter | `su2-dry-run.txt` |
| `scripts/check_artifacts.py` | `artifact conventions: OK` | `su2-check-artifacts.txt` |
| environment size | 1.8G | `su2-checks.txt` |

### The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)
- **PyTorch:** current wheels cannot use it. The CUDA‑13 build that the bad install brought listed `sm_75 … sm_120` and no `sm_61` (`import-before.json`). The project uses CPU PyTorch on the laptop by design (`decisions/004`).
- **Qiskit Aer:** reports only `CPU`. The installed `qiskit-aer` is a CPU build.
- **What does work on it, in `coding`:** the CUDA driver through `cuda.bindings` 12.9.9, CuPy array operations, and loading the cuQuantum libraries. I did not check whether cuStateVec or cuTensorNet kernels run on compute capability 6.1. NVIDIA's documentation lists a higher minimum for cuQuantum, so do not count on them.

## Code graph
Not applicable: no code changed. The committed graph (829 nodes, 1600 edges; `evidence/ENV.json`) matches a fresh rebuild with graphifyy 0.9.74, because `test_committed_graph_is_fresh` passed.

## Problems and assumptions
1. **`graphify` on `PATH` changed when `coding` was cleaned.** The first test run this session (`su2-pytest-2.log`) failed `tests/test_repo_conventions.py::test_committed_graph_is_fresh` with "committed code graph is stale: 59 nodes only in committed". Cause: the shell had `coding` activated. Before the repair, `PATH` found `coding/bin/graphify` (0.9.74, installed by the bad install). After the repair it finds `~/.local/bin/graphify`, which is **0.9.53** (a separate install under `~/.local/share/graphify/venv`, outside the two environments this prompt allows me to touch). Different versions build different graphs. With `$SU2/bin` first on `PATH` (i.e. `conda activate su2qc-jepa`), the test passes; nothing in the test or the graph was changed. **For Digonto:** always `conda activate su2qc-jepa` before working in this repository. Optionally, bring the user-level command up to the pinned version: `uv tool install --force graphifyy==0.9.74` (or however it was installed; this also clears graphify's own "package is older than skill" warning).
2. **Another session wrote to this repository during this one.** At 15:18 local time it added `reports/005`, `tests/test_scrontab_merge.py`, changed `scripts/worker/*`, `README.md`, `docs/PERLMUTTER.md` and rebuilt the graph. I did not touch those files. The 47 tests include its new test.
3. **Old `cuda-bindings` version unknown.** No conda record or install transcript held the pre-install version (`changed-by-install.md`). I installed the newest version that satisfies `cuquantum-python-cu12` (`>=12.9.4,<13` → 12.9.9). If the old one was a different 12.9.x, no requirement distinguishes them.
4. **Generic libraries kept** (rule 7): scikit-learn 1.9.1, networkx 3.7, joblib 1.6.0, threadpoolctl 3.7.0, fsspec 2026.9.0, filelock 4.0.9, cloudpickle 3.1.2, narwhals 2.26.0, rapidfuzz 3.14.6. None conflicts with anything. Whether each one was newly installed or upgraded cannot be told; their old versions, if any, are unknown.
5. **Leftover empty folder:** `coding/lib/python3.12/site-packages/nvidia/cu13` contains 2 empty directories (0 files, 0 bytes). It is harmless; to tidy it up: `find /home/digimonk/anaconda3/envs/coding/lib/python3.12/site-packages/nvidia/cu13 -depth -type d -empty -delete`.
6. **Getting `torch` back into `coding`, if it was ever wanted there** (no package needs it; I did not install either):
   - CPU build: `nice -n 10 /home/digimonk/anaconda3/envs/coding/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu`;
   - GPU build for the GTX 1060: PyTorch's CUDA 12.8 and 12.9 wheels dropped Pascal (`sm_60`/`sm_61`). The CUDA 12.6 index (`https://download.pytorch.org/whl/cu126`) is the place to look, but **I have not verified** that a current cu126 wheel still contains `sm_61`. Run with `--dry-run` first: a cu126 torch pins its own `nvidia-*-cu12` versions and could downgrade the ones cuQuantum and CUDA‑Q use. After installing, check `python -c "import torch; print(torch.cuda.get_arch_list())"` lists `sm_61`; if not, uninstall it.
7. The start-of-session steps that need git (`git_head`, `graph_update.sh --check` against a commit, commits, `git log`) do not apply: the folder is not a git repository yet, by design of prompts/009. No commit was made.

## Next action
`prompts/000` (bootstrap). `STATE.json`: `compute.laptop.laptop_env_ready = true`, `milestones.M-env.status = "DONE"`, `milestones.M-env.report = "reports/006"`.
