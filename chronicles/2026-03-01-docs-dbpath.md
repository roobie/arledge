# Chronicle: DB path configurability implemented and docs updated

- timestamp: 2026-03-01T11:24:39+01:00
- participants: assistant

## Summary
Implemented a configurable DB path retrieval function and updated documentation to reflect the new behavior.

## Changes made
- Historical note: earlier iterations added `get_db_path()` and `LEDGER_DB_PATH` support for a SQLite backend. That backend has since been removed in favor of a beancount-file-first approach. Current storage uses `ledger/beancount_store.py` and `ledger/beancount_write.py`.
- README.md and other docs were updated previously to describe DB path options; those references have been replaced or removed as part of the SQLite removal.

## Commands run
- Edited ledger/db.py, ledger/config.py, README.md, docs/IMPROVEMENTS_CHECKLIST.md

## Suggested next steps
- Add unit tests to assert behavior when LEDGER_DB_PATH is set and when ledger.config.ledger_db_path is set.
- Optionally, add a global CLI option to override DB path at runtime.

