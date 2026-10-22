"""Fast end-to-end checks of the data, model, twin and gate paths (no hardware)."""
import json

import numpy as np
import pytest

from su2qc_jepa.data.records import (
    ObservationSpec,
    estimate_chain,
    estimate_diagonal,
    sample_exact_chain,
    sample_exact_diagonal,
)
from su2qc_jepa.data.trajectories import DatasetConfig, FamilyConfig, generate_dataset, load_dataset
from su2qc_jepa.gates.j3_hardware import auroc, spearman
from su2qc_jepa.gates.ledger import GateResult, write_gate
from su2qc_jepa.physics import conventions as C
from su2qc_jepa.physics.chain import ChainSpec, chain_amplitudes
from su2qc_jepa.physics.dynamics import evolve, lanczos, sector_restrict
from su2qc_jepa.physics.observables import ObservableSet, named_states
from su2qc_jepa.physics.plaquette import PlaquetteModel


@pytest.fixture(scope="module")
def setup():
    m = PlaquetteModel(0.5)
    obs = ObservableSet.primary(m)
    names = named_states(m)
    N4 = m.sector(4)
    H4 = sector_restrict(m.hamiltonian(C.POINT_PA), N4)
    psi0 = np.zeros(len(N4))
    psi0[list(N4).index(names["S3"])] = 1
    return m, obs, names, N4, H4, psi0


def test_estimators_unbiased(setup):
    m, obs, names, N4, H4, psi0 = setup
    psi = evolve(H4, psi0, np.array([1.5]))[0]
    full = np.zeros(m.dim, dtype=complex)
    full[N4] = psi
    exact = obs.expectation(full)
    rng = np.random.default_rng(3)
    ests = np.array([estimate_diagonal(sample_exact_diagonal(full, 1024, rng), obs)[0] for _ in range(100)])
    se = ests.std(0, ddof=1) / 10 + 1e-12
    assert np.max(np.abs(ests.mean(0) - exact) / se) < 4.5
    kr = lanczos(H4, psi0, K=12)
    c = kr.Q.T @ psi
    ests = np.array([estimate_chain(sample_exact_chain(c, 1024, rng), kr, obs, N4)[0] for _ in range(100)])
    fullK = np.zeros(m.dim, dtype=complex)
    fullK[N4] = kr.Q @ c
    se = ests.std(0, ddof=1) / 10 + 1e-12
    assert np.max(np.abs(ests.mean(0) - obs.expectation(fullK)) / se) < 4.5


def test_observation_spec_roundtrip():
    spec = ObservationSpec(["a", "b"])
    v = spec.assemble(np.array([0.5, 0.25]), 0.1, "twin", "chain")
    parts = spec.split(v)
    assert parts["obs"].tolist() == [0.5, 0.25] and parts["flag"] == 0.1
    assert parts["source"].tolist() == [0, 1, 0] and parts["carrier"].tolist() == [0, 1]


def test_dataset_generation_and_splits(tmp_path):
    fam = FamilyConfig.onfamily(dts=(0.25,))
    cfg = DatasetConfig(n_traj=30, n_steps_min=6, n_steps_max=6, families=(fam, FamilyConfig.strong()), name="t")
    generate_dataset(cfg, tmp_path, verbose=False)
    d = load_dataset(tmp_path)
    assert d["ctx"].shape == (30, 7, d["manifest"]["obs_dim"])
    for i in d["split_train"]:
        mt = d["meta"][i]
        if mt["family"] == "onfam":
            assert mt["label"] not in fam.heldout
        else:
            assert mt["mu"] not in FamilyConfig.strong().heldout and mt["mu2"] not in FamilyConfig.strong().heldout
    assert len(d["manifest"]["checksum_sha256"]) == 64
    n = d["manifest"]["n_obs"]
    err = np.abs(d["ctx"][..., :n] - d["tgt"])[d["valid"]]
    assert err.mean() < 0.05


