import textwrap
from beancount.loader import load_string

from ledger.beancount_spike import map_custom_to_creditor, map_custom_to_payment_account
from ledger.models import Creditor, PaymentAccount


def test_map_creditor_and_payment_account():
    content = textwrap.dedent('''
    2026-03-01 custom "creditor" "Office Supplies Ltd"
      creditor_id: 7
      email: "billing@office.example"
      address: "456 Avenue"

    2026-03-01 custom "payment_account" "Business Checking"
      creditor_id: 7
      type: "bank"
      label: "Main checking"
      identifier: "SE1234567890"
      bank: "Nordea"
      currency: "SEK"
      is_default: "true"
    ''')
    entries, errors, options = load_string(content)
    assert not errors
    customs = [e for e in entries if e.__class__.__name__ == "Custom"]
    # Expect two customs
    assert len(customs) == 2
    cred = map_custom_to_creditor(customs[0])
    assert isinstance(cred, Creditor)
    assert cred.id == 7
    assert cred.name == "Office Supplies Ltd"

    pa = map_custom_to_payment_account(customs[1])
    assert isinstance(pa, PaymentAccount)
    assert pa.creditor_id == 7
    assert pa.type == "bank"
    assert pa.identifier == "SE1234567890"
    assert pa.bank_name == "Nordea"
    assert pa.currency == "SEK"
    assert pa.is_default is True
