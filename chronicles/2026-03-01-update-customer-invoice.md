# Chronicle: Add PATCH-style update for Customer and Invoice

- timestamp: 2026-03-01T21:00:00+01:00
- participants: assistant (automated), user

## Summary
Implemented PATCH-style update commands for customers and invoices and corresponding write/store helpers.

## Files modified
- src/arledge/cli.py
  - Added `arledge customer update <customer_id>` which applies a JSON patch (merge) onto the existing customer record and appends an updated `custom "customer"` entry via beancount_write.update_customer.
  - Added `arledge invoice update <invoice_id>` which applies a JSON patch onto the existing invoice model and updates the invoice sidecar JSON atomically via beancount_write.update_invoice.

- src/arledge/beancount_write.py
  - Added `update_customer(c: models.Customer)` to append updated customer custom entries (append-only update).
  - Added `update_invoice(inv: models.Invoice)` to atomically overwrite the invoice sidecar JSON file for the given invoice id.

- src/arledge/beancount_store.py
  - list_customers() updated to pick the newest custom entry per customer_id so appended updates are authoritative.
  - Added get_invoice_sidecar_path(invoice_id) helper to locate the sidecar path for an invoice (used by update_invoice).

## Rationale
- Customers: append-only updates (new custom entry) mirror the creditor update approach and keep write operations simple and atomic.
- Invoices: updating the sidecar JSON is the most direct way to change invoice line items or metadata without touching historical beancount transactions. Sidecar writes are atomic (write-temp + os.replace).
- CLI update commands perform PATCH semantics: they accept a partial JSON object and merge it onto the existing model before validation and persisting. This mirrors RESTful PATCH behavior and avoids requiring clients to provide the full resource representation.

## Next steps
- Run the full test suite (unit + e2e) and adjust tests if any expectations change.
- Optionally add `customer replace` or `invoice replace` if PUT-style semantics are required.

