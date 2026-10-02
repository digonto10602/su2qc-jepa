#!/usr/bin/env python
"""CI/session-end check of the numbered-artifact conventions (decisions/001)."""
import sys

from su2qc_jepa.repo.artifacts import check_artifacts

problems = check_artifacts(sys.argv[1] if len(sys.argv) > 1 else ".")
for pr in problems:
    print("PROBLEM:", pr)
print("artifact conventions:", "OK" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
