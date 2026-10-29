---
id: prompts/011
title: 'M3 exploratory: J1 training improvement experiments'
series: prompts
created_utc: '2026-10-29T00:12:47Z'
author: planner
milestone: M3
status: active
supersedes: null
superseded_by: null
---

# M3 exploratory: J1 training improvement experiments

**Session protocol:** follow `CLAUDE.md` §2 (start: env check, graph freshness, read the latest report; end: tests, gate, graph refresh, numbered report, artifact check, commit).
**Read first:** `~/.claude/CLAUDE.md`, `CLAUDE.md`, the current plan (`plans/INDEX.md`, status active), `STATE.json`, the latest entry in `reports/INDEX.md`, and **`reports/017`** (the research and comparison this prompt executes; §1 diagnosis, §3 table, §4 shortlist).

## Context
J1 (training health) is FAIL after 14 configurations and a fresh-seed confirmation (`reports/016` §6.3): energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$ $R^2$ pass everywhere; the effective rank (min over seeds, threshold 8 of 16) and the semigroup residual (max over seeds, threshold $10^{-3}$) trade off and each has failed on single seeds at the working point $(w_{\text{sigreg}},w_{\text{sg}})=(3,10)$: `v1_wsig3_wsg10` PASS on its selection seeds, `v1_confirm` semigroup $1.48\times10^{-3}$ on seed 3, `v1_final` rank 7.967 on seed 4. J2 (forecasting) is FAIL at strong coupling ($P_{\text{baryonic}}$ MAE 0.105 / 0.123 vs 0.05). Both verdicts are preregistered and **stand**; everything in this prompt is **EXPLORATORY / post-hoc** and is labelled so in every file name, commit message, ledger location and report sentence.

`reports/017` §1 adds three measured facts: (i) the training semigroup MSE is about 6x smaller than the validation residual, and the validation split holds out *couplings*, so the inconsistency is a held-out-coupling generalisation problem of the predictor's action conditioning; (ii) the clean observables themselves have effective rank 11.2, so rank $\ge8$ is compression, not over-stretching, and two latent dimensions are nearly dead (std 0.34, 0.42); (iii) the SIGReg estimate with 64 random projections has 10 % relative noise against 2.2 % with 1024.

Base configuration for every arm: `v2_final` (`decisions/010`): `--w-sigreg 3 --w-semigroup 10 --physics-only`, latent 16, AdamW lr $2\times10^{-3}$, wd $10^{-5}$, batch 64, cosine schedule, clip 1.0. `v2_final` itself (`jobs/033`) is the 200-epoch reference; fetch it first (`reports/016` §9 step 2).

Hard constraints (from Digonto, 28/29 Oct): no threshold or row definition in `configs/gates.yaml` changes; nothing touches `ObservationSpec`, `conventions.py` or the dataset checksums; new flags default to the current behaviour so every old run and old checkpoint reproduces; selection seeds and confirmation seeds are different master seeds (`numpy.random.SeedSequence`, no adjacent integers); desktop budget for the whole programme $\le8$ h (plan: 3.9–5.4 h); exploratory J1 records never go into `evidence/GATE_LEDGER.md`.

**Open decision for Digonto before task 3 (reports/017 problem 6):** the Markov predictor (arm S1) satisfies the semigroup identity by construction, so its semigroup row passes to float rounding. Digonto says whether such a pass may be reported "for information" next to the GRU results (then S1 is queued) or not (then S1 is dropped and S2 is the only semigroup arm). Do not queue S1 before the answer is in the session log.

## Tasks

### 1. Code changes (builder; `graphify affected "GaugeJEPA"`, `"ActionPredictor"`, `"run_j1"` first and run the tests it lists)
All defaults reproduce today's behaviour bit for bit; old checkpoints (`evidence/runs/v1_final/seed0/model.pt`) must still load with `JEPAConfig(**ck["jcfg"])` and `load_state_dict(strict=True)`.

