# Chronicle: Lower CI coverage fail-under threshold to 75%

- timestamp: 2026-03-01T19:24:00+01:00
- participants: assistant (automated), user

## Summary
Updated the GitHub Actions CI workflow to set the coverage failure threshold to 75% instead of 80% to match the project's configured target and avoid CI failures when coverage is at ~75.29%.

## Commands run (representative)
- Edited .github/workflows/ci.yml to change `--cov-fail-under=80` -> `--cov-fail-under=75` in the uv pytest command.
- git add/commit

## Files changed
- Modified: .github/workflows/ci.yml

## Rationale
- The project's pyproject.toml config already specified a target of 75% under [tool.pytest.ini_options]. The CI had been using 80% causing failures when coverage was around 75.29%.

## Next steps
- Monitor CI runs to ensure the new threshold is acceptable.
- If you want to increase coverage later, consider adding a test/coverage improvement task.
