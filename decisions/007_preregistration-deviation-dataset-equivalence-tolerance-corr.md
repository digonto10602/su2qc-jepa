---
id: decisions/007
title: 'Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale'
series: decisions
created_utc: '2026-10-21T17:01:48Z'
author: claude-code
milestone: M3
status: active
supersedes: null
superseded_by: null
---

# Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale

**Decided by:** Digonto, 2026-10-21 (option "Decision record" in the M3 session). **Drafted by:** claude-code, which also wrote the original rule; the error is in that draft. **Deviation from:** `docs/PREREGISTRATION.md` §2, row "equivalence rule for rebuilds", signed by tag `prereg-2026-10-16` (commit `d7655e2`). **Made before** any result of the preregistered J2/J3 model `v1_final` exists: that model has not been trained.

## Decision
A rebuild of a preregistered dataset (on Perlmutter, the desktop or any other machine) is equivalent to the reference build when, by `scripts/compare_fingerprints.py`:
1. `ctx`, `act` and `valid` are **bit-identical** (unchanged); and
2. `tgt` and `energy` differ by at most $10^{-12}$ **per sampled value** and at most $10^{-10}$ **per trajectory sum**.

The signed text required $\le10^{-12}$ per trajectory sum.

## Why
- **The signed rule contradicts its own example.** The same table row quotes the `data/main` rebuild ("largest difference $5.7\times10^{-12}$"), which fails the $10^{-12}$ bound it states. The intent was "the two builds differ only by floating-point rounding", but the number was written for single values and applied to sums of about 200–300 values. Rounding errors of order $10^{-13}$ add up to a few $10^{-12}$ in such sums.
- **Measured differences:**

  | comparison | max per sampled value (`tgt` / `energy`) | max per-trajectory sum (`tgt` / `energy`) | inputs |
  |---|---|---|---|
  | `data/main`, laptop vs Perlmutter | $5.7\times10^{-14}$ / $1.9\times10^{-13}$ | $5.7\times10^{-12}$ / $2.5\times10^{-12}$ | bit-identical |
  | `gpu_smoke`, laptop vs desktop | $5.0\times10^{-14}$ / $2.0\times10^{-13}$ | $2.7\times10^{-12}$ / $1.6\times10^{-12}$ | bit-identical |
  | `gpu_smoke`, desktop vs Perlmutter | 0 | 0 | bit-identical |

  Sources: `evidence/J0_data/fingerprint_compare_main_laptop_vs_perlmutter.json`, `…_gpu_smoke_laptop_vs_desktop.json`, `scripts/compare_fingerprints.py` on `evidence/jobs/010` and `018`.
- **Margins of the new bounds.** They are at least 5× above the largest measured rounding difference (per value $2.0\times10^{-13}$, per sum $5.7\times10^{-12}$). They are also about $10^{10}$ times below the statistical noise of the noisy inputs: the shot noise of a probability at 4,096 shots is about $1/\sqrt{4096}\approx0.016$. No physical or statistical quantity can differ at this level.
- **The choice is independent of any preregistered outcome.** No `v1_final` model, forecast or hardware record exists, and the rule concerns data that the model never sees differently: the inputs are identical bit for bit.

## Alternatives considered
- **Copy the laptop's exact `data/main` to the desktop and train on those bytes:** this avoids the rule entirely but needs a manual copy and a job-runner change, and it would still leave a wrong rule in the preregistration for later rebuilds. Not chosen.
- **Keep the rule and report the violation:** this is honest but reports a "non-equivalent" dataset that differs only by rounding, which misleads more than it informs. Not chosen.

## Consequences
- `docs/PREREGISTRATION.md` keeps its signed text unchanged and gains a "Deviations after signing" section that points here. The paper reports this as a deviation.
- `v1_final` is trained on the desktop's rebuild of `data/main`. Its fingerprint is compared with the reference under the corrected rule, and the result is recorded with the J2 evidence.
- No threshold in `configs/gates.yaml` changes; its frozen sha256 is unaffected.
