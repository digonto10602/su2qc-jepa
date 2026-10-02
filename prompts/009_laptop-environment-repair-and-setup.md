---
id: prompts/009
title: Laptop environment repair and setup
series: prompts
created_utc: '2026-10-02T20:23:20Z'
author: planner
milestone: M0
status: active
supersedes: null
superseded_by: null
---

# Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)

**How to start this session (Digonto):** unzip the starter package, `cd su2qc-jepa`, then `claude --dangerously-skip-permissions` and say: *"Read prompts/009_laptop-environment-repair-and-setup.md and execute it."* You run without permission prompts, so the safety rules below are absolute. This session runs before the repository exists on GitHub. Do not run `git push`, `gh`, or `scripts/bootstrap_repo.sh`.

## Context

- **Machine:** the laptop — Dell G7 7588, Omarchy (an Arch-based Linux), 64 GB RAM, 6-core i7-8750H, GTX 1060 Max-Q (Pascal, compute capability 6.1). Conda/mamba lives under the user's home (find it with `conda info --base`). Other Claude Code sessions may be running on this laptop right now, some of them using the `coding` environment. Your work must never disturb them.
- **What broke.** `pip install -e ".[ml,ibm,dev]"` for the su2qc-jepa package was run inside the `coding` environment. It printed:

  ```
  ERROR: pip's dependency resolver ... cuquantum-python-cu12 26.3.2 requires cuda-bindings<13.0.0,>=12.9.4, but you have cuda-bindings 13.4.3 which is incompatible.
  Successfully installed cloudpickle-3.1.2 cuda-bindings-13.4.3 cuda-toolkit-13.0.3.0 filelock-4.0.9 fsspec-2026.9.0 graphifyy-0.9.74
  joblib-1.6.0 mthree-3.0.0 narwhals-2.26.0 networkx-3.7 nvidia-cublas-13.1.1.3 nvidia-cuda-cupti-13.0.85 nvidia-cuda-nvrtc-13.0.88
  nvidia-cuda-runtime-13.0.96 nvidia-cudnn-cu13-9.24.0.43 nvidia-cufft-12.0.0.61 nvidia-cufile-1.15.1.6 nvidia-curand-10.4.0.35
  nvidia-cusolver-12.0.4.66 nvidia-cusparse-12.6.3.3 nvidia-cusparselt-cu13-0.8.1 nvidia-nccl-cu13-2.30.7 nvidia-nvjitlink-13.4.92
  nvidia-nvshmem-cu13-3.4.5 nvidia-nvtx-13.0.85 rapidfuzz-3.14.6 runningman-2.3.0 scikit-learn-1.9.1 su2qc-jepa-0.1.0
  threadpoolctl-3.7.0 torch-2.14.1 tree-sitter-0.25.2 (+ ~25 tree-sitter-<language> packages) triton-3.8.0
  ```

  So the install (a) replaced `cuda-bindings` 12.x by 13.4.3, breaking `cuquantum-python-cu12`; (b) added a PyTorch built for CUDA 13 with about 20 CUDA-13 runtime packages (several GB). CUDA 13 has no support for the Pascal GTX 1060, so that PyTorch cannot use the laptop's GPU anyway. (c) It added the su2qc-jepa package itself, Graphify and some generic libraries.
- **Goal.** `coding` works exactly as before the install: cuQuantum, CUDA-Q, Qiskit/Aer and everything else importable, and `pip check` free of conflicts caused by the bad install. A new, separate environment `su2qc-jepa` holds this project, with CPU-only PyTorch. The project never uses the laptop GPU; GPU work goes to Perlmutter (`decisions/004`).

## Absolute safety rules (you have no permission prompts)

