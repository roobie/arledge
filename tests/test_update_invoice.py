import json
from click.testing import CliRunner
from arledge import cli


def test_invoice_update_patch_changes_sidecar_and_totals():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # init
        r = runner.invoke(cli.cli, ["init"])
        assert r.exit_code == 0
        # create customer
        r = runner.invoke(cli.cli, ["customer", "create", "--model", '{"name":"InvCust","email":"inv@ex.com"}'])
        assert r.exit_code == 0
        cust = json.loads(r.output)
        cid = cust.get("id")
        assert cid is not None
        # create invoice with one line
        model = json.dumps({
            "customer_id": cid,
            "lines": [{"description": "Service A", "quantity": "1", "unit_price": "100.00", "vat_rate": "25"}]
        })
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", model])
        assert r.exit_code == 0
        created = json.loads(r.output)
        inv_id = created.get("id")
        assert inv_id is not None
        # view invoice and record totals
        r = runner.invoke(cli.cli, ["invoice", "view", str(inv_id)])
        assert r.exit_code == 0
        inv = json.loads(r.output)
        old_total = inv.get("total")
        assert old_total is not None
        # patch invoice: add another line
        patch = json.dumps({
            "lines": [
                {"description": "Service A", "quantity": "1", "unit_price": "100.00", "vat_rate": "25"},
                {"description": "Service B", "quantity": "2", "unit_price": "50.00", "vat_rate": "0"}
            ]
        })
        r = runner.invoke(cli.cli, ["invoice", "update", str(inv_id), "--model", patch])
        assert r.exit_code == 0
        updated = json.loads(r.output)
        # totals should have changed
        assert updated.get("total") is not None
        assert updated.get("total") != old_total
        # view again and ensure sidecar reflected
        r = runner.invoke(cli.cli, ["invoice", "view", str(inv_id)])
        assert r.exit_code == 0
        inv2 = json.loads(r.output)
        assert len(inv2.get("lines", [])) == 2
        # patch description only
        r = runner.invoke(cli.cli, ["invoice", "update", str(inv_id), "--model", '{"description":"Updated desc"}'])
        assert r.exit_code == 0
        upd2 = json.loads(r.output)
        assert upd2.get("description") == "Updated desc"
