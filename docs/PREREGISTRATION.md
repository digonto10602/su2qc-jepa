# Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)

Status: **DRAFT until the tag exists.** Filled in by session M2b. Nothing below changes after the tag without a decision record in `decisions/`.

## Hypotheses (from PLAN §11)
- H1 (no collapse): effective rank ≥ 8/16; grounding $R^2$ ≥ 0.887 (energy; 0.97 × the measured ceiling 0.9145 for one observation, `decisions/005`), ≥ 0.99 ($C_{\text{string}}$), ≥ 0.95 ($P_{\text{meson}}$), ≥ 0.98 ($P_{\text{baryonic}}$); semigroup residual < 1e-3; 5 seeds.
- H2 (forecasting): MAE ≤ 0.05 at +4 and +8 steps on the held-out split of each family; not worse than ridge and autoregressive within 1.1× on ≥ 2/3 targets; masked-coupling task reported.
- H3 (label-free error signal): Spearman(`jepa_twin`, exact error) ≥ 0.7 at 512 shots; non-inferior to `raw_twin` within 0.05; AUROC(arm B vs A) ≥ 0.8; three calibration days.
- H4 (depth extrapolation on hardware): forecast of $t=3/g_E$ from $r\le2$ records beats the direct $r=8$ estimate on ≥ 2/3 targets at each $g_E$.
- H5 (resonance from hardware): $\mu^*$ from the strong-coupling KC-prep points within 0.05 of 3/8.

## Frozen inputs (fill in)
| item | value |
|---|---|
| `configs/gates.yaml` sha256 | |
| `data/main` checksum | |
| `data/chain_onfam` checksum | |
| `data/chain_strong` checksum | |
| model configuration (JEPAConfig JSON) | |
| hardware design (families, points, settings, shots, arms) | PLAN §8 |
| backend(s) | |

## Analysis plan (exact commands)
- J1: `python scripts/run_gate.py J1 --runs runs/v1_final/seed0 ... seed4`
- J2: `python scripts/train_jepa.py --data data/main --name v1_final --epochs 200 --seeds 5 --masked` then `python scripts/run_gate.py J2 --eval runs/v1_final/forecast_eval.json`
- J3: `python scripts/residual_eval.py --source hardware --shots-levels 0 512 256 ...` then `python scripts/run_gate.py J3 --eval evidence/hardware/residual_eval_all.json`
- H4: `scripts/depth_extrapolation.py` (to be written in M5; forecast from the $r=1$ and $r=2$ hardware records using the released model, compared with the direct $r=8$ estimate; MAE on $P_{\text{baryonic}}$, $P_{\text{meson}}$, $C_{\text{string}}$)
- H5: `scripts/resonance_eval.py --source hardware`

## Exclusion rules
- Hardware points with flag rate > 0.8 are excluded from J3/H4/H5 and listed in the paper.
- A hardware job whose calibration snapshot differs from the twin's snapshot (hash) is a new "day".
- No post-hoc change of shots levels, targets or eval steps.

## Signatures
Digonto (researcher) — date — commit — tag.
