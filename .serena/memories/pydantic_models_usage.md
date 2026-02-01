# Pydantic Models Usage (arledge) — UPDATED (model_version)

This memory documents the Pydantic model conventions for arledge after the recent changes.

Location
- Primary models live in `ledger/models.py`: `Customer`, `Creditor`, `PaymentAccount`, `InvoiceLine`, `Invoice`.

Key conventions
- Validation/parsing:
  - Prefer `Model.model_validate_json()` for raw JSON input from CLI.
  - Use `Model.model_validate_strings()` when accepting string-keyed string values (if/when needed).
- Serialization:
  - Use `ledger/config.dump_model()` to produce canonical JSON for CLI output and file exports. This ensures:
    - `datetime` values are normalized to timezone-aware UTC ISO-8601 strings with `Z`.
    - `Decimal` values are serialized as culture-invariant strings.
- model_version:
  - All models now include a `model_version: str` field defaulting to the package `__version__` (from `ledger/__init__.py`).
  - This field is present in model inputs/outputs and is intended to help compatibility and migrations.
- JSON Schema and introspection:
  - `Model.model_json_schema()` is used by `--json-schema` and `ledger schema` command to produce JSON Schema for programmatic use and validation.

DB integration
- DB layer (`ledger/db.py`) continues to accept and return Pydantic model instances. The models include `model_version` and the DB serialization uses `dump_model()` on exports.

Date recorded: 2026-02-01