from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any


def dt_to_iso_utc(dt: datetime) -> str:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def iso_to_dt(s: str) -> datetime:
    # Accept ISO strings and return tz-aware UTC datetime
    if s is None:
        return None
    # Use fromisoformat then ensure UTC
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def decimal_to_str(d: Decimal) -> str:
    if d is None:
        return None
    # Culture-invariant string representation
    return format(d, 'f')


def str_to_decimal(s: Any) -> Decimal:
    if s is None:
        return None
    if isinstance(s, Decimal):
        return s
    return Decimal(str(s))


# Exported helpers for models' json encoders
JSON_ENCODERS = {
    datetime: dt_to_iso_utc,
    Decimal: decimal_to_str,
}


def _serialize_value(v):
    if v is None:
        return None
    if isinstance(v, Decimal):
        return decimal_to_str(v)
    if isinstance(v, datetime):
        return dt_to_iso_utc(v)
    if isinstance(v, dict):
        return {k: _serialize_value(val) for k, val in v.items()}
    if isinstance(v, (list, tuple)):
        return [_serialize_value(x) for x in v]
    # Fallback: return as-is
    return v


def dump_model(m):
    """Return a JSON-serializable dict for a pydantic model or plain mapping.

    This converts Decimal and datetime values to invariant strings.
    """
    try:
        data = m.model_dump()  # pydantic model
    except Exception:
        data = dict(m)
    return _serialize_value(data)
