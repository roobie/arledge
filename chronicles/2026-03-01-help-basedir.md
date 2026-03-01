# Chronicle: Expose ARLEDGE_BASEDIR in CLI help text

- timestamp: 2026-03-01T14:52:00+01:00
- participants: agent (assistant), developer

## Summary
Updated the CLI help text to mention the ARLEDGE_BASEDIR environment variable and show usage examples. This makes it discoverable from `ledger --help` and per-command help output.

## Changes
- Modified: src/ledger/cli.py
  - Enhanced the top-level CLI docstring with a short Environment section explaining ARLEDGE_BASEDIR and example usage with `uv run ledger`.
  - Enhanced the `ledger init` command docstring to state that the base directory is configurable via ARLEDGE_BASEDIR and included an example.

## Next steps
- Consider adding an explicit `--basedir` option to commands that operate on the filesystem if users prefer flag-based overrides.
- Update other modules to consistently use config.get_basedir() if not already done (db, export, sidecars).
- Add tests asserting that help text contains ARLEDGE_BASEDIR hints.
