import os
import json
from decimal import Decimal

from datetime import datetime, timezone
from click.testing import CliRunner

from ledger import cli, config, models


def test_instructions_and_schema_unknown():
    runner = CliRunner()
    res = runner.invoke(cli.cli, ["instructions"])
    assert res.exit_code == 0
    assert "Instructions for agentic systems" in res.stderr

    res2 = runner.invoke(cli.cli, ["schema", "nope"])
    assert res2.exit_code != 0
    assert "Unknown schema name" in res2.output


def test_creditor_flow_and_view(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        # create creditor via model
        model = json.dumps({"name": "Cred", "email": "c@c.test"})
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", model])
        assert r.exit_code == 0
        c = json.loads(r.output)
        assert c["name"] == "Cred"

        # list and view
        rl = runner.invoke(cli.cli, ["creditor", "list"])
        arr = json.loads(rl.output)
        assert any(x["name"] == "Cred" for x in arr)

        vid = c["id"]
        rv = runner.invoke(cli.cli, ["creditor", "view", str(vid)])
        assert rv.exit_code == 0
        assert json.loads(rv.output)["id"] == vid


def test_account_create_missing_and_list_text_export():
    runner = CliRunner()
    # missing model for account create
    r = runner.invoke(cli.cli, ["creditor", "account", "create"])
    assert r.exit_code != 0
    assert "Provide --model" in r.output

    # text export not implemented
    r2 = runner.invoke(cli.cli, ["invoice", "export", "1", "--format", "text"])
    assert r2.exit_code != 0
    assert "Text export not implemented yet" in r2.output


def test_config_str_to_decimal_currency_rounding():
    # strings should be parsed and rounded to 2 decimals
    d = config.str_to_decimal_currency("1.235")
    assert isinstance(d, Decimal)
    assert d == Decimal("1.24")
