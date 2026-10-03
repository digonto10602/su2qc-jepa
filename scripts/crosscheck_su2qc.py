#!/usr/bin/env python
"""Cross-check the starter physics core ("route C", su2qc_jepa) against the project's verified `su2qc` code
(SU2ZX run section8_v0.5.0, routes 1 = spin network and 2 = Gauss kernel).  prompts/001 Part A.

    python scripts/run.py -- python scripts/crosscheck_su2qc.py [--su2qc-src PATH] [--out evidence/J0_data/crosscheck_su2qc.json]

The su2qc package is imported read-only from PATH (default: $SU2QC_SRC, else the SU2ZX checkout on the laptop).

Units.  su2qc works in lattice units, H = (g2/2) E + m M + T - 1/(2 g2) B with
    E = sum_l j_l(j_l+1),  M = sum_v (-1)^{x+y} n_v,  T = (1/2) sum_l (eta_l psi^dag U psi + h.c.),  B = Tr(U_sq + U_sq^dag).
Route C works in units of g_E:  H/g_E = cE E + cM M + cH (2T) + cB B.  The su2qc builders only take (g2, m), so the four
term matrices are recovered exactly by a linear solve over four builds and verified on a fifth, independent build; this
gives su2qc's Hamiltonian at any (cE, cM, cH, cB), including the off-family point P-S.  At P-A the native su2qc build
H(g2 = 2 g_E, m = mu g_E) / g_E is also compared directly (no term extraction).

Geometry.  Same vertices in both codes ((0,0),(1,0),(1,1),(0,1)).  Route-C links (la, l1, l2, l3) are su2qc link
indices (0, 3, 2, 1); eta, the plaquette loop and the mass signs then coincide.  A basis state is matched by
(link spins, occupations), which is unique at j_max = 1/2.

Comparisons per coupling point (tolerance 1e-10): (i) the 82 diagonal energies, (ii) the full sorted spectrum, (iii) the
38x38 N = 4 block (and the full 82x82 matrix) after the label permutation and a diagonal sign gauge D = diag(+-1)
(basis-state phase conventions differ between codes; D is fixed on a spanning tree of the coupling graph, so the
remaining entries -- every closed loop, including the plaquette -- are a genuine test), (iv) exact dynamics from S3 (all 38 sector populations and the route-C observables) at 12
times, (v) Lanczos coefficients (alpha_k, beta_k), k < 12, from S3 in the N = 4 sector.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

import numpy as np

from su2qc_jepa.physics import conventions as C
from su2qc_jepa.physics.dynamics import evolve, lanczos
from su2qc_jepa.physics.observables import ObservableSet, named_states
from su2qc_jepa.physics.plaquette import PlaquetteModel

DEFAULT_SU2QC_SRC = "/home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/runs/section8_v0.5.0_20260907T0628Z/src"
TOL = 1e-10
# route-C link order (la, l1, l2, l3) -> su2qc link index
C_TO_SU2QC_LINK = (0, 3, 2, 1)
# term extraction: four builds (g2, m) with independent coefficient vectors, one more build for verification
EXTRACT_POINTS = ((1.0, 0.0), (2.0, 0.0), (1.0, 1.0), (4.0, 0.0))
VERIFY_POINT = (3.0, 0.7)
# 12 times per point, in units of 1/g_E: the hardware window at P-A, the strong-coupling time scale at P-S
TIMES = {"P-A": 0.25 * np.arange(1, 13), "P-S": 2.0 * np.arange(1, 13)}
N_LANCZOS = 12


def import_su2qc(src: str):
    if not Path(src, "su2qc").is_dir():
        raise FileNotFoundError(f"su2qc package not found under {src}")
    sys.path.insert(0, src)
    from su2qc import conventions as cv
    from su2qc.ham import route_gausskernel, route_spinnet

    return cv, {"route1_spinnet": route_spinnet, "route2_gausskernel": route_gausskernel}


def su2qc_label_to_c(label) -> tuple:
    js, ns = label[0], label[1]
    return tuple(float(js[i]) for i in C_TO_SU2QC_LINK), tuple(int(n) for n in ns)


def extract_terms(route) -> tuple[dict[str, np.ndarray], list, float]:
    """Term matrices (E, M, T, B) of an su2qc route, in its own basis order, and the verification residual."""
    builds, basis = [], None
    for g2, m in EXTRACT_POINTS + (VERIFY_POINT,):
        H, b = route.build_hamiltonian(g2, m, 0.5)[:2]  # route 2 returns extra items; su2qc's compare.py uses [0], [1]
        if basis is None:
            basis = list(b)
        elif list(b) != basis:
            raise RuntimeError("su2qc basis order changed between builds")
        builds.append(np.asarray(H.toarray()))
    coef = np.array([[g2 / 2.0, m, 1.0, -1.0 / (2.0 * g2)] for g2, m in EXTRACT_POINTS])
    stack = np.stack(builds[:4]).reshape(4, -1)
    terms = np.linalg.solve(coef, stack).reshape(4, *builds[0].shape)
    E, M, T, B = terms
    g2, m = VERIFY_POINT
    resid = float(np.max(np.abs(g2 / 2.0 * E + m * M + T - B / (2.0 * g2) - builds[4])))
    return {"E": E, "M": M, "T": T, "B": B}, basis, resid


def sign_gauge(A: np.ndarray, B: np.ndarray, tol: float = 1e-8) -> np.ndarray:
    """D = diag(+-1) with D A D ~ B, fixed by walking the connectivity graph of B (one root per component)."""
    n = A.shape[0]
    d = np.zeros(n)
    for root in range(n):
        if d[root] != 0:
            continue
        d[root] = 1.0
        queue = deque([root])
        while queue:
            i = queue.popleft()
            for j in np.nonzero(np.abs(B[i]) > tol)[0]:
                if d[j] == 0 and abs(A[i, j]) > tol:
                    d[j] = np.sign(B[i, j] / A[i, j]) * d[i]
                    queue.append(j)
    d[d == 0] = 1.0
    return d


def compare_point(name: str, coup: C.Couplings, model: PlaquetteModel, routes: dict, native: dict) -> dict:
    Hc = model.hamiltonian(coup)
    idx4 = model.sector(4)
    s3 = named_states(model)["S3"]
    s3_local = int(np.nonzero(idx4 == s3)[0][0])
    obs = ObservableSet.primary(model)
    times = TIMES[name]
    out = {"couplings": dict(zip(("cE", "cM", "cH", "cB"), coup.as_tuple())), "times": times.tolist(), "routes": {}}

    psi_c = evolve(Hc[np.ix_(idx4, idx4)], np.eye(len(idx4))[s3_local], times)
    kc = lanczos(Hc[np.ix_(idx4, idx4)], np.eye(len(idx4))[s3_local], K=N_LANCZOS + 1)

    gauges = {}
    for rname, (terms, perm) in routes.items():
        cE, cM, cH, cB = coup.as_tuple()
        Hs = cE * terms["E"] + cM * terms["M"] + 2.0 * cH * terms["T"] + cB * terms["B"]
        imag = float(np.max(np.abs(Hs.imag)))
        Hs = Hs.real[np.ix_(perm, perm)]  # rows/cols now in route-C order
        r = {"max_imag_part": imag}
        # (i) diagonal energies
        r["i_diag_max_abs_dev"] = float(np.max(np.abs(np.diag(Hs) - np.diag(Hc))))
        # (ii) spectra
        r["ii_spectrum_max_abs_dev"] = float(np.max(np.abs(np.linalg.eigvalsh(Hs) - np.linalg.eigvalsh(Hc))))
        # (iii) N = 4 block up to permutation (labels) and sign gauge
        A, B4 = Hs[np.ix_(idx4, idx4)], Hc[np.ix_(idx4, idx4)]
        d = sign_gauge(A, B4)
        r["iii_N4_block_max_abs_dev"] = float(np.max(np.abs(d[:, None] * A * d[None, :] - B4)))
        r["iii_N4_block_raw_max_abs_dev"] = float(np.max(np.abs(A - B4)))
        r["iii_sign_flips"] = int(np.sum(d < 0))
        # the same check on the full 82x82 matrix (all N sectors); the gauge is kept for the native-build check below
        dfull = sign_gauge(Hs, Hc)
        r["iii_full82_max_abs_dev"] = float(np.max(np.abs(dfull[:, None] * Hs * dfull[None, :] - Hc)))
        gauges[rname] = dfull
        # (iv) dynamics from S3 (sign-gauge invariant: populations and diagonal-in-basis observables)
        psi_s = evolve(A, np.eye(len(idx4))[s3_local], times)
        pop_dev = float(np.max(np.abs(np.abs(psi_s) ** 2 - np.abs(psi_c) ** 2)))
        full_s = np.zeros((len(times), model.dim), complex)
        full_c = np.zeros((len(times), model.dim), complex)
        full_s[:, idx4], full_c[:, idx4] = psi_s, psi_c
        obs_dev = float(np.max(np.abs(obs.expectation(full_s) - obs.expectation(full_c))))
        r["iv_population_max_abs_dev"] = pop_dev
        r["iv_observable_max_abs_dev"] = obs_dev
        # (v) Lanczos coefficients from S3
        ks = lanczos(A, np.eye(len(idx4))[s3_local], K=N_LANCZOS + 1)
        r["v_alpha_max_abs_dev"] = float(np.max(np.abs(ks.alpha[:N_LANCZOS] - kc.alpha[:N_LANCZOS])))
        r["v_beta_max_abs_dev"] = float(np.max(np.abs(ks.beta[:N_LANCZOS] - kc.beta[:N_LANCZOS])))
        keys = [k for k in r if k.endswith("_dev") and "raw" not in k] + ["max_imag_part"]
        r["max_dev"] = max(r[k] for k in keys)
        r["pass"] = bool(r["max_dev"] <= TOL)
        out["routes"][rname] = r

    if name in native:
        # P-A only: su2qc's own on-family build, H(g2 = 2 gE, m = mu gE) / gE, no term extraction
        for rname, Hn in native[name].items():
            d = gauges[rname]  # same basis order and phases as the extracted terms
            out["routes"][rname]["native_build_max_abs_dev"] = float(np.max(np.abs(d[:, None] * Hn * d[None, :] - Hc)))
            out["routes"][rname]["pass"] &= bool(out["routes"][rname]["native_build_max_abs_dev"] <= TOL)

    out["route_C"] = {"alpha": kc.alpha[:N_LANCZOS].tolist(), "beta": kc.beta[:N_LANCZOS].tolist(),
                      "spectrum_N4": np.linalg.eigvalsh(Hc[np.ix_(idx4, idx4)]).tolist(),
                      "P_S3": (np.abs(psi_c[:, s3_local]) ** 2).tolist()}
    out["pass"] = all(r["pass"] for r in out["routes"].values())
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--su2qc-src", default=os.environ.get("SU2QC_SRC", DEFAULT_SU2QC_SRC))
    p.add_argument("--out", default="evidence/J0_data/crosscheck_su2qc.json")
    a = p.parse_args(argv)
    t0 = time.time()
    cv, mods = import_su2qc(a.su2qc_src)
    model = PlaquetteModel(0.5)

    # su2qc's frozen conventions must be the ones this script assumes
    assert tuple(cv.ETA) == (1, -1, 1, 1) and tuple(cv.PARITY) == (1, -1, 1, -1) and tuple(cv.N_VAC) == C.VACUUM_N
    assert tuple(cv.PLAQUETTE_SEQUENCE) == ((0, 1), (1, 1), (2, -1), (3, -1))
    assert all(cv.ETA[C_TO_SU2QC_LINK[l]] == C.LINK_ETA[l] for l in range(4))

    routes, extraction, native = {}, {}, {"P-A": {}}
    gE, mu = 2.0, C.RESONANCE_MU
    for rname, mod in mods.items():
        terms, basis, resid = extract_terms(mod)
        labels = [su2qc_label_to_c(b) for b in basis]
        if len(set(labels)) != len(labels):
            raise RuntimeError(f"{rname}: labels are not unique")
        perm = np.array([labels.index((b.jconf, b.Nconf)) for b in model.basis])  # route-C index -> su2qc index
        routes[rname] = (terms, perm)
        Hn = mod.build_hamiltonian(2.0 * gE, mu * gE, 0.5)[0]
        native["P-A"][rname] = (np.asarray(Hn.toarray()).real / gE)[np.ix_(perm, perm)]
        extraction[rname] = {"dim": len(basis), "verify_point_g2_m": VERIFY_POINT, "verify_max_abs_residual": resid,
                             "pass": bool(resid <= TOL and len(basis) == model.dim)}

    points = {"P-A": C.POINT_PA, "P-S": C.POINT_PS}
    res = {name: compare_point(name, coup, model, routes, native) for name, coup in points.items()}
    status = "PASS" if all(r["pass"] for r in res.values()) and all(e["pass"] for e in extraction.values()) else "FAIL"

    def git(*args):
        r = subprocess.run(["git", *args], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None

    su2qc_head = subprocess.run(["git", "-C", a.su2qc_src, "rev-parse", "HEAD"], capture_output=True, text=True)
    record = {
        "status": status, "tolerance": TOL,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "seconds": round(time.time() - t0, 1),
        "commit": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain", "--untracked-files=no")),
        "machine": platform.node(), "command": " ".join([Path(sys.argv[0]).name, *(argv or sys.argv[1:])]),
        "su2qc_src": a.su2qc_src, "su2qc_git_head": su2qc_head.stdout.strip() or None,
        "link_map_routeC_to_su2qc": C_TO_SU2QC_LINK, "term_extraction": extraction, "points": res,
    }
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=1) + "\n")
    for name, r in res.items():
        for rname, rr in r["routes"].items():
            print(f"{name:4s} {rname:20s} max_dev={rr['max_dev']:.2e} sign_flips={rr['iii_sign_flips']:2d} "
                  f"{'PASS' if rr['pass'] else 'FAIL'}")
    for rname, e in extraction.items():
        print(f"term extraction {rname}: residual {e['verify_max_abs_residual']:.2e}")
    print(f"== crosscheck: {status} -> {out}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
