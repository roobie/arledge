import sqlite3
import os
import datetime
from typing import List, Dict, Any, Optional

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
    cur.execute(
        "INSERT INTO invoices (customer_id,status,created_at,due_at,description) VALUES (?,?,?,?,?)",
        (customer_id, status, created_at, due_at, description),
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
