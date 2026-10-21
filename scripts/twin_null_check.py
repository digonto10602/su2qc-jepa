#!/usr/bin/env python
"""Known-answer checks for a noiseless twin campaign (`run_twin.py --noise ideal`) and its residual evaluation.

Without noise every outcome is known in advance, so this tests the measurement pipeline (12-qubit sampling, bit order,
excitation flag, post-selection, estimators, residual scores) and the error signal's behaviour on a null:
  1. flag rate: the circuits conserve the single excitation, so every flag rate must be exactly 0;
  2. post-selected populations vs the ideal-circuit populations |c_k|^2: Pearson chi-square per point (bins with an
     expected count < 5 merged); under correct sampling the p-values are uniform on [0, 1];
  3. arms A and B are identical without noise: no score may separate them (AUROC near 0.5, within 3 sigma of the
     Mann-Whitney null spread); reference points (arm A, seed 0) are excluded because they are compared with themselves;
  4. Spearman of each score with the exact error, which here is only Trotter error plus shot noise (reported).
The pass criteria below are this script's own (stated in the output), not gate thresholds.
  python scripts/twin_null_check.py --records evidence/twin/ideal0/records.json \
      --residual evidence/twin/ideal0/residual_eval.json --out evidence/twin/ideal0/null_check.json
"""
import argparse
import json
import subprocess
import time
from pathlib import Path

import numpy as np
from scipy import stats

from su2qc_jepa.gates.j3_hardware import auroc, spearman

p = argparse.ArgumentParser()
p.add_argument("--records", required=True)
p.add_argument("--residual", required=True)
p.add_argument("--out", required=True)
a = p.parse_args()

rec = json.loads(Path(a.records).read_text())
res = json.loads(Path(a.residual).read_text())
pts = rec["points"]

# 1. flag rate
flags = np.array([q["flag_rate"] for q in pts])

# 2. populations: chi-square of the post-selected Z populations against |c_k|^2
pvals, chi = [], []
for q in pts:
    z = next(r for r in q["records"] if r["setting"] == "Z")
    n = int(round(q["p1"] * z["shots"]))
    obs_n = np.rint(np.array(q["pops"]) * n)
    exp_n = np.array(q["ideal_pops"]) * n
    big = exp_n >= 5
    o = np.append(obs_n[big], obs_n[~big].sum())
    e = np.append(exp_n[big], exp_n[~big].sum())
    if e[-1] < 5:  # merge the small-bin remainder into the smallest large bin
        j = int(np.argmin(e[:-1]))
        o[j] += o[-1]
        e[j] += e[-1]
        o, e = o[:-1], e[:-1]
    stat = float(((o - e) ** 2 / e).sum())
    chi.append(stat)
    pvals.append(float(stats.chi2.sf(stat, len(e) - 1)))
pvals = np.array(pvals)
ks = stats.kstest(pvals, "uniform")

# 3. and 4. scores from the residual evaluation
rp = res["points"]
levels = sorted({q["shots"] for q in rp})
full = max(levels)
arms_rows = {}
for lvl in levels:
    sel = [q for q in rp if q["shots"] == lvl and not (q["arm"] == "A" and q["seed"] == 0)]
    lab = np.array([q["arm"] == "B" for q in sel])
    nA, nB = int((~lab).sum()), int(lab.sum())
    sigma = float(np.sqrt((nA + nB + 1) / (12 * nA * nB))) if nA and nB else float("nan")
    row = {"n_A": nA, "n_B": nB, "null_sigma": sigma}
    for score in ("jepa_twin", "raw_twin", "jepa_self", "jepa_t0", "flag_rate"):
        v = np.array([q[score] for q in sel], float)
        row[f"auroc_{score}"] = auroc(v, lab)
        row[f"spearman_{score}_vs_exact_error"] = spearman(v, [q["exact_error"] for q in sel])
    arms_rows[str(lvl)] = row
fr = arms_rows[str(full)]
arm_dev = {s: abs(fr[f"auroc_{s}"] - 0.5) / fr["null_sigma"] for s in ("jepa_twin", "raw_twin", "jepa_self", "jepa_t0")}

checks = {
    "flag_rate_exactly_zero": {"pass": bool(np.all(flags == 0)), "max_flag_rate": float(flags.max()), "n_points": len(flags)},
    "populations_match_ideal": {"pass": bool(ks.pvalue > 0.01 and (pvals < 1e-3).sum() <= max(1, len(pvals) // 200)),
                                "criterion": "KS test of the chi-square p-values against uniform has p > 0.01, and at most "
                                             "max(1, n/200) points have p < 1e-3",
                                "ks_statistic": float(ks.statistic), "ks_pvalue": float(ks.pvalue),
                                "fraction_p_below_0.01": float((pvals < 0.01).mean()), "n_p_below_1e-3": int((pvals < 1e-3).sum()),
                                "min_p": float(pvals.min()), "n_points": len(pvals)},
    "arms_not_separated": {"pass": bool(all(d <= 3 for d in arm_dev.values())),
                           "criterion": f"|AUROC - 0.5| <= 3 null sigma at full shots ({full}) for every score",
                           "deviation_in_sigma": arm_dev},
    "observables_vs_ideal": {"max_abs_twin_minus_ideal": float(max(np.abs(np.array(q["twin_est"]) - np.array(q["ideal_circuit"])).max()
                                                                   for q in pts)),
                             "max_abs_ideal_minus_exact": float(max(np.abs(np.array(q["ideal_circuit"]) - np.array(q["exact"])).max()
                                                                    for q in pts)),
                             "note": "twin - ideal is shot noise only; ideal - exact is the Strang (Trotter) error"},
}
out = {"what": "noiseless twin known-answer checks", "records": a.records, "residual": a.residual, "noise": rec.get("noise"),
       "shots": rec.get("shots"), "K": rec["K"], "n_points": len(pts), "checks": checks, "by_shots_level": arms_rows,
       "all_pass": all(c.get("pass", True) for c in checks.values()),
       "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()}
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
Path(a.out).write_text(json.dumps(out, indent=1))
for k, c in checks.items():
    print(f"{'PASS' if c.get('pass', True) else 'FAIL':5s} {k}: " + ", ".join(f"{kk}={vv}" for kk, vv in c.items() if kk not in ("pass", "criterion", "note")))
print("all pass:", out["all_pass"], "| wrote", a.out)
