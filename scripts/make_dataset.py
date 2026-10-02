#!/usr/bin/env python
"""Generate a trajectory dataset.  Examples:
  python scripts/make_dataset.py --name smoke --n-traj 200 --out data/smoke
  python scripts/make_dataset.py --name main --n-traj 20000 --families onfam strong --out data/main
  python scripts/make_dataset.py --name chain_onfam --n-traj 5000 --families onfam --carrier chain --starts S3 --quench-fraction 0 --out data/chain_onfam
"""
import argparse

from su2qc_jepa.data.trajectories import ONFAM, STRONG, DatasetConfig, generate_dataset

FAMILIES = {"onfam": ONFAM, "strong": STRONG}

p = argparse.ArgumentParser()
p.add_argument("--name", default="smoke")
p.add_argument("--n-traj", type=int, default=200)
p.add_argument("--steps", type=int, nargs=2, default=(8, 12), metavar=("MIN", "MAX"))
p.add_argument("--families", nargs="+", choices=list(FAMILIES), default=("onfam", "strong"))
p.add_argument("--carrier", choices=("diagonal", "chain"), default="diagonal")
p.add_argument("--starts", nargs="+", default=("S3", "S3", "S3", "S1", "random"))
p.add_argument("--quench-fraction", type=float, default=0.2)
p.add_argument("--seed", type=int, default=20261005)
p.add_argument("--out", required=True)
a = p.parse_args()
cfg = DatasetConfig(n_traj=a.n_traj, n_steps_min=a.steps[0], n_steps_max=a.steps[1], families=tuple(FAMILIES[f] for f in a.families),
                    carrier=a.carrier, starts=tuple(a.starts), quench_fraction=a.quench_fraction, seed=a.seed, name=a.name)
generate_dataset(cfg, a.out)
