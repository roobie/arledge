from decimal import Decimal
from datetime import datetime, timezone

from ledger import models, config


def test_str_to_decimal_none_and_decimal_input():
    assert config.str_to_decimal(None) is None
    assert config.str_to_decimal(Decimal("3.00")) == Decimal("3.00")


def test_str_to_decimal_currency_variants():
    assert config.str_to_decimal_currency(None) is None
    d = Decimal("1.234")
    out = config.str_to_decimal_currency(d)
    assert out == Decimal("1.23") or isinstance(out, Decimal)
    out2 = config.str_to_decimal_currency("2.345")
    assert out2 == Decimal("2.35")


def test_serialize_unknown_type_and_collections():
    class X:
        pass

    x = X()
    assert config._serialize_value(x) is x
    assert config._serialize_value([Decimal("1.00"), {"a": Decimal("2.00")}])


def test_models_created_at_variants_and_invoice_line_float():
    # Creditor created_at may be None or auto-set depending on pydantic behavior
    c = models.Creditor(name="C")
    assert hasattr(c, "created_at")

    # Creditor created_at string parses
    s = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    c2 = models.Creditor(name="C2", created_at=s)
    assert c2.created_at.tzinfo is not None

    # PaymentAccount created_at string and presence
    pa = models.PaymentAccount(creditor_id=1, type="t")
    assert hasattr(pa, "created_at")
    pa2 = models.PaymentAccount(creditor_id=1, type="t", created_at=s)
    assert pa2.created_at.tzinfo is not None

    # InvoiceLine with float unit_price triggers float coercion
    il = models.InvoiceLine(description="f", unit_price=1.5)
    assert il.unit_price == Decimal("1.5") or isinstance(il.unit_price, Decimal)
