[1] **Mind Map Format Overview** - A graph-based documentation format stored as plain text where each node is a single line containing an ID, title, and inline references; read overview nodes [1-5] first and consult PROJECT_MIND_MAPPING.md for details [2][4].

[2] **Node Syntax Structure** - Each node follows: [N] **Node Title** - node text with [N] references inlined; nodes are line-oriented to allow line-by-line loading and grep lookups for quick retrieval [1][3].

[3] **Technical Advantages** - Line-oriented nodes enable line-by-line overwrites, easy incremental updates, grep-based lookup, VCS-friendly diffs, and LLM-friendly citation syntax mirroring academic references [2][1].

[4] **Graph Topology Benefits** - The format supports many-to-many relationships, cyclic references, cross-cutting concerns, and progressive refinement making it suitable for trees, lists, or arbitrary graphs [1][2].

[5] **Scalability and Usage Patterns** - Small projects use <50 nodes; complex systems scale to 500+ nodes by adding deep-dive nodes; navigation relies on overview nodes and grep-based search [1][3][4].

[6] **Planner Agent (agents/planner.agent.md)** - Planner-agent config and rules for Serena: frontmatter lists tools/handoffs and mandates calling Serena MCP 'initial_instructions', loading memories, and reading README.md; workflow: research → draft plan → iterate; never implement code in planner phase [1][10].

[7] **CLI Surface & Conventions (.serena/memories/cli-surface-and-conventions.md)** - Canonical CLI patterns: `arledge <group> <action>` in `arledge/cli.py`; JSON input via `--model`/`--model-file`; Pydantic model validation and machine JSON to stdout, human logs to stderr; tests exercise these behaviors [1][11].

[8] **Coverage Learnings (.serena/memories/coverage-learnings.md)** - Coverage setup added pytest-cov/coverage, pyproject addopts, .coveragerc, CI workflow; final measured coverage 91.02% after tests and recommended next steps for reporting [1][12].

[9] **Domain: Creditors & Payment Accounts (.serena/memories/domain-creditor-payment-accounts.md)** - Business rules and schemas for `creditors` and `creditor_payment_accounts`; metadata as free-form JSON, `is_default` semantics, monetary storage as integer cents, exporter preferences for `beancount_account`; see `arledge/beancount_store.py`, `arledge/models.py` [1][11].

[10] **Project General (.serena/memories/project-general.md)** - Onboarding and quickstart: use `uv` wrapper (e.g. `uv run pytest`), pytest configured in `pyproject.toml`, coverage/dev-deps noted; README and pyproject are entry points for run/test info [1].

[11] **Pydantic Models & Serialization (.serena/memories/pydantic-models-and-serialization.md)** - Model conventions: models in `arledge/models.py` (Customer, Creditor, PaymentAccount, InvoiceLine, Invoice); prefer `model_validate_json()`, include `model_version`, use `ledger/config.dump_model()` for canonical serialization and JSON Schema for `--json-schema` [1][7].

[12] **Test Coverage Setup (.serena/memories/test-coverage-setup.md)** - Coverage config: pytest addopts in pyproject, .coveragerc ignores, CI workflow; local commands `uv run pytest` and recommendation to raise coverage threshold once stable [8][11].

[13] **Beancount Notes (docs/beancount.md)** - Double-entry bookkeeping reference: account types, transaction/posting rules, trial balance, reporting perspectives; used for `beancount_account` mappings [9].

[14] **Repository Layout & Key Files** - Layout: `arledge/` package (cli.py, models.py, config.py, mcp_server.py, beancount_store.py, beancount_write.py, __main__.py), `tests/`, `.github/workflows/ci.yml`, `pyproject.toml`, README, and `.serena/memories/` [15][18].

[15] **Entry Points & CLI Invocation** - Console script `arledge` maps to `arledge.cli:cli` in pyproject; `python -m arledge` uses `arledge.__main__` which calls `cli()`; tests use Click's CliRunner or `uv run arledge` [7][14].

