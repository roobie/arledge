import os
import tempfile
import shutil
from ledger import db
from ledger import models


def setup_module(module):
    # ensure clean DB for tests
    try:
        os.remove(os.path.join(os.getcwd(), "ledger.db"))
    except Exception:
        pass
    db.init_db()


def test_create_and_list_creditor():
    cred = models.Creditor(
        name="ACME Inc",
        address="1 Road",
        email="a@acme.test",
        phone="+46-8-000",
        tax_id="556677-8899",
        payment_instructions="Pay to IBAN",
        default_currency="SEK",
        beancount_account="Equity:Owner",
    )
    created = db.create_creditor(cred)
    assert isinstance(created.id, int)
    creds = db.list_creditors()
    assert any(c.id == created.id for c in creds)


def test_create_payment_account_and_default():
    creds = db.list_creditors()
    assert creds, "no creditors present"
    cid = creds[0].id
    pa1 = models.PaymentAccount(creditor_id=cid, type="bank", label="Main account", identifier="SE000123", bank_name="Bank A", currency="SEK", beancount_account="Assets:Bank:Main", is_default=True)
    pa2 = models.PaymentAccount(creditor_id=cid, type="paypal", label="PayPal", identifier="pp@example.com", currency="SEK", beancount_account="Assets:Paypal", is_default=False)
    created_pa1 = db.create_payment_account(pa1)
    db.create_payment_account(pa2)
    accounts = db.list_payment_accounts(creditor_id=cid)
    assert len(accounts) >= 2
    default = db.get_default_payment_account(cid)
    assert default and default.id == created_pa1.id
