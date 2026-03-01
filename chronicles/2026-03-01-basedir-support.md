# Chronicle: Add ARLEDGE_BASEDIR environment variable support

- timestamp: 2026-03-01T14:33:00+01:00
- participants: agent (assistant), developer

## Summary

Added support for the ARLEDGE_BASEDIR environment variable which controls the base directory used by CLI operations, and exposed it in help text for discoverability.

The `ledger init` and other filesystem-aware commands now use this base directory (via `config.get_basedir()`) instead of always using the current working directory.

## Changes

**Modified: src/arledge/config.py**
- Added `get_basedir()` helper which returns Path based on ARLEDGE_BASEDIR env var or current working directory.

**Modified: src/arledge/cli.py**
- `ledger init` now calls `config.get_basedir()` and initializes the layout at that path.
- Enhanced top-level CLI docstring with Environment section explaining ARLEDGE_BASEDIR and example usage.
- Enhanced `ledger init` command docstring with ARLEDGE_BASEDIR example.

## Example usage

```bash
ARLEDGE_BASEDIR=/path/to/ledger uv run ledger init
ARLEDGE_BASEDIR=/path/to/ledger uv run ledger customer list
```

## Next steps

- Update other filesystem-aware modules to use `config.get_basedir()` if not already done.
- Consider adding an explicit `--basedir` flag option as an alternative to the env var.
