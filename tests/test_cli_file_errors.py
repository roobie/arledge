import os
from click.testing import CliRunner

from ledger import cli, db


def test_model_file_read_errors(tmp_path):
    db.DB_PATH = os.path.join(tmp_path, 'g.db')
    db.init_db()
    # create a directory to pass as model-file (open will fail)
    d = tmp_path / 'adir'
    d.mkdir()
    runner = CliRunner()
    cmds = [
        ['customer', 'create', '--model-file', str(d)],
        ['creditor', 'create', '--model-file', str(d)],
        ['creditor', 'account', 'create', '--model-file', str(d)],
        ['invoice', 'create', '--model-file', str(d)],
    ]
    for cmd in cmds:
        r = runner.invoke(cli.cli, cmd)
        assert r.exit_code != 0
        assert 'Failed to read model file' in r.output

def test_schema_invoice_line_and_payment_account():
    runner = CliRunner()
    r = runner.invoke(cli.cli, ['schema', 'invoice-line'])
    assert r.exit_code == 0
    assert 'properties' in r.output

    r2 = runner.invoke(cli.cli, ['schema', 'payment-account'])
    assert r2.exit_code == 0
    assert 'properties' in r2.output
