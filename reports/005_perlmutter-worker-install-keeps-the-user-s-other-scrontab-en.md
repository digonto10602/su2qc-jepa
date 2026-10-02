---
id: reports/005
title: Perlmutter worker install keeps the user's other scrontab entries
series: reports
created_utc: '2026-10-02T21:14:04Z'
author: planner
milestone: null
status: done
supersedes: null
superseded_by: null
---

# Perlmutter worker install keeps the user's other scrontab entries

**Milestone:** before M0 · **Prompt:** Digonto's question of 2 Oct 2026 (Cowork) · **Commit range:** not yet under git

## What was asked
Digonto already has two scrontab entries for two other repositories on Perlmutter. Does `scrontab scrontab.txt` remove them?

## Actions taken
1. Confirmed the problem. `scrontab <file>` replaces the user's whole scrontab table, like `crontab <file>`, and `scrontab -r` deletes all of it. The setup in `docs/PERLMUTTER.md` and `install_perlmutter.sh` told the user to run both.
2. Added `scripts/worker/scrontab_merge.sh` (`add <block-file>` | `remove`). It:
   - saves the current table to `~/.scrontab-backup-<UTC>.txt`;
   - keeps every line outside the markers `# >>> su2qc-jepa worker >>>` and `# <<< su2qc-jepa worker <<<` exactly as it was;
   - adds or replaces only the block between those markers;
   - installs the result and reads it back;
   - restores the backup if any other line changed.
   
   `remove` deletes only the block, and uses `scrontab -r` only if nothing else is left.
3. `install_perlmutter.sh` now copies the script to `$SCRATCH/su2qc-worker/` and prints the merge commands instead of `scrontab <file>` and `scrontab -r`. Updated `docs/PERLMUTTER.md` and the README.
4. Added `tests/test_scrontab_merge.py` (2 tests, with a stand-in `scrontab` holding two other repositories' entries).

## Results and what they mean
- **Tests.** Adding the block twice leaves exactly one block; the two other entries survive byte for byte; removing the block restores the original table; adding to an empty table and then removing leaves no table. 47 fast tests pass.
- **Meaning.** Installing or stopping this worker can no longer touch the other repositories' scheduled jobs. Each scrontab entry carries its own `#SCRON` options (the lines just above it), so entries do not interfere with one another.

## Code graph
Refreshed with `bash scripts/graph_update.sh`; see `evidence/graph/stats.json`. No Python module changed apart from the new test.

## Problems and assumptions
- The check assumes `scrontab -l` returns the table as installed, which is how Slurm stores it. If Slurm has meanwhile disabled one of the other entries (it marks such lines with `#DISABLED`), the check sees a difference and restores the backup. That is safe, but the run then has to be repeated.
- Not yet run on the real Perlmutter.

## Next action
On Perlmutter, after `install_perlmutter.sh`: `bash $SCRATCH/su2qc-worker/scrontab_merge.sh add $SCRATCH/su2qc-worker/scrontab.txt`, then `scrontab -l`.
