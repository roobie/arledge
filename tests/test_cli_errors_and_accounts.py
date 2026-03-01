import json
import os
from decimal import Decimal

from click.testing import CliRunner

from ledger import cli, models


def test_invalid_json_for_create(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        # invalid JSON should exit non-zero
        r = runner.invoke(cli.cli, ["customer", "create", "--model", "{bad"])
        assert r.exit_code != 0
        assert "Invalid customer JSON" in r.output or "Invalid" in r.output

        r2 = runner.invoke(cli.cli, ["creditor", "create", "--model", "{bad"])
        assert r2.exit_code != 0


def test_account_list_filter_and_json_schema(tmp_path):
    # create via CLI to persist in beancount files
    runner = CliRunner()
    with runner.isolated_filesystem():
        # create creditor
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", json.dumps({"name":"Ac"})])
        assert r.exit_code == 0
        c = json.loads(r.output)
        # create payment accounts
        pa1 = {"creditor_id": c["id"], "type": "a", "identifier": "i1"}
        pa2 = {"creditor_id": c["id"] + 1, "type": "b", "identifier": "i2"}
        r1 = runner.invoke(cli.cli, ["creditor", "account", "create", "--model", json.dumps(pa1)])
        r2 = runner.invoke(cli.cli, ["creditor", "account", "create", "--model", json.dumps(pa2)])
        assert r1.exit_code == 0 and r2.exit_code == 0
        res = runner.invoke(cli.cli, ["creditor", "account", "list", "--creditor-id", str(c["id"])])
        assert res.exit_code == 0
        arr = json.loads(res.output)
        assert all(item["creditor_id"] == c["id"] for item in arr)

        # invoice json-schema
        r2 = runner.invoke(cli.cli, ["invoice", "create", "--json-schema"])
        assert r2.exit_code == 0
        assert "properties" in r2.output