def test_dataset_fingerprint_is_exact_and_locates_differences(tmp_path):
    from su2qc_jepa.data.trajectories import dataset_fingerprint

    cfg = DatasetConfig(n_traj=30, n_steps_min=4, n_steps_max=5, families=(FamilyConfig.onfamily(dts=(0.25,)),), name="t")
    generate_dataset(cfg, tmp_path, verbose=False)
    written = json.loads((tmp_path / "fingerprint.json").read_text())
    z = np.load(tmp_path / "dataset.npz")
    arrays = {k: z[k] for k in ("ctx", "tgt", "act", "valid", "energy")}
    assert json.loads(json.dumps(dataset_fingerprint(arrays))) == written  # recomputed from the saved arrays, bit for bit
    arrays["energy"] = arrays["energy"].copy()
    arrays["energy"][7, 1] += 1e-10
    moved = dataset_fingerprint(arrays)["arrays"]["energy"]
    d = np.abs(np.array(moved["row_sums"]) - np.array(written["arrays"]["energy"]["row_sums"]))
    assert np.argmax(d) == 7 and abs(d[7] - 1e-10) < 1e-12 and np.delete(d, 7).max() == 0.0
    assert moved["checksum_sha256"] != written["arrays"]["energy"]["checksum_sha256"]


def test_fingerprint_equivalence_verdict(tmp_path):
    """decisions/007: rounding-level target differences are EQUIVALENT; an input change or a 1e-11 target change is not."""
    import subprocess
    import sys
    from pathlib import Path

    from su2qc_jepa.data.trajectories import dataset_fingerprint

    cfg = DatasetConfig(n_traj=12, n_steps_min=4, n_steps_max=4, families=(FamilyConfig.onfamily(dts=(0.25,)),), name="t")
    generate_dataset(cfg, tmp_path, verbose=False)
    z = np.load(tmp_path / "dataset.npz")
    base = {k: z[k] for k in ("ctx", "tgt", "act", "valid", "energy")}

    def verdict(mod):
        arrays = {k: v.copy() for k, v in base.items()}
        mod(arrays)
        f = tmp_path / "b.json"
        f.write_text(json.dumps(dataset_fingerprint(arrays)))
        r = subprocess.run([sys.executable, "scripts/compare_fingerprints.py", str(tmp_path / "fingerprint.json"), str(f)],
                           capture_output=True, text=True, cwd=Path(__file__).resolve().parents[1])
        assert r.returncode == 0, r.stderr
        return "NOT EQUIVALENT" not in r.stdout and "EQUIVALENT" in r.stdout

    assert verdict(lambda a: a["tgt"].__iadd__(1e-14))            # rounding: every target value shifted by 1e-14
    assert not verdict(lambda a: a["tgt"].__setitem__((0, 0, 0), a["tgt"][0, 0, 0] + 1e-11))
    assert not verdict(lambda a: a["ctx"].__setitem__((0, 0, 0), a["ctx"][0, 0, 0] + 1e-15))  # inputs must be bit-identical


def test_chain_dataset_uses_chain_carrier(tmp_path):
    cfg = DatasetConfig(n_traj=6, n_steps_min=4, n_steps_max=4, families=(FamilyConfig.onfamily(gEs=(2.0,), dts=(0.25,)),),
                        starts=("S3",), quench_fraction=0.0, carrier="chain", name="c")
    generate_dataset(cfg, tmp_path, verbose=False)
    d = load_dataset(tmp_path)
    assert all(m["carrier"] == "chain" for m in d["meta"])


