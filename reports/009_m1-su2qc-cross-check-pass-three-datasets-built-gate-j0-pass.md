---
id: reports/009
title: 'M1: su2qc cross-check PASS, three datasets built, gate J0 PASS'
series: reports
created_utc: '2026-10-04T00:35:01Z'
author: claude-code
milestone: M1
status: done
supersedes: null
superseded_by: null
---

# M1: su2qc cross-check PASS, three datasets built, gate J0 PASS

**Milestone:** M1 · **Prompt:** prompts/001 · **Commit range:** `0bb5d6d..` (from the cross-check code to the final graph refresh) · **Gate:** J0 **PASS** (`evidence/GATE_LEDGER.md`, `evidence/J0_data/20261003T201012Z.json`)

## What was asked
Run `prompts/001` (Digonto: "Read ~/.claude/CLAUDE.md then ./CLAUDE.md and then read prompts/001_physics-and-data.md, and then execute the M1 session"). The prompt has three parts:
- **Part A:** cross-check the starter physics core ("route C") against the project's verified `su2qc` code (routes 1 and 2) at P-A and P-S, to $10^{-10}$, and stop on any disagreement.
- **Part B:** build the datasets `main`, `chain_onfam` and `chain_strong`, and record their checksums and split sizes.
- **Part C:** run gate J0 in full mode.

## Actions taken
1. **Session start:** `scripts/env_check.py` (CPU, torch 2.14.1+cpu); `bash scripts/graph_update.sh --check` → FRESH (858 nodes, 1638 edges, 68 communities, built at `2b4bad4`); fast tests 47/47.
2. **Located `su2qc`.** It is not an installed package. It lives inside SU2ZX at `~/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/runs/section8_v0.5.0_20260907T0628Z/src/su2qc` (SU2ZX git head `0bfa96d`). I oriented with that run's own committed code graph (`graphify query/explain --graph …/graphify-out/graph.json`, read-only), then read `conventions.py`, `ham/compare.py` and the `build_hamiltonian` signatures.
3. **Mapped the conventions.** `su2qc` works in lattice units: $H=\tfrac{g^2}{2}\mathcal{E}+m\mathcal{M}+\mathcal{T}-\tfrac{1}{2g^2}\mathcal{B}$, with $\mathcal{E}=\sum_\ell j_\ell(j_\ell+1)$, $\mathcal{M}=\sum_v(-1)^{x+y}n_v$, $\mathcal{T}=\tfrac12\sum_\ell(\eta_\ell\psi^\dagger U\psi+\text{h.c.})$ and $\mathcal{B}=\mathrm{Tr}(U_\square+U_\square^\dagger)$. Route C works in units of $g_E=g^2/2$: $H/g_E=c_E\mathcal{E}+c_M\mathcal{M}+2c_H\mathcal{T}+c_B\mathcal{B}$, which is the same Hamiltonian with $g^2=2g_E$, $m=\mu g_E$. The vertex coordinates are identical in the two codes. Route-C links $(l_a,l_1,l_2,l_3)$ are `su2qc` link indices $(0,3,2,1)$; with that map, $\eta$, the plaquette loop $U_\square$, the mass signs and the staggered vacuum all coincide (asserted at run time). Our S3 is `su2qc`'s `STRETCHED` label.
4. **Wrote `scripts/crosscheck_su2qc.py`** (commit `0bb5d6d`). `su2qc` builds only on-family $(g^2,m)$, and P-S $=(1,0.375,0.02,-0.02)$ is off-family. So for each route the four term matrices are recovered by a linear solve over four builds and checked on a fifth, independent build $(g^2,m)=(3,0.7)$. The checks are those of prompts/001: (i)–(v), each at P-A and P-S against both routes. In addition: the full $82\times82$ matrix after the sign gauge, and, at P-A, `su2qc`'s native build $H(g^2{=}4,m{=}0.75)/2$ with no term extraction. Dynamics times: $t=0.25,\dots,3.0$ at P-A (the hardware window) and $t=2,\dots,24$ at P-S (the strong-coupling time scale), both in units of $1/g_E$. My choice: the prompt says "12 times" without naming them.
5. **Two bugs of my own** were found and fixed during the first runs, before any result was used. Route 2 returns more than two values from `build_hamiltonian`. And the native-build comparison was first made without the sign gauge, which reported 0.5; that is a basis-phase artifact (see Results), not physics.
6. **Added `tests/test_crosscheck.py`** (7 tests). It is skipped where `su2qc` is absent, e.g. in CI, and takes about 15 s on the laptop, so it runs in the fast suite.
7. **Datasets:**
   - `main`: built through `scripts/run.py`.
   - `chain_onfam`: built through `scripts/run.py`.
   - `chain_strong`: a first laptop attempt was killed when my background shell hit its 1-hour limit (no partial output kept). A 20-trajectory timing run gave 0.82 s per trajectory, so the full set would take about 41 min on the laptop, over the 20-minute rule. The runner estimated 0.3 min, so I used its documented override, `run.py --est-minutes 45 --push`, to queue it as `jobs/001` for Perlmutter, and fetched it with `scripts/jobs/fetch.py 001`.
