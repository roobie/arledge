#!/bin/sh
# Shared helpers for e2e brat tests

# Wrapper for ledger command with proper uv context
ledger() {
  ARLEDGE_BASEDIR="$BASEDIR" uv run ledger "$@"
}

# Create and initialize a temp base directory for the test
setup_basedir() {
  BASEDIR="$(mktemp -d)"
  export ARLEDGE_BASEDIR="$BASEDIR"
  # Initialize the beancount layout
  ledger init >/dev/null 2>&1
}

# Remove the temp base directory
teardown_basedir() {
  rm -rf "$BASEDIR"
}

# Extract a field from JSON stdout using jq
jq_field() {
  jq -r "$1" "$2"
}

# Check if command exists
cmd_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Skip test if jq is missing
require_jq() {
  if ! cmd_exists jq; then
    skip "jq not available"
  fi
}
