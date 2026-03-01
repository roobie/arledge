# Chronicle: Add `creditor update` CLI command

- timestamp: 2026-03-01T20:45:00+01:00
- participants: assistant (automated), user

## Summary
Added a new CLI subcommand `arledge creditor update <creditor_id>` which allows updating creditor metadata by appending an updated `custom` entry to the beancount includes. Implemented an append-only update in `src/arledge/beancount_write.py` and adjusted the read-path to prefer the most recent entry for a given creditor id.

## Files modified / added
- src/arledge/cli.py — added `creditor update <creditor_id>` command. The command accepts `--model` or `--model-file` and `--json-schema` and calls `beancount_write.update_creditor`.
- src/arledge/beancount_write.py — added `update_creditor(cred: models.Creditor)` which composes and appends an updated `custom "creditor"` entry. The function validates the snippet before appending.
- src/arledge/beancount_store.py — updated `list_creditors()` to deduplicate by creditor_id and return the latest entry (by date) for each id so that appended updates become authoritative.

## Rationale
- Beancount is used as a file-first, append-based datastore. Rewriting include files is more error-prone and would require more complex parsing. An append-only update keeps write logic simple and atomic.
- To make updates visible to read helpers, `list_creditors()` now returns the newest entry per creditor_id.

## Usage example
- Print creditor JSON schema:
  `arledge creditor update --json-schema`
- Update creditor 3 using inline JSON (partial or full fields):
  `arledge creditor update 3 --model '{"name":"New Name","email":"billing@example.com"}'`

## Notes & caveats
- This update is append-only: old entries remain in the include file but the store picks the newest entry by date for each id.
- If you prefer rewrite semantics (replace the existing entry in the include file), we can implement file rewrite, but it introduces more complexity and risk.
- I did not add an explicit `delete` or `replace` operation.

## Next steps
- Run the test suite (unit + e2e) to ensure no regressions — I can run this and report results or push commits for CI runs.
- Optionally implement similar update behavior for customers and payment accounts if desired.

