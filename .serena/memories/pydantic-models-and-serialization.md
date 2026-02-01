# Pydantic Models and Serialization (arledge)

Summary
- Project conventions for Pydantic models, parsing, serialization, and JSON Schema generation.

Key points
- Models live in `ledger/models.py` and include `Customer`, `Creditor`, `PaymentAccount`, `InvoiceLine`, `Invoice`.
- Parsing: prefer `Model.model_validate_json()` for CLI raw JSON; `model_validate_strings()` only when consuming string-keyed string-valued maps.
- Schema: `Model.model_json_schema()` is used by `--json-schema` and `ledger schema`.
- model_version: all models include a `model_version` field (default package `__version__`) to aid compatibility/migrations.
- Serialization: use `ledger/config.dump_model()` for CLI and export outputs to ensure:
  - datetimes serialized as timezone-aware UTC ISO-8601 with `Z` suffix
  - `Decimal` values serialized as culture-invariant strings
- Performance/constructors: `model_construct()` exists but should be used only when data is already validated/trusted.

Files referenced
- ledger/models.py
- ledger/config.py

Provenance
- Merged and pruned from `pydantic_models_usage` and selected project-relevant excerpts from `pydantic` docs.