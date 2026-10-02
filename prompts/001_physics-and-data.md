---
id: prompts/001
title: M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M1
status: active
supersedes: null
superseded_by: null
---

# M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)

**Session protocol:** `CLAUDE.md` §2 — start with `scripts/env_check.py` and `bash scripts/graph_update.sh --check` (read the first screen of `graphify-out/GRAPH_REPORT.md`); use `graphify query/explain/affected` before broad searches; end with tests, the gate, `bash scripts/graph_update.sh`, a numbered session report (`python scripts/new_artifact.py reports "M1: <result>" --milestone M1`), `scripts/check_artifacts.py` OK, `STATE.json`, and a final `chore(graph):` commit. Any new prompt you write for a later session goes into `prompts/` via `scripts/new_artifact.py prompts ...`; every figure via `scripts/new_artifact.py figures ... --ext .png`.

**Read first:** `CLAUDE.md`, `plans/001_gauge-jepa-p-v2.md` §3, §4, §6, §10 (W1), `docs/PHYSICS.md`.

## Part A — cross-check against the project's verified `su2qc` code
The starter package's physics core ("route C") must agree with the SU2ZX `su2qc` code (routes A/B) before any data is generated.
1. Locate the project's code: ask Digonto for the path or clone the SU2ZX repository (read-only). Map it with Graphify *outside* this repository's graph: `graphify update <path-to-SU2ZX>` writes `<path-to-SU2ZX>/graphify-out/`; then `graphify query "where is the Hamiltonian built" --graph <path-to-SU2ZX>/graphify-out/graph.json` and `graphify explain "run_counts" --graph ...` to find the builders, conventions and the twin seeding code before reading files. Do not commit that graph here. If it is not available, record that and use the published numbers in `docs/PHYSICS.md` as the cross-check (fingerprints, named energies, the $g_E=1$ dynamics table) — all already asserted by `tests/test_physics.py`.
2. Write `scripts/crosscheck_su2qc.py` that, for the coupling points P-A and P-S: builds both Hamiltonians, matches basis states by (link spins, occupations), compares (i) all 82 diagonal energies, (ii) the full spectra, (iii) the 38×38 $N=4$ block up to a basis permutation and sign, (iv) exact dynamics from S3 at 12 times, (v) the Lanczos coefficients $(\alpha_k,\beta_k)$ for $k<12$. Tolerance 1e-10. Write `evidence/J0_data/crosscheck_su2qc.json`.
3. If anything disagrees: STOP, document the smallest disagreeing object (a single matrix element with its basis labels), and propose the convention fix in the session report. Do not change `conventions.py` in this session; a convention change needs a decision record (`scripts/new_artifact.py decisions ...`) and a follow-up prompt (`scripts/new_artifact.py prompts ...`).

## Part B — datasets
4. `python scripts/run.py -- python scripts/make_dataset.py --name main --n-traj 20000 --steps 8 12 --families onfam strong --out data/main`
5. `python scripts/run.py -- python scripts/make_dataset.py --name chain_onfam --n-traj 5000 --families onfam --carrier chain --starts S3 --quench-fraction 0 --out data/chain_onfam`
6. `python scripts/run.py -- python scripts/make_dataset.py --name chain_strong --n-traj 3000 --families strong --carrier chain --starts S3 --quench-fraction 0 --out data/chain_strong` (the strong family uses $K=24$ for exact emulation; this is cheap).
7. Record checksums and split sizes in `evidence/J0_data/datasets.json`.

## Part C — gate
8. `python scripts/run.py -- python scripts/run_gate.py J0 --data data/main` (full mode, includes the 160,000-dimensional route-B check).
9. Commit evidence; update `STATE.json` (`M1.status`), the session report.

## Expected
J0 PASS: D1 fingerprints; D2 two-route difference ~1e-16 and Gauss commutator 0; D3 estimator bias ≤ 2.5 SE; D4 $K=12$ error 1.1e-4; D5 5/5 distinct twin repeats; D6 leakage 0.

## Tests to add
`tests/test_crosscheck.py` (skipped if the `su2qc` package is absent) asserting the five comparisons.
