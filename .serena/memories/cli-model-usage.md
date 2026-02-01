# CLI Model Usage (arledge)

Summary of CLI behavior and business rules after refactor to `--model`/`--model-file`.

- CLI create/update commands accept either:
  - `--model` : a JSON string passed inline, or
  - `--model-file` : a path to a JSON file (explicit file arg).

- Parsing & validation:
  - Input JSON is parsed and validated using Pydantic v2 model methods:
    - `Model.model_validate_json()` is used to parse raw JSON into model instances.
  - Validation errors are printed to stderr and the CLI exits with a non-zero status code.

- Output semantics (Unix philosophy):
  - Actionable machine-readable outputs (created models, lists, exported file paths) are printed to stdout as JSON or plain path strings.
  - Informational or human-facing messages (progress, warnings, validation errors) are printed to stderr.

- Pydantic models and canonical serialization:
  - Models live in `ledger/models.py` (`Customer`, `Creditor`, `PaymentAccount`, `Invoice`, `InvoiceLine`, etc.).
  - For CLI output, `ledger/config.py::dump_model()` is used to convert models to canonical JSON (decimals and datetimes normalized: ISO-8601 Z and culture-invariant decimals).

- DB API expectations:
  - The DB layer (`ledger/db.py`) accepts and returns Pydantic model instances for create/get/list operations.
  - CLI constructs validated model instances and passes them directly to DB create/update functions.

- File input:
  - `--model-file` is explicit; the CLI reads the file and treats its contents as the JSON payload.

- Error handling and exit codes:
  - Validation or I/O errors -> printed to stderr, exit code `2`.
  - Successful operations -> actionable JSON on stdout, exit code `0`.

Date recorded: 2026-02-01
