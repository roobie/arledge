# Beancount-First Replacement Plan for arledge

Generated: 2026-03-01T11:24:39+01:00
Revised: 2026-03-01

This plan defines a safe, testable, incremental approach to fully replace the SQLite backend with a beancount-file-first implementation. The project is pre-release, so we will not provide migrations; instead we will implement beancount as the primary persistence mechanism.

Status: approved for implementation (no migration required)

Target audience: single entrepreneurs / freelancers — single-user, single-machine usage. Concurrency, multi-machine, and file-locking concerns are explicitly out of scope.

---

## I. Goals (success criteria)

- arledge persists domain data (customers, creditors, payment accounts, invoices and invoice lines, metadata) exclusively to beancount files and JSON sidecar files.
- CLI surface, JSON contracts and Pydantic models remain unchanged.
- Writes are validated using a temp-file + snippet-validate-then-append pattern.
- Tests provide parity guarantees (expected outputs and behavior) and verify write semantics.
- A simple, deterministic invoice-number mechanism exists for new invoices.
- An `init` command bootstraps the beancount directory structure for new users.
- Documentation describes file layout and recommended workflows.

---

## II. High-level strategy

1. Replace `ledger/db.py` (SQLite) with a direct beancount store module (`arledge/beancount_store.py`). No generic storage abstraction — beancount is the only backend.
2. Implement append-only writes: write snippets to temp files, validate the snippet with the beancount parser, then append to target include files.
3. Keep the CLI, models, schema output, and API unchanged; only the storage implementation changes.

---

## III. Design decisions

- **No storage abstraction layer.** Beancount is the sole backend; SQLite is being removed. A direct `beancount_store.py` module avoids unnecessary indirection (YAGNI).
- **`custom` directives for entities.** Customers, creditors, and payment accounts are represented as beancount `custom` directives with metadata — not as fake transactions.
- **JSON sidecar files for invoice lines.** Invoice line items are stored as separate `.json` files referenced from invoice transaction metadata. This avoids fragile JSON-in-comments.
- **Snippet-only validation by default.** Writes validate only the new snippet (syntax + balance), not the entire ledger. A separate `ledger validate` subcommand performs full-ledger validation.
- **No file locking.** Single-user CLI tool; concurrent writes cannot happen. Simple temp-file → validate → append is sufficient.
- **No update/delete operations.** Users edit beancount files directly for corrections. The CLI provides create and read operations only.
- **Cross-platform.** Windows support is required. Use `portalocker` if any file-locking needs arise in the future.

---

## IV. Atomic task list (prioritized)

Each task is small, testable, and intended for short iterations.

### 1) `init` command & directory bootstrap

- Deliverable: `arledge init` command that creates the beancount directory structure (see §V) and a minimal `ledger.beancount` with include directives.
- Acceptance: running `init` in an empty directory produces a valid, parseable ledger structure.

### 2) `custom` directive spike — verify parsing approach

- Deliverable: small spike script or test that confirms beancount's `custom` directive + metadata can round-trip through `beancount.loader` and map to Pydantic models.
- Approaches to test:
  - **`beancount.loader.load_file()`** — returns typed `Custom` entries; metadata is accessible via `entry.meta`. This is the standard approach.
  - **`beancount.parser.parser.parse_file()`** — lower-level, returns the same entry types but without running plugins. May be faster for snippet validation.
  - **Direct text parsing** — regex or line-based parsing of `.beancount` files. Fragile; avoid unless the above APIs prove insufficient.
- Acceptance: confirmed approach documented; mapping code sketched.

### 3) Read-only beancount store + mapping tests

- Deliverable: `arledge/beancount_store.py` with read-only functions that parse beancount file(s) and map to Pydantic models for list/get operations (customers, creditors, payment accounts, invoices).
- Tests: mapping unit tests and parity tests against expected JSON fixtures.
- Acceptance: read-only parity verified for a small dataset.

### 4) Write flow: temp-file + snippet-validate + append

- Deliverable: write operations (`create_customer`, `create_invoice`, etc.) that compose beancount snippets, validate the snippet in isolation, and append to the target include file.
- Mechanics:
  1. Compose the beancount snippet for the target file.
  2. Write snippet to a temp file on the same filesystem and fsync.
  3. Validate the snippet by parsing only the temp file. If validation fails, remove temp file and return error.
  4. Append snippet to target file with a single write + fsync.
- For invoices: also write the JSON sidecar file to `invoices/data/`.
- Tests: write → read-back round-trip tests for each entity type.
- Acceptance: validated writes; no parse errors admitted into files.

### 5) Invoice-number / ID allocation

- Deliverable: sequence file (e.g., `.arledge/invoice_seq`) incremented on each invoice creation.
- Recovery: if the sequence file is missing or corrupted, scan existing invoice files for the highest invoice number and rebuild the sequence from max + 1.
- Tests: sequence increment tests; recovery-from-missing-file test.
- Acceptance: deterministic and monotonic invoice numbering.

### 6) CLI integration & parity tests

- Deliverable: CLI uses beancount store; end-to-end CLI tests pass (create/list/export flows).
- Tests: existing test suite adapted for beancount backend; new tests for beancount-specific behaviors.
- Acceptance: CLI behavior identical to current; tests pass.

### 7) `validate` subcommand

- Deliverable: `arledge validate` command that parses the full `ledger.beancount` (with all includes) and reports any parse errors, balance errors, or orphaned sidecar files.
- Acceptance: validates a known-good ledger with no errors; detects intentionally broken files.

