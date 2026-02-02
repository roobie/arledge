`mise` is a command-line tool that unifies **tool version management**, **environment configuration**, and **task running** for development projects. It reads cascading config files (`mise.toml`, global config, local overrides) to: (1) install and pin specific versions of runtimes/CLIs (Node, Python, Terraform, etc.) per project or globally; (2) define environment variables that automatically apply when in a directory; and (3) define named tasks/commands that can be run consistently by any developer on the project.

Example `mise.toml` with tasks:

```toml
[tools]
node = "22"
python = "3.12"

[env]
APP_ENV = "development"

[tasks.build]
run = "npm run build"

[tasks.test]
run = "pytest"
depends = ["build"]

[tasks.dev]
run = "npm run dev"
watch = ["src/**/*", "package.json"]

[tasks.lint]
run = "npm run lint"

[tasks.ci]
run = "echo 'CI pipeline'"
depends = ["lint", "test"]
```

Example usage:

```bash
# Install tools defined in mise.toml
mise install

# List tasks
mise tasks

# Run a task
mise run build
mise run test
mise run ci

# Shorthand
mise build
mise test

# Run with file watching (re-run on changes)
mise dev

# One-off command with project tools/env
mise x node --version
mise x python -m http.server 8000
```
