# arledge

Simple CLI ledger for customers and invoices.

## Information for AGENTS

ALWAYS Call Serena MCP initial_instructions!
At the end of implementing a feature or refactorings: make sure to keep Serena memories in sync by encoding the learnings of the changeset.

Requirements:
- Python 3.8+
- uv 0.9+

```bash
# Use uv to run this program
❯ uvx --from git+https://github.com/roobie/arledge ledger instructions
```

### Quick CLI examples (machine-friendly)

The CLI accepts a single JSON model (inline text) or a JSON file for create/update operations. Machine-actionable outputs (JSON objects, JSON arrays, or exported file paths) are printed to stdout; human-facing informational and error messages are printed to stderr. The CLI prints actionable JSON by calling `json.dumps(config.dump_model(...))` on created/listed models; note that `dump_model()` returns a Python dict (decimals and datetimes are converted to strings) and the CLI serializes that dict to JSON before printing.

Examples (inline JSON):

```bash
# Initialize the DB
uv run python -m ledger database initialize

# Create a customer from JSON (prints created customer JSON to stdout)
uv run python -m ledger customer create --model '{"name":"ACME","email":"sales@example.com","address":"123 Road"}'

# Create a creditor from file (prints created creditor JSON to stdout)
uv run python -m ledger creditor create --model-file ./creditor.json

# Create a payment account for a creditor
uv run python -m ledger creditor account create --model '{"creditor_id":1,"type":"bank","identifier":"SE455...","currency":"SEK"}'

# Create an invoice (lines must be an array of objects)
uv run python -m ledger invoice create --model '{"customer_id":1,"lines":[{"description":"Service","quantity":1,"unit_price":"1000.00","vat_rate":"25"}]}'

# Export an invoice to JSON (prints exported path to stdout)
uv run python -m ledger invoice export 1 --format json --path invoice-1.json

# List customers or invoices (outputs JSON array to stdout)
uv run python -m ledger customer list
uv run python -m ledger invoice list
```

Notes:
- Use `--model` to provide inline JSON text and `--model-file` to provide a path to a UTF-8 encoded JSON file (the CLI reads files with `encoding='utf-8'`).
- JSON is validated using Pydantic (v2) with `Model.model_validate_json()`; validation errors and file-read errors are printed to stderr and the CLI exits non-zero (the code uses `sys.exit(2)` for these error conditions). Agents and scripts should check the process exit code before parsing stdout.
- Use `ledger/config.dump_model()` to obtain a JSON-serializable Python dict for models; `dump_model` converts `Decimal` values to culture-invariant strings and `datetime` values to UTC ISO strings ending with `Z`. The CLI then uses `json.dumps(...)` to produce machine JSON from that dict.

### Schema examples

You can print the Pydantic JSON Schema for models either via the top-level `schema` command or the per-command `--json-schema` flag. Schema output is JSON on stdout.

```bash
# Top-level schema command
uv run python -m ledger schema customer

# Per-command schema flag
uv run python -m ledger customer create --json-schema
```

The schema is generated from the Pydantic models defined in `ledger/models.py`.


````

## MCP stdio server

This project can run an MCP server over stdin/stdout using the official `mcp` package's `FastMCP` implementation. The CLI exposes a small wrapper command:

```
# Dry-run (validate imports and configuration, then exit)
uv run python -m ledger mcp start --dry-run

# Start the stdio MCP server (blocks, listens on stdin/stdout)
uv run python -m ledger mcp start
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

