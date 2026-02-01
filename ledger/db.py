import sqlite3
import os
from typing import List, Optional
import json
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone

from . import config
from . import models

DB_PATH: str = os.path.join(os.getcwd(), "ledger.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        address TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'draft',
        created_at TEXT NOT NULL,
        due_at TEXT,
        description TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoice_lines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        quantity TEXT NOT NULL,
        unit_price INTEGER NOT NULL,
        vat_rate TEXT NOT NULL
    )
    """)
    # Creditors: the entity issuing invoices (us / contractor)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS creditors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        email TEXT,
        phone TEXT,
        tax_id TEXT,
        payment_instructions TEXT,
        default_currency TEXT DEFAULT 'SEK',
        beancount_account TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Multiple inbound payment accounts for a creditor (bank, paypal, etc.)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS creditor_payment_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creditor_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        label TEXT,
        identifier TEXT,
        bank_name TEXT,
        currency TEXT,
        beancount_account TEXT,
        is_default INTEGER DEFAULT 0,
        metadata TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Ensure invoices have creditor_id and currency columns (safe for existing DB)
    def ensure_column(table: str, column: str, definition: str) -> None:
        cur2 = conn.cursor()
        cur2.execute(f"PRAGMA table_info({table})")
        cols = [r[1] for r in cur2.fetchall()]
        if column not in cols:
            cur2.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    ensure_column("invoices", "creditor_id", "INTEGER")
    ensure_column("invoices", "currency", "TEXT DEFAULT 'SEK'")
    conn.commit()
    conn.close()


def create_customer(customer: models.Customer) -> models.Customer:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO customers (name,email,address) VALUES (?,?,?)",
        (customer.name, customer.email, customer.address),
    )
    conn.commit()
    customer.id = cur.lastrowid
    conn.close()
    return customer


def create_creditor(creditor: models.Creditor) -> models.Creditor:
    created_at = config.dt_to_iso_utc(creditor.created_at or datetime.now(timezone.utc))
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO creditors (name,address,email,phone,tax_id,payment_instructions,default_currency,beancount_account,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
        (
            creditor.name,
            creditor.address,
            creditor.email,
            creditor.phone,
            creditor.tax_id,
            creditor.payment_instructions,
            creditor.default_currency,
            creditor.beancount_account,
            created_at,
        ),
    )
    conn.commit()
    creditor.id = cur.lastrowid
    creditor.created_at = config.iso_to_dt(created_at)
    conn.close()
    return creditor


def list_creditors() -> List[models.Creditor]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id,name,address,email,phone,tax_id,payment_instructions,default_currency,beancount_account,created_at FROM creditors ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()
    return [models.Creditor.model_validate(dict(r)) for r in rows]


def get_creditor(cred_id: int) -> Optional[models.Creditor]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id,name,address,email,phone,tax_id,payment_instructions,default_currency,beancount_account,created_at FROM creditors WHERE id=?",
        (cred_id,),
    )
    row = cur.fetchone()
    conn.close()
    return models.Creditor.model_validate(dict(row)) if row else None


def create_payment_account(pa: models.PaymentAccount) -> models.PaymentAccount:
    created_at = config.dt_to_iso_utc(pa.created_at or datetime.now(timezone.utc))
    conn = get_conn()
    cur = conn.cursor()
    if pa.is_default:
        cur.execute(
            "UPDATE creditor_payment_accounts SET is_default=0 WHERE creditor_id=?",
            (pa.creditor_id,),
        )
    meta_json = json.dumps(pa.metadata or {})
    cur.execute(
        "INSERT INTO creditor_payment_accounts (creditor_id,type,label,identifier,bank_name,currency,beancount_account,is_default,metadata,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (
            pa.creditor_id,
            pa.type,
            pa.label,
            pa.identifier,
            pa.bank_name,
            pa.currency,
            pa.beancount_account,
            1 if pa.is_default else 0,
            meta_json,
            created_at,
        ),
    )
    conn.commit()
    pa.id = cur.lastrowid
    pa.created_at = config.iso_to_dt(created_at)
    conn.close()
    return pa


def list_payment_accounts(creditor_id: Optional[int] = None) -> List[models.PaymentAccount]:
    conn = get_conn()
    cur = conn.cursor()
    if creditor_id is None:
        cur.execute(
            "SELECT id,creditor_id,type,label,identifier,bank_name,currency,beancount_account,is_default,metadata,created_at FROM creditor_payment_accounts ORDER BY id"
        )
    else:
        cur.execute(
            "SELECT id,creditor_id,type,label,identifier,bank_name,currency,beancount_account,is_default,metadata,created_at FROM creditor_payment_accounts WHERE creditor_id=? ORDER BY id",
            (creditor_id,),
        )
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        item = dict(r)
        try:
            item["metadata"] = json.loads(item.get("metadata") or "{}")
        except Exception:
            item["metadata"] = {}
        results.append(models.PaymentAccount.model_validate(item))
    return results


def get_default_payment_account(creditor_id: int) -> Optional[models.PaymentAccount]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id,creditor_id,type,label,identifier,bank_name,currency,beancount_account,is_default,metadata,created_at FROM creditor_payment_accounts WHERE creditor_id=? AND is_default=1 LIMIT 1",
        (creditor_id,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    try:
        item["metadata"] = json.loads(item.get("metadata") or "{}")
    except Exception:
        item["metadata"] = {}
    return models.PaymentAccount.model_validate(item)


def list_customers() -> List[models.Customer]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,address FROM customers ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [models.Customer.model_validate(dict(r)) for r in rows]


def get_customer(cid: int) -> Optional[models.Customer]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,address FROM customers WHERE id=?", (cid,))
    row = cur.fetchone()
    conn.close()
    return models.Customer.model_validate(dict(row)) if row else None


def create_invoice(invoice: models.Invoice) -> models.Invoice:
    created_at = config.dt_to_iso_utc(invoice.created_at or datetime.now(timezone.utc))
    due_at = config.dt_to_iso_utc(invoice.due_at) if invoice.due_at else None
    conn = get_conn()
    cur = conn.cursor()
    if invoice.creditor_id is None and invoice.currency is None:
        cur.execute(
            "INSERT INTO invoices (customer_id,status,created_at,due_at,description) VALUES (?,?,?,?,?)",
            (invoice.customer_id, invoice.status, created_at, due_at, invoice.description),
        )
    else:
        cur.execute(
            "INSERT INTO invoices (customer_id,status,created_at,due_at,description,creditor_id,currency) VALUES (?,?,?,?,?,?,?)",
            (
                invoice.customer_id,
                invoice.status,
                created_at,
                due_at,
                invoice.description,
                invoice.creditor_id,
                invoice.currency or "SEK",
            ),
        )
    invoice_id = cur.lastrowid
    for line in invoice.lines:
        up_cents = int((Decimal(line.unit_price) * Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        qty = config.decimal_to_str(Decimal(line.quantity))
        vat = config.decimal_to_str(Decimal(line.vat_rate))
        cur.execute(
            "INSERT INTO invoice_lines (invoice_id,description,quantity,unit_price,vat_rate) VALUES (?,?,?,?,?)",
            (invoice_id, line.description, qty, up_cents, vat),
        )
    conn.commit()
    invoice.id = invoice_id
    invoice.created_at = config.iso_to_dt(created_at)
    invoice.due_at = config.iso_to_dt(due_at) if due_at else None
    conn.close()
    return invoice


def list_invoices() -> List[models.Invoice]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, customer_id, status, created_at, due_at, description FROM invoices ORDER BY id DESC"
    )
    rows = cur.fetchall()
    conn.close()
    result = []
    for r in rows:
        inv = dict(r)
        inv['created_at'] = inv.get('created_at')
        inv['due_at'] = inv.get('due_at')
        # lines and totals will be computed by model
        inv['lines'] = []
        result.append(models.Invoice.model_validate(inv))
    return result


def get_invoice(invoice_id: int) -> Optional[models.Invoice]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, customer_id, status, created_at, due_at, description, creditor_id, currency FROM invoices WHERE id=?",
        (invoice_id,),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    inv = dict(row)
    cur.execute(
        "SELECT description,quantity,unit_price,vat_rate FROM invoice_lines WHERE invoice_id=?",
        (invoice_id,),
    )
    lines = cur.fetchall()
    inv_lines = []
    for l in lines:
        qty = Decimal(str(l["quantity"]))
        up = (Decimal(l["unit_price"]) / Decimal("100")).quantize(Decimal("0.01"))
        vat_rate = Decimal(str(l["vat_rate"]))
        inv_lines.append(
            {
                "description": l["description"],
                "quantity": qty,
                "unit_price": up,
                "vat_rate": vat_rate,
            }
        )
    inv["lines"] = inv_lines
    conn.close()
    return models.Invoice.model_validate(inv)


def format_invoice_number(invoice_id: int) -> str:
    return f"INV-{invoice_id:04d}"


def export_invoice_json(invoice_id: int, path: Optional[str] = None) -> Optional[str]:
    import json

    inv = get_invoice(invoice_id)
    if not inv:
        return None
    data = config.dump_model(inv)
    data["invoice_number"] = format_invoice_number(inv.id)
    if path is None:
        path = f"invoice-{inv.id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path
