import textwrap
from beancount.loader import load_string

from ledger.beancount_spike import map_custom_to_customer
from ledger.models import Customer


def test_map_custom_entry_to_customer():
    content = textwrap.dedent('''
    2026-03-01 custom "customer" "ACME Corp"
      customer_id: 42
      email: "sales@acme.example"
      address: "123 Road"
    ''')
    entries, errors, options = load_string(content)
    assert not errors
    customs = [e for e in entries if e.__class__.__name__ == "Custom"]
    assert len(customs) == 1
    cust = map_custom_to_customer(customs[0])
    assert isinstance(cust, Customer)
    assert cust.id == 42
    assert cust.name == "ACME Corp"
    assert cust.email == "sales@acme.example"
    assert cust.address == "123 Road"


def test_map_raises_on_missing_title():
    class NoTitle:
        meta = {"customer_id": "1"}

    nt = NoTitle()
    try:
        map_custom_to_customer(nt)
        assert False, "Expected ValueError"
    except ValueError:
        pass
