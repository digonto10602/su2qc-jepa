#!/usr/bin/env bash
# ONE-TIME, run ON PERLMUTTER after `scripts/worker/setup_env_perlmutter.sh <project>` (docs/PERLMUTTER.md).
# Installs the pull-based worker: a deploy key for pushing to the `results` branch, a tick script, and the scrontab entry.
#   bash install_perlmutter.sh m1234
set -euo pipefail
ACCOUNT="${1:?usage: install_perlmutter.sh <NERSC project, e.g. m1234>}"
ENV_PREFIX="/global/common/software/${ACCOUNT}/su2qc-jepa-env"
BASE="$SCRATCH/su2qc-worker"
KEY="$HOME/.ssh/su2qc_deploy"
mkdir -p "$BASE" "$HOME/.ssh"

if [ ! -f "$KEY" ]; then
  ssh-keygen -t ed25519 -N "" -C "su2qc-worker@perlmutter" -f "$KEY"
fi
if ! grep -q "Host github-su2qc" "$HOME/.ssh/config" 2>/dev/null; then
  cat >> "$HOME/.ssh/config" <<CFG

Host github-su2qc
    HostName github.com
    User git
    IdentityFile $KEY
    IdentitiesOnly yes
CFG
  chmod 600 "$HOME/.ssh/config"
fi

cat > "$BASE/tick.sh" <<TICK
#!/bin/bash
# one worker tick (called by scrontab)
module load conda
conda activate $ENV_PREFIX
[ -d $BASE/main ] || git clone -q git@github-su2qc:digonto10602/su2qc-jepa.git $BASE/main
git -C $BASE/main fetch -q origin && git -C $BASE/main checkout -q --detach origin/main
python $BASE/main/scripts/worker/worker.py --name perlmutter --mode slurm --base $BASE \\
  --repo git@github-su2qc:digonto10602/su2qc-jepa.git --account $ACCOUNT --env-prefix $ENV_PREFIX \\
  --budget-node-hours \${SU2QC_BUDGET_NODE_HOURS:-50}
TICK
chmod +x "$BASE/tick.sh"

cp "$(dirname "$0")/scrontab_merge.sh" "$BASE/scrontab_merge.sh"
# the su2qc-jepa entry only; scrontab_merge.sh adds it next to your other entries (never `scrontab <file>`, which replaces them all)
cat > "$BASE/scrontab.txt" <<CRON
#SCRON -q cron
#SCRON -C cron
#SCRON -A $ACCOUNT
#SCRON -t 00:10:00
#SCRON -o $BASE/tick-%j.log
#SCRON --open-mode=append
*/15 * * * * bash $BASE/tick.sh
CRON

echo
echo "=== 1. Add this public key to GitHub: repo digonto10602/su2qc-jepa > Settings > Deploy keys > Add deploy key,"
echo "       title 'perlmutter worker', tick 'Allow write access' (it can only write to this one repository):"
cat "$KEY.pub"
echo
echo "=== 2. Test:   ssh -T git@github-su2qc        (expect: 'Hi digonto10602/su2qc-jepa! You've successfully authenticated')"
echo "=== 3. Test one tick by hand:   bash $BASE/tick.sh"
echo "=== 4. Add the schedule (every 15 min, times in UTC) WITHOUT touching your other scrontab entries:"
echo "         bash $BASE/scrontab_merge.sh add $BASE/scrontab.txt      ;  check: scrontab -l"
echo "       Stop only this worker:   bash $BASE/scrontab_merge.sh remove"
echo "       Do NOT use 'scrontab $BASE/scrontab.txt' (replaces your whole table) or 'scrontab -r' (deletes all of it)."
