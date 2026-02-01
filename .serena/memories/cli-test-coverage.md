# CLI Test Coverage (arledge)

Summary of CLI tests added in this refactor and what they assert.

Files added:
- `tests/test_cli_json_output.py`
  - Runs `init-db` then `customer create --model ...` in an isolated filesystem.
  - Asserts exit code 0 and that the command stdout is valid JSON and contains the created `Customer` fields.

- `tests/test_cli_all_json_outputs.py`
  - Comprehensive coverage of JSON-returning CLI endpoints in an isolated filesystem.
  - Exercises (create/list/view) for `customer`, `creditor`, `creditor account`, and `invoice`.
  - Checks that each command exits 0 and that stdout parses as valid JSON (dict or list as appropriate).
  - Verifies `ledger schema <name>` and `--json-schema` per-command flags produce valid JSON schema objects.

Testing philosophy
- Tests run CLI in isolated filesystems so the temporary DB is contained.
- Tests assert machine-actionable output (stdout) is valid JSON; human messages/errors are not parsed as JSON and are printed to stderr.

Date recorded: 2026-02-01