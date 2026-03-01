# Chronicle: Review beancount plan & invoice transaction parsing spike — AMENDED

- timestamp: 2026-03-01T15:40:00+01:00
- participants: agent (assistant), developer

## Summary
This entry updates the earlier spike notes to record what we actually implemented and validated in the session. We progressed the beancount-first plan substantially: implemented the custom-directive spike, coercion/mapping helpers, an on-disk read-only beancount store, many unit/integration tests, and rewired the CLI reads to use the beancount store. We also exercised the system against the `qa/` example layout.

Changes implemented in this session (high-level)
- Implemented `ledger init` CLI command (bootstraps beancount layout).
- Added ARLEDGE_BASEDIR support via `config.get_basedir()` and exposed it in CLI help.
- Implemented conservative beancount parsing helpers and deterministic mappers (Custom -> Pydantic models): customers, creditors, payment accounts, invoices (via transaction mapping + JSON sidecar).
- Added a read-only `src/ledger/beancount_store.py` that loads ledger.beancount via beancount.loader and maps entries to Pydantic models.
- Rewired CLI read commands (customer/creditor/payment-account/invoice list/view/export) to use the beancount-backed store exclusively (SQLite fallback removed).
- Extensive tests added: unit spikes, mapping tests, integration tests using temporary on-disk ledgers, and edge-case tests.
- Pinned beancount in pyproject.toml to a minor range (beancount>=3.2.0,<3.3) to reduce API drift risk.
- Demonstrated the end-to-end read path against the qa/ directory and exported an invoice JSON file.

Files added or modified (representative)
- Added: src/ledger/beancount_spike.py (parsing + mapping helpers, coercion functions)
- Added: src/ledger/beancount_store.py (read-only beancount store)
- Modified: src/ledger/cli.py (init command, basedir help; rewired read commands to beancount_store)
- Modified: src/ledger/config.py (get_basedir + BASEDIR alias)
- Modified: pyproject.toml (pin beancount minor version)
- Added tests under tests/spikes/ and tests/store/ covering parsing, mapping, edge cases, and loader.load_file integration
- Added chronicles entries: this one and others documenting incremental steps

Key technical findings (what the spikes proved)
- beancount.loader.load_file/load_string returns Custom and Transaction entries where metadata is available as entry.meta. Numeric meta often appears as Decimal; quoted meta appears as str. Dates may appear as datetime.date.
- Parsing snippets with beancount.parser.parse_string can return varying arity across versions; code/tests should unpack defensively (entries, errors, *rest).
- Mapping requires explicit coercion utilities (int, bool, Decimal, date->datetime). I added these to avoid subtle type issues when building Pydantic models.
- The invoice model mapping strategy works: Transaction metadata references a JSON sidecar (invoice_data) which contains canonical invoice lines; totals are computed by Invoice model after loading sidecar lines.
- Beancount loader will parse transactions even if accounts are not declared in advance; balance or account validation may still be needed at write time or via a full-ledger validation command.

Tests and quality
- Multiple new tests were added; full test suite now passes locally with coverage above the project threshold (>=75%).
- Tests cover:
  - custom directive round-trip via loader and parser
  - mapping Custom -> Customer/Creditor/PaymentAccount models
  - mapping Transaction -> Invoice with sidecar read
  - edge cases: missing meta, Decimal vs quoted string meta, malformed snippets reporting errors
  - loader.load_file integration with on-disk includes

Operational notes from the QA run
- Using ARLEDGE_BASEDIR=qa we exercised the UI end-to-end:
  - ledger customer list -> showed ACME Corp from qa/includes/customers.beancount
  - ledger creditor list/view -> showed Office Supplies Ltd
  - ledger creditor account list --creditor-id 7 -> showed payment account details (including metadata about filename/lineno)
  - ledger invoice list/view -> showed invoice parsed from includes/invoices/2026-03.beancount with sidecar lines
  - ledger invoice export -> wrote JSON to the requested path, including invoice_number
- ledger init refuses to overwrite existing files without --force (expected)

Decisions made and rationale
- No SQLite fallback for reads: CLI read commands now exclusively use beancount files. This implements the plan's beancount-first direction early and avoids dual-source parity issues.
- Mapping is conservative and skips entries that fail to map (to avoid a single malformed directive breaking all reads). We can tighten this later if desired.
- Sidecar-first invoice lines: invoice transaction meta points to a JSON sidecar; the store prefers sidecar lines for line item details and relies on the transaction metadata for identifiers and posting-level amounts.
- Pin beancount minor version to reduce API surprises; tests are defensive about parse return shapes.

Open gaps (next work items)
- IV.4 Write flow: implement temp-file → snippet validate → append and sidecar writes for invoices. Then switch CLI create commands to use the write flow.
- IV.5 Invoice-number allocation: implement .arledge/invoice_seq, sequence recovery, and tests (we created a placeholder in init but need full semantics for concurrent safety not required now).
- IV.7 Full validation command: implement `ledger validate` to parse full ledger (with includes) and report parse/balance errors and orphan sidecars.
- IV.9 Cleanup & remove SQLite remnants: after write flow is implemented and CLI create commands switched, remove SQLite create/update code and tests and update CHANGELOG.
- More tests for rare edge cases: duplicate directives, unusual quoting, non-UTF file encodings, and account name conventions.

Representative commands run in this session
- uv run ledger init
- ARLEDGE_BASEDIR=qa uv run ledger customer list
- ARLEDGE_BASEDIR=qa uv run ledger creditor list
- ARLEDGE_BASEDIR=qa uv run ledger creditor account list --creditor-id 7
- ARLEDGE_BASEDIR=qa uv run ledger invoice list
- ARLEDGE_BASEDIR=qa uv run ledger invoice view 1
- ARLEDGE_BASEDIR=qa uv run ledger invoice export 1 --format json --path qa/out-inv1.json

## Chronology (high level)
- 2026-03-01: Plan and spike created
- 2026-03-01 (later): Implemented custom directive spike, mapping helpers, tests, beancount_store, CLI rewiring, and QA run (this entry)

## Next steps (short term)
1. Implement IV.4 (write flow) and switch create commands to use it.
2. Implement invoice sequence allocation and recovery (IV.5).
3. Implement `ledger validate` (IV.7) including orphan sidecar detection.
4. Remove SQLite code and tests once write flow is live and covered by tests.

