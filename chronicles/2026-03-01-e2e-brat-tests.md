# Chronicle: Add brat e2e workflow tests

- timestamp: 2026-03-01T16:00:00+01:00
- participants: assistant, developer

## Summary

Implemented comprehensive end-to-end workflow tests using brat (POSIX shell TAP harness). Created 26 tests covering complete CLI workflows: init → create entities → create invoices → export → validate. All tests pass.

## Changes

- Added: `tests/e2e/helpers.sh` — shared helpers (ledger wrapper, setup/teardown, jq_field utility)
- Added: `tests/e2e/init.brat` — 4 tests for `ledger init` command
- Added: `tests/e2e/customers.brat` — 6 tests for customer create/list workflows
- Added: `tests/e2e/creditors.brat` — 7 tests for creditor + payment account workflows
- Added: `tests/e2e/invoices.brat` — 7 tests for invoice create/list/view/export workflows
- Added: `tests/e2e/full.brat` — 1 comprehensive workflow test (init → all entities → export → validate)
- Added: `script/test-e2e` — thin shell script to run brat tests

## Test Results

```
✓ 26 tests (26 passed, 0 failed, 0 skipped)
```

Test coverage by command:
- `ledger init` — idempotence, directory structure creation, --force flag
- `customer` — create, list, error handling
- `creditor` — create, list, view; payment account create/list
- `invoice` — create (with multiple lines), list, view, export, sequential numbering
- `ledger validate` — full ledger validation after create operations

## How to run

```sh
# Run all e2e tests
./script/test-e2e

# Run a single test file
vendor/brat/bin/brat tests/e2e/customers.brat

# Run in parallel
vendor/brat/bin/brat -j 4 tests/e2e/*.brat

# Run a specific test by line number
vendor/brat/bin/brat tests/e2e/invoices.brat:50
```

## Technical notes

- Uses `uv run ledger` to invoke CLI in test environment
- `ARLEDGE_BASEDIR` controls ledger location for test isolation
- `jq` is required for JSON field extraction
- Brat's `match` helper supports both literal substrings and ERE regex patterns (delimited by `/`)
- JSON output includes spaces after colons (e.g., `"name": "value"`)
- All monetary values are strings with 2 decimal places (e.g., `"1000.00"`)

## Next steps

- Add tests for error cases (invalid JSON, missing fields, etc.)
- Add tests for MCP server integration
- Consider adding brat tests to CI/CD pipeline
