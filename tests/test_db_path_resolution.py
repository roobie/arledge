import os
from ledger import db, config


def test_get_db_path_precedence(tmp_path, monkeypatch):
    # 1) Module-level DB_PATH takes precedence
    orig_db_path = db.DB_PATH
    try:
        db.DB_PATH = str(tmp_path / "module.db")
        monkeypatch.delenv("LEDGER_DB_PATH", raising=False)
        config.ledger_db_path = None
        assert db.get_db_path() == str(tmp_path / "module.db")
    finally:
        db.DB_PATH = orig_db_path

    # 2) Environment variable next
    monkeypatch.setenv("LEDGER_DB_PATH", str(tmp_path / "env.db"))
    try:
        db.DB_PATH = None
        config.ledger_db_path = None
        assert db.get_db_path() == str(tmp_path / "env.db")
    finally:
        monkeypatch.delenv("LEDGER_DB_PATH", raising=False)

    # 3) Config.ledger_db_path next
    db.DB_PATH = None
    monkeypatch.delenv("LEDGER_DB_PATH", raising=False)
    try:
        config.ledger_db_path = str(tmp_path / "conf.db")
        assert db.get_db_path() == str(tmp_path / "conf.db")
    finally:
        config.ledger_db_path = None

    # 4) Fallback to cwd/ledger.db
    db.DB_PATH = None
    monkeypatch.delenv("LEDGER_DB_PATH", raising=False)
    config.ledger_db_path = None
    expected = os.path.join(os.getcwd(), "ledger.db")
    assert db.get_db_path() == expected
