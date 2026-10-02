"""scrontab_merge.sh must never remove the user's other scrontab entries (scrontab <file> replaces the whole table)."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OTHERS = """#SCRON -q cron
#SCRON -A m1234
#SCRON -t 00:05:00
*/30 * * * * bash $SCRATCH/repoA/tick.sh

#SCRON -q cron
#SCRON -A m1234
0 3 * * * bash $SCRATCH/repoB/nightly.sh
"""
BLOCK = "#SCRON -q cron\n#SCRON -C cron\n#SCRON -A m1234\n*/15 * * * * bash $SCRATCH/su2qc-worker/tick.sh\n"


def _env(tmp_path):
    table = tmp_path / "table.txt"
    fake = tmp_path / "scrontab"
    fake.write_text(f"""#!/bin/bash
T={table}
case "$1" in
  -l) [ -f $T ] && cat $T || {{ echo "no crontab" >&2; exit 1; }} ;;
  -r) rm -f $T ;;
  *) cp "$1" $T ;;
esac
""")
    fake.chmod(0o755)
    return table, {**os.environ, "SCRONTAB": str(fake), "HOME": str(tmp_path)}


def _run(env, *args):
    return subprocess.run(["bash", str(ROOT / "scripts/worker/scrontab_merge.sh"), *args], env=env, capture_output=True, text=True)


def test_add_update_remove_keeps_other_entries(tmp_path):
    table, env = _env(tmp_path)
    table.write_text(OTHERS)
    block = tmp_path / "scrontab.txt"
    block.write_text(BLOCK)
    for _ in range(2):  # adding twice must not duplicate the block
        r = _run(env, "add", str(block))
        assert r.returncode == 0, r.stderr + r.stdout
    t = table.read_text()
    assert OTHERS.strip() in t and t.count("su2qc-worker/tick.sh") == 1 and t.count(">>> su2qc-jepa worker >>>") == 1
    assert list(tmp_path.glob(".scrontab-backup-*.txt")), "a backup must be written"
    r = _run(env, "remove")
    assert r.returncode == 0, r.stderr
    assert table.read_text().strip() == OTHERS.strip()


def test_add_to_empty_table_and_remove_last_entry(tmp_path):
    table, env = _env(tmp_path)
    block = tmp_path / "scrontab.txt"
    block.write_text(BLOCK)
    assert _run(env, "add", str(block)).returncode == 0
    assert "su2qc-worker/tick.sh" in table.read_text()
    assert _run(env, "remove").returncode == 0
    assert not table.exists()
