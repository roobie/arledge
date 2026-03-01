import json
from click.testing import CliRunner
from pathlib import Path

from arledge import cli


def test_invoice_seq_initial_and_increment():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # init layout
        r = runner.invoke(cli.cli, ["init"])
        assert r.exit_code == 0
        # create creditor and customer
        r = runner.invoke(cli.cli, ["customer", "create", "--model", json.dumps({"name":"CUST","email":"a@b"})])
        assert r.exit_code == 0
        cust = json.loads(r.output)
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", json.dumps({"name":"CR"})])
        assert r.exit_code == 0
        cred = json.loads(r.output)
        # create first invoice
        inv_payload = {"customer_id": cust.get("id"), "creditor_id": cred.get("id"), "lines": [{"description":"L","unit_price":"1.00"}]}
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps(inv_payload)])
        assert r.exit_code == 0
        inv1 = json.loads(r.output)
        assert inv1.get("id") == 1
        # seq file should contain 2
        seq = Path(".arledge") / "invoice_seq"
        assert seq.exists()
        assert seq.read_text(encoding="utf-8").strip() == "2"
        # create second invoice
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps(inv_payload)])
        assert r.exit_code == 0
        inv2 = json.loads(r.output)
        assert inv2.get("id") == 2
        assert seq.read_text(encoding="utf-8").strip() == "3"


def test_invoice_seq_recovers_from_corrupt_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        r = runner.invoke(cli.cli, ["init"])
        assert r.exit_code == 0
        r = runner.invoke(cli.cli, ["customer", "create", "--model", json.dumps({"name":"CUST"})])
        assert r.exit_code == 0
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", json.dumps({"name":"CR"})])
        assert r.exit_code == 0
        # create one invoice to populate
        inv_payload = {"customer_id": 1, "creditor_id": 1, "lines": [{"description":"L","unit_price":"1.00"}]}
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps(inv_payload)])
        assert r.exit_code == 0
        # corrupt seq
        seq = Path(".arledge") / "invoice_seq"
        seq.write_text("not-an-int\n", encoding="utf-8")
        # creating next invoice should recover and allocate id=2
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps(inv_payload)])
        assert r.exit_code == 0
        inv2 = json.loads(r.output)
        assert inv2.get("id") == 2
        assert seq.read_text(encoding="utf-8").strip() == "3"
