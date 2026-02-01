import os
import json
from decimal import Decimal

from ledger import db, models


def setup_function(fn):
    # ensure a fresh DB in the repo root for these tests; use test-specific file
    db.DB_PATH = os.path.join(os.getcwd(), "test_ledger.db")
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()


def teardown_function(fn):
    try:
        os.remove(db.DB_PATH)
    except Exception:
        pass


def test_create_and_list_creditor_and_payment_account():
    c = models.Creditor(name="X")
    created = db.create_creditor(c)
    assert created.id is not None
    all_cs = db.list_creditors()
    assert len(all_cs) == 1

    pa = models.PaymentAccount(
        creditor_id=created.id, type="bank", label="L", identifier="I"
    )
    pa2 = db.create_payment_account(pa)
    assert pa2.id is not None
    # default behavior: is_default False -> created as provided
    all_pas = db.list_payment_accounts()
    assert any(p.creditor_id == created.id for p in all_pas)
    assert db.get_default_payment_account(created.id) is None

    # create default account and ensure previous default reset
    pa3 = models.PaymentAccount(
        creditor_id=created.id, type="bank", is_default=True, identifier="D"
    )
    db.create_payment_account(pa3)
    default = db.get_default_payment_account(created.id)
    assert default is not None and default.is_default


def test_customers_and_invoices_and_export(tmp_path):
    c = models.Customer(name="Cust")
    created = db.create_customer(c)
    assert created.id is not None
    customers = db.list_customers()
    assert customers and customers[0].name == "Cust"

    inv = models.Invoice(
        customer_id=created.id,
        lines=[models.InvoiceLine(description="one", unit_price=Decimal("10.00"))],
    )
    created_inv = db.create_invoice(inv)
    assert created_inv.id is not None
    got = db.get_invoice(created_inv.id)
    assert got is not None
    # export JSON
    outpath = tmp_path / f"out-{created_inv.id}.json"
    path = db.export_invoice_json(created_inv.id, path=str(outpath))
    assert path is not None and os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "invoice_number" in data
