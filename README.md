# ledger

Simple CLI ledger for customers and invoices.

Requirements:
- Python 3.8+
- pip install -r requirements.txt

Usage:
python -m ledger init-db
python -m ledger customer create --name "ACME" --email "sales@example.com" --address "123 Road"
python -m ledger invoice create --customer-id 1 --line "Service,1,1000,25" --due-days 30
