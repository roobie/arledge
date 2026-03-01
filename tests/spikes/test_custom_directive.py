import textwrap


def test_loader_roundtrip_custom_directive():
    content = textwrap.dedent('''
    2026-03-01 custom "customer" "ACME Corp"
      customer_id: 1
      email: "sales@acme.example"
      address: "123 Road"
    ''')

    # Lazy import so test requires beancount only when run
    from beancount.loader import load_string

    entries, errors, options = load_string(content)
    assert not errors, f"Unexpected parse errors: {errors}"

    customs = [e for e in entries if e.__class__.__name__ == "Custom"]
    assert len(customs) == 1
    entry = customs[0]
    # Metadata should round-trip
    assert "customer_id" in entry.meta
    assert entry.meta.get("email") == "sales@acme.example"
    assert entry.meta.get("address") == "123 Road"


def test_parser_parse_snippet():
    content = textwrap.dedent('''
    2026-03-01 custom "customer" "ACME Corp"
      customer_id: 1
      email: "sales@acme.example"
      address: "123 Road"
    ''')

    # Use lower-level parser for snippet-only validation
    from beancount.parser import parser

    # parser.parse_string may return more than two values across beancount versions.
    # Unpack the first two (entries, errors) and ignore the rest for compatibility.
    entries, errors, *rest = parser.parse_string(content)
    # parser.parse_string returns a list of errors as the second element
    assert not errors, f"Parser reported errors: {errors}"

    customs = [e for e in entries if e.__class__.__name__ == "Custom"]
    assert len(customs) == 1
    entry = customs[0]
    assert hasattr(entry, "meta")
    assert entry.meta.get("customer_id") == "1" or entry.meta.get("customer_id") == 1
