# Chronicle: Start IV.5 — Invoice seq allocation (allocate_invoice_id)

- timestamp: 2026-03-01T13:05:00+01:00
- participants: assistant

## Summary
Implemented atomic, recoverable invoice-id allocation for the beancount-first write flow. Added tests to exercise initial allocation, sequential allocations, and recovery from a corrupt sequence file. Updated create_invoice to use the allocator.

## Changes made
- src/ledger/beancount_write.py
  - Added _atomic_write helper that writes to a temporary file in the same directory and uses os.replace for atomic replace.
  - Implemented allocate_invoice_id() which:
    - Scans existing invoices to compute a recovery base (max id)
    - Reads the sequence file if present, falling back to recovery if corrupt
    - Writes next available id atomically and returns the allocated id
  - create_invoice now calls allocate_invoice_id() to assign inv.id prior to writing the sidecar and snippet.
- Tests added: tests/test_invoice_seq.py
  - test_invoice_seq_initial_and_increment
  - test_invoice_seq_recovers_from_corrupt_file

## Commands run
- Ran pytest iteratively during development: `uv run pytest tests/test_invoice_seq.py -q` and full suite `uv run pytest -q`

## Representative outputs
- On fresh layout: create invoice allocates id=1 and .arledge/invoice_seq contains "2\n".
- On corrupt seq: allocator recovers by scanning existing invoices and allocates the next id (2) and writes "3\n".

## Next steps
- Add more edge-case tests (concurrent allocations are out of scope for single-user model).
- Implement CLI-visible `ledger invoice allocate` if you want to expose allocation without creating an invoice.
- Proceed to IV.7 (ledger validate).
