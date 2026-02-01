from datetime import datetime, timezone
from decimal import Decimal

from ledger import config


def test_dt_iso_roundtrip():
    dt = datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    s = config.dt_to_iso_utc(dt)
    assert s.endswith("Z")
    dt2 = config.iso_to_dt(s)
    assert dt2.tzinfo is not None


def test_dt_none():
    assert config.dt_to_iso_utc(None) is None
    assert config.iso_to_dt(None) is None


def test_decimal_serialization():
    assert config.decimal_to_str(Decimal('1.50')) == '1.50'
    assert config.decimal_to_str_currency(Decimal('1')) == '1.00'
    assert config.decimal_to_str_currency(Decimal('1.5')) == '1.50'
    assert config.decimal_to_str_currency(None) is None


def test_str_to_decimal():
    assert config.str_to_decimal('1.23') == Decimal('1.23')
    assert config.str_to_decimal(Decimal('2.00')) == Decimal('2.00')


def test_serialize_value_nested():
    data = {
        'a': Decimal('1.23'),
        'b': datetime(2020, 1, 1, tzinfo=timezone.utc),
        'c': [Decimal('2.00'), {'d': Decimal('3.00')}],
    }
    res = config._serialize_value(data)
    assert isinstance(res['a'], str)
    assert res['b'].endswith('Z')
    assert isinstance(res['c'][0], str)


def test_dump_model_with_mapping():
    m = {'x': Decimal('1.00'), 'y': datetime(2020, 1, 1, tzinfo=timezone.utc)}
    out = config.dump_model(m)
    assert out['x'] == '1.00'
    assert out['y'].endswith('Z')
