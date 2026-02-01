# Project General (arledge)

Summary
- Short onboarding and run/test instructions for working with the repository.

Quick start
- Use `uv` wrapper for python commands in this repo, e.g. `uv run python` or `uv run pytest`.
- Run tests with `uv run pytest` (CI/local uses pytest).

Test coverage integration (added 2026-02-01):
- `pytest` is configured in `pyproject.toml`.
- Dev deps `pytest-cov` and `coverage` were added via `uv add --dev pytest-cov coverage`.
- `tool.pytest.ini_options.addopts` updated to include coverage flags producing `coverage.xml` and `htmlcov/` and enforcing `--cov-fail-under=75` (adjustable).
- `.coveragerc` and `.github/workflows/ci.yml` were added to configure coverage behavior and CI reporting.
- `.gitignore` updated to ignore coverage artifacts.


Files referenced
- README.md
- pyproject.toml

Provenance
- Pruned and condensed from `general-info`.