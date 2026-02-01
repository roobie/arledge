import json
from click.testing import CliRunner

from ledger import cli, models, config


def test_schema_flags_and_missing_model():
    runner = CliRunner()
    # schema for customer
    res = runner.invoke(cli.cli, ["customer", "create", "--json-schema"])
    assert res.exit_code == 0
    assert "properties" in res.output

    # missing model
    res2 = runner.invoke(cli.cli, ["customer", "create"])
    assert res2.exit_code != 0
    assert "Provide --model" in res2.output


def test_customer_create_and_list(tmp_path):
    runner = CliRunner()
    # create via inline model
    model = json.dumps({"name": "ACME", "email": "x@a.test"})
    res = runner.invoke(cli.cli, ["customer", "create", "--model", model])
    assert res.exit_code == 0
    out = json.loads(res.output)
    assert out["name"] == "ACME"

    # list should show created
    res2 = runner.invoke(cli.cli, ["customer", "list"])
    assert res2.exit_code == 0
    arr = json.loads(res2.output)
    assert any(x["name"] == "ACME" for x in arr)


def test_invoice_export_not_found():
    runner = CliRunner()
    res = runner.invoke(cli.cli, ["invoice", "export", "9999", "--format", "json"])
    assert res.exit_code != 0
    assert "Invoice not found" in res.output
