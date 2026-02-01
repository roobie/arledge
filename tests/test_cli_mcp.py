from click.testing import CliRunner

from ledger import cli


def test_mcp_help_shows_options():
    runner = CliRunner()
    r = runner.invoke(cli.cli, ["mcp", "start", "--help"])
    assert r.exit_code == 0, r.output
    # help should mention the dry-run and json-response options
    assert "--dry-run" in r.output
    assert "--json-response" in r.output


def test_mcp_dry_run_reports_and_exits_zero():
    runner = CliRunner()
    r = runner.invoke(cli.cli, ["mcp", "start", "--dry-run"])
    assert r.exit_code == 0, r.output
    assert "MCP dry-run" in r.output


def test_mcp_name_flag_affects_dry_run_message():
    runner = CliRunner()
    r = runner.invoke(cli.cli, ["mcp", "start", "--dry-run", "--name", "MyServer"])
    assert r.exit_code == 0, r.output
    assert "name=MyServer" in r.output


def test_mcp_unknown_flag_errors():
    runner = CliRunner()
    r = runner.invoke(cli.cli, ["mcp", "start", "--unknown-flag"])
    assert r.exit_code != 0
    assert "Usage" in r.output