1. Touch only two environments: modify `coding`; create `su2qc-jepa`. Never modify `base` or any other environment. Never run `conda env remove`, `conda remove --all`, or delete an environment directory.
2. Never use `sudo`, never change system packages, NVIDIA drivers, shell start-up files (`~/.bashrc`, `~/.zshrc`, …) or other projects' files.
3. Call pip only as `<env-prefix>/bin/python -m pip ...` with the absolute path. Never use a bare `pip` or `python`, which could resolve to another environment. Print the resolved path before every install or uninstall.
4. **Never pull packages out from under a running program.** Before changing `coding`, list processes using it: `pgrep -af "<coding-prefix>/bin/python"` and `pgrep -af "<coding-prefix>/"`. If any are running (another Claude session's job, a notebook, a server), do not touch `coding`. Do phase C (the new environment) first, then re-check every 10 minutes for up to 2 hours. If still busy, stop and write the exact remaining commands into the report for Digonto. Never kill or signal processes you did not start.
5. Back up before changing anything (phase A). Every change must be reversible from the backup.
6. Run installs at low priority (`nice -n 10`), one at a time. Never start background jobs.
7. Remove a package from `coding` only if all three hold:
   - it is in the "Successfully installed" list above;
   - it belongs to the CUDA-13/PyTorch stack or is specific to this project (`su2qc-jepa`, `graphifyy`, `tree-sitter*`, `mthree`, `runningman`);
   - no other installed distribution requires it (check the reverse dependencies, see B2).

   Generic libraries from the list (`scikit-learn`, `networkx`, `joblib`, `threadpoolctl`, `fsspec`, `filelock`, `cloudpickle`, `narwhals`, `rapidfuzz`) stay unless `pip check` shows they now conflict with something. In that case install the version that something requires.
8. If any step makes the import test or `pip check` worse than the step before, undo that step at once from the backup (`python -m pip install <pkg>==<version from the freeze>`) and record it.

## Phase A — inventory and backup (no changes)

1. `conda info --base`; `conda env list`; resolve `CODING=<prefix of coding>`; `$CODING/bin/python -V`.
2. Make `~/env-repair-<YYYYMMDD-HHMM>/` and save into it:
   - `conda list -p $CODING --explicit` → `coding-conda-explicit.txt`
   - `conda env export -p $CODING` → `coding-env.yml`
   - `$CODING/bin/python -m pip freeze` → `coding-pip-freeze-before.txt`
   - `$CODING/bin/python -m pip list --format=json` → `coding-pip-list-before.json`
   - `$CODING/bin/python -m pip check` → `coding-pip-check-before.txt`
   - a copy of `$CODING/conda-meta/history`
   - `du -sh $CODING`
   - `nvidia-smi` (driver and CUDA versions), `free -g`, `uptime`.
3. Write `~/env-repair-<stamp>/import_test.py`. It tries each of these and records version, `ok` or the exact error: `numpy`, `scipy`, `matplotlib`, `pandas`, `qiskit`, `qiskit_aer` (plus `AerSimulator().available_devices()`), `qiskit_ibm_runtime`, `cuquantum` (and `cuquantum.custatevec`, `cuquantum.cutensornet`), `cuda.bindings`, `cudaq` (with `cudaq.get_target()`), `cupy`, `torch` (with `torch.version.cuda` and `torch.cuda.is_available()`), and `pennylane`, `jax`, `tensorflow` if installed. Run it with `$CODING/bin/python` → `import-before.json`.
4. Find which distributions in `coding` were conda-installed (`conda list -p $CODING`, channel not `pypi`) and which were pip-installed. Note which names in the list above already existed in conda's records: pip may have overwritten a conda-managed package, and that is restored with conda, not pip.
5. **What did the bad install add, and what did it replace?** pip's list mixes new packages with upgrades, and the freeze you just saved was taken *after* the bad install, so it does not hold the old versions. For every name in the list, record in `changed-by-install.md`:
   - **replaced conda package:** `conda-meta/<name>-<version>-*.json` exists with a different version → the old version is known; restore it with conda (B4);
   - **replaced pip package:** the dist-info folder's modification time equals the bad install's (they all share it) and some installed distribution requires a version range that the new version breaks (`pip check`) → old version unknown; restore a version inside the required range;
   - **new:** neither of the above.
   
   This table decides what B3 may remove (only **new** packages) and what B4 must restore.

## Phase B — repair `coding` (only after rule 4 allows it)

1. Process check (rule 4). If busy, go to phase C and come back.
2. **Reverse dependencies.** Use a short `importlib.metadata` script run by `$CODING/bin/python` to list, for each candidate package (the CUDA-13 stack, `torch`, `triton`, `cuda-toolkit`, `cuda-bindings`, the `nvidia-*` packages without a `-cu12` suffix, `su2qc-jepa`, `graphifyy`, `tree-sitter*`, `mthree`, `runningman`), every installed distribution whose `Requires-Dist` names it. Save the table → `reverse-deps.md`.
3. **Uninstall in this order**, each with `nice -n 10 $CODING/bin/python -m pip uninstall -y ...`, re-running the import test and `pip check` after each group:
   1. `su2qc-jepa`;
   2. `torch triton`, unless step 2 shows a pre-existing package requires `torch`; then keep a working `torch` (step 5). If A5 shows `torch` replaced a conda `pytorch`, restore that with conda instead. Since nobody can tell whether a pip-installed `torch` was used in `coding` before, list in the report the command to get one back: the CPU build (step 5), or, for the GTX 1060, an older CUDA 12.x build whose `torch.cuda.get_arch_list()` contains `sm_61` (check it; do not install it yourself);
   3. the CUDA-13 runtime packages that A5 marks **new**: `cuda-toolkit`, `nvidia-cublas`, `nvidia-cuda-cupti`, `nvidia-cuda-nvrtc`, `nvidia-cuda-runtime`, `nvidia-cudnn-cu13`, `nvidia-cufft`, `nvidia-cufile`, `nvidia-curand`, `nvidia-cusolver`, `nvidia-cusparse`, `nvidia-cusparselt-cu13`, `nvidia-nccl-cu13`, `nvidia-nvjitlink`, `nvidia-nvshmem-cu13`, `nvidia-nvtx`. Only exact names without a `-cu12` suffix, and only if step 2 shows nothing else needs them. Never touch any `*-cu12` package: cuQuantum and CUDA-Q use those;
   4. `graphifyy`, the `tree-sitter*` packages, `mthree`, `runningman` (project-specific; the new environment gets its own copies).
4. **Restore what was replaced.**
   - `cuda-bindings`: if the conda records show the pre-install version, reinstall exactly that version; otherwise `nice -n 10 $CODING/bin/python -m pip install "cuda-bindings>=12.9.4,<13"`. Also fix any `cuda-python` mismatch.
   - Each **replaced conda package** from A5: `nice -n 10 conda install -p $CODING --no-deps --force-reinstall "<name>=<old version>"` (print the plan first; abort it if conda proposes changing anything else).
   - Each **replaced pip package**: `nice -n 10 $CODING/bin/python -m pip install "<name><range required by its dependant>"`.
   - Repeat until `pip check` shows **no conflict that involves** `cuda-bindings`, `cuda-python`, `cuquantum*`, `cudaq`/`cuda-quantum*`, `torch`, or any name in the list above. Any other conflict must already be in `coding-pip-check-before.txt` (it predates the bad install and is not yours to fix; list it in the report).
5. If a pre-existing package requires `torch`: install the CPU build, `nice -n 10 $CODING/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu`. It works on any hardware and brings no CUDA libraries. Check that `pip list` shows no new `nvidia-*` packages.
6. **Verify.**
   - Re-run the import test → `import-after.json`.
   - `pip check` → `coding-pip-check-after.txt`.
   - `du -sh $CODING`, to report the space freed.
   - Run a tiny cuQuantum-dependent check if one is cheap; otherwise the import test plus the `cuda.bindings` version is enough.
   - If anything that worked before now fails, roll back that step (rule 8) and report.

## Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment)

1. From the repository folder: `nice -n 10 mamba env create -f environment.yml` (use `conda` if `mamba` is missing). It creates `su2qc-jepa` with Python 3.12 and the pip packages in the file; PyTorch is deliberately not in it. Resolve `SU2=<prefix of su2qc-jepa>`.
2. `nice -n 10 $SU2/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu` (CPU build first).
3. `nice -n 10 $SU2/bin/python -m pip install -e ".[ml,ibm,dev]"`. Then check that `torch.__version__` ends in `+cpu`, that `$SU2/bin/python -m pip list` contains no `nvidia-*` and no `cuda-bindings`, and that `$SU2/bin/graphify --help` works.
4. Verify with the project's own tools, always through the laptop runner:
   - `$SU2/bin/python scripts/env_check.py`: expect `"torch_device_used": "cpu"`, `qiskit`, `qiskit_aer`, `graphify` present;
   - `$SU2/bin/python scripts/run.py -- $SU2/bin/python -m pytest -q`: all tests pass (`tests/test_localrun.py` includes a real run that hits the memory ceiling and retries);
   - `$SU2/bin/python -c "from su2qc_jepa.localrun import _systemd_scope_ok as f; print('cgroup' if f() else 'address-space')"`: report which memory limiter the runner uses here (`cgroup` needs the systemd user manager with the memory controller delegated; otherwise the runner falls back to an address-space limit — both work, the cgroup one is exact);
   - `$SU2/bin/python scripts/run.py --dry -- python scripts/train_jepa.py --data data/main --name x --epochs 200 --seeds 5 --masked`: expect `"heavy": true`, i.e. sent to Perlmutter;
   - `$SU2/bin/python scripts/check_artifacts.py`.
5. Do not add `conda activate su2qc-jepa` to any shell start-up file. Digonto activates it per terminal.

## Phase D — report

1. Create the numbered report with the new environment: `$SU2/bin/python scripts/new_artifact.py reports "Laptop environments: coding repaired, su2qc-jepa created" --milestone M0`. Fill it in the template's order:
   - **What was asked.**
   - **Actions taken:** every command that changed something, in order.
   - **Results and what they mean:**
     - a before/after import table for `coding`;
     - `pip check` before and after;
     - disk freed;
     - the `su2qc-jepa` verification results;
     - what the GTX 1060 can and cannot do (`torch.cuda` unusable with current wheels; whether `qiskit_aer` reports a GPU device).
   - **Code graph:** "not applicable — no code changed".
   - **Problems and assumptions:** anything skipped because of rule 4 or rule 7, with the exact commands left for Digonto.
   - **Next action:** `prompts/000`.

   Set the report's `status: done`. Copy the `~/env-repair-<stamp>/` path into it. Update `STATE.json`: `compute.laptop.laptop_env_ready: true`, `milestones.M-env.status: "DONE"` and `milestones.M-env.report` (the report id).
2. End by printing a short summary: `coding` status (repaired / partly repaired / untouched because busy), `su2qc-jepa` status, tests passed, space freed, and anything Digonto must do by hand.

## Definition of done

- In `coding`: `cuquantum` and `cuda.bindings` 12.x import, no CUDA-13 packages remain, `pip check` shows no conflict involving the CUDA/cuQuantum/CUDA-Q/PyTorch stack or the listed packages, and every module that imported before still imports.
- `su2qc-jepa` exists with CPU PyTorch and no NVIDIA packages; all tests pass through `scripts/run.py`; `env_check` reports `cpu`.
- The backup folder exists, and the numbered report is written.
