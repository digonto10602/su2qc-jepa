"""Device selection must never pick a GPU the installed PyTorch cannot use (laptop GTX 1060 case)."""
import pytest

from su2qc_jepa import compute


def test_cpu_override(monkeypatch):
    monkeypatch.setenv("SU2QC_DEVICE", "cpu")
    assert compute.pick_device() == "cpu"


def test_unsupported_gpu_falls_back_to_cpu(monkeypatch):
    torch = pytest.importorskip("torch")
    monkeypatch.delenv("SU2QC_DEVICE", raising=False)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "get_device_capability", lambda i=0: (6, 1))  # Pascal, GTX 1060
    monkeypatch.setattr(torch.cuda, "get_arch_list", lambda: ["sm_75", "sm_80", "sm_90"])
    monkeypatch.setattr(torch.cuda, "get_device_name", lambda i=0: "GeForce GTX 1060 with Max-Q Design")
    assert compute.pick_device() == "cpu"
    monkeypatch.setenv("SU2QC_DEVICE", "cuda")
    with pytest.raises(RuntimeError):
        compute.pick_device()


def test_run_py_routes_heavy_jobs_to_perlmutter():
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    r = subprocess.run([sys.executable, "scripts/run.py", "--dry", "--", "python", "scripts/train_jepa.py", "--data", "data/main",
                        "--name", "x", "--epochs", "200", "--seeds", "5", "--masked"], cwd=root, capture_output=True, text=True)
    assert r.returncode == 0 and "Perlmutter" in r.stdout and '"heavy": true' in r.stdout
    r = subprocess.run([sys.executable, "scripts/run.py", "--dry", "--", "python", "scripts/make_dataset.py", "--n-traj", "2000",
                        "--out", "data/x"], cwd=root, capture_output=True, text=True)
    assert r.returncode == 0 and '"heavy": false' in r.stdout
