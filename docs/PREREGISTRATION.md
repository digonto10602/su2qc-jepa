# Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)

Status: **SIGNED** — approved by Digonto on 15 Oct 2026 (22:02 UTC) and signed by the annotated git tag `prereg-2026-10-16` on the commit that adds this line (the tag name is fixed by `CLAUDE.md` §3; the signature came one day before the planned date). Written in session M2b (`prompts/002` items 6–8). After the tag, nothing below changes without a decision record in `decisions/`; `tests/test_repo_conventions.py::test_gates_yaml_matches_preregistration` fails if `configs/gates.yaml` changes without this file being updated.

*Preregistration* means fixing the hypotheses, the pass/fail thresholds and the exact analysis **before** the data that test them exist, so that the analysis cannot be tuned to the result.

## 0. What was already known when this was written (disclosure)
| item | status at preregistration | evidence |
|---|---|---|
| J0 (data, physics) | PASS 9/9 (3 Oct) | `evidence/J0_data/20261003T201012Z.json` |
| J1 / H1 (training health) | **FAIL**, measured before preregistration: 14 configurations; the confirmation run `v1_confirm` failed the semigroup row on one seed (1.48e-3 vs 1e-3) | `evidence/GATE_LEDGER.md`, `docs/MODEL_CARD.md`, `reports/013` |
| J1 energy threshold | changed 0.99 → 0.887 on 5 Oct, before any J1 run, because one record cannot determine the energy beyond $R^2=0.9145$ | `decisions/005`, `evidence/J1_training/ceiling_main.json` |
| J2 / H2 (forecasting) | **preliminary numbers were seen**: `runs/v1_confirm/forecast_eval.json`, quoted in `docs/MODEL_CARD.md` §5. That run therefore cannot be the J2 evidence; J2 is scored on a fresh run trained after the tag (§3) | `docs/MODEL_CARD.md` |
| J3, H3, H4, H5 | no twin campaign, no hardware job has been run; QPU seconds spent: 0 | `STATE.json` |

## 1. Hypotheses (thresholds are those of `configs/gates.yaml`, frozen below)
- **H1 (no collapse)** — 5 seeds; no NaN; effective rank $\ge8$; grounding $R^2$: energy $\ge0.887$, $C_{\text{string}}\ge0.99$, $P_{\text{meson}}\ge0.95$, $P_{\text{baryonic}}\ge0.98$; semigroup residual $<10^{-3}$. **Result already measured: not met (J1 FAIL).** It is not re-tested; §3 reports J1 on `v1_final` for information only.
- **H2 (forecasting)** — on the held-out split of each family (on-family, strong coupling), JEPA MAE $\le0.05$ at $+4$ and $+8$ steps after the context step $c=4$ (512-shot context) for $P_{\text{baryonic}}$, $P_{\text{meson}}$, $C_{\text{string}}$; and JEPA MAE $\le1.1\times$ the ridge and the autoregressive baseline MAE on $\ge2$ of 3 targets at each step. The masked-coupling task (couplings hidden) is reported for both JEPA and ridge.
- **H3 (label-free error signal)** — on $\ge24$ hardware points: Spearman rank correlation between `jepa_twin` and the exact error $\ge0.7$ at 512 shots; `jepa_twin` Spearman $\ge$ `raw_twin` Spearman $-0.05$ at 512 shots; AUROC of `jepa_twin` separating arm B from arm A $\ge0.8$ at full shots; 3 calibration days; `raw_twin`, `flag_rate`, `jepa_self`, `jepa_t0` all reported.
- **H4 (depth extrapolation on hardware)** — for each on-family point $g_E\in\{1.3,1.75,2.0\}$, $\mu=3/8$: the forecast of the $t=3/g_E$ observables from the hardware records at $r=1$ and $r=2$ has lower absolute error (against the exact value) than the direct $r=8$ hardware estimate for $\ge2$ of the 3 targets, at all three $g_E$ (definition in §3).
- **H5 (resonance from hardware)** — the resonance mass estimated from the strong-coupling KC-prep hardware points lies within 0.05 of $\mu^*=3/8$ (definition in §3).

