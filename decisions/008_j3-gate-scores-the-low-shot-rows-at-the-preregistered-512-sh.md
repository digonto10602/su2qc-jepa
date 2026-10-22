---
id: decisions/008
title: J3 gate scores the low-shot rows at the preregistered 512 shots
series: decisions
created_utc: '2026-10-22T16:46:34Z'
author: claude-code
milestone: M3
status: active
supersedes: null
superseded_by: null
---

# J3 gate scores the low-shot rows at the preregistered 512 shots

**Decided by:** Digonto, 2026-10-22 ("yes, use 512 shots with a decision record"). **Drafted by:** claude-code. **Kind:** the analysis code is aligned with the preregistration. No threshold, hypothesis or command changes. **Made before** any hardware J3 data exist; found during the twin rehearsal on the Kingston calibration (`jobs/026`).

## Decision
`src/su2qc_jepa/gates/j3_hardware.py: run_j3` takes the low-shot level from `configs/gates.yaml: J3_hardware.low_shot_level` (512). It raises an error if the evaluation file has no points at that level. Before this record it used the lowest shot level present in the file.

## Why
- **The preregistration says 512.** H3 (`docs/PREREGISTRATION.md` §1) reads "at 512 shots", and `configs/gates.yaml` sets `low_shot_level: 512`, frozen with sha256 `dbb29733…`. But the preregistered J3 command (§3) passes `--shots-levels 0 512 256` to `residual_eval.py`, so the gate code, taking the minimum, scored the Spearman and non-inferiority rows at **256** shots: the preregistered hypothesis and the code disagreed.
- **This aligns the code with the frozen text** (the hypothesis and the frozen gate file) and changes nothing that was preregistered. 256 shots remain evaluated and are reported in the report-only Spearman rows.
- **The rehearsal outcome on the Kingston twin is the same either way:** Spearman(`jepa_twin`) 0.31 at 256 and 0.33 at 512, both below 0.7 and below `raw_twin`. So the choice could not have been steered by a favourable result.

## Alternatives considered
- **Keep the code and treat 256 as the low-shot level:** this contradicts H3 and the frozen `gates.yaml`. Rejected.
- **Drop 256 from the preregistered command:** this would change a preregistered command and lose a reported level. Rejected.

## Consequences
- Test `tests/test_pipeline.py::test_j3_uses_the_preregistered_low_shot_level`.
- The twin rehearsals already recorded at 256 (`jobs/026`, `jobs/027`) are re-scored with the corrected gate. Both versions stay in the ledger, the newer one marked as following `decisions/008`.
- `docs/PREREGISTRATION.md` §7 lists this record.
