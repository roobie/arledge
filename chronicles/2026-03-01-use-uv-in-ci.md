# Chronicle: Use uv in GitHub Actions CI

- timestamp: 2026-03-01T11:52:00+01:00
- participants: assistant (automated), user

## Summary
Updated the repository CI workflow to use uv (astral-sh) for dependency management and running tests. Replaced direct pip install and python pytest invocation with `astral-sh/setup-uv` and `uv sync` / `uv run pytest` steps. Enabled built-in caching in the setup-uv step.

## Commands run (representative)
- Replaced .github/workflows/ci.yml contents to use setup-uv and uv commands.
- nl -ba .github/workflows/ci.yml | sed -n '1,200p'

## Files changed
- Modified: .github/workflows/ci.yml
- Created: chronicles/2026-03-01-use-uv-in-ci.md

## Why
- The project contains uv.lock and a .python-version file; using uv gives reproducible installs aligned with the project's lockfile and simplifies managing Python toolchain.
- `uv sync --locked --all-extras --dev` installs pinned dependencies including dev extras, ensuring CI mirrors local development environment.
- `uv run pytest ...` runs tests inside the uv-managed environment to ensure the correct interpreter and deps are used.
- Enabled uv caching via the setup-uv action's `enable-cache: true` option to speed up CI runs.

## Notes / Next steps
- If you prefer uv to install Python (rather than actions/setup-python), we can remove the setup-python step and let `astral-sh/setup-uv` manage Python versions (it supports `python-version` input or matrix overrides).
- For private dependencies (private GitHub repos), you may need to configure a PAT and register it via `gh auth login --with-token` as documented in the uv docs.
- Consider adding a matrix job to test multiple Python versions with `astral-sh/setup-uv` when needed.