[16] **CLI Commands & UX** - Top-level CLI groups: `database`, `customer`, `creditor` (and `creditor account`), `invoice`, `mcp`; `schema` and `instructions` serve agent-facing needs; machine outputs to stdout, human logs to stderr, non-zero exit codes on errors [7][11][14].

[17] **Pydantic Models (arledge/models.py)** - Models include Customer, Creditor, PaymentAccount, InvoiceLine, Invoice; validators coerce datetimes/decimals; InvoiceLine computes net/vat/line_total with ROUND_HALF_UP quantize(0.01); Invoice computes subtotal/total and sets created_at default UTC now; `model_version` uses package __version__ [11].

[18] **Storage: Beancount files (arledge/beancount_store.py)** - Ledger is now file-first using Beancount include files and custom directives. `arledge/beancount_store.py` reads beancount loader entries and maps them to Pydantic models. Invoice lines are stored in JSON sidecar files referenced by transaction metadata. CLI create operations write beancount snippets via `arledge/beancount_write.py`. [9][17].

[19] **Config Helpers & Serialization (arledge/config.py)** - Utilities: dt_to_iso_utc / iso_to_dt, decimal_to_str / decimal_to_str_currency, JSON_ENCODERS for Pydantic, and `dump_model()` converting datetimes and Decimals for CLI/MCP outputs [11][18].

[20] **MCP stdio Server (arledge/mcp_server.py)** - FastMCP launcher with lazy imports; `start_mcp_stdio_server` supports `dry_run` for tests, registers tools mirroring CLI ops (customer/creditor/account/invoice), and prints a `ping` tool; CLI `mcp start` lazily imports this launcher [16].

[21] **Migrations Strategy** - The project uses a file-first approach (Beancount). Traditional SQL migrations are not applicable; schema evolution focuses on beancount snippet formats and sidecar layout migrations. Historical SQLite migration notes were removed when storage migrated to beancount files.

[22] **Tests & Coverage (tests/)** - Test suite covers CLI, DB CRUD integration, model property tests, serialization/config tests, and CLI error branches; pytest configured in pyproject with coverage addopts; local measured coverage was 76.13% with reports output to coverage.xml and htmlcov/ [7][8][13].

[23] **CI Configuration (.github/workflows/ci.yml)** - GitHub Actions job uses Python 3.13, installs deps, runs pytest with `--cov-fail-under=75`, and uploads coverage artifacts; suggest aligning local and CI thresholds [8][22].

[24] **Packaging & Dependencies (pyproject.toml)** - Project metadata: name `arledge`, version `0.1.0`, console script `ledger`; dependencies include click, pydantic, mcp[cli], beancount, pytest; note pyproject requires Python >=3.13 while README/code may support older versions [14][23].

[25] **Known Behaviors, Tradeoffs & Risks** - Notable issues: sensitive identifiers stored plaintext (consider encryption), init_db may remove DB in development mode (risk if mis-set), decimal handling uses quantize(0.01) and ROUND_HALF_UP, MCP lazy imports minimize deps [9][18][17][20].

[26] **Next Update Suggestions** - Suggested actions: reconcile Python-version mismatch, add migrations framework or protect init_db, document `arledge_db_prefix`, add encryption for sensitive fields, raise CI coverage gate, and update MINDMAP when changes occur [24][25].

[27] **Test Pruning Actions (2026-02-02)** - Recent maintenances: removed redundant CLI tests then restored a test to keep coverage at 76.13%; test runs used `uv run pytest --maxfail=1 -q`; update MINDMAP when further pruning occurs [22].

[28] **Mise Tool Docs (docs/mise.md)** - `mise` task runner and environment manager reads `mise.toml` to pin tools and define tasks; examples include `mise install`, `mise tasks`, `mise run test`; repo contains `mise.toml` illustrating tasks and env setup [24][22].