def test_jepa_trains_one_epoch(tmp_path):
    pytest.importorskip("torch")
    from su2qc_jepa.models.jepa import JEPAConfig
    from su2qc_jepa.models.train import TrainConfig, fit_probe, forecast_jepa, prepare_tensors, train_jepa

    cfg = DatasetConfig(n_traj=40, n_steps_min=6, n_steps_max=6, families=(FamilyConfig.onfamily(dts=(0.25,)),), name="t")
    generate_dataset(cfg, tmp_path, verbose=False)
    d = load_dataset(tmp_path)
    model, info = train_jepa(d, JEPAConfig(obs_dim=d["manifest"]["obs_dim"]), TrainConfig(epochs=2, log_every=100), tmp_path / "run")
    assert np.isfinite(info["final"]["total"])
    assert (tmp_path / "run" / "history.json").exists()
    tr = prepare_tensors(d, "train")
    W = fit_probe(model, tr)
    pred, truth = forecast_jepa(model, W, tr, 2)
    assert pred.shape == truth.shape == (len(d["split_train"]), 4, d["manifest"]["n_obs"])


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_training_and_baselines_run_on_device(tmp_path, device):
    """The whole train_jepa.py path (JEPA, probe, forecast, all three baselines) on one device.

    The CUDA case runs only where a usable GPU exists (Perlmutter); it is the regression test for jobs/002 and 003,
    which trained on the GPU and then crashed in baseline_autoregressive with tensors on two devices."""
    torch = pytest.importorskip("torch")
    if device == "cuda" and not torch.cuda.is_available():
        pytest.skip("no CUDA device")
    from su2qc_jepa.models.jepa import JEPAConfig
    from su2qc_jepa.models.train import (
        TrainConfig,
        baseline_autoregressive,
        baseline_ridge,
        baseline_supervised_mlp,
        fit_probe,
        forecast_jepa,
        prepare_tensors,
        train_jepa,
    )

    cfg = DatasetConfig(n_traj=40, n_steps_min=6, n_steps_max=6, families=(FamilyConfig.onfamily(dts=(0.25,)),), name="t")
    generate_dataset(cfg, tmp_path, verbose=False)
    d = load_dataset(tmp_path)
    model, _ = train_jepa(d, JEPAConfig(obs_dim=d["manifest"]["obs_dim"]), TrainConfig(epochs=1, log_every=100, device=device))
    tr = prepare_tensors(d, "train", device)
    assert tr["ctx"].device.type == device
    c = 2
    shape = (len(d["split_train"]), 6 - c, d["manifest"]["n_obs"])
    outs = {"jepa": forecast_jepa(model, fit_probe(model, tr), tr, c), "ridge": baseline_ridge(tr, tr, c),
            "autoregressive": baseline_autoregressive(tr, tr, c, epochs=1),
            "supervised_mlp": baseline_supervised_mlp(tr, tr, c, epochs=1)}
    for name, (pred, truth) in outs.items():
        assert isinstance(pred, np.ndarray) and pred.shape == truth.shape == shape, name
        assert np.isfinite(pred).all() and np.isfinite(truth).all(), name


