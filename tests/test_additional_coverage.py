import json
import os
from datetime import datetime, timezone
from decimal import Decimal

from click.testing import CliRunner

from ledger import cli, models, config


def test_customer_and_creditor_via_file(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        # create temp file with model and use --model-file
        cust = {"name": "FileCust", "email": "f@f.test"}
        p = tmp_path / "cust.json"
        p.write_text(json.dumps(cust), encoding="utf-8")
        r = runner.invoke(cli.cli, ["customer", "create", "--model-file", str(p)])
        assert r.exit_code == 0
        rc = json.loads(r.output)
        assert rc["name"] == "FileCust"

        # creditor via file
        cred = {"name": "FileCred"}
        p2 = tmp_path / "cred.json"
        p2.write_text(json.dumps(cred), encoding="utf-8")
        r2 = runner.invoke(cli.cli, ["creditor", "create", "--model-file", str(p2)])
        assert r2.exit_code == 0
        assert json.loads(r2.output)["name"] == "FileCred"


def test_invoice_with_creditor_and_invoice_list_and_view(tmp_path):
    # create creditor and invoice using CLI in isolated filesystem
    runner = CliRunner()
    with runner.isolated_filesystem():
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", json.dumps({"name":"C1"})])
        assert r.exit_code == 0
        created_cred = json.loads(r.output)
        r2 = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps({"customer_id":1, "creditor_id": created_cred.get("id"), "currency":"USD", "lines": [{"description":"l","unit_price":"3.00"}]})])
        assert r2.exit_code == 0
        created = json.loads(r2.output)
        assert created.get("currency") == "USD"
        # list via CLI
        res = runner.invoke(cli.cli, ["invoice", "list"])
        assert res.exit_code == 0
        arr = json.loads(res.output)
        assert isinstance(arr, list)
        # view non-existing should exit non-zero
        rv = runner.invoke(cli.cli, ["invoice", "view", "9999"])
        assert rv.exit_code != 0
        assert "Invoice not found" in rv.output


def test_models_created_at_string_and_dump_model():
    iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    c = models.Creditor(name="T", created_at=iso)
    assert c.created_at is not None
    out = config.dump_model(c)
    assert isinstance(out, dict)


def test_serialize_tuple_and_tuple_roundtrip():
    data = (Decimal("1.00"), datetime.now(timezone.utc))
    res = config._serialize_value(data)
    assert isinstance(res, list)
