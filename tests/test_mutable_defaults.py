from arledge.models import PaymentAccount, Invoice, InvoiceLine


def test_paymentaccount_metadata_independent():
    a = PaymentAccount(creditor_id=1, type="bank")
    b = PaymentAccount(creditor_id=2, type="bank")
    a.metadata["x"] = "1"
    assert b.metadata == {}


def test_invoice_lines_independent():
    a = Invoice(customer_id=1)
    b = Invoice(customer_id=2)
    # append a line to a; b.lines should remain empty
    a.lines.append(InvoiceLine(description="d", unit_price="1.00"))
    assert b.lines == []
