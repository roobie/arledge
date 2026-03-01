import os
from click.testing import CliRunner
import tempfile
from arledge.cli import cli


def test_init_uses_arledge_basedir(monkeypatch, tmp_path):
    # Set ARLEDGE_BASEDIR to a temporary directory
    monkeypatch.setenv("ARLEDGE_BASEDIR", str(tmp_path))
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "--force"])
    assert result.exit_code == 0
    # Check that ledger.beancount was created in the base dir
    ledger_file = tmp_path / "ledger.beancount"
    assert ledger_file.exists()
    includes = tmp_path / "includes"
    assert includes.exists()
    invoices = includes / "invoices"
    assert invoices.exists()
    arledge = tmp_path / ".arledge"
    assert arledge.exists()
    seq = arledge / "invoice_seq"
    assert seq.exists()
    # help text mentions ARLEDGE_BASEDIR when requesting --help
    help_result = runner.invoke(cli, ["--help"])
    assert "ARLEDGE_BASEDIR" in help_result.output
