# CLI Surface and Conventions (arledge)

Summary
- Canonical CLI patterns and machine/human I/O rules for automation.

Commands & flags
- `ledger <group> <action>` command groups implemented in `ledger/cli.py`.
- JSON input accepted via `--model` (inline JSON string) or `--model-file` (path to a JSON file).
- Per-command `--json-schema` flag and top-level `ledger schema <name>` print Pydantic JSON Schema to stdout.

Parsing & validation
- CLI uses Pydantic parsing for incoming JSON: prefer `Model.model_validate_json()` for raw JSON inputs.
- Validation and I/O errors print human-readable messages to stderr and exit non-zero (tests expect non-zero on validation errors).

Output conventions
- Machine-actionable outputs (created/listed models, schema) are printed to stdout as canonical JSON using `ledger/config.dump_model()`.
- Human/informational messages (progress, warnings, validation errors) are printed to stderr.

Test coverage
- Tests that assert JSON outputs are in `tests/test_cli_json_output.py` and `tests/test_cli_all_json_outputs.py` (see tests for exact commands exercised).

Files referenced
- ledger/cli.py
- ledger/config.py
- tests/test_cli_all_json_outputs.py
- tests/test_cli_json_output.py

Provenance
- Merged from memories: `cli-model-usage`, `cli-test-coverage` (pruned and consolidated).