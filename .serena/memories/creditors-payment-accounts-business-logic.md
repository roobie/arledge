Summary: design decisions for Creditor + inbound payment accounts (business logic)

- DB entities added
  - `creditors`: id, name, address, email, phone, tax_id, payment_instructions, default_currency ('SEK'), beancount_account, created_at
  - `creditor_payment_accounts`: id, creditor_id, type (bank|paypal|card|other), label, identifier (IBAN/email/id), bank_name, currency, beancount_account, is_default (0/1), metadata (JSON), created_at

- Invoice linkage
  - `invoices` can reference `creditor_id` and have a `currency` field (default 'SEK'). Invoices reference a creditor for header/payment details.

- Data rules
  - Payment-account `metadata` is free-form JSON for provider-specific fields.
  - Creating a payment account with `is_default` clears other defaults for that creditor (atomic in helper).
  - Sensitive identifiers (IBAN, PayPal email) are stored plaintext for now; encryption-at-rest planned as future improvement.
  - Monetary values in invoice lines use integer cents for unit_price; totals computed in code to avoid float drift.

- CLI surface implemented
  - `creditor` group: `create`, `list`, `view`.
  - `creditor account` subgroup: `create`, `list` (supports `--default`, `--metadata` JSON).
  - `invoice create` accepts `--creditor-id` to link invoices to a creditor.

- Beancount mapping guidance
  - Prefer `creditor_payment_accounts.beancount_account` for exporter mapping; fall back to `creditors.beancount_account` or a default `Assets:AccountsReceivable:Customers:<name>`.

- Migrations
  - `init_db()` is idempotent and creates new tables; `ensure_column()` adds `creditor_id` and `currency` if missing. A `migrations.py` placeholder exists for future explicit migrations.

- Next/Unresolved
  - Add encryption for sensitive fields, stronger FK constraints, validation for IBAN/identifiers, and explicit scripted migrations.
