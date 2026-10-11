# Model card — Gauge-JEPA-P v1 (working configuration after M2a)

Living document (edited in place, versioned by git). Written 8 Oct 2026 at the close of session M2a (`prompts/002`, `prompts/010`; session report `reports/013`).

**Status: J1 FAIL.** No configuration passed every J1 row on a fresh set of seeds (§4). The configuration below is the *working* model for M3, chosen as the closest to passing; it is not a J1-validated model.

## 1. What the model is
A JEPA world model (Joint-Embedding Predictive Architecture: an encoder compresses one measurement record into a latent vector, a predictor advances the latent under actions, and the loss compares the predicted latent with the latent of the clean future record) for the SU(2) plaquette with matter (`plans/001` §5, `src/su2qc_jepa/models/jepa.py`).

| part | definition |
|---|---|
| input (observation) | 24 numbers: 18 diagonal physical observables, the flag rate, a source one-hot (exact/twin/hardware), a carrier one-hot (diagonal/chain) (`data/records.py: ObservationSpec`) |
| action | $(\Delta t,\ c_M,\ c_H,\ c_B)$; a mass quench changes $c_M$ mid-trajectory |
| encoder | MLP $24\to128\to128\to16$ with LayerNorm and GELU; input normalised by a non-affine BatchNorm |
| predictor | GRU over embedded action tokens (embedding $4\to32\to32$, hidden 128), initialised from the latent, plus a linear skip connection |
| grounding heads | one linear map latent $\to$ (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag) |
| trainable parameters | **90,309** (encoder 22,288; predictor 67,936; grounding 85), counted in code on 5 Oct 2026 |
| loss | $w_{\text{pred}}\,\text{MSE}_{k\in\{1,2,4,8\}} + w_{\text{sigreg}}\,\text{SIGReg} + w_{\text{ground}}\,\text{grounding MSE} + w_{\text{semigroup}}\,\text{semigroup MSE}$ |

SIGReg is LeJEPA's sketched isotropic Gaussian regulariser (arXiv:2511.08544), which pushes the latent distribution towards a standard Gaussian and so prevents collapse. The semigroup term asks the predictor to compose like time evolution: predicting two steps at once should equal predicting one step twice.

## 2. Working configuration
| setting | value | default before M2a |
|---|---|---|
| $w_{\text{pred}}$ | 1 | 1 |
| $w_{\text{sigreg}}$ | **3** | 0.5 (`scripts/train_jepa.py` default) |
| $w_{\text{ground}}$ | 1 | 1 |
| $w_{\text{semigroup}}$ | **10** | 0.1 |
| latent dimension | 16 | 16 |
| target encoder | shared encoder, no EMA | same |
| curriculum | none | same |
| optimiser | AdamW, lr $2\times10^{-3}$, weight decay $10^{-5}$, cosine schedule, batch 64, gradient clip 1.0, 200 epochs | same |
| command | `python scripts/train_jepa.py --data data/main --epochs 200 --seeds 5 --masked --w-sigreg 3 --w-semigroup 10 --master-seed 31415926` | |
| trained models | `runs/v1_confirm/seed{0..4}` and `seed{0..4}_masked` (Perlmutter `jobs/017`, commit `600197b`; local copies fetched, not in git) | |
| training seeds | `SeedSequence(31415926).spawn(5)` → 788512632, 3846163361, 669117117, 1958259924, 352388378 | |

**Why this configuration.** Fourteen configurations were trained, each with 5 seeds × 200 epochs: the plan's ladder (SIGReg weight, latent 32, EMA target, grounding weight, curriculum) plus a semigroup-weight series (§4). Raising the SIGReg weight lifts the effective rank but raises the semigroup residual. Raising the semigroup weight lowers the residual but lowers the rank. $(w_{\text{sigreg}},w_{\text{semigroup}})=(3,10)$ was the only setting that passed every J1 row on the selection seeds, and on the fresh confirmation seeds it missed only one row on one seed.

## 3. Training cost
| where | per run (one seed, 200 epochs) | 5 seeds | 5 seeds + masked |
|---|---|---|---|
| Perlmutter, one A100 (shared queue) | 700–770 s (≈3.5–3.9 s per epoch) | 1.06–1.15 h, 0.26–0.29 node-hours (`evidence/jobs/011`–`016/status.json`) | 2.09 h, 0.52 node-hours (`evidence/jobs/017`) |
| laptop, 2 CPU threads | 17.5 s per epoch (`runs/v1_check`, 10 epochs) | – | – |

M2a used 4.32 of the 50 node-hour Perlmutter budget in all.

## 4. J1 results (validation split, final epoch; `evidence/GATE_LEDGER.md`, `figures/000`, `figures/001`)
Thresholds: rank $\ge8$; grounding $R^2$ energy $\ge0.887$ (`decisions/005`), $C_{\text{string}}\ge0.99$, $P_{\text{meson}}\ge0.95$, $P_{\text{baryonic}}\ge0.98$; semigroup residual $<10^{-3}$; minimum or maximum taken over 5 seeds.

