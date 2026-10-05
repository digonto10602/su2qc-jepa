---
id: decisions/005
title: J1 energy grounding threshold set relative to the measured information ceiling
series: decisions
created_utc: '2026-10-05T21:07:32Z'
author: claude-code
milestone: M2
status: active
supersedes: null
superseded_by: null
---

# J1 energy grounding threshold set relative to the measured information ceiling

**Decided by:** Digonto, 2026-10-05 (option C of `reports/010`). **Drafted by:** claude-code. **Evidence:** `evidence/J1_training/ceiling_main.json` (commit `f1cc1f3`). **Applies to:** `configs/gates.yaml` → `J1_training.grounding_r2_min.energy`, before the preregistration tag `prereg-2026-10-16`.

## Decision
1. The J1 row "grounding $R^2$ energy (min over seeds)" passes when
   $$R^2_{\text{energy}} \ \ge\ 0.887 .$$
   Before this record the threshold was 0.99.
2. The number is $0.97\times R^2_{\text{ceil}}$, rounded down to three decimals. Here $R^2_{\text{ceil}}=0.9145$ is the best validation $R^2$ that any of four regressors (ridge, 5-nearest-neighbours, gradient-boosted trees, MLP) reached when predicting the energy from one clean observation of `data/main` (checksum `73fff8e5a7b7`). That is the same input the encoder sees, scored on the same split that J1 scores.
3. The other J1 rows are unchanged: $C_{\text{string}}\ge0.99$, $P_{\text{meson}}\ge0.95$, $P_{\text{baryonic}}\ge0.98$, effective rank $\ge8$, semigroup residual $<10^{-3}$, 5 seeds, no NaN.
4. The threshold is tied to `data/main` `73fff8e5a7b7` and to the observation layout (`data/records.py: ObservationSpec`). If either changes, the ceiling is re-measured with `scripts/j1_ceiling.py` and a new decision record sets the threshold. The number is never edited in place.

## Why
- **The old threshold cannot be reached by any encoder of one observation.** The grounding target is
  $$E=\langle\psi|\,c_E\mathcal{E}+c_M\mathcal{M}+2c_H\mathcal{T}+c_B\mathcal{B}\,|\psi\rangle \quad(\text{units of } g_E).$$
  The encoder's input misses two parts of it:
  - the hopping $\langle\mathcal{T}\rangle$ and plaquette $\langle\mathcal{B}\rangle$ expectation values, which are off-diagonal in the configuration basis and are not among the 18 observables;
  - the couplings $(c_M,c_H,c_B)$, which differ between trajectories and reach the model only through the actions.

  The measured ceilings (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows) are:

  | regressor | from the observation | with $(c_M,c_H,c_B)$ appended |
  |---|---|---|
  | ridge | 0.8868 | 0.9509 |
  | 5-nearest-neighbours | 0.8509 | 0.9696 |
  | gradient-boosted trees | 0.8902 | 0.9851 |
  | MLP | **0.9145** | 0.9941 |

  The four regressor families agree to within 0.07 (0.851–0.915), and adding the couplings closes most of the gap. So the shortfall is missing information in the input, not a weak regressor.
- **What the row now tests.** It tests what it was meant to test: the latent must keep almost all of the energy information that one record actually contains. The ceiling leaves 8.55% of the energy variance unexplained. The new threshold allows 11.3%, so the model may lose at most 3% of the explainable variance ($0.03\times0.9145=0.027$).
- **Why 0.97.** The factor is a project choice, not a standard value. It lies in the middle of the relative strictness of the existing grounding rows, whose own ceilings are 1.000 (they are entries of the observation): $P_{\text{meson}}$ 0.95, $P_{\text{baryonic}}$ 0.98, $C_{\text{string}}$ 0.99. A factor of 0.99 ($R^2\ge0.905$) would leave no margin for a linear readout of a 16-dimensional latent against an MLP on the raw input. A factor of 0.95 ($R^2\ge0.869$) would sit below the ridge ceiling (0.887). With 0.97, the threshold lies within 0.0003 of the *linear* ceiling of the raw observation (ridge 0.8868), which is a natural floor for a linear grounding head.
- **Known weakness.** $R^2_{\text{ceil}}$ is an estimate: a better regressor could exceed 0.9145. That would make the true ceiling, and so the fair threshold, slightly higher. The 10-epoch laptop check already reached 0.895, so this row is a check against information loss, not a hard target. This is stated in the report of every J1 run that uses it.

## Alternatives considered
(as laid out in `reports/010`)
- **A. Keep 0.99.** The row would fail for every model and could not tell a good model from a bad one. Rejected.
- **B. Ground energy from (latent, $c_M,c_H,c_B$).** The ceiling becomes 0.994, so it would pass by only 0.004. It also changes the model to fit the gate, and all seven queued Perlmutter runs would have to be redone. Rejected.
- **D. Report energy $R^2$ without a pass/fail row.** The other three grounding targets are entries of the observation, so their rows are almost automatic, and J1 would lose its only non-trivial grounding check. Rejected.

## Consequences (what must be re-run or re-checked)
- `configs/gates.yaml`: `J1_training.grounding_r2_min.energy: 0.887`, citing this record. The gate code (`src/su2qc_jepa/gates/j1_training.py`) reads the value from there, so no code change is needed.
- No J1 run used the old value: J1 has never been run (`evidence/GATE_LEDGER.md`). The queued runs `jobs/002`–`008` are unaffected: training does not read gate thresholds.
- `plans/001` §9 and §11 (H1) still say "energy $\ge0.99$". Plans are not edited; this record overrides them for this row. `docs/PREREGISTRATION.md` H1 is updated to match (it is a draft until the tag).
- M2b (preregistration) freezes `configs/gates.yaml` with this value and lists this record and the ceiling evidence among the frozen inputs.
- `prompts/010`: the J1 runs it prescribes use this threshold. Its task 3 ("every J1 row that is reachable") now means every row.
