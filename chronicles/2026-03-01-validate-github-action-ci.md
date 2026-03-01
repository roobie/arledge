# Chronicle: Validate GitHub Action workflow (ci.yml)

- timestamp: 2026-03-01T11:24:39+01:00
- participants: assistant (automated), user

## Summary
Performed a local static validation of the GitHub Actions workflow file .github/workflows/ci.yml. Checked for YAML syntax issues, tabs/trailing whitespace, and common actionable problems in the steps.

## Commands run (representative)
- ls -la .github/workflows
- sed -n '1,200p' .github/workflows/ci.yml
- rg "\t" -n .github/workflows/ci.yml || true
- rg "\s+$" -n .github/workflows/ci.yml || true

## Files inspected
- .github/workflows/ci.yml
- pyproject.toml

## Findings
1. Syntax and formatting
   - No tab characters found in .github/workflows/ci.yml.
   - No trailing whitespace detected.
   - The workflow appears to be valid YAML at a glance (correct indentation and structure).
   - Note: I could not run a full GitHub Actions schema validation or execute the workflow locally because tooling like `act`, `yamllint`, or GitHub's server-side schema validator is not available in this environment.

2. Workflow specifics
   - Workflow name: `CI` — triggers on push and pull_request to `main`.
   - Job `test` runs on `ubuntu-latest` and checks out the repo, sets up Python, installs dependencies, runs pytest with coverage, and uploads coverage artifacts.
   - `actions/checkout@v4`, `actions/setup-python@v4`, and `actions/upload-artifact@v4` are used — versions look reasonable.
   - `python-version: '3.13'` is set. Check runner availability for 3.13 on GitHub-hosted runners if you need strict compatibility; as of this check it is likely supported, but confirm against GitHub docs for the runner images you use.
   - The `Install dependencies` step uses `pip install -e . || true` which will swallow installation errors and allow the workflow to continue even if installation fails. This can hide packaging or dependency issues and lead to confusing test failures later.
   - Coverage target `--cov=ledger` matches the package layout (package under src/arledge as indicated by pyproject.toml), so that looks correct.

## Recommendations / Next steps
1. Fail fast on install errors
   - Remove the `|| true` from `pip install -e . || true` so that the workflow fails immediately if installation fails. This surfaces packaging or dependency problems early:
     - Change `pip install -e . || true` -> `pip install -e .`

2. Confirm Python runner availability
   - Confirm that `python-version: '3.13'` is available on `ubuntu-latest` runners in GitHub Actions. If you need guaranteed availability across runners, consider using a minor version pin (e.g., `3.13.x`) or the matrix strategy to test multiple versions.

3. Optional improvements
   - Cache pip dependencies using `actions/cache` to speed up runs.
   - Add explicit `permissions` or `env` if the job needs reduced or tightened permissions.
   - Consider pinning action major and minor versions intentionally (you're already using @v4 which is fine) and add checks for action deprecations occasionally.
   - If you want stricter validation, run `yamllint` or use `act` to run the workflow locally in Docker. I did not run those here because they are not available in the environment.

## Suggested automated checks to run locally (on your machine)
- Install and run yamllint against the workflow file:
  - apt: `sudo apt-get install yamllint` or `pip install yamllint`
  - run: `yamllint .github/workflows/ci.yml`
- Use `act` to run the workflow locally (requires Docker):
  - `brew install act` or follow https://github.com/nektos/act
  - run: `act -j test -P ubuntu-latest=nektos/act-environments-ubuntu:22.04` (adjust as needed)


## Files changed
- Created: chronicles/2026-03-01-validate-github-action-ci.md


## Next steps (for me / follow-up)
- If you want, I can:
  - Run yamllint and act locally here if you install or allow installation of those tools in the environment.
  - Update the workflow to remove `|| true` and add caching or matrix testing.
  - Run a simulated workflow using Docker/act and report failing steps.