| # | file / symbol | change | flag in `scripts/train_jepa.py` |
|---|---|---|---|
| 1a | `src/su2qc_jepa/models/jepa.py: JEPAConfig` | new fields `predictor: str = "gru"` (`"gru"` or `"markov"`, `ValueError` otherwise), `semigroup_mix: int = 0`, `w_var: float = 0.0`, `w_cov: float = 0.0`, `var_gamma: float = 1.0`, `var_eps: float = 1e-4` | `--predictor {gru,markov}`, `--semigroup-mix N`, `--w-var`, `--w-cov`, `--sigreg-projections` (field exists, default 64) |
| 1b | `jepa.py: class MarkovPredictor(nn.Module)` | same constructor as `ActionPredictor(latent_dim, action_dim, action_embed, hidden)`; `forward(s, actions) -> (B, k, d)`: for each action token in order, `h = tanh(init(s))`, `h = cell(embed(a_t), h)` with `nn.GRUCell(action_embed, hidden)`, `s = out(h) + skip(s)`, collect `s`. Composition is then exact: $P(s,[a_1,a_2])=P(P(s,a_1),a_2)$. `GaugeJEPA.__init__` picks the class from `cfg.predictor`. | `--predictor markov` |
| 1c | `jepa.py: GaugeJEPA.loss` semigroup block | if `cfg.semigroup_mix > 0` and the real semigroup term exists: for each of `semigroup_mix` draws, `perm = torch.randperm(n, generator=generator, device=...)`, `alpha ~ U(0,1)` per row from `generator`, `a_mix = a2m.clone(); a_mix[..., 1:] = alpha*a2m[..., 1:] + (1-alpha)*a2m[perm][..., 1:]` (the $\Delta t$ column 0 is kept from the first partner; columns 1–3 are $c_M,c_H,c_B$), then the same `two / one / comp` MSE on `s0[m]` with `a_mix`; `losses["semigroup"]` becomes the mean of the real term and the mixed terms. The weight stays `w_semigroup`. | `--semigroup-mix 1` |
| 1d | `jepa.py: vicreg_terms(z, gamma, eps) -> (v, c)` | VICReg eq. 1 and 4 (arXiv:2105.04906): $v=\frac1d\sum_j\max(0,\gamma-\sqrt{\mathrm{Var}(z_j)+\epsilon})$, $c=\frac1d\sum_{i\ne j}C_{ij}^2$ with $C$ the batch covariance of the centred latents. In `loss`, only when `w_var>0 or w_cov>0`: compute on `zall` (the same batch SIGReg sees), add `losses["var"]`, `losses["cov"]`, and `w_var*var + w_cov*cov` to `losses["total"]`. With both weights 0 the keys are absent and the history schema is unchanged. | `--w-var 1 --w-cov 0.1` |
| 1e | `scripts/train_jepa.py` | `--skip-baselines` (default off): skip ridge / autoregressive / supervised-MLP; `forecast_eval.json` then holds `jepa` (and `jepa_masked`) only and the key `"baselines": "skipped"`. New flags flow into `jcfg` and `args.json` as the existing ones do. | `--skip-baselines` |
| 1f | `scripts/run_gate.py` | `--evidence-dir` (default `evidence`), passed to `run_j1(..., evidence_dir=...)` (the parameter already exists). Exploratory J1 runs use `--evidence-dir evidence/exploratory`. | – |

Note for the report (`reports/017` §5): new `JEPAConfig` fields change the `scripts/prereg_hashes.py` hash of *new* checkpoints even at default values; the frozen hash stays verifiable on `evidence/runs/v1_final/seed0/model.pt`. Do not change the hash script in this session.

### 2. Unit tests (builder; `tests/test_jepa_options.py`, fast, fixed seeds, small `generate_dataset` as in `tests/test_pipeline.py::test_jepa_ema_target_and_curriculum`)
- `test_markov_predictor_composes_exactly`: random `s (B,16)`, actions `(B,2,4)`; `rel = mean((P(s,[a1,a2]) - P(P(s,a1),a2))^2) / mean(P(s,[a1,a2])^2) < 1e-10`; output shape equals the GRU predictor's.
- `test_default_config_is_unchanged`: `JEPAConfig(obs_dim=24)` has `predictor=="gru"`, `semigroup_mix==0`, `w_var==w_cov==0.0`, `sigreg_projections==64`; `loss()` returns exactly the keys `pred, sigreg, ground, semigroup, total` and `total == w_pred*pred + w_sigreg*sigreg + w_ground*ground + w_semigroup*semigroup` (`torch.allclose`, `atol 1e-7`).
- `test_old_checkpoint_loads`: `ck = torch.load("evidence/runs/v1_final/seed0/model.pt", weights_only=False)`; `GaugeJEPA(JEPAConfig(**ck["jcfg"])).load_state_dict(ck["state_dict"], strict=True)` succeeds and `encode` of a fixed input is finite.
- `test_semigroup_mix`: with `semigroup_mix=2` the loss is finite and `losses["semigroup"]` differs from `semigroup_mix=0` on the same batch and seed; with `predictor="markov"` and `semigroup_mix=2` the semigroup term is `< 1e-10`; the mixed actions keep column 0 and lie between the two partners' values in columns 1–3 (test the helper on a hand-made batch).
- `test_vicreg_terms`: a batch with per-dimension std $>\gamma$ gives $v=0$; a batch with one constant dimension gives $v=\gamma/d$ (to $\sqrt\epsilon/d$); a 2-d hand-made batch with known covariance gives $c=2C_{12}^2/d$; gradients finite.
- `test_sigreg_projections_flag` and `test_skip_baselines_flag`: run `scripts/train_jepa.py` by `subprocess` on a tiny dataset with `--epochs 1 --seeds 1 --sigreg-projections 128 --skip-baselines --predictor markov --semigroup-mix 1 --w-var 1 --w-cov 0.1`; `args.json` and `seed0/model.pt["jcfg"]` carry the values; `forecast_eval.json["baselines"] == "skipped"`.
- `test_run_gate_evidence_dir`: `run_j1([...], evidence_dir=tmp_path)` writes `tmp_path/J1_training/*.json` and `tmp_path/GATE_LEDGER.md` and leaves `evidence/GATE_LEDGER.md` untouched (compare bytes before/after).

