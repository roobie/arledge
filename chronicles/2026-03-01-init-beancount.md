# Chronicle: Implement `ledger init` (Beancount layout bootstrap)

- timestamp: 2026-03-01T11:24:39+01:00
- participants: agent (assistant), developer

## Summary
Implemented the `ledger init` CLI command which bootstraps the beancount-first directory layout for the arledge project. This implements task #IV 1) from BEANCOUNT_REPLACEMENT_PLAN.md.

The command creates the following structure in the current working directory:

- ledger.beancount (top-level include file)
- includes/
  - customers.beancount
  - creditors.beancount
  - payment_accounts.beancount
  - invoices/
    - YYYY-MM.beancount (current month created as example)
    - data/ (for invoice JSON sidecars)
- .arledge/
  - invoice_seq (initialized to "1")

By default the command will not overwrite existing files or directories; pass `--force` to replace.

## Representative commands run
- Edited: ledger/cli.py (added `init` command)
- Wrote: chronicles/2026-03-01-init-beancount.md

## Files added/modified
- modified: ledger/cli.py  (added CLI command `ledger init`)
- added: chronicles/2026-03-01-init-beancount.md

N.B
Moved `ledger` into `src` dir

## Suggested next steps
- Add unit tests for `ledger init` to verify idempotence, --force behaviour, and file contents.
- Implement beancount parsing spike (task 2) and read-only mapping (task 3).
- Begin write-flow implementation (task 4) and invoice-seq handling (task 5).

