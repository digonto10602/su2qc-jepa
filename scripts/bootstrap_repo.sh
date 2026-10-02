#!/usr/bin/env bash
# First-session bootstrap (prompts/000): create the public GitHub repository digonto10602/su2qc-jepa, set up the
# Graphify code graph, and push.  Idempotent: safe to re-run.
# Requires: `gh auth status` succeeds (GitHub CLI logged in as digonto10602); Python env with the package installed.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="${1:-digonto10602/su2qc-jepa}"
GRAPHIFY_VERSION="0.9.74"

echo "== 1/5 checks"
command -v gh >/dev/null || { echo "GitHub CLI 'gh' not found - install it and run 'gh auth login'"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh is not logged in - run 'gh auth login' first"; exit 1; }
python scripts/check_artifacts.py

echo "== 2/5 Graphify (code graph; decisions/001)"
if ! command -v graphify >/dev/null 2>&1; then
  pip install "graphifyy==${GRAPHIFY_VERSION}"
fi
graphify claude install            # adds the PreToolUse hook to .claude/settings.json (machine-local, git-ignored);
                                   # CLAUDE.md already contains the graphify section, so it is left unchanged
if [ "${GRAPHIFY_HOOKS:-0}" = "1" ]; then
  graphify hook install            # optional: background rebuild after each commit (leaves the tree dirty; see decisions/001)
fi
bash scripts/graph_update.sh

echo "== 3/5 git"
[ -d .git ] || git init -b main
git add -A
if ! git diff --cached --quiet; then
  git -c user.name="${GIT_AUTHOR_NAME:-Digonto}" -c user.email="${GIT_AUTHOR_EMAIL:-digonto10602@gmail.com}" \
    commit -m "chore: bootstrap su2qc-jepa starter package (Gauge-JEPA-P v2, plans/001)"
fi

echo "== 4/5 GitHub"
if gh repo view "$REPO" >/dev/null 2>&1; then
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
else
  gh repo create "$REPO" --public --source=. --remote=origin \
    --description "Gauge-JEPA-P v2: JEPA world model for SU(2) string breaking on one plaquette with a Krylov-chain hardware carrier (SU2QC)"
fi
git push -u origin main

echo "== 5/5 done: https://github.com/$REPO"
python scripts/graph_stats.py --top 5
