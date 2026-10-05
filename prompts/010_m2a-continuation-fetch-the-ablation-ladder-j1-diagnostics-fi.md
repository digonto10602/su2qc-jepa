---
id: prompts/010
title: 'M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card'
series: prompts
created_utc: '2026-10-05T17:42:30Z'
author: claude-code
milestone: M2
status: active
supersedes: null
superseded_by: null
---

# M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card

**Session protocol:** follow `CLAUDE.md` §2 (start: env check, graph freshness, read the latest report; end: tests, gate, graph refresh, numbered report, artifact check, commit).
**Read first:** `~/.claude/CLAUDE.md`, `CLAUDE.md`, the current plan (`plans/INDEX.md`, status active), `STATE.json`, the latest entry in `reports/INDEX.md`.

## Context
Session M2a (`prompts/002`, report `reports/010`) implemented the ladder options (EMA target, grounding weight, horizon curriculum; commit `0a76800`), ran the 10-epoch laptop check (`runs/v1_check`, local) and queued the baseline and all ladder rungs on Perlmutter, each at commit `0a76800`, 5 seeds, 200 epochs, `data/main` rebuilt on Perlmutter from its manifest:

| job | run | change vs base |
|---|---|---|
| `jobs/002` | `runs/v1_base` | none (`--w-sigreg 0.5` default; also `--masked`) |
| `jobs/003` | `runs/v1_wsigreg2` | `--w-sigreg 2` |
| `jobs/004` | `runs/v1_wsigreg5` | `--w-sigreg 5` |
| `jobs/005` | `runs/v1_latent32` | `--latent 32` |
| `jobs/006` | `runs/v1_ema` | `--ema-target 0.996` |
| `jobs/007` | `runs/v1_wground3` | `--w-ground 3` |
| `jobs/008` | `runs/v1_curriculum` | `--curriculum-epochs 50` |

The rung `--w-sigreg 0.5` of prompts/002 is the base itself (the CLI default is 0.5).

**Open decision (Digonto, before this session or before the 16 Oct preregistration):** `evidence/J1_training/ceiling_main.json` shows that no function of one clean observation predicts the energy better than $R^2=0.914$ on the validation split (ridge, kNN, gradient-boosted trees, MLP), because the energy contains the hopping and plaquette expectation values and the couplings, which are not in the observation. With the couplings added the ceiling is $0.994$. The J1 row "energy $R^2\ge0.99$" is therefore unreachable for the encoder as specified. Thresholds change only by a decision record (`decisions/`); this session does not change `configs/gates.yaml` on its own.

## Tasks
1. `python scripts/jobs/status.py`; for each COMPLETED job `python scripts/jobs/fetch.py NNN`. Compare each fetched `data/main` checksum with the laptop's `73fff8e5a7b7` and report it (this is the laptop-vs-Perlmutter reproducibility check of report 009, Problem 2). A FAILED job (program error) is fixed in code and queued again as a new number; TIMEOUT/OOM are resubmitted by the worker.
2. J1 per rung, unmasked seeds only: `python scripts/run.py -- python scripts/run_gate.py J1 --runs runs/<rung>/seed0 runs/<rung>/seed1 runs/<rung>/seed2 runs/<rung>/seed3 runs/<rung>/seed4` (do not use the glob `seed*`: it also matches `seed*_masked`). Report the masked base seeds separately, as information.
3. Ablation table: per rung, min over seeds of effective rank, the four grounding $R^2$, max semigroup residual, isotropy, and the forecast MAE from `forecast_eval.json`. Chosen configuration = the first rung (ladder order) that passes every J1 row that is reachable; if none passes, the best rung by rank, and J1 PARTIAL with the diagnosis (which loss term dominates; latent spectrum).
4. Figure: `python scripts/new_artifact.py figures "J1 effective rank and grounding R2 vs epoch" --ext .png` gives the path; then `python scripts/run.py -- python scripts/plot_j1_diagnostics.py --out <path> --rungs v1_base v1_wsigreg2 v1_wsigreg5 v1_latent32 v1_ema v1_wground3 v1_curriculum`.
5. `docs/MODEL_CARD.md`: architecture, parameter count (count it in code), training time per rung on the A100 (from the fetched job status), the chosen configuration and why, the energy ceiling.

## Definition of done
- every ladder job COMPLETED and fetched, or its failure explained; J1 run once per rung (ledger rows in `evidence/GATE_LEDGER.md`)
- figure and its JSON sidecar committed; `docs/MODEL_CARD.md` written
- session report created with `scripts/new_artifact.py reports ...`, `scripts/check_artifacts.py` OK, `STATE.json` updated

## Out of scope / stop conditions
- Changing `configs/gates.yaml` or the J1 rows without a decision record.
- Preregistration (M2b, 16 Oct, `prompts/002` items 6–8).
- Stop on any `CLAUDE.md` §2 stop condition.
