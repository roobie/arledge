from datetime import date, datetime, timezone
import json

from ledger import beancount_spike as spike
from ledger import config


class DummyEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_coerce_helpers_and_title_detection():
    assert spike.coerce_int("5") == 5
    assert spike.coerce_int(None) is None

    assert spike.coerce_bool(True) is True
    assert spike.coerce_bool("yes") is True
    assert spike.coerce_bool("0") is False
    assert spike.coerce_bool("nope") is None

    assert str(spike.coerce_decimal("1.23")) == "1.23"
    # float input
    d = spike.coerce_decimal(1.2)
    assert str(d).startswith("1.2")

    # date coercion from date and ISO string
    dt = spike.coerce_date_to_dt(date(2020, 1, 2))
    assert dt.year == 2020
    iso = "2020-01-01T00:00:00Z"
    dt2 = spike.coerce_date_to_dt(iso)
    assert dt2 is not None

    # title detection from attribute
    e = DummyEntry(payee="ACME")
    assert spike.detect_entry_title(e) == "ACME"

    # fallback to values list
    class Val:
        def __init__(self, value):
            self.value = value

    e2 = DummyEntry(values=[Val("Something")])
    assert spike.detect_entry_title(e2) == "Something"


def test_map_custom_to_models_and_payment_account():
    # customer mapping
    e = DummyEntry(payee="CustName", meta={"customer_id": "2", "email": "a@b."})
    cust = spike.map_custom_to_customer(e)
    assert cust.name == "CustName"
    assert cust.id == 2

    # creditor mapping with created_at via date attr
    e2 = DummyEntry(payee="CredName", meta={"creditor_id": "3", "email": "c@d."}, date=date(2021, 5, 4))
    cred = spike.map_custom_to_creditor(e2)
    assert cred.name == "CredName"
    assert cred.id == 3

    # payment account mapping
    meta = {"creditor_id": "3", "type": "bank", "identifier": "I1", "currency": "SEK", "is_default": "1"}
    e3 = DummyEntry(meta=meta)
    pa = spike.map_custom_to_payment_account(e3)
    assert pa.creditor_id == 3
    assert pa.type == "bank"
    assert pa.is_default is True


def test_map_transaction_to_invoice_with_sidecar(tmp_path):
    # prepare sidecar JSON
    data = {"lines": [{"description": "S", "unit_price": "10.00"}]}
    p = tmp_path / "inv.json"
    p.write_text(json.dumps(data), encoding="utf-8")

    class Units:
        def __init__(self, currency):
            self.currency = currency

    class Posting:
        def __init__(self, units):
            self.units = units

    meta = {"invoice_id": "7", "customer_id": "1", "invoice_data": str(p)}
    entry = DummyEntry(meta=meta, postings=[Posting(Units("USD"))], narration="Invoice INV-0007", date=date(2022, 1, 2))
    inv = spike.map_transaction_to_invoice(entry)
    assert inv.id == 7
    assert inv.currency == "USD"
    assert inv.lines and inv.lines[0].description == "S"
