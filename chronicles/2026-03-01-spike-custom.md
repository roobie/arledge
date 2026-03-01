# Chronicle: Implement custom directive spike and tests

- timestamp: 2026-03-01T15:05:00+01:00
- participants: agent (assistant), developer

## Summary
Added a small spike module and two pytest tests that verify beancount `custom`
directives round-trip metadata through beancount's loader and parser APIs.

This implements IV.2 (custom directive spike) from the BEANCOUNT_REPLACEMENT_PLAN.

## Changes
- Added: src/ledger/beancount_spike.py (helpers for extracting custom entries and mapping)
- Added: tests/spikes/test_custom_directive.py (pytest tests using beancount.loader and beancount.parser)

## Representative commands run
- Created files (above) — tests are runnable with the project's test runner (e.g., `uv run ledger` project's pytest invocation).

## Next steps
- Run the tests in a local environment with beancount installed to validate behavior.
- If the mapping heuristics need refinement, update src/ledger/beancount_spike.py to map onto Pydantic models directly.
- Add a test that maps a Custom entry to src/ledger/models.Customer using the spike mapping helper.
