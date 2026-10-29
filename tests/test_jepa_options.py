"""Exploratory J1 options (prompts/011): Markov predictor, semigroup mixing, VICReg terms, flags; defaults unchanged."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from su2qc_jepa.data.trajectories import DatasetConfig, FamilyConfig, generate_dataset, load_dataset  # noqa: E402
from su2qc_jepa.models.jepa import (  # noqa: E402
    ActionPredictor,
    GaugeJEPA,
    JEPAConfig,
    MarkovPredictor,
    mix_actions,
    vicreg_terms,
)
from su2qc_jepa.models.train import prepare_tensors  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def dataset_dir(tmp_path_factory):
    p = tmp_path_factory.mktemp("jepa_opts_data")
    cfg = DatasetConfig(n_traj=40, n_steps_min=6, n_steps_max=6, families=(FamilyConfig.onfamily(dts=(0.25,)),), name="t")
    generate_dataset(cfg, p, verbose=False)
    return p


def _batch(dataset_dir, n=24):
    d = load_dataset(dataset_dir)
    tr = prepare_tensors(d, "train")
    return d, {k: v[:n] for k, v in tr.items()}


def _loss(jcfg, tr, seed=7):
    torch.manual_seed(0)
    m = GaugeJEPA(jcfg)
    g = torch.Generator().manual_seed(seed)
    return m.loss(tr["ctx"], tr["clean"], tr["act"], tr["ground"], tr["valid"], g)


def test_markov_predictor_composes_exactly():
    torch.manual_seed(1)
    mk, gru = MarkovPredictor(16, 4, 32, 128), ActionPredictor(16, 4, 32, 128)
    s, a = torch.randn(32, 16), torch.randn(32, 2, 4)
    with torch.no_grad():
        two = mk(s, a)
        comp = mk(mk(s, a[:, :1])[:, -1], a[:, 1:])[:, -1]
        gshape = gru(s, a).shape
    rel = ((two[:, -1] - comp) ** 2).mean() / (two[:, -1] ** 2).mean()
    assert float(rel) < 1e-10
    assert two.shape == gshape == (32, 2, 16)
    with pytest.raises(ValueError):
        JEPAConfig(obs_dim=24, predictor="lstm")
    assert isinstance(GaugeJEPA(JEPAConfig(obs_dim=24, predictor="markov")).predictor, MarkovPredictor)


def test_default_config_is_unchanged(dataset_dir):
    c = JEPAConfig(obs_dim=24)
    assert c.predictor == "gru" and c.semigroup_mix == 0 and c.w_var == 0.0 and c.w_cov == 0.0 and c.sigreg_projections == 64
    assert isinstance(GaugeJEPA(c).predictor, ActionPredictor)
    d, tr = _batch(dataset_dir)
    jc = JEPAConfig(obs_dim=d["manifest"]["obs_dim"])
    ls = _loss(jc, tr)
    assert set(ls) == {"pred", "sigreg", "ground", "semigroup", "total"}
    tot = jc.w_pred * ls["pred"] + jc.w_sigreg * ls["sigreg"] + jc.w_ground * ls["ground"] + jc.w_semigroup * ls["semigroup"]
    assert torch.allclose(ls["total"], tot, atol=1e-7)


def test_old_checkpoint_loads():
    ck = torch.load(ROOT / "evidence/runs/v1_final/seed0/model.pt", map_location="cpu", weights_only=False)  # trained on the desktop GPU
    jc = JEPAConfig(**ck["jcfg"])
    assert jc.predictor == "gru" and jc.semigroup_mix == 0
    m = GaugeJEPA(jc)
    m.load_state_dict(ck["state_dict"], strict=True)
    m.eval()
    torch.manual_seed(0)
    with torch.no_grad():
        z = m.encode(torch.randn(5, jc.obs_dim))
    assert z.shape == (5, jc.latent_dim) and torch.isfinite(z).all()


def test_semigroup_mix(dataset_dir):
    d, tr = _batch(dataset_dir)
    od = d["manifest"]["obs_dim"]
    base = _loss(JEPAConfig(obs_dim=od), tr)
    mixed = _loss(JEPAConfig(obs_dim=od, semigroup_mix=2), tr)
    assert torch.isfinite(mixed["total"]) and float(mixed["semigroup"]) != float(base["semigroup"])
    mk = _loss(JEPAConfig(obs_dim=od, predictor="markov", semigroup_mix=2), tr)
    assert float(mk["semigroup"]) < 1e-10
    # helper on a hand-made batch: column 0 (dt) kept, columns 1-3 between the two partners
    a = torch.tensor([[[0.25, 0.0, 0.0, 0.0]] * 2, [[0.5, 1.0, 2.0, 3.0]] * 2, [[0.75, 4.0, 4.0, 4.0]] * 2])
    perm, alpha = torch.tensor([1, 2, 0]), torch.tensor([0.25, 0.5, 1.0])
    am = mix_actions(a, perm, alpha)
    assert torch.equal(am[..., 0], a[..., 0])
    assert torch.allclose(am[0, :, 1:], torch.tensor([0.75, 1.5, 2.25]).expand(2, 3))
    assert torch.allclose(am[1, :, 1:], torch.tensor([2.5, 3.0, 3.5]).expand(2, 3))
    assert torch.equal(am[2, :, 1:], a[2, :, 1:])
    lo, hi = torch.minimum(a[..., 1:], a[perm][..., 1:]), torch.maximum(a[..., 1:], a[perm][..., 1:])
    assert ((am[..., 1:] >= lo) & (am[..., 1:] <= hi)).all()


def test_vicreg_terms(dataset_dir):
    g = torch.Generator().manual_seed(3)
    z = 3.0 * torch.randn(512, 4, generator=g)
    v, c = vicreg_terms(z, 1.0, 1e-4)
    assert float(v) == 0.0 and float(c) >= 0.0
    z2 = z.clone()
    z2[:, 0] = 1.7  # one constant dimension
    v2, _ = vicreg_terms(z2, 1.0, 1e-4)
    assert abs(float(v2) - 1.0 / 4) < 1e-2 / 4 * 1.5
    # 2-d batch with known covariance: C = [[2, 1], [1, 2]] / ... built from exact +-1 patterns
    x = torch.tensor([[1.0, 1.0], [-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0], [2.0, 2.0], [-2.0, -2.0]])
    xc = x - x.mean(0)
    C12 = float((xc[:, 0] * xc[:, 1]).sum() / (x.shape[0] - 1))
    _, c3 = vicreg_terms(x, 1.0, 1e-4)
    assert abs(float(c3) - 2 * C12**2 / 2) < 1e-6
    zr = torch.randn(64, 16, generator=g, requires_grad=True)
    v4, c4 = vicreg_terms(zr * 0.5, 1.0, 1e-4)
    (v4 + c4).backward()
    assert torch.isfinite(zr.grad).all()
    # wired into the loss only when a weight is on
    d, tr = _batch(dataset_dir)
    ls = _loss(JEPAConfig(obs_dim=d["manifest"]["obs_dim"], w_var=1.0, w_cov=0.1), tr)
    assert {"var", "cov"} <= set(ls)
    jc = JEPAConfig(obs_dim=d["manifest"]["obs_dim"], w_var=1.0, w_cov=0.1)
    tot = (jc.w_pred * ls["pred"] + jc.w_sigreg * ls["sigreg"] + jc.w_ground * ls["ground"] + jc.w_semigroup * ls["semigroup"]
           + ls["var"] + 0.1 * ls["cov"])
    assert torch.allclose(ls["total"], tot, atol=1e-6)


def test_cli_flags_reach_config_and_skip_baselines(dataset_dir, tmp_path):
    """--sigreg-projections, --predictor, --semigroup-mix, --w-var, --w-cov, --skip-baselines through scripts/train_jepa.py."""
    cmd = [sys.executable, str(ROOT / "scripts/train_jepa.py"), "--data", str(dataset_dir), "--name", "opt", "--epochs", "1", "--seeds", "1",
           "--context-steps", "2", "--eval-steps", "1", "2", "--sigreg-projections", "128", "--skip-baselines", "--predictor", "markov",
           "--semigroup-mix", "1", "--w-var", "1", "--w-cov", "0.1", "--device", "cpu", "--threads", "1"]
    r = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]
    run = tmp_path / "runs" / "opt"
    args = json.loads((run / "args.json").read_text())
    assert args["sigreg_projections"] == 128 and args["predictor"] == "markov" and args["skip_baselines"] is True
    assert args["semigroup_mix"] == 1 and args["w_var"] == 1.0 and args["w_cov"] == 0.1
    ck = torch.load(run / "seed0/model.pt", weights_only=False)
    assert ck["jcfg"]["sigreg_projections"] == 128 and ck["jcfg"]["predictor"] == "markov" and ck["jcfg"]["semigroup_mix"] == 1
    assert ck["jcfg"]["w_var"] == 1.0 and ck["jcfg"]["w_cov"] == 0.1
    GaugeJEPA(JEPAConfig(**ck["jcfg"])).load_state_dict(ck["state_dict"], strict=True)
    ev = json.loads((run / "forecast_eval.json").read_text())
    assert ev["baselines"] == "skipped" and ev["mae"]
    for fam in ev["mae"].values():
        assert set(fam) == {"jepa"}


def test_run_gate_evidence_dir(tmp_path):
    ledger = ROOT / "evidence/GATE_LEDGER.md"
    before = ledger.read_bytes()
    runs = []
    for s in range(5):
        rd = tmp_path / "runs" / f"seed{s}"
        rd.mkdir(parents=True)
        (rd / "history.json").write_text(json.dumps([{"epoch": 1, "eff_rank": 9.0, "ground_r2": [0.99, 0.99, 0.99, 0.99, 0.9],
                                                     "semigroup_resid": 1e-4}]))
        runs.append(rd)
    ev = tmp_path / "ev"
    r = subprocess.run([sys.executable, str(ROOT / "scripts/run_gate.py"), "J1", "--runs", *map(str, runs), "--evidence-dir", str(ev)],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode in (0, 1), r.stderr[-2000:]
    assert list((ev / "J1_training").glob("*.json")) and (ev / "GATE_LEDGER.md").exists()
    assert ledger.read_bytes() == before