## 2. Frozen inputs
| item | value |
|---|---|
| `configs/gates.yaml` sha256 | `dbb297336a329b723326fd736b93ce7b6e06b473128c1c2aa4e4f4144b0aa078` |
| `data/main` checksum (reference, laptop build) | `73fff8e5a7b7f670b26056a000b4d50d13db79499a7467f36b15c69f66539828` (20,000 trajectories, seed 20261005) |
| `data/chain_onfam` checksum | `bdcd6e895a06ca28ea107bfe374be1b44bbfabe3398780b9f903b788d352e1ac` |
| `data/chain_strong` checksum | `935692f343d89895f5e93c232ec1b7bef470a1c3d638fcbb813364914e60cd59` (built on Perlmutter) |
| equivalence rule for rebuilds | a rebuild of a dataset (e.g. on Perlmutter, `data/main` → `76f4c9055591…`) is equivalent to the reference when, by `scripts/compare_fingerprints.py`, `ctx`, `act` and `valid` are bit-identical and `tgt`, `energy` differ by $\le10^{-12}$ in every per-trajectory sum. Measured for `data/main`: bit-identical inputs, largest difference $5.7\times10^{-12}$ (`evidence/J0_data/fingerprint_compare_main_laptop_vs_perlmutter.json`) |
| model configuration | $(w_{\text{pred}},w_{\text{sigreg}},w_{\text{ground}},w_{\text{semigroup}})=(1,3,1,10)$, latent 16, hidden 128, horizons (1,2,4,8), no EMA, no curriculum; AdamW lr $2\times10^{-3}$, weight decay $10^{-5}$, batch 64, 200 epochs |
| model configuration sha256 | `cd4faece6fcb3dafd4f84e112e6028fb228c4fa8d809f6d0061cafc8a4ec968c` = sha256 of the canonical JSON in `evidence/prereg/hashes.json` (`scripts/prereg_hashes.py`; seed and device excluded) |
| training master seed for the J2/J3 model `v1_final` | **27182818** (`SeedSequence(27182818).spawn(5)`); never used before |
| code | the commit carrying the tag `prereg-2026-10-16` |
| hardware design | `plans/001` §8 (families, points, settings, 4,000 shots, arms A and B) |
| backend(s) | IBM Open-plan Heron r2 devices; the backend of each day is recorded with its calibration snapshot (not fixed in advance: device availability is not under our control) |

## 3. Analysis plan (exact commands; every computation through `scripts/run.py`)
**J2 / H2.** Train the preregistered configuration with the fresh master seed, on Perlmutter:
`python scripts/run.py --push --prompt prompts/003 -- python scripts/train_jepa.py --data data/main --name v1_final --epochs 200 --seeds 5 --masked --w-sigreg 3 --w-semigroup 10 --master-seed 27182818`;
fetch with `python scripts/jobs/fetch.py NNN`; check the rebuilt dataset against the equivalence rule (§2); then
`python scripts/run.py -- python scripts/run_gate.py J2 --eval runs/v1_final/forecast_eval.json`.
J1 on `runs/v1_final/seed0 … seed4` is run and reported for information only (H1 is already decided).

**J3 / H3.** The model is `runs/v1_final/seed0/model.pt` (the other four seeds are reported as a sensitivity check). For each calibration day, after `hw_submit.py collect`:
`python scripts/run.py -- python scripts/residual_eval.py --model runs/v1_final/seed0/model.pt --records <day records> --source hardware --reference <day twin records> --shots-levels 0 512 256 --out evidence/hardware/residual_eval_<day>.json`;
the days are concatenated into `evidence/hardware/residual_eval_all.json` and
`python scripts/run.py -- python scripts/run_gate.py J3 --eval evidence/hardware/residual_eval_all.json`.

