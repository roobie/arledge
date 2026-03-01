# Chronicle: Restore DB_PATH compatibility and fix failing tests

- timestamp: 2026-03-01T11:24:39+01:00
- participants: assistant

## Summary
After making the DB path configurable via get_db_path(), running the test suite revealed failures because tests and other code set `db.DB_PATH` directly. To maintain backwards compatibility and keep tests passing, I restored a module-level `DB_PATH` variable and made `get_db_path()` prefer it as the highest precedence.

## Changes made
- ledger/db.py: added `DB_PATH: str | None = None` and updated `get_db_path()` to prefer DB_PATH, then LEDGER_DB_PATH env var, then ledger.config.ledger_db_path, then default to `<cwd>/ledger.db`.
- Added chronicle entry.

## Rationale
Tests in the repo set `db.DB_PATH` to a temporary path; removing or ignoring that variable broke tests. Restoring DB_PATH preserves backward compatibility with minimal surface area change.

## Next steps
- Run the full test suite to confirm all tests pass.
- Consider adding a deprecation note if we plan to migrate away from module-level DB_PATH in the future.
