import json
import os
from decimal import Decimal

from click.testing import CliRunner

from ledger import cli, db, models


def test_invalid_json_for_create(tmp_path):
    db.DB_PATH = os.path.join(tmp_path, "e.db")
    db.init_db()
    runner = CliRunner()
    # invalid JSON should exit non-zero
    r = runner.invoke(cli.cli, ["customer", "create", "--model", "{bad"])
    assert r.exit_code != 0
    assert "Invalid customer JSON" in r.output or "Invalid" in r.output

    r2 = runner.invoke(cli.cli, ["creditor", "create", "--model", "{bad"])
    assert r2.exit_code != 0


def test_account_list_filter_and_json_schema(tmp_path):
    db.DB_PATH = os.path.join(tmp_path, "f.db")
    db.init_db()
    cred = models.Creditor(name="Ac")
    c = db.create_creditor(cred)
    pa1 = models.PaymentAccount(creditor_id=c.id, type="a", identifier="i1")
    pa2 = models.PaymentAccount(creditor_id=c.id + 1, type="b", identifier="i2")
    db.create_payment_account(pa1)
    db.create_payment_account(pa2)
    runner = CliRunner()
    res = runner.invoke(
        cli.cli, ["creditor", "account", "list", "--creditor-id", str(c.id)]
    )
    assert res.exit_code == 0
    arr = json.loads(res.output)
    assert all(item["creditor_id"] == c.id for item in arr)

    # invoice json-schema
    r2 = runner.invoke(cli.cli, ["invoice", "create", "--json-schema"])
    assert r2.exit_code == 0
    assert "properties" in r2.output