def test_jepa_ema_target_and_curriculum(tmp_path):
    torch = pytest.importorskip("torch")
    from su2qc_jepa.models.jepa import GaugeJEPA, JEPAConfig
    from su2qc_jepa.models.train import TrainConfig, prepare_tensors, train_jepa

    cfg = DatasetConfig(n_traj=40, n_steps_min=6, n_steps_max=6, families=(FamilyConfig.onfamily(dts=(0.25,)),), name="t")
    generate_dataset(cfg, tmp_path, verbose=False)
    d = load_dataset(tmp_path)
    jcfg = JEPAConfig(obs_dim=d["manifest"]["obs_dim"], ema_target=0.9)
    # the target encoder starts as an exact copy, takes no gradient, and the prediction target carries no graph
    m = GaugeJEPA(jcfg)
    assert all(not p.requires_grad for p in m.target_encoder.parameters())
    assert all(torch.equal(a, b) for a, b in zip(m.target_encoder.parameters(), m.encoder.parameters()))
    tr = prepare_tensors(d, "train")
    assert not m.encode_target(tr["clean"]).requires_grad
    model, info = train_jepa(d, jcfg, TrainConfig(epochs=2, log_every=100, seed=12345, curriculum_epochs=1), tmp_path / "run")
    assert np.isfinite(info["final"]["total"])
    # after training the EMA copy lags the online encoder: different, but it moved away from its initial value
    torch.manual_seed(12345)  # same init as in train_jepa, which seeds torch with tcfg.seed before building the model
    m0 = GaugeJEPA(jcfg)
    tgt = list(model.target_encoder.parameters())
    assert any(not torch.equal(a, b) for a, b in zip(tgt, model.encoder.parameters()))
    assert any(not torch.equal(a, b) for a, b in zip(tgt, m0.target_encoder.parameters()))
    # one EMA step is the convex combination tau * target + (1 - tau) * online
    before = [p.clone() for p in tgt]
    model.update_target()
    for b, a, o in zip(before, model.target_encoder.parameters(), model.encoder.parameters()):
        assert torch.allclose(a, 0.9 * b + 0.1 * o, atol=1e-7)
    # the curriculum restricts the prediction loss to the requested horizons
    with torch.no_grad():
        l12 = model.loss(tr["ctx"], tr["clean"], tr["act"], tr["ground"], tr["valid"], horizons=(1, 2))["pred"]
        l1 = model.loss(tr["ctx"], tr["clean"], tr["act"], tr["ground"], tr["valid"], horizons=(1,))["pred"]
        lall = model.loss(tr["ctx"], tr["clean"], tr["act"], tr["ground"], tr["valid"])["pred"]
    assert float(l12) != float(lall) and float(l1) != float(l12)


def test_twin_runner_seed_independence(setup):
    pytest.importorskip("qiskit_aer")
    from su2qc_jepa.twin.noise import heron_like_noise_model
    from su2qc_jepa.twin.run import TwinRunner, twin_variance_check

    m, obs, names, N4, H4, psi0 = setup
    kr = lanczos(H4, psi0, K=6)
    spec = ChainSpec.from_krylov(kr, 6, 0.375, 1)
    v = twin_variance_check(TwinRunner(heron_like_noise_model(6)), spec, shots=256, repeats=3)
    assert v["pass"]


def test_ideal_twin_has_no_flags_and_matches_populations(setup):
    """Noiseless chain circuits conserve the single excitation (flag rate exactly 0) and the post-selected Z populations
    follow |c_k|^2 within shot noise - the bit order and the estimator are right."""
    pytest.importorskip("qiskit_aer")
    from scipy import stats

    from su2qc_jepa.data.records import estimate_chain
    from su2qc_jepa.twin.run import TwinRunner, chain_point_records

    m, obs, names, N4, H4, psi0 = setup
    kr = lanczos(H4, psi0, K=6)
    runner = TwinRunner(None, method="statevector")
    for r in (1, 3):
        spec = ChainSpec.from_krylov(kr, 6, 0.375, r)
        recs = chain_point_records(runner, spec, 4000, salt=f"ideal-{r}")
        _, flag, extra = estimate_chain(recs, kr, obs, N4)
        assert flag == 0.0
        p = np.abs(chain_amplitudes(spec)) ** 2
        n = np.rint(extra["pops"] * 4000)
        keep = p * 4000 >= 5
        o, e = np.append(n[keep], n[~keep].sum()), np.append(p[keep] * 4000, p[~keep].sum() * 4000)
        if e[-1] < 5:
            o, e = o[:-1], e[:-1]
        assert stats.chi2.sf(((o - e) ** 2 / e).sum(), len(e) - 1) > 1e-4


