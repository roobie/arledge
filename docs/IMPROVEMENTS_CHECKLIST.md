# Prioritized Findings & Improvements Checklist

Generated: 2026-03-01T11:24:39+01:00

This checklist contains prioritized findings and suggested improvements from the recent codebase analysis. Check items when completed and update owners/estimates as appropriate.

## High priority

- [ ] Fix any remaining mutable-default usages across the codebase
  - Priority: High
  - Rationale: Shared mutable defaults cause subtle, hard-to-detect bugs. Two instances were fixed (PaymentAccount.metadata, Invoice.lines) and tests were added, but there may be other occurrences.
  - Suggested action: Run a repository-wide search for class attributes assigned to literals of mutable types ([], {}, set(), dict()) and convert to Field(default_factory=...) or equivalent.
  - Suggested owner: Backend dev
  - Estimated effort: 0.5 - 2 hours depending on occurrences

- [ ] Make the SQLite DB path configurable (env var / CLI option)  
  - Priority: High
  - Rationale: DB_PATH currently uses CWD (os.getcwd()). This can surprise users and complicate test isolation and deployments.
  - Status: In progress — `get_db_path()` implemented in ledger/db.py; README updated to document `LEDGER_DB_PATH`. Unit tests were run to verify behavior.
  - Suggested action (next): Expose CLI/global option if desired, add unit tests that set LEDGER_DB_PATH, and update any deployment docs.
  - Suggested owner: Backend dev
  - Estimated effort remaining: 0.5 - 2 hours

- [ ] Add tests that explicitly assert independence of default containers (already added)
  - Priority: High
  - Rationale: Prevent regressions to mutable-default bugs.
  - Status: Added tests/test_mutable_defaults.py
  - Suggested owner: QA / Test author
  - Estimated effort: done (low)

## Medium priority

- [ ] Document SQLite concurrency limitations and recommended usage patterns
  - Priority: Medium
  - Rationale: SQLite is appropriate for single-user CLI workflows but has limitations under concurrent multi-process access.
  - Suggested action: Update README.md with a short section on concurrency, plus possible mitigations (advisory locks, use of a server DB for concurrent workloads).
  - Suggested owner: Maintainer
  - Estimated effort: 0.5 - 1 hour

- [ ] Convert implicit idempotent migrations into explicit migration tooling
  - Priority: Medium
  - Rationale: db.init_db() is idempotent and adequate now, but non-trivial schema changes will be safer with explicit migrations.
  - Suggested action: Introduce a simple migration runner or integrate a lightweight migration library, add versioning to migrations.py, and add tests for migration scenarios.
  - Suggested owner: Backend dev
  - Estimated effort: 4 - 8 hours

- [ ] Make table-prefix validation explicit and document it
  - Priority: Medium
  - Rationale: prefixed() validates arledge_db_prefix by allowing alnum and underscore. Document the behavior and ensure no user-controlled unsafe inputs can reach it.
  - Suggested action: Add docs and consider raising clearer errors when prefix invalid. Add unit tests for invalid prefixes.
  - Suggested owner: Maintainer
  - Estimated effort: 0.5 - 1 hour

## Low priority

- [ ] Add MCP integration tests beyond dry-run
  - Priority: Low
  - Rationale: mcp_server.start_mcp_stdio_server offers a dry-run path; full runtime tests could validate stdio behavior in an integration test harness.
  - Suggested action: Create controlled subprocess tests that start the MCP server and issue a small RPC (e.g., ping) over stdio, or mock FastMCP.
  - Suggested owner: QA / Integration engineer
  - Estimated effort: 2 - 6 hours

- [ ] Consider documentation: CONTRIBUTING.md and developer notes for agent-friendly I/O
  - Priority: Low
  - Rationale: README already covers agent I/O conventions; a CONTRIBUTING.md could add developer guidelines and checklist items (mutable defaults, DB path, tests).
  - Suggested action: Draft CONTRIBUTING.md with code style, test expectations, and agent integration notes.
  - Suggested owner: Maintainer
  - Estimated effort: 1 - 2 hours

## Notes
- Unit tests currently pass (47 tests), coverage is ~76%.
- The mutable-default bug was fixed and tests added; ensure no other mutable defaults exist.
- When marking items done, update this checklist and add a brief chronicle entry describing the change.