8. **Wrote `scripts/record_datasets.py`**. It recomputes the array checksum with the generator's own rule, records split sizes, and accepts a manifest-only dataset built on Perlmutter. A first version also hashed the `split_*` arrays and reported a false MISMATCH; it was fixed to hash the data arrays only, as the generator does.
9. **Gate:** `python scripts/run.py -- python scripts/run_gate.py J0 --data data/main` (full mode).

## Results and what they mean

### Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS)
| quantity (max abs deviation) | P-A route 1 | P-A route 2 | P-S route 1 | P-S route 2 |
|---|---|---|---|---|
| (i) 82 diagonal energies | 0 | $4.4\times10^{-16}$ | 0 | $4.4\times10^{-16}$ |
| (ii) full spectrum | $6.2\times10^{-15}$ | $6.2\times10^{-15}$ | $8.2\times10^{-15}$ | $5.3\times10^{-15}$ |
| (iii) $N=4$ block, after sign gauge | $5.6\times10^{-17}$ | $4.4\times10^{-16}$ | $1.2\times10^{-16}$ | $4.4\times10^{-16}$ |
| (iii) full $82\times82$, after sign gauge | $5.6\times10^{-17}$ | $4.4\times10^{-16}$ | $1.2\times10^{-16}$ | $4.4\times10^{-16}$ |
| basis states with opposite sign convention | 8 | 24 | 8 | 24 |
| (iv) sector populations from S3, 12 times | $1.1\times10^{-15}$ | $2.7\times10^{-15}$ | $3.9\times10^{-14}$ | $2.7\times10^{-14}$ |
| (iv) route-C observables from S3 | $2.1\times10^{-15}$ | $3.0\times10^{-15}$ | $7.3\times10^{-14}$ | $5.9\times10^{-14}$ |
| (v) Lanczos $\alpha_k$, $k<12$ | $1.3\times10^{-15}$ | $1.3\times10^{-15}$ | $5.8\times10^{-15}$ | $2.7\times10^{-15}$ |
| (v) Lanczos $\beta_k$, $k<12$ | $6.7\times10^{-16}$ | $1.1\times10^{-15}$ | $1.7\times10^{-15}$ | $6.9\times10^{-15}$ |
| native su2qc build (P-A only) | $5.6\times10^{-17}$ | $4.4\times10^{-16}$ | – | – |
| term extraction, residual on a 5th build | $1.1\times10^{-16}$ | $8.9\times10^{-16}$ | (same) | (same) |

The largest deviation anywhere is $7.3\times10^{-14}$, more than three orders of magnitude inside the $10^{-10}$ tolerance. So route C is the same Hamiltonian as the verified code at both coupling points, including the off-family point P-S.

The sign gauge needs a word. The codes choose opposite phases for 8 (route 1) or 24 (route 2) basis states, so raw matrix entries differ by $\pm2c_H$ (0.5 at P-A). The script fixes $D=\mathrm{diag}(\pm1)$ on a spanning tree of the coupling graph and then requires every remaining entry to agree. Every closed loop, including the plaquette, therefore checks the relative signs, so a wrong plaquette sign or a wrong Jordan–Wigner string would show up here. Populations, spectra and Lanczos coefficients do not depend on $D$ at all.

A hand check: $\alpha_0=\langle S3|H|S3\rangle=3\cdot\tfrac34+\mu(1-1+0-2)=1.5$ at $\mu=3/8$, and the computed $\alpha_0$ is $1.5$. Route-C Lanczos coefficients at P-A: $\alpha_{0..11}=(1.5, 1.684, 1.492, 0.399, 0.434, 1.144, 2.394, 2.452, 1.876, 1.889, 0.946, 0.828)$, $\beta_{0..11}=(0.472, 0.846, 1.341, 1.502, 1.439, 1.482, 1.534, 1.141, 0.408, 1.156, 0.546, 1.117)$.

### Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`)
| dataset | trajectories | built on | wall time | array checksum (sha256, first 12) | check | splits train / val / held-out mass / held-out family |
|---|---|---|---|---|---|---|
| `main` | 20,000 | laptop | 158 s | `73fff8e5a7b7` | recomputed, match | 11,539 / 2,392 / 6,069 / onfam 2,935, strong 3,134 |
| `chain_onfam` | 5,000 | laptop | 1,668 s | `bdcd6e895a06` | recomputed, match | 2,859 / 741 / 1,400 / onfam 1,400 |
| `chain_strong` | 3,000 | Perlmutter (`jobs/001`, Slurm 59281851, 0.223 h, 0.056 node-h) | 789 s | `935692f343d8` | manifest only | 1,897 / 276 / 827 / strong 827 |