def test_noiseless_twin_pipeline_end_to_end(tmp_path):
    """run_twin.py --noise ideal -> residual_eval.py -> twin_null_check.py on a tiny case: the files chain together and the
    flag check passes (the statistical checks need the full campaign's size and are not asserted here)."""
    pytest.importorskip("qiskit_aer")
    pytest.importorskip("torch")
    import subprocess
    import sys
    from pathlib import Path

    from su2qc_jepa.models.jepa import JEPAConfig
    from su2qc_jepa.models.train import TrainConfig, train_jepa

    root = Path(__file__).resolve().parents[1]
    cfg = DatasetConfig(n_traj=20, n_steps_min=4, n_steps_max=4, families=(FamilyConfig.onfamily(dts=(0.25,)),), name="t")
    generate_dataset(cfg, tmp_path / "data", verbose=False)
    d = load_dataset(tmp_path / "data")
    train_jepa(d, JEPAConfig(obs_dim=d["manifest"]["obs_dim"]), TrainConfig(epochs=1, log_every=100), tmp_path / "model")

    def run(*args):
        r = subprocess.run([sys.executable, *args], cwd=tmp_path, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
        return r.stdout

    run(str(root / "scripts/run_twin.py"), "--name", "t", "--K", "6", "--depths", "1", "2", "--masses", "0.375",
        "--shots", "300", "--seeds", "2", "--noise", "ideal")
    rec = json.loads((tmp_path / "evidence/twin/t/records.json").read_text())
    assert rec["noise"] == "ideal" and len(rec["points"]) == 1 * 2 * 2 * 2  # masses x arms x seeds x depths
    run(str(root / "scripts/residual_eval.py"), "--model", str(tmp_path / "model/model.pt"), "--records", "evidence/twin/t/records.json",
        "--out", "evidence/twin/t/residual_eval.json", "--shots-levels", "0", "100")
    out = run(str(root / "scripts/twin_null_check.py"), "--records", "evidence/twin/t/records.json",
              "--residual", "evidence/twin/t/residual_eval.json", "--out", "evidence/twin/t/null_check.json")
    chk = json.loads((tmp_path / "evidence/twin/t/null_check.json").read_text())
    assert chk["checks"]["flag_rate_exactly_zero"]["pass"] and "all pass" in out


def test_calibrated_line_noise_model_offline(tmp_path):
    """build_noise_model.py on Qiskit's offline FakeKingston (its thermal relaxation is stored as Kraus matrices, which
    broke jobs/024): the line model keeps the calibrated CZ errors on qubits 0..K-1,
    and in run_twin.py --noise-model the degraded arm B flags more shots than the calibrated arm A."""
    pytest.importorskip("qiskit_aer")
    pytest.importorskip("qiskit_ibm_runtime")
    import subprocess
    import sys
    from pathlib import Path

    from qiskit.quantum_info import average_gate_fidelity

    from su2qc_jepa.twin.noise import load_line_noise_model

    root = Path(__file__).resolve().parents[1]

    def run(*args):
        r = subprocess.run([sys.executable, *args], cwd=tmp_path, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]

    run(str(root / "scripts/build_noise_model.py"), "--backend", "FakeKingston", "--fake", "--K", "4", "--name", "t")
    nmA, nmB, meta = load_line_noise_model(tmp_path / "evidence/twin/t/noise_model.json")
    assert meta["backend"] == "fake_kingston" and len(meta["line"]) == 4 and len(meta["line_cz_errors"]) == 3
    assert set(nmA.noise_qubits) <= {0, 1, 2, 3}
    stored = json.loads((tmp_path / "evidence/twin/t/noise_model.json").read_text())["noise_model"]["errors"]
    assert any(i["name"] == "kraus" for e in stored for ins in e.get("instructions", []) for i in ins)  # the hard case
    infid = 1 - average_gate_fidelity(nmA._local_quantum_errors["cz"][(0, 1)].to_quantumchannel())
    assert abs(infid - meta["line_cz_errors"][0]) < 1e-6  # the calibrated CZ error survives the renumbering exactly
    run(str(root / "scripts/run_twin.py"), "--name", "t", "--K", "4", "--depths", "2", "--masses", "0.375", "--shots", "4000",
        "--seeds", "1", "--noise-model", "evidence/twin/t/noise_model.json")
    rec = json.loads((tmp_path / "evidence/twin/t/records.json").read_text())
    flag = {q["arm"]: q["flag_rate"] for q in rec["points"]}
    assert rec["noise"] == "calibrated" and rec["calibration"]["line"] == meta["line"]
    assert 0 < flag["A"] < flag["B"]


def test_gate_ledger(tmp_path):
    res = GateResult("Jtest")
    res.add("row", True, 1.0, 2.0)
    res.add_status("other", "NOT RUN")
    p = write_gate(res, tmp_path)
    assert res.status == "PARTIAL"
    assert json.loads(p.read_text())["gate"] == "Jtest"
    assert (tmp_path / "GATE_LEDGER.md").exists()


def test_spearman_auroc():
    assert abs(spearman([1, 2, 3, 4], [10, 20, 30, 40]) - 1) < 1e-12
    assert abs(auroc([0.9, 0.8, 0.2, 0.1], [True, True, False, False]) - 1) < 1e-12


def test_j3_rehearsal_mode(tmp_path):
    """A twin rehearsal is recorded as J3_twin_rehearsal (never J3_hardware) and drops the self-compared reference points
    (arm A, seed 0: jepa_twin = raw_twin = 0), which would otherwise inflate the arm-B AUROC; hardware mode keeps every point."""
    from pathlib import Path

    from su2qc_jepa.gates.j3_hardware import run_j3

    root = Path(__file__).resolve().parents[1]
    rng = np.random.default_rng(np.random.SeedSequence(20261021))
    pts = []
    for arm in ("A", "B"):
        for seed in range(3):
            for depth in range(10):
                ref = arm == "A" and seed == 0
                s = 0.0 if ref else float(rng.random())
                pts.append({"arm": arm, "seed": seed, "day": seed, "depth": depth, "shots": 512, "jepa_twin": s, "raw_twin": s,
                            "jepa_self": s, "jepa_t0": s, "flag_rate": 0.1, "exact_error": float(rng.random())})
    f = tmp_path / "eval.json"
    f.write_text(json.dumps({"points": pts}))
    th = str(root / "configs/gates.yaml")
    hw = run_j3(f, thresholds_path=th, evidence_dir=tmp_path / "hw")
    rh = run_j3(f, thresholds_path=th, evidence_dir=tmp_path / "rh", rehearsal=True)
    assert hw.gate == "J3_hardware" and rh.gate == "J3_twin_rehearsal"
    assert (tmp_path / "rh/J3_twin_rehearsal").is_dir() and not (tmp_path / "rh/J3_hardware").exists()
    n = {r.name: r.measured for r in hw.rows}["number of points (per shot level)"]
    m = {r.name: r.measured for r in rh.rows}["number of points (per shot level)"]
    assert (n, m) == (60, 50)  # the 10 self-compared reference points are left out of the rehearsal
    a_hw = {r.name: r.measured for r in hw.rows}["AUROC jepa_twin separates arm B (degraded) from arm A"]
    a_rh = {r.name: r.measured for r in rh.rows}["AUROC jepa_twin separates arm B (degraded) from arm A"]
    assert a_hw > a_rh  # zeros in arm A inflate the AUROC when the references are kept


def test_chain_cz_budget_PA(setup):
    """The P-A window t <= 3/g_E at K = 12 with dt = 0.375 costs 188 CZ and has Trotter infidelity ~1e-3."""
    from su2qc_jepa.physics.chain import cz_count, trotter_error

    m, obs, names, N4, H4, psi0 = setup
    kr = lanczos(H4, psi0, K=12)
    assert cz_count(12, 8, 2) == 188
    assert trotter_error(kr, 12, 0.375, 8, 2) < 2e-3
    c = chain_amplitudes(ChainSpec.from_krylov(kr, 12, 0.375, 8))
    assert abs(np.sum(np.abs(c) ** 2) - 1) < 1e-12
