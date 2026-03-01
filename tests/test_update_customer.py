import json
from click.testing import CliRunner
from arledge import cli


def test_customer_update_patch():
    runner = CliRunner()
    with runner.isolated_filesystem():
        r = runner.invoke(cli.cli, ["init"])
        assert r.exit_code == 0
        r = runner.invoke(cli.cli, ["customer", "create", "--model", '{"name":"Cust A","email":"a@ex.com","address":"Addr 1"}'])
        assert r.exit_code == 0
        created = json.loads(r.output)
        cid = created.get("id")
        assert cid is not None
        # patch: change address only
        r = runner.invoke(cli.cli, ["customer", "update", str(cid), "--model", '{"address":"New Addr"}'])
        assert r.exit_code == 0
        updated = json.loads(r.output)
        assert updated.get("address") == "New Addr"
        assert updated.get("name") == "Cust A"
        assert updated.get("email") == "a@ex.com"
        # patch: change name
        r = runner.invoke(cli.cli, ["customer", "update", str(cid), "--model", '{"name":"Cust B"}'])
        assert r.exit_code == 0
        updated2 = json.loads(r.output)
        assert updated2.get("name") == "Cust B"
        assert updated2.get("address") == "New Addr"
