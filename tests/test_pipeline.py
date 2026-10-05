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
    from su2qc_jepa.models.train import (TrainConfig, baseline_autoregressive, baseline_ridge, baseline_supervised_mlp,
                                         fit_probe, forecast_jepa, prepare_tensors, train_jepa)

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


def test_chain_cz_budget_PA(setup):
    """The P-A window t <= 3/g_E at K = 12 with dt = 0.375 costs 188 CZ and has Trotter infidelity ~1e-3."""
    from su2qc_jepa.physics.chain import cz_count, trotter_error

    m, obs, names, N4, H4, psi0 = setup
    kr = lanczos(H4, psi0, K=12)
    assert cz_count(12, 8, 2) == 188
    assert trotter_error(kr, 12, 0.375, 8, 2) < 2e-3
    c = chain_amplitudes(ChainSpec.from_krylov(kr, 12, 0.375, 8))
    assert abs(np.sum(np.abs(c) ** 2) - 1) < 1e-12
