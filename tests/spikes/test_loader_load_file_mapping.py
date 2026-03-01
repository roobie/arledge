from beancount.loader import load_file
from pathlib import Path

from arledge.beancount_spike import map_custom_to_customer
from arledge.models import Customer


def test_loader_load_file_maps_customers(tmp_path):
    includes_dir = tmp_path / "includes"
    includes_dir.mkdir()
    customers_file = includes_dir / "customers.beancount"
    customers_file.write_text('''
2026-03-01 custom "customer" "ACME Corp"
  customer_id: 1
  email: "sales@acme.example"
  address: "123 Road"

2026-03-02 custom "customer" "Beta LLC"
  customer_id: 2
  email: "hello@beta.test"
  address: "456 Lane"
''')
    entries, errors, options = load_file(str(customers_file))
    assert not errors
    customs = [e for e in entries if e.__class__.__name__ == "Custom"]
    assert len(customs) == 2
    c1 = map_custom_to_customer(customs[0])
    assert isinstance(c1, Customer)
    assert c1.id == 1
    assert c1.name == "ACME Corp"
    c2 = map_custom_to_customer(customs[1])
    assert c2.id == 2
    assert c2.name == "Beta LLC"
