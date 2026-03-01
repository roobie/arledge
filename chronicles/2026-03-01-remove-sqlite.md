# Chronicle: Remove SQLite backend & migrate tests to beancount-first

- timestamp: 2026-03-01T12:45:00+01:00
- participants: assistant

## Summary
Removed the legacy SQLite persistence layer and migrated the codebase and tests to a beancount-file-first architecture. Replaced db.* usages across CLI and MCP server with ledger/beancount_store.py (read) and ledger/beancount_write.py (write). Updated tests to create fixture data via the CLI (isolated filesystem) and added smoke/spike tests exercising the beancount helpers. Ensured test suite passes and coverage remains above the configured threshold.

## Commands run (representative)
- Ran full test suite repeatedly while migrating tests: `uv run pytest -q`
- Searched code for `db.py` references: `rg "db.py|from ledger import db|db\.init_db"`
- Removed legacy files: `git rm src/arledge/db.py src/arledge/migrations.py`
- Edited CLI and MCP server to call beancount_write/beancount_store instead of db
- Updated tests to use Click's isolated_filesystem and CLI create commands

## Files removed
- src/arledge/db.py
- src/arledge/migrations.py

## Files added/modified
- Modified: src/arledge/cli.py (removed db usage, ensure beancount-first flows)
- Modified: src/arledge/mcp_server.py (replaced db.* with beancount_write/beancount_store equivalents)
- Modified: src/arledge/beancount_write.py (ensure ledger.beancount created on first write)
- Tests removed: tests/test_creditor.py, tests/test_db_operations.py, tests/test_db_path_resolution.py, tests/test_misc_uncovered.py, tests/test_force_coverage.py
- Tests added: tests/test_smoke_cover.py, tests/test_spike_cover.py
- Tests migrated/edited: many tests under tests/ (customer/creditor/invoice CLI flows now use beancount-first fixtures)
- Documentation updated: MINDMAP.md, docs/IMPROVEMENTS_CHECKLIST.md, various chronicles updated to reflect removal

## Rationale
- The project decided on a beancount-only backend to simplify architecture and avoid dual-source parity issues.
- Beancount custom directives and JSON sidecars provide a natural representation for customers, creditors, payment accounts, and complex invoice line items.
- Removing SQLite reduces maintenance burden and improves developer mental model for a single canonical source-of-truth (files under the project base dir).

## Representative test patterns after migration
- Use Click's isolated_filesystem in tests to create a temporary base dir for ledger files
- Seed data via CLI create commands (which use beancount_write) rather than direct DB inserts
- Use beancount_store.* functions for read assertions where appropriate

## Next steps
- Sweep remaining docs and external references to remove mentions of `LEDGER_DB_PATH` or legacy DB initialization (done in this pass but please review external docs)
- Implement IV.5 (invoice_seq robustness and tests) and IV.7 (ledger validate)
- Consider adding a short migration note in the README describing the removal of SQLite and how to migrate old projects (if any)

## Suggested follow-up tasks
- Add a deprecation/upgrade path doc for users who might have existing SQLite DBs (optional)
- Add end-to-end examples showing ledger init, create invoice, and export workflows for new users

