import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "ledger.db")

MIGRATIONS = [
    # Migration 1: create creditors and payment accounts tables handled in db.init_db
]


def run_migrations():
    # For now migrations are handled by db.init_db() which is idempotent.
    # This placeholder allows future explicit ALTER TABLE migrations.
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    run_migrations()
