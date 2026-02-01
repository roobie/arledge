# CLI Model Usage (arledge) — UPDATED

This memory captures the canonical CLI behaviour after the recent refactor.

Inputs
- Create/update commands accept either:
  - `--model` : inline JSON string
  - `--model-file` : explicit path to a JSON file
- Commands also accept `--json-schema` to print the Pydantic JSON Schema for that model and exit.
- There is a top-level command: `ledger schema <name>` that prints the JSON Schema for named models (`customer`, `creditor`, `account`, `invoice`, `invoice-line`).

Parsing & validation
- All incoming JSON is parsed and validated using Pydantic v2 methods:
  - `Model.model_validate_json()` is used to parse raw JSON strings into model instances.
- On validation errors or I/O errors the CLI prints the error message to stderr and exits with a non-zero status code (exit code `2` for validation/I/O errors).

Output conventions (Unix philosophy)
- Actionable machine-readable outputs are printed to stdout:
  - Created/returned models are printed as canonical JSON (via `ledger/config.dump_model()`), lists are JSON arrays, schema output is JSON, and export commands print the exported filepath string to stdout.
- Human/informational messages (progress, warnings, validation errors) are printed to stderr.

Schema support
- `Model.model_json_schema()` is used to produce JSON Schema for Pydantic models.
- `ledger schema <name>` and per-command `--json-schema` both print this schema to stdout in pretty JSON (indent=2).

Tests and docs
- README updated with examples for `--model`, `--model-file`, `--json-schema`, and `ledger schema` usage.
- Tests were added to assert that all CLI endpoints expected to output JSON do so and that the output parses as JSON.

Date recorded: 2026-02-01