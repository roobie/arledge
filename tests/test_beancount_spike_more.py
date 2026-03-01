from ledger.beancount_spike import detect_entry_title, coerce_decimal


class Dummy:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_detect_entry_title_from_string_values():
    e = Dummy(values=["Hello"])
    assert detect_entry_title(e) == "Hello"


def test_detect_entry_title_from_value_object():
    class V:
        def __init__(self, value):
            self.value = value

    e = Dummy(values=[V("Val")])
    assert detect_entry_title(e) == "Val"


def test_detect_entry_title_vars_typeerror_fallback():
    class NoDict:
        __slots__ = ("a",)

        def __init__(self, a):
            self.a = a

    e = NoDict("slotval")
    # vars() may raise TypeError for objects with __slots__ and no __dict__
    # detect_entry_title should handle this gracefully and return None
    assert detect_entry_title(e) is None


def test_coerce_decimal_str_and_float():
    assert str(coerce_decimal("1.20")) == "1.20"
    d = coerce_decimal(1.5)
    assert str(d).startswith("1.5")
