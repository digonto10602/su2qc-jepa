#!/usr/bin/env python
"""Create the next numbered plan / prompt / report / decision / figure, or re-index.

  python scripts/new_artifact.py prompts "M2 repair: latent rank collapse" --milestone M2 --supersedes prompts/002
  python scripts/new_artifact.py reports "M1 physics cross-check and J0" --milestone M1
  python scripts/new_artifact.py decisions "Freeze SIGReg weight" --milestone M2
  python scripts/new_artifact.py figures "J2 forecast vs exact onfam" --ext .png    # prints the path to save to
  python scripts/new_artifact.py --reindex                                          # regenerate every INDEX.md
  python scripts/new_artifact.py --check                                            # same check as CI

The planner (Claude in Cowork) and Claude Code both use this tool; nobody picks numbers by hand.
"""
import argparse
import sys

from su2qc_jepa.repo.artifacts import SERIES, check_artifacts, new_artifact, write_index

p = argparse.ArgumentParser()
p.add_argument("series", nargs="?", choices=list(SERIES))
p.add_argument("title", nargs="?")
p.add_argument("--author", default="claude-code", help="claude-code | planner | Digonto")
p.add_argument("--milestone")
p.add_argument("--supersedes", help="id of the artifact this one replaces, e.g. prompts/004")
p.add_argument("--status", default="draft")
p.add_argument("--ext")
p.add_argument("--reindex", action="store_true")
p.add_argument("--check", action="store_true")
p.add_argument("--root", default=".")
a = p.parse_args()

if a.reindex:
    for s in SERIES:
        print("wrote", write_index(a.root, s))
if a.check or a.reindex:
    problems = check_artifacts(a.root)
    for pr in problems:
        print("PROBLEM:", pr)
    print("artifact conventions:", "OK" if not problems else f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)
if not (a.series and a.title):
    p.error("series and title are required (or use --reindex / --check)")
path = new_artifact(a.root, a.series, a.title, author=a.author, milestone=a.milestone, supersedes=a.supersedes, ext=a.ext,
                    status=a.status)
print(path)
