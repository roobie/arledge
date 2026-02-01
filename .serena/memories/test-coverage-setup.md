Added test coverage integration details (2026-02-01):

- Test framework: `pytest` configured in `pyproject.toml` under `[tool.pytest.ini_options]`.
- Dev dependencies added with `uv`: `pytest-cov` and `coverage` (installed via `uv add --dev pytest-cov coverage`).
- Pytest default addopts updated to run coverage: `--cov=ledger --cov-report=xml:coverage.xml --cov-report=html:htmlcov --cov-fail-under=75` (stored in `tool.pytest.ini_options.addopts` in `pyproject.toml`).
- Coverage config: `.coveragerc` added to omit `tests/*`, `*/__init__.py`, `ledger/migrations/*`, `.venv/*`, and `*/__pycache__/*` and set HTML output directory.
- CI: Added `.github/workflows/ci.yml` to run tests on `ubuntu-latest`, install dependencies, run pytest with coverage, and upload `coverage.xml` and `htmlcov/` as artifacts.
- Git ignore: `.gitignore` updated to ignore `.coverage`, `coverage.xml`, `htmlcov/`, and `.pytest_cache/`.
- Local run command: `uv run pytest` (or `pytest`) will produce `coverage.xml` and `htmlcov/`.
- Current coverage: `77.29%` (on 2026-02-01) and `--cov-fail-under` set to `75` to allow the current suite to pass; recommended target is `80%+`.

Notes / Next steps:
- Raise `--cov-fail-under` to 80 after adding tests to increase coverage.
- Consider adding Codecov/coveralls upload step to CI for reporting.
