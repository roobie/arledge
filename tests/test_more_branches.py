import os
import json
from decimal import Decimal

import sqlite3
from datetime import datetime, timezone
from click.testing import CliRunner

from ledger import cli, db, config, models


def test_instructions_and_schema_unknown():
    runner = CliRunner()
    res = runner.invoke(cli.cli, ['instructions'])
    assert res.exit_code == 0
    assert 'Instructions for agentic systems' in res.stderr

    res2 = runner.invoke(cli.cli, ['schema', 'nope'])
    assert res2.exit_code != 0
    assert 'Unknown schema name' in res2.output


def test_creditor_flow_and_view(tmp_path):
    # use isolated DB for CLI operations
    db.DB_PATH = os.path.join(tmp_path, 'cli_ledger.db')
    db.init_db()
    runner = CliRunner()
    # create creditor via model
    model = json.dumps({'name': 'Cred', 'email': 'c@c.test'})
    r = runner.invoke(cli.cli, ['creditor', 'create', '--model', model])
    assert r.exit_code == 0
    c = json.loads(r.output)
    assert c['name'] == 'Cred'

    # list and view
    rl = runner.invoke(cli.cli, ['creditor', 'list'])
    arr = json.loads(rl.output)
    assert any(x['name'] == 'Cred' for x in arr)

    vid = c['id']
    rv = runner.invoke(cli.cli, ['creditor', 'view', str(vid)])
    assert rv.exit_code == 0
    assert json.loads(rv.output)['id'] == vid


def test_account_create_missing_and_list_text_export():
    runner = CliRunner()
    # missing model for account create
    r = runner.invoke(cli.cli, ['creditor', 'account', 'create'])
    assert r.exit_code != 0
    assert 'Provide --model' in r.output

    # text export not implemented
    r2 = runner.invoke(cli.cli, ['invoice', 'export', '1', '--format', 'text'])
    assert r2.exit_code != 0
    assert 'Text export not implemented yet' in r2.output


def test_db_prefixed_validation_and_bad_metadata(tmp_path):
    # invalid prefix should raise
    orig = config.arledge_db_prefix
    try:
        config.arledge_db_prefix = 'bad-prefix!'
        try:
            db.prefixed('x')
            assert False, 'should have raised ValueError'
        except ValueError:
            pass
    finally:
        config.arledge_db_prefix = orig

    # create DB and insert a payment account with invalid metadata JSON to hit exception path
    db.DB_PATH = os.path.join(tmp_path, 'test_ledger2.db')
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()
    conn = sqlite3.connect(db.DB_PATH)
    cur = conn.cursor()
    table = db.prefixed('creditor')
    # insert creditor
    cur.execute(f"INSERT INTO {table} (name,created_at) VALUES (?,?)", ('Z', config.dt_to_iso_utc(db.datetime.now(db.timezone.utc)) if hasattr(db, 'datetime') else config.dt_to_iso_utc(None) ))
    cred_id = cur.lastrowid
    pa_table = db.prefixed('creditor_payment_account')
    cur.execute(f"INSERT INTO {pa_table} (creditor_id,type,metadata,created_at) VALUES (?,?,?,?)", (cred_id, 'b', 'not-a-json', config.dt_to_iso_utc(datetime.now(timezone.utc))))
    conn.commit()
    conn.close()
    # list_payment_accounts should not raise and should return metadata as {}
    results = db.list_payment_accounts(creditor_id=cred_id)
    assert results and isinstance(results[0].metadata, dict)
    try:
        os.remove(db.DB_PATH)
    except Exception:
        pass


def test_config_str_to_decimal_currency_rounding():
    # strings should be parsed and rounded to 2 decimals
    d = config.str_to_decimal_currency('1.235')
    assert isinstance(d, Decimal)
    assert d == Decimal('1.24')
