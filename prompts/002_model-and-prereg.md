---
id: prompts/002
title: M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M2
status: active
supersedes: null
superseded_by: null
---

# M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)

**Session protocol:** `CLAUDE.md` §2 — start with `scripts/env_check.py` and `bash scripts/graph_update.sh --check` (read the first screen of `graphify-out/GRAPH_REPORT.md`); use `graphify query/explain/affected` before broad searches; end with tests, the gate, `bash scripts/graph_update.sh`, a numbered session report (`python scripts/new_artifact.py reports "M2: <result>" --milestone M2`), `scripts/check_artifacts.py` OK, `STATE.json`, and a final `chore(graph):` commit. Any new prompt you write for a later session goes into `prompts/` via `scripts/new_artifact.py prompts ...`; every figure via `scripts/new_artifact.py figures ... --ext .png`.

**Read first:** `CLAUDE.md`, `plans/001_gauge-jepa-p-v2.md` §5, §9, §10 (W2), `src/su2qc_jepa/models/jepa.py`, `models/train.py`.

## Session M2a — make the model healthy
1. Quick sanity check, light: `python scripts/run.py -- python scripts/train_jepa.py --data data/main --name v1_check --epochs 10 --seeds 1`. Then the baseline run, which the runner sends to Perlmutter by itself (commit and push the code first): `python scripts/run.py --push --prompt prompts/002 -- python scripts/train_jepa.py --data data/main --name v1_base --epochs 200 --seeds 5 --masked` (exit code 10 = queued; the job rebuilds `data/main` on Perlmutter from its manifest). Follow with `python scripts/jobs/status.py`; when COMPLETED, `python scripts/jobs/fetch.py NNN` and compare the fetched dataset checksum with the laptop's. If the worker looks stopped (status warns), say so in the report, run 1 seed on the laptop through `run.py` with `--epochs 30` instead, and stop there.
2. `python scripts/run.py -- python scripts/run_gate.py J1 --runs runs/v1_base/seed*` — expect FAIL on effective rank and some $R^2$ rows at first (the smoke run gave rank 4–6/16).
3. Ablation ladder through the queue (one `run.py --push -- python scripts/train_jepa.py ...` per rung, several rungs may be queued at once), one change at a time, each with 5 seeds, each logged as `runs/v1_<change>/`: (1) `--w-sigreg` ∈ {0.5, 2, 5}; (2) `--latent 32`; (3) add an EMA target encoder with stop-gradient (implement `JEPAConfig.ema_target: float | None` in `jepa.py`; the target latent uses the EMA copy; SIGReg stays on the context latent); (4) `w_ground` 3.0; (5) horizon curriculum (train 50 epochs on horizons (1,2), then all). Stop at the first configuration that passes all J1 rows; keep going through the ladder only to fill the ablation table.
4. Diagnostics figure (`python scripts/new_artifact.py figures "J1 effective rank and grounding R2 vs epoch" --ext .png` gives the path): effective rank and grounding $R^2$ vs epoch for every ladder rung.
5. Write `docs/MODEL_CARD.md`: architecture, parameter count, training time, the chosen configuration and why.

## Session M2b — preregistration (16 Oct)
6. Freeze `configs/gates.yaml` (no threshold changes after this point without a decision record in `decisions/`). Write `docs/PREREGISTRATION.md` from the template: hypotheses H1–H5, exact analysis commands, exclusion rules (e.g. hardware points with flag rate > 0.8 are excluded from J3 and reported), the dataset checksums, the model configuration hash.
7. `git tag -a prereg-2026-10-16 -m "preregistration"`; `git push --tags`.
8. Run J1 on the chosen configuration; commit evidence; `STATE.json`, the session report.

## Expected
J1 PASS with rank 10–14/16, $R^2>0.99$ (energy, $C_{\text{string}}$), semigroup residual < 1e-3. If the ladder ends without a pass: J1 PARTIAL with the best run and a one-paragraph diagnosis (which loss term dominates, latent spectrum plot).
