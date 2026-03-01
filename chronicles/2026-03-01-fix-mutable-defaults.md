# Chronicle: Fix mutable-default bugs

- timestamp: 2026-03-01T11:24:39+01:00
- participants: assistant

## Summary
Fixed mutable default value usage in Pydantic models to prevent shared mutable state across instances. Changes were made to arledge/models.py to use pydantic Field(default_factory=...) instead of literal mutable defaults.

## Commands run (representative)
- Edited arledge/models.py to replace mutable defaults

## Files modified
- arledge/models.py
  - Replaced `from pydantic import BaseModel, field_validator, model_validator` with `from pydantic import BaseModel, field_validator, model_validator, Field`.
  - Replaced `metadata: Dict[str, Any] = {}` with `metadata: Dict[str, Any] = Field(default_factory=dict)` in PaymentAccount.
  - Replaced `lines: List[InvoiceLine] = []` with `lines: List[InvoiceLine] = Field(default_factory=list)` in Invoice.

## Rationale
Mutable defaults like {} and [] are shared across all instances created without explicit values, which can cause surprising behavior and bugs. Using default_factory ensures each instance gets its own fresh container.

## Next steps / Suggested review
1. Review arledge/models.py changes.
2. Run the test suite (pytest -q) to ensure no regressions.
3. If acceptable, commit the changes locally. I did NOT stage/commit or open a PR per your instruction.

