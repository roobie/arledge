import json
from click.testing import CliRunner
from pathlib import Path

from arledge import cli


def test_validate_ok():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # init and create minimal data
        r = runner.invoke(cli.cli, ["init"])
        assert r.exit_code == 0
        r = runner.invoke(cli.cli, ["customer", "create", "--model", json.dumps({"name":"C1","email":"c@d"})])
        assert r.exit_code == 0
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", json.dumps({"name":"CR"})])
        assert r.exit_code == 0
        # create invoice
        inv = {"customer_id":1, "creditor_id":1, "lines":[{"description":"S","unit_price":"10.00"}]}
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps(inv)])
        assert r.exit_code == 0
        # validate should pass
        r = runner.invoke(cli.cli, ["validate"]) 
        assert r.exit_code == 0, f"validate failed stderr:\n{r.stderr}"
        assert "Ledger OK" in r.stderr


def test_validate_missing_sidecar():
    runner = CliRunner()
    with runner.isolated_filesystem():
        r = runner.invoke(cli.cli, ["init"])
        assert r.exit_code == 0
        r = runner.invoke(cli.cli, ["customer", "create", "--model", json.dumps({"name":"C1"})])
        assert r.exit_code == 0
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", json.dumps({"name":"CR"})])
        assert r.exit_code == 0
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps({"customer_id":1, "creditor_id":1, "lines":[{"description":"S","unit_price":"10.00"}]})])
        assert r.exit_code == 0
        # delete the sidecar to simulate missing file
        data_dir = Path("includes") / "invoices" / "data"
        for f in data_dir.iterdir():
            f.unlink()
        # validate should fail and mention missing sidecar or report parse errors
        r = runner.invoke(cli.cli, ["validate"]) 
        assert r.exit_code != 0
        assert ("Missing invoice sidecars" in r.stderr) or ("Beancount parse/load errors:" in r.stderr)
