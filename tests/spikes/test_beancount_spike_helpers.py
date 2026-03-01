from ledger.beancount_spike import (
    extract_custom_entries_from_loader_entries,
    entry_meta_map,
    detect_entry_title,
    map_custom_entry_to_dict,
)


class Custom:
    def __init__(self):
        self.meta = {"customer_id": "1", "email": "x@acme.test"}
        self.payee = "ACME Corp"


def test_map_custom_entry_to_dict():
    d = Custom()
    mapped = map_custom_entry_to_dict(d)
    assert mapped["title"] == "ACME Corp"
    assert "customer_id" in mapped["meta"]


def test_extract_custom_entries_from_loader_entries():
    items = [Custom(), object(), Custom()]
    customs = extract_custom_entries_from_loader_entries(items)
    assert len(customs) == 2


def test_entry_meta_map_returns_empty_for_missing():
    class NoMeta:
        pass

    nm = NoMeta()
    assert entry_meta_map(nm) == {}


def test_detect_entry_title_fallbacks():
    class S:
        def __init__(self):
            self.description = "A description"

    s = S()
    assert detect_entry_title(s) == "A description"
