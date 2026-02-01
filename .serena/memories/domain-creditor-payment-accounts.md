# Domain: Creditor & Payment Accounts (arledge)

Summary
- Business rules, DB schema notes, and mapping guidance for creditors, creditor payment accounts, and invoice-creditor relationships.

Entities & fields (high level)
- `creditors`: `id`, `name`, `address`, `email`, `phone`, `tax_id`, `payment_instructions`, `default_currency` (default 'SEK'), `beancount_account`, `created_at`.
- `creditor_payment_accounts`: `id`, `creditor_id`, `type` (bank|paypal|card|other), `label`, `identifier` (IBAN/email/id), `bank_name`, `currency`, `beancount_account`, `is_default` (0/1), `metadata` (JSON), `created_at`.

Business rules
- `metadata` is free-form JSON for provider-specific fields; stored as JSON text in DB and loaded with `json.loads`.
- Creating a payment account with `is_default` clears other defaults for that creditor (operation handled atomically in DB helper).
- Sensitive identifiers (IBAN, PayPal email) currently stored plaintext; encryption-at-rest is a future improvement.
- Monetary values: invoice line `unit_price` stored as integer cents in DB; conversion happens in DB layer (multiply/quantize) to avoid float drift.

Invoice linkage & beancount mapping
- `invoices` reference `creditor_id` and have `currency`; exporters prefer `payment_account.beancount_account`, fall back to `creditor.beancount_account`.

Migrations & DB
- `ledger/db.py` contains `init_db()` which is idempotent; for explicit migrations see `ledger/migrations.py` (placeholder for scripted migrations).

Files referenced
- ledger/db.py
- ledger/models.py
- ledger/migrations.py

Provenance
- Consolidated from `creditors-payment-accounts-business-logic` and DB implementation notes.