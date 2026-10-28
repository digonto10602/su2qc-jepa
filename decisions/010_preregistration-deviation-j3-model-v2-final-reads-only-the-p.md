---
id: decisions/010
title: 'Preregistration deviation: J3 model v2_final reads only the physical observables'
series: decisions
created_utc: '2026-10-28T23:01:50Z'
author: claude-code
milestone: M3
status: active
supersedes: null
superseded_by: null
---

# Preregistration deviation: J3 model `v2_final` reads only the physical observables

**Decided by:** Digonto, 2026-10-28 (option "Encoder reads physics only"). **Drafted by:** claude-code. **Deviation from:** `docs/PREREGISTRATION.md` §2 ("model configuration", J3 model `v1_final`) and §3 (J3 model `runs/v1_final/seed0/model.pt`). **Made before** any hardware data exist; no hardware job has ever run.

## Decision
1. **The J3 model becomes `v2_final`.** It has the preregistered configuration ($w=(1,3,1,10)$, latent 16, 200 epochs, 5 seeds, masked runs) with one change: `JEPAConfig.encoder_inputs = 18`. The encoder reads only the 18 physical observables, not the flag rate or the source and carrier one-hot labels. The observation layout itself (`ObservationSpec`, frozen) is unchanged.
2. **Training:** on `data/main`, master seed **16180339** (never used before), on the desktop worker, with the command in §3 of this record's companion row in `docs/PREREGISTRATION.md` §7:
   `python scripts/train_jepa.py --data data/main --name v2_final --epochs 200 --seeds 5 --masked --w-sigreg 3 --w-semigroup 10 --master-seed 16180339 --physics-only`.
3. **J3 analysis:** the commands of §3 with `runs/v2_final/seed0/model.pt` in place of `runs/v1_final/seed0/model.pt`. Thresholds, shot levels (`decisions/008`) and baselines are unchanged.
4. **J2 is not repeated as a gate.** Its preregistered result (FAIL, `v1_final`, `evidence/J2_forecast/20261021T201507Z.json`) stands. `v2_final`'s forecasting and J1 numbers are reported for information only.

## Why
- **The cross-carrier check** (`jobs/030`, `evidence/twin/cross_carrier/cross_carrier.json`) found that `v1_final`'s encoder is off-distribution on every twin or hardware record:
  - for the same exact states, changing only the carrier label (diagonal → chain) moves the latent by 7.9, which is 20× the 512-shot noise scale (0.39);
  - changing only the source label (exact → twin) moves it by 9.2, 23×;
  - two chain records of one state differ by 0.03, so the encoder is saturated and nearly blind to their content.
- **The cause:** the flag and the twin/hardware/chain label columns were constant in training, with variance $5.6\times10^{-45}$, so the input normalisation (BatchNorm, running statistics) maps any other value $x$ to about $316x$. On twin or hardware records the JEPA score is therefore dominated by these inputs. In particular, the amplified flag rate is the likely source of the twin-rehearsal AUROC of 1.00, while the physics content is drowned out (Spearman below the raw baseline).
- **The flag rate is not lost:** J3 already reports it as its own label-free baseline (`flag_rate`). The physical observables are post-selected estimates, so the flag still shapes them through post-selection.
- **No hardware data exist,** so the change cannot have been steered by a hardware result. It was steered by the twin rehearsal, which is why it is recorded as a deviation and reported in the paper.

## Alternatives considered
- **Keep the labels, stop normalising them, and add the chain datasets to training:** the "twin" and "hardware" source labels and non-zero flags would still never be seen in training, so the extrapolation problem would remain. Not chosen.
- **Keep `v1_final` and disclose:** J3 would mostly measure an amplified flag rate. Not chosen.

## Consequences
- Code: `JEPAConfig.encoder_inputs`, `train_jepa.py --physics-only`, and test `test_physics_only_encoder_ignores_flag_and_labels` (latent bit-identical when the flag or labels change).
- The twin rehearsals and the cross-carrier check are re-run with `v2_final`. The `v1_final` rehearsals stay in the ledger as artifact-affected.
- `docs/PREREGISTRATION.md` §7 lists this record.
