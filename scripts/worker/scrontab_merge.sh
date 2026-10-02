#!/usr/bin/env bash
# Add, replace or remove ONLY the su2qc-jepa block in your scrontab; every other entry is kept as it is.
#
#   bash scrontab_merge.sh add <block-file>    # install or update the su2qc-jepa worker entry
#   bash scrontab_merge.sh remove              # stop the su2qc-jepa worker only
#
# Why: `scrontab <file>` REPLACES your whole scrontab and `scrontab -r` DELETES all of it, so either would remove the
# entries of your other repositories. This script backs up the current table to ~/.scrontab-backup-<UTC>.txt,
# edits only the lines between the markers below, installs the result, and checks that every other line survived
# (restoring the backup if not).
set -euo pipefail
BEGIN="# >>> su2qc-jepa worker >>>"
END="# <<< su2qc-jepa worker <<<"
SCRONTAB="${SCRONTAB:-scrontab}"   # overridable for tests
mode="${1:?usage: scrontab_merge.sh add <block-file> | remove}"
block="${2:-}"
[ "$mode" = add ] && [ ! -f "$block" ] && { echo "block file not found: $block" >&2; exit 2; }

stamp=$(date -u +%Y%m%dT%H%M%SZ)
backup="$HOME/.scrontab-backup-$stamp.txt"
tmp=$(mktemp)
others=$(mktemp)
trap 'rm -f "$tmp" "$others"' EXIT

"$SCRONTAB" -l > "$backup" 2>/dev/null || : > "$backup"   # no table yet -> empty backup
echo "backup of your current scrontab: $backup ($(grep -c . "$backup" || true) non-empty lines)"

# everything outside our markers (the other repositories' entries), exactly as it was
awk -v b="$BEGIN" -v e="$END" '$0==b{skip=1; next} $0==e{skip=0; next} !skip' "$backup" > "$others"
cp "$others" "$tmp"
if [ "$mode" = add ]; then
  [ -s "$tmp" ] && [ -n "$(tail -c1 "$tmp")" ] && echo >> "$tmp"
  { echo "$BEGIN"; grep -v -x -F -e "$BEGIN" -e "$END" "$block"; echo "$END"; } >> "$tmp"
fi

echo "--- new scrontab ---"; cat "$tmp"; echo "--------------------"
if grep -q '[^[:space:]]' "$tmp"; then
  "$SCRONTAB" "$tmp"
else
  "$SCRONTAB" -r   # nothing left at all (su2qc-jepa was the only entry)
fi

# verify: every line of the other entries is still installed, in order
installed=$(mktemp)
"$SCRONTAB" -l > "$installed" 2>/dev/null || : > "$installed"
check=$(awk -v b="$BEGIN" -v e="$END" '$0==b{skip=1; next} $0==e{skip=0; next} !skip' "$installed")
rm -f "$installed"
if [ "$check" != "$(cat "$others")" ]; then
  echo "ERROR: your other scrontab entries changed; restoring the backup $backup" >&2
  "$SCRONTAB" "$backup"
  exit 1
fi
if [ "$mode" = add ]; then what="installed"; else what="removed"; fi
echo "OK: your other entries are unchanged; su2qc-jepa block $what. Check with: $SCRONTAB -l"
