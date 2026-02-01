import sqlite3
import os
import datetime
from typing import List, Dict, Any, Optional
import json

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
        quantity REAL NOT NULL,
        unit_price INTEGER NOT NULL,
        vat_rate REAL NOT NULL
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


def create_customer(
    name: str, email: Optional[str] = None, address: Optional[str] = None
) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO customers (name,email,address) VALUES (?,?,?)",
        (name, email, address),
    )
    conn.commit()
    return cur.lastrowid


def create_creditor(
    name: str,
    address: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    tax_id: Optional[str] = None,
    payment_instructions: Optional[str] = None,
    default_currency: str = "SEK",
    beancount_account: Optional[str] = None,
) -> int:
    created_at = datetime.datetime.utcnow().isoformat()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO creditors (name,address,email,phone,tax_id,payment_instructions,default_currency,beancount_account,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
        (
            name,
            address,
            email,
            phone,
            tax_id,
            payment_instructions,
            default_currency,
            beancount_account,
            created_at,
        ),
    )
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid


def list_creditors() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id,name,address,email,phone,tax_id,payment_instructions,default_currency,beancount_account,created_at FROM creditors ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_creditor(cred_id: int) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id,name,address,email,phone,tax_id,payment_instructions,default_currency,beancount_account,created_at FROM creditors WHERE id=?",
        (cred_id,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_payment_account(
    creditor_id: int,
    type: str,
    label: Optional[str] = None,
    identifier: Optional[str] = None,
    bank_name: Optional[str] = None,
    currency: Optional[str] = None,
    beancount_account: Optional[str] = None,
    is_default: bool = False,
    metadata: Optional[Dict[str, Any]] = None,
) -> int:
    created_at = datetime.datetime.utcnow().isoformat()
    conn = get_conn()
    cur = conn.cursor()
    # If setting default, clear other defaults for this creditor
    if is_default:
        cur.execute(
            "UPDATE creditor_payment_accounts SET is_default=0 WHERE creditor_id=?",
            (creditor_id,),
        )
    meta_json = json.dumps(metadata or {})
    cur.execute(
        "INSERT INTO creditor_payment_accounts (creditor_id,type,label,identifier,bank_name,currency,beancount_account,is_default,metadata,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (
            creditor_id,
            type,
            label,
            identifier,
            bank_name,
            currency,
            beancount_account,
            1 if is_default else 0,
            meta_json,
            created_at,
        ),
    )
    conn.commit()
    pa_id = cur.lastrowid
    conn.close()
    return pa_id


def list_payment_accounts(creditor_id: Optional[int] = None) -> List[Dict[str, Any]]:
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
        results.append(item)
    return results


def get_default_payment_account(creditor_id: int) -> Optional[Dict[str, Any]]:
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
    return item


def list_customers() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,address FROM customers ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_customer(cid: int) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,address FROM customers WHERE id=?", (cid,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_invoice(
    customer_id: int,
    lines: List[Dict[str, Any]],
    status: str = "draft",
    due_days: Optional[int] = None,
    description: Optional[str] = None,
    creditor_id: Optional[int] = None,
    currency: Optional[str] = None,
) -> int:
    created_at = datetime.datetime.utcnow().isoformat()
    due_at = None
    if due_days is not None:
        due_at = (
            (datetime.datetime.utcnow() + datetime.timedelta(days=int(due_days)))
            .date()
            .isoformat()
        )
    conn = get_conn()
    cur = conn.cursor()
    # Insert invoice, optionally linking a creditor and currency
    if creditor_id is None and currency is None:
        cur.execute(
            "INSERT INTO invoices (customer_id,status,created_at,due_at,description) VALUES (?,?,?,?,?)",
            (customer_id, status, created_at, due_at, description),
        )
    else:
        # Use provided values or defaults
        cur.execute(
            "INSERT INTO invoices (customer_id,status,created_at,due_at,description,creditor_id,currency) VALUES (?,?,?,?,?,?,?)",
            (
                customer_id,
                status,
                created_at,
                due_at,
                description,
                creditor_id,
                currency or "SEK",
            ),
        )
    invoice_id = cur.lastrowid
    for line in lines:
        unit_price_cents = int(round(float(line["unit_price"]) * 100))
        quantity = float(line.get("quantity", 1))
        vat_rate = float(line.get("vat_rate", 0))
        cur.execute(
            "INSERT INTO invoice_lines (invoice_id,description,quantity,unit_price,vat_rate) VALUES (?,?,?,?,?)",
            (invoice_id, line["description"], quantity, unit_price_cents, vat_rate),
        )
    conn.commit()
    conn.close()
    return invoice_id


def list_invoices() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, customer_id, status, created_at, due_at, description FROM invoices ORDER BY id DESC"
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_invoice(invoice_id: int) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, customer_id, status, created_at, due_at, description FROM invoices WHERE id=?",
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
    subtotal = 0.0
    total_vat = 0.0
    for l in lines:
        qty = l["quantity"]
        up = l["unit_price"] / 100.0
        line_net = up * qty
        vat_amount = line_net * (l["vat_rate"] / 100.0)
        subtotal += line_net
        total_vat += vat_amount
        inv_lines.append(
            {
                "description": l["description"],
                "quantity": qty,
                "unit_price": round(up, 2),
                "vat_rate": l["vat_rate"],
                "net": round(line_net, 2),
                "vat": round(vat_amount, 2),
                "line_total": round(line_net + vat_amount, 2),
            }
        )
    inv["lines"] = inv_lines
    inv["subtotal"] = round(subtotal, 2)
    inv["total_vat"] = round(total_vat, 2)
    inv["total"] = round(subtotal + total_vat, 2)
    conn.close()
    return inv


def format_invoice_number(invoice_id: int) -> str:
    return f"INV-{invoice_id:04d}"


def export_invoice_json(invoice_id: int, path: Optional[str] = None) -> Optional[str]:
    import json

    inv = get_invoice(invoice_id)
    if not inv:
        return None
    inv["invoice_number"] = format_invoice_number(inv["id"])
    if path is None:
        path = f"invoice-{inv['id']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(inv, f, indent=2, ensure_ascii=False)
    return path