`python scripts/run.py -- python -m pytest -q` all green; `ruff check src tests scripts` clean; `bash scripts/graph_update.sh`; commit `model: exploratory J1 options (markov predictor, semigroup-mix, VICReg terms, sigreg projections flag; defaults unchanged) (prompts/011)`, push.

### 3. Screening stage (paired design: one master seed for every arm, so seeds are matched)
Common flags: `--data data/main --epochs 100 --seeds 3 --w-sigreg 3 --w-semigroup 10 --physics-only --skip-baselines --master-seed 14142135`. Queue with `python scripts/run.py --push --where desktop --prompt prompts/011 --name <run name> -- python scripts/train_jepa.py <common flags> --name <run name> <arm flag>`; all five may be queued at once (the worker runs them one at a time). About 0.25 h each (10 min training at 2 s/epoch/seed from `jobs/019`, plus the dataset rebuild).

| job | run name | arm flag | targets |
|---|---|---|---|
| S0 | `x_s0_base` | (none) | screening-protocol baseline |
| S1 | `x_s1_markov` | `--predictor markov` | semigroup (only after Digonto's answer, see Context) |
| S2 | `x_s2_mix` | `--semigroup-mix 1` | semigroup on held-out couplings |
| S3 | `x_s3_varcov` | `--w-var 1 --w-cov 0.1` | rank (dead dimensions, anisotropy) |
| S4 | `x_s4_proj1024` | `--sigreg-projections 1024` | rank (less noisy regulariser) |

For each fetched run: `python scripts/jobs/fetch.py NNN`; copy `runs/<name>/args.json`, `forecast_eval.json`, `seed{0,1,2}/history.json` into `evidence/exploratory/runs/<name>/`; then `python scripts/run.py --no-queue --threads 1 -- python scripts/run_gate.py J1 --runs evidence/exploratory/runs/<name>/seed0 evidence/exploratory/runs/<name>/seed1 evidence/exploratory/runs/<name>/seed2 --evidence-dir evidence/exploratory` (this exits 1 on FAIL; that is a result, not an error). Tabulate per arm: rank min/max, the four $R^2$ mins, semigroup max/min, final `pred` loss (seed mean), JEPA MAE (seed mean) per family at +4/+8 for the three targets. Model files of screening runs are not committed.

**Decision rules, fixed now (3 seeds, final epoch 100, compared with S0):**
- *Semigroup arm "changes anything"* (S1, S2): arm max $<$ S0 min (non-overlapping ranges) **and** arm max $<0.5\times$ S0 max.
- *Rank arm "changes anything"* (S3, S4): arm min $>$ S0 max **and** arm min $-$ S0 min $\ge0.3$ (ten times the measured tail noise sd 0.03).
- *Guardrails, all required for an arm to advance:* no NaN; the four $R^2$ mins at or above the gate thresholds; for semigroup arms rank min $\ge$ S0 min $-0.2$; for rank arms semigroup max $\le1.5\times$ S0 max; JEPA MAE (seed mean, each target, each horizon) on-family $\le$ S0 $+0.005$ and strong coupling $\le$ S0 $+0.010$. Justification: on-family JEPA is 0.032 against autoregressive 0.030 at +4 (`reports/016` §6.5), so 0.005 is the scale at which the non-inferiority row flips; at strong coupling the error is 0.105 against a 0.05 bound, so 0.010 is a 10 % change, well above the step-to-step noise of a 3-seed mean (assumption: the 5-seed spread of `v1_final` MAE is not recorded).
- *Combination (S5):* if at least one semigroup arm and at least one rank arm pass their rules and guardrails, queue `x_s5_combo` = best semigroup arm flag + best rank arm flag (same common flags and master seed). If S1 and S2 both pass, prefer S2 (keeps the row's meaning); run S1's combination too only if Digonto allowed S1 and budget remains. If no arm passes its rule, skip S5 and go to the report with outcome NO CHANGE.

### 4. Confirmation stage (fresh master seeds, full protocol)
Candidates (at most two): the combo if it passes both rules, otherwise the best single passing arm per row. Command: `python scripts/run.py --push --where desktop --prompt prompts/011 --name <name> -- python scripts/train_jepa.py --data data/main --name <name> --epochs 200 --seeds 5 --masked --w-sigreg 3 --w-semigroup 10 --physics-only <arm flags> --master-seed 17320508` (second candidate: `--master-seed 22360679`). About 1.2 h each. Fetch as above (also `seed*_masked/history.json`), J1 in information mode under `evidence/exploratory`, commit `seed0/model.pt` as well (`evidence/exploratory/runs/<name>/seed0/model.pt`).
**Success rule (fixed now):** all J1 rows PASS on all 5 seeds at epoch 200 **and** J2 guardrails against `v2_final`'s `forecast_eval.json` (on-family $\le+0.005$, strong $\le+0.010$ per target and horizon, seed means) **and** the count of targets on which JEPA is within $1.1\times$ ridge and within $1.1\times$ autoregressive, per family and horizon, is not lower than `v2_final`'s.

### 5. Replication (one more fresh master seed)
The confirmed candidate again with `--master-seed 26457513` (spare: 33166247), same command and success rule. Outcome labels: **CONFIRMED** (both fresh master seeds pass), **FRAGILE** (one of two), **NO CHANGE** (none). Only CONFIRMED may lead to a proposal; the proposal is a `decisions/` record (deviation D4: new J3 model, J1/J2 verdicts unchanged) written for Digonto's approval and never acted on in this session.

### 6. Session report
`python scripts/new_artifact.py reports "M3 exploratory: J1 improvement arms — <outcome>" --milestone M3`; template order; a table of every arm with the rule outcomes; the decision rules quoted verbatim before the numbers; desktop hours used (sum of `elapsed_hours` from the job status files); the list of seeds used; the disclosure line about new config fields and the preregistration hash. `STATE.json`: add an `exploratory` entry under M3 with the job numbers and the outcome. Commit scoped (`model:`, `data:`, `docs:`, `chore(graph):`).

## Definition of done
- Task 1 and 2 merged: `pytest -q` green, `ruff` clean, graph FRESH, old checkpoint test passes.
- Jobs S0, S2, S3, S4 (and S1 if allowed) COMPLETED and fetched; per-arm tables in the report; the decision rules applied with PASS/FAIL per rule.
- If any arm advanced: confirmation and replication jobs COMPLETED and fetched with the success rule applied; otherwise the report states NO CHANGE with the numbers.
- No new block in `evidence/GATE_LEDGER.md`; all exploratory records under `evidence/exploratory/`.
- Desktop hours used reported and $\le8$ h.
- Session report created with `scripts/new_artifact.py reports ...`, `scripts/check_artifacts.py` OK, `STATE.json` updated.

## Out of scope / stop conditions
- Editing `configs/gates.yaml`, `docs/PREREGISTRATION.md` §1–§6, `ObservationSpec`, `conventions.py`, dataset generation, `scripts/prereg_hashes.py`.
- Re-tuning $(w_{\text{sigreg}}, w_{\text{sg}})$, EMA target, latent 32, horizon curriculum, $w_{\text{ground}}$ (`reports/017` §2, do-not-retry list).
- Stop and ask Digonto when: any arm produces NaN; S0 at 100 epochs has rank min $<7.0$ or semigroup max $>3\times10^{-3}$ (the screening protocol would not be representative of 200 epochs; re-plan); cumulative desktop time exceeds 8 h; the desktop worker shows no heartbeat for 24 h while jobs wait; anyone believes a threshold or the semigroup-row definition itself is wrong; a CONFIRMED result is in hand (the D4 decision is Digonto's).
- All `CLAUDE.md` §2 stop conditions.
