# Pydantic Models Usage (arledge)

Summary of important points about how this application uses Pydantic models and canonical encoding.

- Location of models: `ledger/models.py`.
  - Models implemented: `Creditor`, `PaymentAccount`, `Customer`, `InvoiceLine`, `Invoice`.
  - Models use Pydantic v2 APIs and `model_validate` / `model_dump` semantics.

- Canonical encoders/decoders and dump helper: `ledger/config.py`.
  - `dt_to_iso_utc(datetime) -> str` and `iso_to_dt(str) -> datetime` — always produce/consume timezone-aware UTC datetimes.
  - `decimal_to_str(Decimal) -> str` and `str_to_decimal(str) -> Decimal` — culture-invariant decimal strings.
  - `dump_model(model)` returns a JSON-serializable dict where `Decimal` and `datetime` values are converted to invariant strings (ISO-8601 with `Z` for UTC, and decimal as `'-1234.56'`).

- Money and dates policy:
  - All monetary values in models use `decimal.Decimal` for precise arithmetic.
  - `InvoiceLine.unit_price` and other inputs accept strings/floats and are coerced to `Decimal` in validators.
  - Datetimes are timezone-aware and normalized to UTC in models; stored/exported as ISO-8601 UTC strings (e.g., `2026-02-01T12:00:00Z`).

- Database storage conventions (`ledger/db.py`):
  - Public DB API now accepts and returns Pydantic model instances (breaking change).
  - `unit_price` is persisted as integer cents in DB (`unit_price` column stores cents as INTEGER).
  - Decimal fields stored in DB columns as culture-invariant strings where appropriate (e.g., `quantity`, `vat_rate` saved as strings).
  - Datetimes are stored as ISO-8601 UTC strings in TEXT columns.
  - `create_*` functions now take model instances and return model instances with `id` fields assigned.

- Invoice computation:
  - `InvoiceLine` computes `net`, `vat`, and `line_total` in a `model_validator`.
  - `Invoice` computes `subtotal`, `total_vat`, and `total` in a `model_validator` and ensures `created_at` defaults to UTC now when missing.

- Exports and backward compatibility:
  - Use `config.dump_model()` for JSON export to ensure Decimal and datetime are serialized consistently.
  - This refactor is intentionally breaking: delete existing `ledger.db` and run `init_db()` to recreate schema.

- Tests and CLI:
  - Tests updated to use models (see `tests/test_creditor.py`).
  - CLI (`ledger/cli.py`) still needs final updates to use models end-to-end; current code may use old dict-based access in some places.

- Dependencies and notes:
  - `pyproject.toml` updated to require `pydantic>=2.12.5` (v2).
  - Avoid `json_encoders` deprecated API; `dump_model()` centralizes serialization.

- Quick migration steps:
  1. Delete `ledger.db`.
  2. Run: `python -m ledger init-db` (or `uv run pytest` will re-run tests using the fresh DB in CI).
  3. Update any external code expecting dicts to consume Pydantic models or use `dump_model()`.

- Files to inspect:
  - `ledger/models.py`, `ledger/config.py`, `ledger/db.py`, `ledger/cli.py`, `ledger/migrations.py`, `tests/test_creditor.py`.

Date recorded: 2026-02-01
