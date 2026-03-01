import json
from click.testing import CliRunner
from arledge import cli


def test_creditor_update_patch():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # init layout
        r = runner.invoke(cli.cli, ["init"])
        assert r.exit_code == 0
        # create creditor
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", '{"name":"Orig Ltd","email":"orig@example.com","address":"Old Addr"}'])
        assert r.exit_code == 0
        created = json.loads(r.output)
        cid = created.get("id")
        assert cid is not None
        # patch update: change email only
        r = runner.invoke(cli.cli, ["creditor", "update", str(cid), "--model", '{"email":"new@example.com"}'])
        assert r.exit_code == 0
        updated = json.loads(r.output)
        # email changed, name/address unchanged
        assert updated.get("email") == "new@example.com"
        assert updated.get("name") == "Orig Ltd"
        assert updated.get("address") == "Old Addr"

        # patch update: change name and phone
        r = runner.invoke(cli.cli, ["creditor", "update", str(cid), "--model", '{"name":"Renamed","phone":"+460000"}'])
        assert r.exit_code == 0
        updated2 = json.loads(r.output)
        assert updated2.get("name") == "Renamed"
        assert updated2.get("phone") == "+460000"
        # ensure email persisted from previous patch
        assert updated2.get("email") == "new@example.com"
