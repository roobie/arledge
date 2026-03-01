# Chronicle: Restore DB_PATH compatibility and fix failing tests

- timestamp: 2026-03-01T11:24:39+01:00
- participants: assistant

## Summary
After making the DB path configurable via get_db_path(), running the test suite revealed failures because tests and other code set `db.DB_PATH` directly. To maintain backwards compatibility and keep tests passing, I restored a module-level `DB_PATH` variable and made `get_db_path()` prefer it as the highest precedence.

## Changes made
- Note: Earlier work added `DB_PATH` support for a SQLite backend. The project later migrated to a beancount-first storage model and removed the SQLite implementation. Tests were migrated to use the beancount CLI/write flow and no longer set `db.DB_PATH`.
- Added chronicle entry documenting the migration and test updates.

## Rationale
The SQLite compatibility changes were a temporary compatibility measure during migration. The final decision was to remove SQLite and consolidate on a beancount-file-first architecture; tests and server tools were updated accordingly.

## Next steps
- Ensure any external docs referencing `LEDGER_DB_PATH` or legacy DB initialization are updated or removed.
- Archive or delete legacy SQLite migration notes if not needed for historical purposes.
