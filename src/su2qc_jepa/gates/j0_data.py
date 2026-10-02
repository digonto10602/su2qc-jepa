"""Gate J0 - data integrity: physics fingerprints, two routes, estimator bias, twin seeds, Krylov window, splits."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ..data.records import estimate_chain, estimate_diagonal, sample_exact_chain, sample_exact_diagonal
from ..physics import conventions as C
from ..physics.chain import ChainSpec
from ..physics.dynamics import evolve, krylov_error, lanczos, sector_restrict
from ..physics.observables import ObservableSet, named_states
from ..physics.plaquette import FullSpaceOperators, PlaquetteModel
from .ledger import GateResult, load_thresholds, write_gate

__all__ = ["run_j0"]


def run_j0(dataset_dir: str | Path | None = None, thresholds_path: str = "configs/gates.yaml", evidence_dir: str = "evidence",
           chain_K: int = 12, quick: bool = False) -> GateResult:
    th = load_thresholds(thresholds_path)["J0_data"]
    res = GateResult("J0_data")
    model = PlaquetteModel(0.5)
    obs = ObservableSet.primary(model)
    names = named_states(model)
    N4 = model.sector(4)
    # D1 fingerprints
    N = model.N_total()
    sectors = tuple(int((N == n).sum()) for n in (0, 2, 4, 6, 8))
    deg = tuple(int((model.excited_links() == n).sum()) for n in range(5))
    res.add("D1 state counts", (model.dim, sectors, deg) == (82, C.EXPECTED_SECTORS[0.5], C.EXPECTED_ELECTRIC_DEGENERACY_HALF),
            {"dim": model.dim, "sectors": sectors, "electric": deg}, {"dim": 82, "sectors": C.EXPECTED_SECTORS[0.5], "electric": C.EXPECTED_ELECTRIC_DEGENERACY_HALF})
    # D2 two routes + Gauss law
    HA = model.hamiltonian(C.POINT_PA)
    if quick:
        res.add_status("D2 two-route agreement", "NOT RUN", note="quick mode")
    else:
        F = FullSpaceOperators(0.5)
        Hf = F.hamiltonian(C.POINT_PA)
        worst = max(abs(F.gauss(v, a) @ Hf - Hf @ F.gauss(v, a)).max() for v in range(4) for a in range(3))
        Q = model.full_space_vectors()
        HB = (Q.conj().T @ Hf @ Q).toarray().real
        diff = float(np.abs(HA - HB).max())
        res.add("D2 two-route agreement", diff <= th["two_route_agreement_max"], diff, th["two_route_agreement_max"])
        res.add("D2 Gauss-law commutator", worst <= th["gauss_commutator_max"], float(worst), th["gauss_commutator_max"])
    # D3 estimator bias, both carriers, at a mid-window state
    H4 = sector_restrict(HA, N4)
    psi0 = np.zeros(len(N4))
    psi0[list(N4).index(names["S3"])] = 1
    psi = evolve(H4, psi0, np.array([1.5]))[0]
    full = np.zeros(model.dim, dtype=complex)
    full[N4] = psi
    exact = obs.expectation(full)
    rng = np.random.default_rng(np.random.SeedSequence(12345))
    S, M = int(th["estimator_shots"]), int(th["estimator_trials"])
    ests = np.array([estimate_diagonal(sample_exact_diagonal(full, S, rng), obs)[0] for _ in range(M)])
    se = ests.std(0, ddof=1) / np.sqrt(M) + 1e-12
    zmax_diag = float(np.max(np.abs(ests.mean(0) - exact) / se))
    res.add("D3 estimator bias (diagonal carrier)", zmax_diag <= th["estimator_bias_sigma"], zmax_diag, th["estimator_bias_sigma"],
            note=f"max |bias|/SE over {len(obs.names)} observables, S={S}, M={M}")
    kr = lanczos(H4, psi0, K=chain_K)
    c = kr.Q.T @ psi
    ests = np.array([estimate_chain(sample_exact_chain(c, S, rng), kr, obs, N4)[0] for _ in range(M)])
    se = ests.std(0, ddof=1) / np.sqrt(M) + 1e-12
    fullK = np.zeros(model.dim, dtype=complex)
    fullK[N4] = kr.Q @ c
    exactK = obs.expectation(fullK)
    zmax_chain = float(np.max(np.abs(ests.mean(0) - exactK) / se))
    res.add("D3 estimator bias (chain carrier, Z+X)", zmax_chain <= th["estimator_bias_sigma"], zmax_chain, th["estimator_bias_sigma"],
            note="against the K-truncated state")
    # D4 Krylov window
    times = np.linspace(0, 3.0, 25)
    err = float(np.abs(krylov_error(H4, psi0, times, kr, obs.diag[:, N4])["obs_err"]).max())
    res.add(f"D4 Krylov K={chain_K} reproduces P-A window t<=3", err <= th["krylov_obs_error_max"], err, th["krylov_obs_error_max"])
    # D5 twin seeds
    try:
        from ..twin.noise import heron_like_noise_model
        from ..twin.run import TwinRunner, twin_variance_check

        spec = ChainSpec.from_krylov(kr, 8, 0.375, 2)
        v = twin_variance_check(TwinRunner(heron_like_noise_model(8)), spec, shots=512, repeats=int(th["twin_distinct_repeats"]))
        res.add("D5 twin repeats independent", v["pass"], v["distinct_count_dicts"], th["twin_distinct_repeats"], note=f"sigma(p1)={v['sigma']:.3g}")
    except Exception as e:  # pragma: no cover
        res.add_status("D5 twin repeats independent", "NOT RUN", note=repr(e))
    # D6 split leakage + checksum
    if dataset_dir is not None:
        man = json.loads((Path(dataset_dir) / "manifest.json").read_text())
        meta = json.loads((Path(dataset_dir) / "meta.json").read_text())
        z = np.load(Path(dataset_dir) / "dataset.npz")
        fams = {f["name"]: f for f in man["config"]["families"]}
        train_idx = z["split_train"]
        leaks = 0
        for i in train_idx:
            f = fams[meta[i]["family"]]
            keys = (meta[i]["label"],) if f["heldout_by"] == "label" else (meta[i]["mu"], meta[i]["mu2"])
            leaks += int(any(abs(k - h) < 1e-9 for k in keys for h in f["heldout"]))
        res.add("D6 split leakage", leaks <= th["split_leakage_allowed"], leaks, th["split_leakage_allowed"], evidence=str(Path(dataset_dir) / "manifest.json"))
        res.add("D6 checksum recorded", bool(man.get("checksum_sha256")), man.get("checksum_sha256", "")[:12], "present")
    else:
        res.add_status("D6 split leakage", "NOT RUN", note="no dataset given")
    write_gate(res, evidence_dir)
    return res
