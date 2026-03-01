# Chronicle: Invoice transaction parsing spike

- timestamp: 2026-03-01T15:40:00+01:00
- participants: agent (assistant), developer

## Summary

Implemented invoice transaction parsing spike — extending task IV.2 to cover beancount transactions (not just custom directives). Demonstrated that beancount Transaction entries expose metadata, postings, and amounts in a form that maps cleanly to the Invoice/InvoiceLine Pydantic models.

## Files added

- `src/arledge/beancount_spike.py` — Added `extract_transaction_entries()` and `map_transaction_to_invoice()` functions
- `tests/spikes/test_invoice_transaction_parsing.py` — 17 tests covering raw parsing, model mapping, and edge cases (all passing)

## Key technical findings

- beancount.loader returns Transaction entries with accessible narration, metadata (as entry.meta), and postings (with account names, amounts, currencies).
- Metadata values are auto-coerced: numeric values become Decimal, dates become datetime.date, strings stay as strings.
- Invoice lines are loaded from JSON sidecar files referenced in transaction metadata (invoice_data field).
- Invoice model auto-computes totals (subtotal, VAT, total) from line items and VAT rates.
- Transaction parsing works even if account names are not declared in advance; account validation is deferred to write-time or full-ledger validation.

## Tests added (summary)

- `TestTransactionParsing`: raw beancount parsing — narration, metadata types, postings, amounts
- `TestMapTransactionToInvoice`: round-trip mapping, date coercion, sidecar line loading, total auto-computation, currency detection
- `TestInvoiceMappingEdgeCases`: missing customer_id (error), missing sidecar (empty lines), status defaults, multiple invoices

## Open gaps

- IV.4 Write flow: temp-file → snippet validate → append + sidecar writes for invoices.
- IV.5 Invoice-number allocation: .arledge/invoice_seq with recovery semantics.
- IV.7 Full validation command: `ledger validate` for parse/balance/orphan-sidecar checks.
- IV.9 SQLite cleanup: remove create/update code once write flow is live.

## Next steps

1. Implement write flow and spike (temp-file pattern, snippet validation).
2. Implement invoice sequence allocation.
3. Add `ledger validate` command.
