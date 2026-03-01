End-to-end (e2e) tests for arledge

Overview

This directory contains brat-style shell-based e2e tests that exercise the CLI end-to-end. Tests live in .brat files and use the shared helpers in helpers.sh. The tests run the CLI through uv to ensure the locked environment is used and assets are created in an ephemeral base directory per test.

Requirements

- uv (https://github.com/astral-sh/uv) available in PATH (CI uses astral-sh/setup-uv and `uv sync`)
- jq (used for constructing JSON models and for extracting fields from JSON output)
- bash / sh
- brat test runner (included in vendor/brat/ and invoked by script/test-e2e). The bundled runner lives at @vendor/brat/ (vendor/brat/ in the repository) and is executed by the test script as vendor/brat/bin/brat.

How tests run

- script/test-e2e invokes vendor/brat/bin/brat on the .brat files in this directory.
- helpers.sh provides:
  - ledger() wrapper that runs `uv run arledge ...` with ARLEDGE_BASEDIR set to the test's temporary base directory
  - setup_basedir/teardown_basedir to create and remove a temporary ARLEDGE_BASEDIR
  - jq_field() to extract JSON fields from CLI stdout
  - require_jq() to skip tests when jq is not available

Recommended local workflow

1. Ensure dependencies are available:
   - Install uv and jq. Example using pip for jq's binary helper: jq is usually available via your package manager (apt/brew) or as the `jq` binary.
2. Sync the project environment:
   - uv sync --locked --all-extras --dev
3. Run e2e tests:
   - ./script/test-e2e
   - or via the top-level test command: mise test (project convenience wrapper)

Model construction pattern

Tests use jq -nc to construct JSON models in a readable way, e.g.:

  model=$(jq -nc '{name: "ACME Corp", email: "sales@acme.example"}')
  run arledge customer create --model "$model"

When a created object's id is required for a follow-up request, tests use jq -nc with --arg and tonumber, e.g.:

  cred_id=$(jq_field '.id' "$stdout")
  account_model=$(jq -nc --arg cid "$cred_id" '{creditor_id: ($cid | tonumber), type: "bank", identifier: "SE123456789", currency: "SEK"}')
  run arledge creditor account create --model "$account_model"

This pattern avoids brittle escaping and keeps test JSON readable.

Tips

- If a test is skipped because jq isn't available, install jq and re-run the e2e tests.
- The tests modify an ephemeral ARLEDGE_BASEDIR and will not touch your local project files.

Maintainers: keep helpers.sh and the jq model pattern consistent when adding new tests.
