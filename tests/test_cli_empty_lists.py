import os
from click.testing import CliRunner

from ledger import cli, db


def test_empty_list_branches(tmp_path):
    db.DB_PATH = os.path.join(tmp_path, 'h.db')
    db.init_db()
    runner = CliRunner()
    # customer list when empty
    r = runner.invoke(cli.cli, ['customer', 'list'])
    assert 'No customers' in r.output

    # creditor list when empty
    r2 = runner.invoke(cli.cli, ['creditor', 'list'])
    assert 'No creditors' in r2.output

    # payment accounts when empty
    r3 = runner.invoke(cli.cli, ['creditor', 'account', 'list'])
    assert 'No payment accounts' in r3.output

    # invoice list when empty
    r4 = runner.invoke(cli.cli, ['invoice', 'list'])
    assert 'No invoices' in r4.output