### 8) Docs & developer UX

- Deliverable: documentation describing file layout, write workflow, git workflow suggestions, and manual editing guidelines.
- Acceptance: docs cover how to use, validate, and manually fix beancount files.

### 9) Cleanup

- Deliverable: remove SQLite-specific code, dependencies, and tests. Update CHANGELOG.
- Acceptance: codebase builds and tests pass; SQLite code removed.

---

## V. Recommended file layout

Created by `arledge init`:

```
ledger.beancount              # top-level file with include directives
includes/
  customers.beancount         # custom directives for customers
  creditors.beancount         # custom directives for creditors
  payment_accounts.beancount  # custom directives for payment accounts
  invoices/                   # invoice transactions, per-month files
    2026-03.beancount
    2026-04.beancount
  invoices/data/              # JSON sidecar files for invoice lines
    inv-0001.json
    inv-0002.json
.arledge/
  invoice_seq                 # current invoice sequence number
```

Notes:
- `ledger.beancount` contains `include` lines for each includes file/glob.
- Per-month invoice files keep individual files small and git-friendly.
- The `.arledge/` directory holds arledge-internal state (sequence files, etc.).

---

## VI. Data mapping

### Customers (includes/customers.beancount)

Use `custom` directives with metadata:

```beancount
2026-03-01 custom "customer" "ACME Corp"
  customer_id: 1
  email: "sales@acme.example"
  address: "123 Road"
```

### Creditors (includes/creditors.beancount)

Same pattern:

```beancount
2026-03-01 custom "creditor" "Office Supplies Ltd"
  creditor_id: 1
  email: "billing@office.example"
  address: "456 Avenue"
```

### Payment accounts (includes/payment_accounts.beancount)

Same pattern:

```beancount
2026-03-01 custom "payment_account" "Business Checking"
  account_id: 1
  bank: "Nordea"
  iban: "SE1234567890"
  currency: "SEK"
```

### Invoices (includes/invoices/YYYY-MM.beancount)

Invoices are real transactions with postings. Line items are stored in a JSON sidecar file:

```beancount
2026-03-01 * "Invoice INV-0001"
  invoice_id: 1
  customer_id: 1
  due_at: 2026-03-31
  invoice_data: "invoices/data/inv-0001.json"
  Assets:Receivable:ACME        1250.00 SEK
  Income:Services              -1000.00 SEK
  Liabilities:VAT               -250.00 SEK
```

### Invoice sidecar (includes/invoices/data/inv-0001.json)

```json
{
  "invoice_id": 1,
  "lines": [
    {
      "description": "Consulting services",
      "quantity": 1,
      "unit_price": "1000.00",
      "vat_rate": "25"
    }
  ]
}
```

---

## VII. Write recipe

1. Compose the beancount snippet text for the appropriate target file.
2. Write snippet to a temp file on the same filesystem (e.g., `includes/.tmp/tmp-<uuid>.beancount`) and fsync.
3. Validate by parsing **only the snippet temp file** with the beancount parser. If validation fails, remove temp file and return an error.
4. Append snippet to the target file with a single write + fsync.
5. Remove temp file.

For invoices, also write the JSON sidecar file before appending the beancount snippet (so the reference is valid immediately).

---

## VIII. Tests to add

- **Spike test:** `custom` directive round-trip through beancount parser → Pydantic model.
- **Mapping tests:** beancount → Pydantic models for customers, creditors, payment accounts, invoices.
- **Parity tests:** verify outputs for representative fixtures match expected JSON.
- **Write round-trip tests:** create entity → read back → verify for each entity type.
- **Invoice-seq tests:** sequence increment; recovery from missing/corrupted seq file.
- **CLI end-to-end tests:** run create/list/export flows using the beancount backend.
- **Validate command tests:** detect parse errors, balance errors, orphaned sidecars.

---

## IX. Operational & UX considerations

- **No update/delete via CLI.** Users edit beancount files directly for corrections (fix typos, void invoices, update addresses). Document this workflow.
- **Backup:** instruct users to use git. Document recommended git workflow (commit after writes, use branches for manual edits).
- **`arledge validate`:** full-ledger validation on demand, including orphan sidecar detection.
- **Orphaned sidecar cleanup:** `validate` flags JSON sidecar files in `invoices/data/` that are not referenced by any invoice transaction. Users can delete them manually.

---

## X. Open questions & risks

- **`custom` directive parsing:** needs spike (task 2) to confirm metadata round-trips cleanly through `beancount.loader`. If metadata on `custom` directives is not well-supported, fallback is `note` directives or zero-posting transactions.
- **Beancount version pinning:** beancount v2 vs v3 have different APIs. We should pin to one and document it.
- **Account names:** the invoice example uses `Assets:Receivable:ACME` — account naming conventions should be documented or configurable.

---

## XI. Notes & decisions log

- 2026-03-01: Plan created and approved. No migration required (pre-release).
- 2026-03-01 (rev 1): Revised based on review:
  - Dropped generic storage abstraction — direct beancount module only.
  - Switched to `custom` directives for customers, creditors, payment accounts.
  - JSON sidecar files as primary approach for invoice lines.
  - Snippet-only validation by default; full validation via `arledge validate`.
  - Dropped file locking (single-user tool, no concurrency concerns).
  - No update/delete operations — users edit files directly.
  - Added `init` command for directory bootstrapping.
  - Added `custom` directive parsing spike as early task.
  - Added orphan sidecar detection to `validate`.
