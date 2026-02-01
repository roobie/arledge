# arledge

Simple CLI ledger for customers and invoices.

## Information for AGENTS

Call Serena MCP initial_instructions

Requirements:
- Python 3.8+
- uv 0.9+

```bash
# Initialize project by
uv sync

# The the application can be called like this:

# Fetch instructions on how to use
uv run python -m ledger instructions

# Initialize the database (sqlite3)
uv run python -m ledger init-db

# Create a customer
uv run python -m ledger customer create --name "ACME" --email "sales@example.com" --address "123 Road"

# Create an invoice
uv run python -m ledger invoice create --customer-id 1 --line "Service,1,1000,25" --due-days 30
```
