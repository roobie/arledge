import os
import runpy
import sys
import sqlite3
from datetime import datetime

from ledger import migrations, db, config


def test_run_migrations_tmp(tmp_path):
    # point migrations to a temp DB and run
    migrations.DB_PATH = str(tmp_path / 'migr.db')
    # should create and close connection without error
    migrations.run_migrations()
    assert os.path.exists(migrations.DB_PATH)


def test_main_module_runs_help():
    # running the package as __main__ should call the CLI; set argv to --help
    old_argv = sys.argv[:]
    try:
        sys.argv[:] = ['ledger', '--help']
        try:
            runpy.run_module('ledger', run_name='__main__')
        except SystemExit as e:
            # click may call sys.exit(0) for --help
            assert e.code == 0
    finally:
        sys.argv[:] = old_argv


def test_dt_naive_becomes_utc():
    # naive datetime should be treated as UTC in dt_to_iso_utc
    dt = datetime(2020, 1, 1, 0, 0, 0)
    s = config.dt_to_iso_utc(dt)
    assert s.endswith('Z')


def test_init_db_adds_columns_when_missing(tmp_path):
    # ensure init_db's ensure_column path runs by creating a DB missing columns
    db.DB_PATH = str(tmp_path / 'coltest.db')
    # prevent init_db from deleting our DB
    orig = config.IS_DEVELOPMENT
    config.IS_DEVELOPMENT = False
    try:
        # Create minimal invoice table without creditor_id/currency
        conn = sqlite3.connect(db.DB_PATH)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS arledge_invoice (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL)')
        conn.commit()
        conn.close()

        # run init_db which should detect missing columns and add them
        db.init_db()
        conn = sqlite3.connect(db.DB_PATH)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(arledge_invoice)")
        cols = [r[1] for r in cur.fetchall()]
        conn.close()
        assert 'creditor_id' in cols
        assert 'currency' in cols
    finally:
        config.IS_DEVELOPMENT = orig
