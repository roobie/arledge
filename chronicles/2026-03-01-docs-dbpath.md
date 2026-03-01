# Chronicle: DB path configurability implemented and docs updated

- timestamp: 2026-03-01T11:24:39+01:00
- participants: assistant

## Summary
Implemented a configurable DB path retrieval function and updated documentation to reflect the new behavior.

## Changes made
- ledger/db.py: added `get_db_path()` which prefers the `LEDGER_DB_PATH` environment variable, then `ledger.config.ledger_db_path`, and finally falls back to `<cwd>/ledger.db`.
- ledger/config.py: added `ledger_db_path: str | None = None` configuration variable.
- README.md: added a "Configurable DB path" section documenting usage via `LEDGER_DB_PATH`.
- docs/IMPROVEMENTS_CHECKLIST.md: marked DB path task as "In progress" and noted next steps.

## Commands run
- Edited ledger/db.py, ledger/config.py, README.md, docs/IMPROVEMENTS_CHECKLIST.md

## Suggested next steps
- Add unit tests to assert behavior when LEDGER_DB_PATH is set and when ledger.config.ledger_db_path is set.
- Optionally, add a global CLI option to override DB path at runtime.

