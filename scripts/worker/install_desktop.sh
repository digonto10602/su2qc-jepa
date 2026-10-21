#!/usr/bin/env bash
# ONE-TIME, run ON THE DESKTOP after setup_env_desktop.sh (docs/DESKTOP.md, decisions/006).
# Installs the desktop job worker: a deploy key that can push only to this repository, a tick script, and a
# systemd *user* timer that runs one tick 3 minutes after boot and then every 15 minutes.  Each tick fetches
# GitHub itself, so after switching the desktop on nothing else is needed; jobs addressed `where: desktop` run on
# the RTX 3070 and their results are pushed to the `results` branch (never to `main`).
#   bash install_desktop.sh
set -euo pipefail
ENV_PREFIX="${SU2QC_ENV_PREFIX:-$HOME/.su2qc-jepa-env}"
BASE="${SU2QC_WORKER_BASE:-$HOME/su2qc-worker}"
KEY="$HOME/.ssh/su2qc_deploy_desktop"
HOST_ALIAS="github-su2qc-desktop"
THREADS="${SU2QC_WORKER_THREADS:-$(( $(nproc) > 4 ? $(nproc) - 2 : 2 ))}"
[ -x "$ENV_PREFIX/bin/python" ] || { echo "no environment at $ENV_PREFIX: run setup_env_desktop.sh first"; exit 1; }
mkdir -p "$BASE" "$HOME/.ssh" "$HOME/.config/systemd/user"

if [ ! -f "$KEY" ]; then
  ssh-keygen -t ed25519 -N "" -C "su2qc-worker@desktop" -f "$KEY"
fi
if ! grep -q "Host $HOST_ALIAS" "$HOME/.ssh/config" 2>/dev/null; then
  cat >> "$HOME/.ssh/config" <<CFG

Host $HOST_ALIAS
    HostName github.com
    User git
    IdentityFile $KEY
    IdentitiesOnly yes
CFG
  chmod 600 "$HOME/.ssh/config"
fi

cat > "$BASE/tick.sh" <<TICK
#!/bin/bash
# one desktop worker tick (started by the su2qc-worker systemd user timer)
set -uo pipefail
export SU2QC_DEVICE=cuda          # a job must fail loudly rather than silently fall back to the CPU
cd "$BASE"
[ -d "$BASE/main/.git" ] || git clone -q git@$HOST_ALIAS:digonto10602/su2qc-jepa.git "$BASE/main"
git -C "$BASE/main" fetch -q origin && git -C "$BASE/main" checkout -q --detach origin/main
"$ENV_PREFIX/bin/python" "$BASE/main/scripts/worker/worker.py" --name desktop --mode local --base "$BASE" \\
  --repo git@$HOST_ALIAS:digonto10602/su2qc-jepa.git --python "$ENV_PREFIX/bin/python" --threads $THREADS \\
  2>> "$BASE/tick_errors.log"
TICK
chmod +x "$BASE/tick.sh"

cat > "$HOME/.config/systemd/user/su2qc-worker.service" <<UNIT
[Unit]
Description=su2qc-jepa desktop job worker (one tick)
After=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash $BASE/tick.sh
# a tick may run one job for hours; never kill it for taking long
TimeoutStartSec=infinity
Nice=10
UNIT

cat > "$HOME/.config/systemd/user/su2qc-worker.timer" <<UNIT
[Unit]
Description=Run the su2qc-jepa desktop worker every 15 minutes

[Timer]
OnBootSec=3min
OnUnitInactiveSec=15min

[Install]
WantedBy=timers.target
UNIT
systemctl --user daemon-reload

echo
echo "=== 1. Add this public key to GitHub: repo digonto10602/su2qc-jepa > Settings > Deploy keys > Add deploy key,"
echo "       title 'desktop worker', tick 'Allow write access' (it can only write to this one repository):"
cat "$KEY.pub"
echo
echo "=== 2. Test:   ssh -T git@$HOST_ALIAS     (expect: 'Hi digonto10602/su2qc-jepa! You've successfully authenticated')"
echo "=== 3. One tick by hand:   bash $BASE/tick.sh        (no job queued yet: it only writes a heartbeat)"
echo "=== 4. Start the timer:    systemctl --user enable --now su2qc-worker.timer"
echo "       so it also runs when you are not logged in (asks for your password once):   sudo loginctl enable-linger $USER"
echo "       check: systemctl --user list-timers su2qc-worker.timer ;  logs: journalctl --user -u su2qc-worker -n 50"
echo "       stop:  systemctl --user disable --now su2qc-worker.timer"
