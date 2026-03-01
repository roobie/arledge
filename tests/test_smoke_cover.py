import json
from click.testing import CliRunner

from ledger import cli


def test_smoke_cli_create_and_export():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # initialize beancount layout
        r = runner.invoke(cli.cli, ["init"])
        assert r.exit_code == 0

        # create customer
        cust = {"name": "ACME", "email": "acme@example.com"}
        r = runner.invoke(cli.cli, ["customer", "create", "--model", json.dumps(cust)])
        assert r.exit_code == 0
        c = json.loads(r.output)
        assert c.get("name") == "ACME"

        # create creditor
        cred = {"name": "MeCo"}
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", json.dumps(cred)])
        assert r.exit_code == 0
        cr = json.loads(r.output)

        # create payment account
        pa = {"creditor_id": cr.get("id"), "type": "bank", "identifier": "I1"}
        r = runner.invoke(cli.cli, ["creditor", "account", "create", "--model", json.dumps(pa)])
        assert r.exit_code == 0

        # create invoice
        inv = {"customer_id": c.get("id"), "creditor_id": cr.get("id"), "lines": [{"description": "S", "unit_price": "10.00"}]}
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps(inv)])
        assert r.exit_code == 0
        iv = json.loads(r.output)
        inv_id = iv.get("id")
        assert inv_id is not None

        # list invoices
        r = runner.invoke(cli.cli, ["invoice", "list"])
        assert r.exit_code == 0
        arr = json.loads(r.output)
        assert isinstance(arr, list)

        # export invoice
        r = runner.invoke(cli.cli, ["invoice", "export", str(inv_id), "--format", "json"]) 
        assert r.exit_code == 0
        # exported path printed
        assert r.output

        # schemas
        r = runner.invoke(cli.cli, ["customer", "create", "--json-schema"])
        assert r.exit_code == 0
        assert "properties" in r.output

        # mcp dry-run
        r = runner.invoke(cli.cli, ["mcp", "start", "--dry-run"]) 
        assert r.exit_code == 0
        assert "MCP dry-run" in r.stderr
