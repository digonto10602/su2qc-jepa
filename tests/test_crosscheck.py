"""Route C (this package) against the verified su2qc routes 1 and 2 (prompts/001 Part A).

Skipped where the su2qc package (SU2ZX run section8_v0.5.0) is absent, e.g. in CI; set SU2QC_SRC to point at it."""
import importlib.util
import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("crosscheck_su2qc", ROOT / "scripts" / "crosscheck_su2qc.py")
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

SRC = os.environ.get("SU2QC_SRC", cc.DEFAULT_SU2QC_SRC)
pytestmark = [pytest.mark.skipif(not Path(SRC, "su2qc").is_dir(), reason=f"su2qc package not found under {SRC}")]  # ~20 s on the laptop


@pytest.fixture(scope="module")
def record(tmp_path_factory):
    out = tmp_path_factory.mktemp("cc") / "crosscheck.json"
    assert cc.main(["--su2qc-src", SRC, "--out", str(out)]) == 0
    return json.loads(out.read_text())


def test_term_extraction_reproduces_an_independent_build(record):
    for e in record["term_extraction"].values():
        assert e["dim"] == 82 and e["verify_max_abs_residual"] <= cc.TOL


@pytest.mark.parametrize("point", ["P-A", "P-S"])
@pytest.mark.parametrize("route", ["route1_spinnet", "route2_gausskernel"])
def test_five_comparisons(record, point, route):
    r = record["points"][point]["routes"][route]
    assert r["max_imag_part"] <= cc.TOL
    assert r["i_diag_max_abs_dev"] <= cc.TOL  # (i) 82 diagonal energies
    assert r["ii_spectrum_max_abs_dev"] <= cc.TOL  # (ii) full spectrum
    assert r["iii_N4_block_max_abs_dev"] <= cc.TOL  # (iii) 38x38 block up to permutation and sign
    assert r["iii_full82_max_abs_dev"] <= cc.TOL  # ... and the full 82x82 matrix
    assert r["iv_population_max_abs_dev"] <= cc.TOL and r["iv_observable_max_abs_dev"] <= cc.TOL  # (iv) dynamics
    assert r["v_alpha_max_abs_dev"] <= cc.TOL and r["v_beta_max_abs_dev"] <= cc.TOL  # (v) Lanczos from S3


def test_native_su2qc_build_at_PA(record):
    for r in record["points"]["P-A"]["routes"].values():
        assert r["native_build_max_abs_dev"] <= cc.TOL
