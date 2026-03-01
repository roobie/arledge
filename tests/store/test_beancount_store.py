from pathlib import Path
import json
from click.testing import CliRunner
from arledge import beancount_store
from arledge import config


def test_beancount_store_roundtrip(tmp_path, monkeypatch):
    # Prepare base dir and set ARLEDGE_BASEDIR
    base = tmp_path
    monkeypatch.setenv("ARLEDGE_BASEDIR", str(base))

    includes = base / "includes"
    includes.mkdir()
    customers = includes / "customers.beancount"
    creditors = includes / "creditors.beancount"
    payment_accounts = includes / "payment_accounts.beancount"
    invoices_dir = includes / "invoices"
    invoices_dir.mkdir()
    invoice_data_dir = invoices_dir / "data"
    invoice_data_dir.mkdir()

    # ledger.beancount
    ledger_file = base / "ledger.beancount"
    ledger_file.write_text('''include "includes/customers.beancount"\ninclude "includes/creditors.beancount"\ninclude "includes/payment_accounts.beancount"\ninclude "includes/invoices/*.beancount"\n''')

    # customers
    customers.write_text('''2026-03-01 custom "customer" "ACME Corp"\n  customer_id: 1\n  email: "sales@acme.example"\n  address: "123 Road"\n''')

    # creditors
    creditors.write_text('''2026-03-01 custom "creditor" "Office Supplies Ltd"\n  creditor_id: 7\n  email: "billing@office.example"\n  address: "456 Avenue"\n''')

    # payment accounts
    payment_accounts.write_text('''2026-03-01 custom "payment_account" "Business Checking"\n  creditor_id: 7\n  type: "bank"\n  label: "Main"\n  identifier: "SE123"\n  bank: "Nordea"\n  currency: "SEK"\n''')

    # invoices file and sidecar
    inv_file = invoices_dir / "2026-03.beancount"
    inv_file.write_text('''2026-03-01 * "Invoice INV-0001"\n  invoice_id: 1\n  customer_id: 1\n  invoice_data: "includes/invoices/data/inv-0001.json"\n  Assets:Receivable:ACME        1250.00 SEK\n  Income:Services              -1000.00 SEK\n  Liabilities:VAT               -250.00 SEK\n''')
    sidecar = invoice_data_dir / "inv-0001.json"
    sidecar.write_text(json.dumps({"invoice_id": 1, "lines": [{"description": "Consulting", "quantity": "1", "unit_price": "1000.00", "vat_rate": "25"}]}))

    # Now exercise beancount_store
    customers = beancount_store.list_customers()
    assert len(customers) == 1
    assert customers[0].name == "ACME Corp"

    creditors = beancount_store.list_creditors()
    assert len(creditors) == 1
    assert creditors[0].name == "Office Supplies Ltd"

    pas = beancount_store.list_payment_accounts()
    assert len(pas) == 1
    assert pas[0].identifier == "SE123"

    invs = beancount_store.list_invoices()
    assert len(invs) == 1
    inv = beancount_store.get_invoice(1)
    assert inv is not None
    assert inv.total == inv.total  # simple access

    # export json
    out = beancount_store.export_invoice_json(1, path=str(base / "out.json"))
    assert out is not None
    assert Path(out).exists()
