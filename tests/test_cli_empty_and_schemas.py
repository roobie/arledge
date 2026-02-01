from click.testing import CliRunner
from ledger import cli, db
import os


def test_empty_lists_and_all_json_schemas(tmp_path):
    db.DB_PATH = os.path.join(tmp_path, "empty.db")
    db.init_db()
    runner = CliRunner()

    # empty list messages
    r = runner.invoke(cli.cli, ["customer", "list"])
    assert r.exit_code == 0
    assert "No customers" in r.output or "No customers" in r.stderr

    r2 = runner.invoke(cli.cli, ["creditor", "list"])
    assert r2.exit_code == 0
    assert "No creditors" in r2.output or "No creditors" in r2.stderr

    r3 = runner.invoke(cli.cli, ["creditor", "account", "list"])
    assert r3.exit_code == 0
    assert "No payment accounts" in r3.output or "No payment accounts" in r3.stderr

    r4 = runner.invoke(cli.cli, ["invoice", "list"])
    assert r4.exit_code == 0
    assert "No invoices" in r4.output or "No invoices" in r4.stderr

    # json-schema flags for all create commands
    for cmd in [
        ["customer", "create", "--json-schema"],
        ["creditor", "create", "--json-schema"],
        ["creditor", "account", "create", "--json-schema"],
        ["invoice", "create", "--json-schema"],
    ]:
        res = runner.invoke(cli.cli, cmd)
        assert res.exit_code == 0
        assert "properties" in res.output
