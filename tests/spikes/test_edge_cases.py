import textwrap
from beancount.loader import load_string
from beancount.parser import parser

from ledger.beancount_spike import (
    map_custom_to_customer,
    map_custom_to_payment_account,
    map_custom_to_creditor,
    coerce_decimal,
)
from ledger.models import Customer


def test_map_customer_missing_id_is_allowed():
    # customer entry without customer_id meta should map with id=None
    content = textwrap.dedent('''
    2026-03-01 custom "customer" "No ID Corp"
      email: "noid@example.test"
    ''')
    entries, errors, options = load_string(content)
    assert not errors
    customs = [e for e in entries if e.__class__.__name__ == "Custom"]
    assert len(customs) == 1
    c = map_custom_to_customer(customs[0])
    assert isinstance(c, Customer)
    assert c.id is None
    assert c.name == "No ID Corp"


def test_map_payment_account_missing_required_fields_raises():
    # missing creditor_id
    content1 = textwrap.dedent('''
    2026-03-01 custom "payment_account" "No Creditor"
      type: "bank"
    ''')
    entries1, errors1, opts1 = load_string(content1)
    assert not errors1
    customs1 = [e for e in entries1 if e.__class__.__name__ == "Custom"]
    try:
        map_custom_to_payment_account(customs1[0])
        assert False, "Expected ValueError for missing creditor_id"
    except ValueError:
        pass

    # missing type
    content2 = textwrap.dedent('''
    2026-03-01 custom "payment_account" "No Type"
      creditor_id: 5
    ''')
    entries2, errors2, opts2 = load_string(content2)
    assert not errors2
    customs2 = [e for e in entries2 if e.__class__.__name__ == "Custom"]
    try:
        map_custom_to_payment_account(customs2[0])
        assert False, "Expected ValueError for missing type"
    except ValueError:
        pass


def test_meta_types_decimal_and_string_coercion():
    # numeric unquoted -> beancount meta returns Decimal
    content_num = textwrap.dedent('''
    2026-03-01 custom "customer" "NumCorp"
      customer_id: 99
      email: "num@example.test"
    ''')
    entries_num, errors_num, opts_num = load_string(content_num)
    assert not errors_num
    cust_num = [e for e in entries_num if e.__class__.__name__ == "Custom"][0]
    c1 = map_custom_to_customer(cust_num)
    assert c1.id == 99

    # quoted string -> meta value is string
    content_str = textwrap.dedent('''
    2026-03-01 custom "customer" "StrCorp"
      customer_id: "100"
      email: "str@example.test"
    ''')
    entries_str, errors_str, opts_str = load_string(content_str)
    assert not errors_str
    cust_str = [e for e in entries_str if e.__class__.__name__ == "Custom"][0]
    c2 = map_custom_to_customer(cust_str)
    assert c2.id == 100

    # check coerce_decimal works for numeric-like strings and Decimal
    assert coerce_decimal("12.34") == coerce_decimal(12.34)


def test_parser_and_loader_report_errors_on_malformed_snippet():
    # malformed: unquoted bareword where a boolean isn't allowed (true without quotes breaks lexer in some beancount versions)
    bad = '2026-03-01 custom "customer" "Bad"\n  customer_id: true\n'
    # parser.parse_string should report errors
    parsed = parser.parse_string(bad)
    # parser may return varying arity; errors is second element
    errors = parsed[1]
    assert errors, "Expected parser errors for malformed snippet"

    # loader should also report errors
    entries, errors2, opts = load_string(bad)
    assert errors2, "Expected loader errors for malformed snippet"
