# Chronicle: Rename CLI invocation to `arledge` and update docs

- timestamp: 2026-03-01T19:50:00+01:00
- participants: assistant (automated), user

## Summary
Performed a repository-wide sweep to update CLI invocation examples and agent-facing instructions to reflect the executable name change from `ledger` -> `arledge` (pyproject defines the console script `arledge`). Changes include updates to the top-level README, the CLI `instructions` output, test helpers, the e2e README, and the MINDMAP. Also updated the e2e test helper to run `uv run arledge` so existing `run ledger ...` test bodies continue to work.

## Files modified
- src/ledger/cli.py — updated top-level docstring examples, `ledger_contents` header, MCP example, `instructions` output (now uses `arledge` in examples), and schema help text.
- README.md — replaced examples invoking the CLI via `python -m ledger` / `uv run python -m ledger` with `uv run arledge` and updated uvx example to reference `arledge instructions`.
- tests/e2e/helpers.sh — changed the test wrapper to call `uv run arledge` (previously `uv run ledger`).
- tests/e2e/README.md — clarified that the bundled runner is at @vendor/brat/ and that the ledger() helper runs `uv run arledge`.
- MINDMAP.md — updated CLI invocation notes to reference `arledge` and aligned CI coverage threshold note.

## Rationale
- The project ships a console script named `arledge` (pyproject.toml) but documentation and examples still referenced `ledger` as the top-level CLI name. This mismatch is confusing for users and automation; updating the docs and instructions ensures consistency.
- Tests still call a helper named `ledger()` in the e2e suite; that helper now executes `uv run arledge` so test bodies need not change.

## Commands run (representative)
- rg/grep to locate occurrences
- Edited files: src/ledger/cli.py, README.md, tests/e2e/helpers.sh, tests/e2e/README.md, MINDMAP.md
- git add/commit

## Next steps
- Consider changing in-repo references that say "ledger" for the Python package vs the CLI executable to avoid ambiguity (e.g., clarify in docs when referring to the Python package `ledger` vs the `arledge` console script).
- Run CI to ensure no missed references; optionally update other chronicle entries that mention running `ledger` examples.

