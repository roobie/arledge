# Chronicle: Respect ARLEDGE_BASEDIR for filesystem operations

- timestamp: 2026-03-01T14:33:00+01:00
- participants: agent (assistant), developer

## Summary
Added support for an environment variable ARLEDGE_BASEDIR which controls the base directory used by CLI operations. The `ledger init` command now uses this base directory (via `ledger.config.get_basedir()`) instead of always using the current working directory.

## Changes
- Modified: src/ledger/config.py
  - Added get_basedir() helper which returns Path based on ARLEDGE_BASEDIR or cwd.
  - Exposed BACKCOMPAT alias BASEDIR = get_basedir().
- Modified: src/ledger/cli.py
  - `ledger init` now calls `config.get_basedir()` and initializes the layout at that path.

## Representative commands run
- Edited: src/ledger/config.py
- Edited: src/ledger/cli.py

## Files modified
- src/ledger/config.py
- src/ledger/cli.py

## Next steps
- Update other modules that perform filesystem operations to use config.get_basedir() where appropriate (db, export paths, invoice sidecar reads/writes).
- Add unit tests verifying that setting ARLEDGE_BASEDIR causes `ledger init` to create the layout at that path and that --force behaves as expected.

