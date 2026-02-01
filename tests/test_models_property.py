from decimal import Decimal
from hypothesis import given, strategies as st

from ledger.models import InvoiceLine, Invoice


@given(q=st.decimals(min_value=-1000, max_value=1000, places=2),
       up=st.decimals(min_value=0, max_value=10000, places=2),
       vat=st.decimals(min_value=0, max_value=100, places=2))
def test_invoice_line_totals(q, up, vat):
    # coerce to sensible positive quantities for quantity
    q = abs(q) or Decimal('1')
    up = abs(up) or Decimal('0.01')
    vat = abs(vat)
    line = InvoiceLine(description='t', quantity=q, unit_price=up, vat_rate=vat)
    # computed fields should be present and consistent
    assert line.net is not None
    assert line.vat is not None
    assert line.line_total == (line.net + line.vat)


def test_invoice_totals_from_lines():
    lines = [
        {'description': 'a', 'quantity': Decimal('2'), 'unit_price': Decimal('10.00'), 'vat_rate': Decimal('25')},
        {'description': 'b', 'quantity': Decimal('1'), 'unit_price': Decimal('5.00'), 'vat_rate': Decimal('0')},
    ]
    inv = Invoice(customer_id=1, lines=lines)
    assert inv.subtotal is not None
    assert inv.total == (inv.subtotal + inv.total_vat)