**H4** (`scripts/depth_extrapolation.py`, to be written in M5 to this definition): for each on-family $g_E\in\{1.3,1.75,2.0\}$ at $\mu=3/8$, encode the post-selected hardware record at $r=1$ ($t=0.375/g_E$) and, separately, at $r=2$ ($t=0.75/g_E$) with `v1_final/seed0`; propagate with the predictor under the known actions to $t=3/g_E$; read out $P_{\text{baryonic}}$, $P_{\text{meson}}$, $C_{\text{string}}$ with the ridge probe fit on the training split; the forecast error is the mean of the two forecasts' absolute errors against the exact values; the direct error is the absolute error of the $r=8$ hardware estimate. H4 holds at a $g_E$ when the forecast error is smaller on $\ge2$ of the 3 targets.

**H5** (`scripts/resonance_eval.py --source hardware`, to be written in M6 to this definition): for each KC-prep time $t\in\{10,15,20\}/g_E$, take the post-selected hardware breaking fraction $P_{\text{meson}}+P_{\text{baryonic}}$ at $\mu\in\{0.3,0.375,0.42,0.5\}$, fit a parabola in $\mu$ by least squares, and take its vertex $\hat\mu^*$ (reported as not found if the parabola opens upward). The primary estimate is $t=20/g_E$; H5 holds when $|\hat\mu^*-0.375|\le0.05$. The other two times and the exact-simulation value are reported alongside.

## 4. Exclusion and handling rules
- Hardware points with flag rate $>0.8$ are excluded from J3, H4 and H5 and listed in the paper.
- A "calibration day" is defined by the calibration-snapshot hash, not by the date.
- A hardware job that fails on the provider's side (device error, not a code error) may be resubmitted once with the identical manifest after a new human approval; the failure is reported.
- No post-hoc change of shot levels, targets, evaluation steps, context step, model configuration, master seed or thresholds. Any change after the tag needs a decision record and is reported as a deviation.
- A training job that fails for a program error is fixed in code and re-run with the same configuration and master seed; a run is never selected among repeats.
- All baselines named in `configs/gates.yaml` are reported whatever the outcome; results are reported as PASS / FAIL / PARTIAL / NOT RUN / VOID, never upgraded in prose.

## 5. Known open items (not part of the frozen record)
- The pilot QPU-time cap differs between `prompts/004` (90 s) and `configs/hardware_budget.yaml` (120 s per approval). The budget file is a human approval document, not a preregistered threshold; Digonto sets it at the pilot.
- The plan states estimator bias $\le2.5$ standard errors (W1) while `configs/gates.yaml` uses 4.0; the gate file governs, and J0 met both (2.36 and 1.44).

## 6. Signatures
Digonto (researcher) — approved 2026-10-15 22:02 UTC ("approve", in the M2b Claude Code session after reviewing this file) — commit: the one carrying the tag — tag `prereg-2026-10-16`.

## 7. Deviations after signing
Changes made after the tag `prereg-2026-10-16`. Each has its own decision record, and each is reported in the paper as a deviation. The signed text above is left unchanged.

| date | item | change | record |
|---|---|---|---|
| 2026-10-21 | §2 equivalence rule for rebuilds | the per-trajectory-sum bound of $10^{-12}$ contradicted the measured rebuild quoted in the same row ($5.7\times10^{-12}$, pure rounding); corrected to $\le10^{-12}$ per value and $\le10^{-10}$ per trajectory sum, with inputs still bit-identical. Made before `v1_final` was trained | `decisions/007` |
| 2026-10-22 | §3 J3 gate code, low-shot level | the code scored the low-shot rows at the lowest level present (256, from the preregistered `--shots-levels 0 512 256`) instead of the preregistered 512 (H3, `gates.yaml low_shot_level`); code aligned to 512. Thresholds and commands unchanged; found in the twin rehearsal, before any hardware data | `decisions/008` |
| 2026-10-28 | §2/§3 J3 model | `v1_final`'s encoder normalised the constant-in-training flag and source/carrier labels to ~316x, so twin/hardware records were off-distribution (cross-carrier check, `jobs/030`); the J3 model becomes `v2_final`: same configuration, encoder reads only the 18 physical observables, master seed 16180339. J2 (v1_final, FAIL) stands. Before any hardware data | `decisions/010` |