| configuration | rank (min) | semigroup (max) | other failing rows | J1 |
|---|---|---|---|---|
| `v1_base` ($w_{\text{sigreg}}=0.5$, $w_{\text{sg}}=0.1$) | 5.16 | $3.29\times10^{-3}$ | – | FAIL |
| `v1_wsigreg2` | 8.26 | $5.34\times10^{-3}$ | – | FAIL |
| `v1_wsigreg5` | 10.53 | $8.47\times10^{-3}$ | – | FAIL |
| `v1_latent32` | 6.12 | $4.72\times10^{-3}$ | – | FAIL |
| `v1_ema` ($\tau=0.996$) | 13.09 | $2.21\times10^{-2}$ | $P_{\text{meson}}$ 0.915 | FAIL |
| `v1_wground3` | 5.63 | $6.94\times10^{-3}$ | – | FAIL |
| `v1_curriculum` | 6.18 | $2.86\times10^{-3}$ | – | FAIL |
| `v1_wsemigroup1` | 4.94 | $1.72\times10^{-3}$ | – | FAIL |
| `v1_wsig2_wsg1` | 8.56 | $5.57\times10^{-3}$ | – | FAIL |
| `v1_wsig2_wsg3` | 8.07 | $1.17\times10^{-3}$ | – | FAIL |
| `v1_wsig2_wsg5` | 7.80 | $1.01\times10^{-3}$ | – | FAIL |
| `v1_wsig2_wsg10` | 7.42 | $9.2\times10^{-4}$ | – | FAIL (rank) |
| `v1_wsig3_wsg10` (selection seeds) | 8.26 | $7.8\times10^{-4}$ | – | PASS |
| **`v1_confirm`** (same settings, fresh seeds) | 8.45 | $1.48\times10^{-3}$ (seed 3; others $3.2$–$7.3\times10^{-4}$) | – | **FAIL** |

For the working configuration on the fresh seeds, all grounding rows pass: energy $R^2\ge0.900$ (measured ceiling 0.9145, `evidence/J1_training/ceiling_main.json`), $C_{\text{string}}\ge0.997$, $P_{\text{meson}}\ge0.968$, $P_{\text{baryonic}}\ge0.997$. The masked-coupling runs (couplings hidden from the actions) have semigroup residuals near $2\times10^{-5}$ and rank 7.5–8.1. They are not part of the J1 gate.

**Diagnosis.** The latent is not collapsing: every grounding row passes, and the rank reaches 8–13 when SIGReg is strong enough. The failing row is predictor consistency. Its residual grows as the latent spreads out, varies about 5× between seeds, and is about 50× smaller when the couplings are hidden. So the inconsistency comes from how the predictor uses the coupling inputs.

## 5. Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`, mean of 5 seeds; NOT a J2 result, since J2 is run in M4a)
MAE (mean absolute error) of $P_{\text{baryonic}}$ / $P_{\text{meson}}$ / $C_{\text{string}}$ at $+8$ steps after the context step, on the held-out split:

| family | JEPA | ridge | autoregressive | supervised MLP | JEPA, couplings masked |
|---|---|---|---|---|---|
| on-family (2,935 trajectories) | 0.046 / 0.021 / 0.027 | 0.144 / 0.030 / 0.136 | 0.403 / 0.188 / 1.134 | 0.048 / 0.020 / 0.024 | 0.093 / 0.021 / 0.059 |
| strong coupling (3,134) | 0.133 / 0.020 / 0.069 | 0.185 / 0.024 / 0.248 | 0.371 / 0.078 / 0.238 | 0.153 / 0.018 / 0.068 | 0.144 / 0.019 / 0.070 |

On-family, the JEPA meets the J2 bound of MAE ≤ 0.05 and beats ridge and the autoregressive baseline. On the strong-coupling family, $P_{\text{baryonic}}$ (0.133) and $C_{\text{string}}$ (0.069) exceed 0.05, so J2 is at risk there. This is reported now so M3 can plan for it.

## 6. Data and reproducibility
- Trained on `data/main` rebuilt on Perlmutter (checksum `76f4c9055591`). The laptop build is `73fff8e5a7b7`. The noisy inputs, actions and validity masks are bit-identical between the two builds; the exact targets differ only by floating-point rounding, at most $5.7\times10^{-14}$ per sampled value (`evidence/J0_data/fingerprint_compare_main_laptop_vs_perlmutter.json`).
- The selection search used master seed 20261005 and the confirmation used 31415926. Both are recorded in `runs/<name>/args.json` and `forecast_eval.json`.

## 7. Known limitations
1. J1 FAIL (semigroup row) on fresh seeds.
2. The energy readout is capped by information: one record cannot determine the energy beyond $R^2\approx0.91$ (`decisions/005`).
3. Strong-coupling forecasting error exceeds the J2 bound (preliminary, §5).
4. The configuration was chosen by searching on the same validation split that J1 scores. Only the confirmation run is free of that selection.
5. No hardware or twin records were used in training: all inputs are exact-source records with emulated shot noise.