The held-out-family sets are subsets of "held-out mass" (the manifest counts both), which is why the numbers do not add up to the totals. Seed 20261005 (the `make_dataset.py` default) throughout. Split rule: on-family by $g_E$ label (held out 1.3, 1.75; validation 1.45), strong by $\mu$ (held out 0.3, 0.42, 0.5; validation 0.45), never by row.

### Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop)
| row | measured | threshold |
|---|---|---|
| D1 state counts | 82; 2/20/38/20/2; 16/16/18/16/16 | same |
| D2 two-route agreement | $4.4\times10^{-16}$ | $10^{-12}$ |
| D2 Gauss-law commutator | 0 | $10^{-12}$ |
| D3 estimator bias, diagonal carrier ($S=1024$, $M=200$, max over 18 observables) | 2.36 SE | 4.0 SE |
| D3 estimator bias, chain carrier (Z+X) | 1.44 SE | 4.0 SE |
| D4 Krylov $K=12$, P-A window $t\le3/g_E$ | $1.05\times10^{-4}$ | $10^{-3}$ |
| D5 twin repeats independent | 5/5 distinct | 5 |
| D6 split leakage | 0 | 0 |
| D6 checksum recorded | `73fff8e5a7b7` | present |

These match the plan's expectations (W1): two-route difference ~$10^{-16}$, $K=12$ error $1.1\times10^{-4}$, bias within bounds.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 858 / 1638 / 68 (`2b4bad4`) | see `evidence/graph/stats.json` in the final `chore(graph)` commit |
| new or changed hubs | – | none expected: two new scripts and one test, no existing function changed |
| `graphify affected` checks run | none needed | no existing function or class was modified (new files only: `scripts/crosscheck_su2qc.py`, `scripts/record_datasets.py`, `tests/test_crosscheck.py`) |

## Problems and assumptions
1. **The runner's time estimate ignores the carrier.** `localrun.estimate_minutes` uses one cost per trajectory (`_UNIT_COST["dataset_per_traj"]`, ≈ 0.006 s, right for the diagonal carrier). Measured per-trajectory costs: `main` 0.008 s; `chain_onfam` 0.33 s on a loaded laptop; `chain_strong` 0.82 s (laptop) and 0.26 s (Perlmutter). The runner therefore estimated 0.5 min for `chain_onfam` (actual 28 min) and 0.3 min for `chain_strong`, so it would keep heavy chain datasets on the laptop. Proposed fix (not done; a later session): carrier- and family-specific unit costs in `compute._UNIT_COST`, plus a test. Until then use `--est-minutes`.
2. **`chain_strong` exists only as a manifest here.** The worker never publishes `.npz` files, so its checksum was computed on Perlmutter and could not be recomputed on the laptop. Training jobs rebuild datasets on Perlmutter from the seed, so this is enough for the plan. But **laptop-versus-Perlmutter reproducibility of a dataset checksum has not been tested yet**: different BLAS libraries could change the last bits of `eigh`. I recommend a cheap check before M2 relies on rebuilds: build a small dataset on both machines and compare the checksums.
3. **D3 threshold differs between the plan and the config.** Plan W1 says estimator bias $\le2.5$ SE; `configs/gates.yaml` uses 4.0 (a maximum over 18 observables). Both measured values (2.36 and 1.44) satisfy the stricter 2.5 as well. Not changed: thresholds change only through the planner.
4. **A false "worker looks stopped" warning.** `scripts/jobs/status.py` warned at a heartbeat age of 8.9 h, but an idle worker heartbeats only every 12 h. The worker was fine and picked up `jobs/001` at the next tick. A small fix to the warning threshold would avoid confusion.
5. **I didn't run `graphify update` on SU2ZX**, which prompts/001 suggests. It would write into another project's folder. I used SU2ZX's existing committed graphs read-only instead, and did not change SU2ZX.
6. `su2qc/conventions.py` prints a harmless `SyntaxWarning` (an invalid `\d` escape in its docstring) when imported. It is their code and was left alone.
7. **The laptop was shared with another session** (load average up to ~28 on 12 logical CPUs from its planner and Quantinuum scripts). The runner waited for room several times, as designed. The session spanned 2–3 Oct (UTC) because of these waits and a pause.

## Next action
`prompts/002_model-and-prereg.md` (M2, gate J1). Before its first queued training job, consider the dataset-reproducibility check in Problem 2.
