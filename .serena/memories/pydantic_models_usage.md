# Pydantic Models Usage (arledge) — UPDATED

This memory records the canonical rules for models and serialization used across the codebase.

- Models: `ledger/models.py` contains `Customer`, `Creditor`, `PaymentAccount`, `Invoice`, `InvoiceLine`, etc.
- Validation: use Pydantic v2 APIs (`model_validate_json()`, `model_validate_strings()` if accepting strings, `model_dump()` for plain dicts).
- Serialization: use `ledger/config.py::dump_model()` when emitting JSON from the CLI or when exporting to files; this ensures `Decimal` and `datetime` are converted to invariant strings (ISO-8601 UTC `Z` and plain decimal strings).
- DB integration: DB functions expect Pydantic model instances and persist canonical representations (datetimes as ISO strings, decimals as culture invariant strings).

Date recorded: 2026-02-01
