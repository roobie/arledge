# arledge

Simple CLI ledger for customers and invoices (beancount-file-first).

## Information for AGENTS

Requirements:
- Python 3.11+
- uv 0.9+

```bash
# Use uv to run this program
❯ uvx --from git+https://github.com/roobie/arledge arledge instructions
```

### Quick CLI examples (machine-friendly)

The CLI accepts a single JSON model (inline text) or a JSON file for create/update operations. Machine-actionable outputs (JSON objects, JSON arrays, or exported file paths) are printed to stdout; human-facing informational and error messages are printed to stderr. The CLI prints actionable JSON by calling `json.dumps(config.dump_model(...))` on created/listed models; note that `dump_model()` returns a Python dict (decimals and datetimes are converted to strings) and the CLI serializes that dict to JSON before printing.

Examples (inline JSON):

```bash
# Initialize the beancount layout (creates ledger.beancount, includes/, .arledge/)
uv run arledge init

# Create a customer from JSON (prints created customer JSON to stdout)
uv run arledge customer create --model '{"name":"ACME","email":"sales@example.com","address":"123 Road"}'

# Create a creditor from file (prints created creditor JSON to stdout)
uv run arledge creditor create --model-file ./creditor.json

# Create a payment account for a creditor
uv run arledge creditor account create --model '{"creditor_id":1,"type":"bank","identifier":"SE455...","currency":"SEK"}'

# Create an invoice (lines must be an array of objects)
uv run arledge invoice create --model '{"customer_id":1,"lines":[{"description":"Service","quantity":1,"unit_price":"1000.00","vat_rate":"25"}]}'

# Export an invoice to JSON (prints exported path to stdout)
uv run arledge invoice export 1 --format json --path invoice-1.json

# List customers or invoices (outputs JSON array to stdout)
uv run arledge customer list
uv run arledge invoice list
```

Notes:
- Use `--model` to provide inline JSON text and `--model-file` to provide a path to a UTF-8 encoded JSON file (the CLI reads files with `encoding='utf-8'`).
- JSON is validated using Pydantic (v2) with `Model.model_validate_json()`; validation errors and file-read errors are printed to stderr and the CLI exits non-zero (the code uses `sys.exit(2)` for these error conditions). Agents and scripts should check the process exit code before parsing stdout.
- Use `ledger/config.dump_model()` to obtain a JSON-serializable Python dict for models; `dump_model` converts `Decimal` values to culture-invariant strings and `datetime` values to UTC ISO strings ending with `Z`. The CLI then uses `json.dumps(...)` to produce machine JSON from that dict.

### Storage & invoice sequence

This project uses a beancount-file-first approach: a top-level `ledger.beancount` file that includes files under `includes/` is the canonical ledger. Entities such as customers, creditors, and payment accounts are stored as `custom` directives in `includes/*.beancount`. Invoice transactions live in `includes/invoices/*.beancount`, and detailed invoice line items are stored in JSON sidecar files under `includes/invoices/data/` referenced by transaction metadata (invoice_data).

Invoice numbering and allocation
- The file `.arledge/invoice_seq` stores the next-available invoice id as a single integer followed by a newline. Example contents: `2\n` means the next allocated id will be 2.
- Allocation is atomic: the code writes the incremented next-value to a temporary file in the same directory and uses `os.replace()` to atomically replace the sequence file.
- Recovery: if the sequence file is missing or corrupt, allocation scans existing invoices (beancount includes) to compute the maximum invoice id and use max+1 as the next id.

Example: allocate and create a new invoice

```bash
# Create an invoice; CLI prints invoice JSON which includes `invoice_number`
uv run arledge invoice create --model '{"customer_id":1,"lines":[{"description":"Service","unit_price":"1000.00"}]}'
```

### Schema examples

You can print the Pydantic JSON Schema for models either via the top-level `schema` command or the per-command `--json-schema` flag. Schema output is JSON on stdout.

```bash
# Top-level schema command
uv run arledge schema customer

# Per-command schema flag
uv run arledge customer create --json-schema
```

The schema is generated from the Pydantic models defined in `ledger/models.py`.


## MCP stdio server

This project can run an MCP server over stdin/stdout using the official `mcp` package's `FastMCP` implementation. The CLI exposes a small wrapper command:

```
# Dry-run (validate imports and configuration, then exit)
uv run arledge mcp start --dry-run

# Start the stdio MCP server (blocks, listens on stdin/stdout)
uv run arledge mcp start
```

Example `FastMCP` usage (the server launcher registers a minimal `ping` tool):

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo Server")

@mcp.tool()
def add(a: int, b: int) -> int:
	return a + b

if __name__ == "__main__":
	print("✅ MCP server has started")
	mcp.run()
```

Note: this CLI command lazily imports the `mcp` runtime so other CLI commands and tests are not affected when `mcp` is not used. Use `--dry-run` in unit tests to avoid blocking the test process.

Migration note

If you previously used a legacy SQLite backend, note that the project now uses beancount files as the single source-of-truth. If you need help migrating an existing SQLite DB to beancount includes/sidecars, get in touch or consider writing a conversion tool that exports DB rows into `includes/*.beancount` and invoice sidecars.

