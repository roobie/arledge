import re
from decimal import Decimal, ROUND_HALF_UP

from hypothesis import given, strategies as st, settings

from ledger import config


pattern = re.compile(r"^-?\d+\.\d{2}$")


@given(
    st.decimals(
        min_value=-(10**8), max_value=10**8, allow_nan=False, allow_infinity=False
    )
)
@settings(max_examples=100)
def test_decimal_to_currency_string_hypothesis(d: Decimal):
    """Hypothesis-based property test: any Decimal should format as a two-decimal
    culture-invariant string and round-trip back to the expected quantized Decimal.
    """
    expected = d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    out = config.decimal_to_str_currency(d)
    assert pattern.match(out), f"formatted string has incorrect shape: {out} (from {d})"

    parsed = config.str_to_decimal_currency(out)
    assert parsed == expected, (
        f"roundtrip mismatch: {d} -> {out} -> {parsed} (expected {expected})"
    )


def test_decimal_to_currency_string_examples():
    assert config.decimal_to_str_currency(Decimal("100")) == "100.00"
    assert config.decimal_to_str_currency(Decimal("1.5")) == "1.50"
    assert config.decimal_to_str_currency(Decimal("0")) == "0.00"
    assert config.decimal_to_str_currency(Decimal("-2.345")) == "-2.35"
    # parsing known strings
    assert config.str_to_decimal_currency("100.00") == Decimal("100.00")
    assert config.str_to_decimal_currency("-2.35") == Decimal("-2.35")
