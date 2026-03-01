# Chronicle: QA session - create a fictitious ledger in ./qa

- timestamp: 2026-03-01T11:26:17+01:00
- participants: assistant

## Summary
Created a temporary QA ledger under `./qa` using the CLI with LEDGER_DB_PATH pointing to `qa/ledger.db`. Created a customer, creditor, payment account, invoice, and exported the invoice to JSON.

## Commands run (representative)
- mkdir -p qa
- LEDGER_DB_PATH=qa/ledger.db uv run python -m ledger database initialize
- LEDGER_DB_PATH=qa/ledger.db uv run python -m ledger customer create --model '{"name":"ACME Corp","email":"sales@acme.example","address":"123 Road"}'
- LEDGER_DB_PATH=qa/ledger.db uv run python -m ledger customer list
- LEDGER_DB_PATH=qa/ledger.db uv run python -m ledger creditor create --model '{"name":"MyCompany","email":"billing@myco.example"}'
- LEDGER_DB_PATH=qa/ledger.db uv run python -m ledger creditor account create --model '{"creditor_id":1,"type":"bank","identifier":"SE455...","currency":"SEK"}'
- LEDGER_DB_PATH=qa/ledger.db uv run python -m ledger invoice create --model '{"customer_id":1,"lines":[{"description":"Service","quantity":1,"unit_price":"1000.00","vat_rate":"25"}]}'
- LEDGER_DB_PATH=qa/ledger.db uv run python -m ledger invoice export 1 --format json --path qa/invoice-1.json

## Files created
- qa/ledger.db (SQLite DB)
- qa/customer.json (created customer JSON output)
- qa/customers.json (list output)
- qa/creditor.json
- qa/payment_account.json
- qa/invoice.json
- qa/invoice-1.json (exported invoice file)
- qa/export.out (stdout of export command)

## Observations
- CLI executed successfully with LEDGER_DB_PATH set.
- invoice JSON contains computed totals and invoice_number as expected.

## Next steps
- Remove QA artifacts when done: rm -rf qa

