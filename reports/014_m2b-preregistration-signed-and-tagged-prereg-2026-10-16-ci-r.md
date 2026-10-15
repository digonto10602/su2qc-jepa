---
id: reports/014
title: 'M2b: preregistration signed and tagged (prereg-2026-10-16); CI repaired; branches consistent'
series: reports
created_utc: '2026-10-15T22:03:40Z'
author: claude-code
milestone: M2
status: done
supersedes: null
superseded_by: null
---

# M2b: preregistration signed and tagged (`prereg-2026-10-16`); CI repaired; branches consistent

**Milestone:** M2 (session M2b) · **Prompt:** prompts/002 items 6–8 · **Commit range:** `c9ddfe6..` (from the CI fix to the final `chore(graph)` commit) · **Tag:** `prereg-2026-10-16` → commit `d7655e2` (tag object `496f958`), pushed · **Previous report:** `reports/013`

## What was asked
Digonto, in order:
1. "first check update, do consistency checks of the package with the master and other branch it has, see which one is updated what is being done, then start M2b";
2. after reviewing the draft: "approve".

## Actions taken
1. **Branch consistency.** The repository has `main` (no `master`) and `results` (written only by the Perlmutter worker).
   - Checked: `main` against GitHub; every job file against its `results` status and its fetched copy in `evidence/jobs/`; artifact numbering; code-graph freshness; the gate ledger against `STATE.json`; recorded against local dataset checksums; GitHub CI; the worker heartbeat.
2. **CI repair.** CI had failed on every push since 5 Oct (`5000bc9`), at the lint step only. The cause was a ruff I001 import-order error in my test `test_training_and_baselines_run_on_device`. Fixed (`c9ddfe6`), graph refreshed (`a2086ad`), CI run 38812487482 green.
3. **Preregistration hashes.** New `scripts/prereg_hashes.py`, run through the runner, wrote `evidence/prereg/hashes.json`. It also checks that six trained runs share one configuration: the five `v1_confirm` seeds and `v1_wsig3_wsg10/seed0`.
4. **Freeze.** New test `test_gates_yaml_matches_preregistration`: the sha256 of `configs/gates.yaml` must equal the value recorded in `docs/PREREGISTRATION.md`. `configs/gates.yaml` itself was not edited, so its frozen hash is that of the file J0/J1 used.
5. **`docs/PREREGISTRATION.md`.** Draft written and pushed (`5119b7a`, CI green), sent to Digonto, approved, signed (`d7655e2`), then tagged with an annotated tag and pushed.
6. **J1 on the chosen configuration** (prompt item 8) had already been run as `v1_confirm` (FAIL, `evidence/GATE_LEDGER.md`), before the preregistration. It is disclosed in §0 of the preregistration.

## Results and what they mean

### Consistency (15 Oct, 21:40 UTC)
| check | result |
|---|---|
| `main` local vs `origin/main` | identical, clean |
| `results` vs `main` | separate history, never merged (by design) |
| jobs 000–017: state, commit, node-hours on `results` vs `evidence/jobs/` | 18/18 consistent; 4.318 node-hours |
| artifacts / code graph | OK / FRESH |
| ledger vs `STATE.json` | consistent (J0 PASS; J1 FAIL, last `v1_confirm`) |
| dataset checksums, `evidence/J0_data/datasets.json` vs local manifests | consistent (`main`, `chain_onfam`, `chain_strong`) |
| CI | failing since 5 Oct → green after `c9ddfe6` |
| Perlmutter worker | last heartbeat 2026-10-08 18:45 UTC: **stopped** (nothing in flight) |

### Frozen by the tag
| item | value |
|---|---|
| `configs/gates.yaml` | sha256 `dbb297336a329b723326fd736b93ce7b6e06b473128c1c2aa4e4f4144b0aa078` |
| datasets | `main` `73fff8e5a7b7…`, `chain_onfam` `bdcd6e895a06…`, `chain_strong` `935692f343d8…`; rebuilds accepted by the fingerprint equivalence rule |
| model configuration | $(w_{\text{pred}},w_{\text{sigreg}},w_{\text{ground}},w_{\text{semigroup}})=(1,3,1,10)$, sha256 `cd4faece6fcb3dafd4f84e112e6028fb228c4fa8d809f6d0061cafc8a4ec968c` |
| J2/J3 model | `v1_final`, to be trained after the tag with master seed 27182818 (not used before) |
| H4, H5 | exact definitions (§3 of the preregistration) |

**What it means.** From the tag on, the thresholds, analysis commands, model configuration and exclusion rules are fixed and publicly timestamped on GitHub. H1 is recorded as already measured (not met). H2–H5 are tested on data that do not yet exist:
- for J2, the fresh `v1_final` run;
- for J3, H4 and H5, the twin and hardware campaigns.

Any change now needs a decision record and is reported as a deviation.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 1078 / 1970 / 96 (`reports/013`) | 1108 / 2014 / 102 before this report; final numbers in `evidence/graph/stats.json` of the closing `chore(graph)` commit |
| new or changed | – | `scripts/prereg_hashes.py`, `test_gates_yaml_matches_preregistration` (new); `tests/test_pipeline.py` import block (lint only) |
| `graphify affected` checks | not needed: no existing function changed | full suite run: 56 passed, 1 skipped (CUDA-only), graph check passed after refresh |

## Problems and assumptions
1. **The CI failure went unnoticed for 10 days** because the session protocol runs pytest but not the linter that CI runs. From now on I run `ruff check src tests scripts` before pushing and check `gh run list` after.
2. **Signed one day early.** The tag name `prereg-2026-10-16` is fixed by `CLAUDE.md` §3; the actual approval time (2026-10-15 22:02 UTC) is in the signature line and the tag message.
3. **The Perlmutter worker is stopped** (no heartbeat since 8 Oct). The next step, training `v1_final` for J2, needs it. Digonto must check on Perlmutter with `scrontab -l` and `cat $SCRATCH/su2qc-worker/tick_errors.log`.
4. **Two discrepancies stay open** (not frozen, §5 of the preregistration): the pilot QPU-time cap (90 s in the prompt vs 120 s in the budget file), and the estimator-bias rule (2.5 vs 4.0 standard errors).
5. The H4 and H5 scripts (`depth_extrapolation.py`, `resonance_eval.py`) must be written to the preregistered definitions in M5/M6.

## Next action
Restart the Perlmutter worker. Then `prompts/003` (M3): queue `v1_final` exactly as written in §3 of `docs/PREREGISTRATION.md`, followed by the forecasting work and the twin and dry-run preparation.
