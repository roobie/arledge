"""Small spike helpers for experimenting with beancount parsing and mapping.

This module provides lightweight helpers used by tests/spikes to validate that
beancount `custom` directives and transactions round-trip their metadata via
the beancount loader/parser APIs and can be mapped to our Pydantic models.

This is intentionally small and dependency-light; its purpose is to capture the
parsing/mapping approach for the BEANCOUNT replacement plan.
"""
from __future__ import annotations
import json
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Tuple

from . import models
from . import config


def extract_custom_entries_from_loader_entries(entries: List[Any]) -> List[Any]:
    """Return entries that look like beancount Custom entries.

    We avoid importing beancount types directly to keep this helper simple and
    tolerant across beancount versions. We identify Custom entries by their
    class name being "Custom".
    """
    return [e for e in entries if e.__class__.__name__ == "Custom"]


def entry_meta_map(entry: Any) -> Dict[str, Any]:
    """Return the meta mapping for a beancount entry in a tolerant way.

    Most beancount entry objects expose a `meta` attribute which is a mapping
    of metadata keys to values. This helper returns that mapping or an empty
    dict if not present.
    """
    return getattr(entry, "meta", {}) or {}


def detect_entry_title(entry: Any) -> str | None:
    """Attempt to find a human-readable title/name for a Custom entry.

    Different beancount versions/entry shapes may store the visible text in
    different attributes (e.g. `payee`, `what`, `name`, `label`). Try a few
    common attribute names and fall back to scanning string attributes.
    """
    # Common attribute candidates
    for attr in ("payee", "what", "name", "label", "narration", "description"):
        val = getattr(entry, attr, None)
        if isinstance(val, str) and val.strip():
            return val.strip()

    # Fallback: try entry.values (common in beancount Custom entries)
    vals = getattr(entry, "values", None)
    if vals:
        try:
            first = vals[0]
            # ValueType objects often expose a `value` attribute
            v = getattr(first, "value", None)
            if isinstance(v, str) and v.strip():
                return v.strip()
            # Some versions may expose the raw value directly
            if isinstance(first, str) and first.strip():
                return first.strip()
        except Exception:
            pass

    # Last resort: inspect __dict__-like items if available
    try:
        for k, v in vars(entry).items():
            if isinstance(v, str) and v.strip():
                return v.strip()
    except TypeError:
        # vars() not supported for this object
        pass
    return None


def map_custom_entry_to_dict(entry: Any) -> Dict[str, Any]:
    """Map a Custom entry into a plain dict containing the detected title and meta.

    This is intentionally conservative: it returns the metadata dictionary and a
    detected title (if any). Higher-level mapping to Pydantic models can be
    implemented in application code once the preferred fields are settled.
    """
    return {"title": detect_entry_title(entry), "meta": entry_meta_map(entry)}


# Deterministic mappers


def coerce_int(v: Any) -> int | None:
    if v is None:
        return None
    try:
        return int(v)
    except Exception:
        return None


def coerce_bool(v: Any) -> bool | None:
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    sval = str(v).lower()
    if sval in ("1", "true", "yes", "on"):
        return True
    if sval in ("0", "false", "no", "off"):
        return False
    return None


def coerce_decimal(v: Any) -> 'Decimal | None':
    from decimal import Decimal
    if v is None:
        return None
    # Handle floats carefully to avoid binary float artifacts
    if isinstance(v, float):
        try:
            return Decimal(str(v))
        except Exception:
            return None
    try:
        return Decimal(v)
    except Exception:
        try:
            return Decimal(str(v))
        except Exception:
            return None


def coerce_date_to_dt(v: Any):
    """Coerce a beancount date (datetime.date or ISO string) to a timezone-aware UTC datetime."""
    from datetime import datetime, timezone, date
    if v is None:
        return None
    if isinstance(v, datetime):
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)
    if isinstance(v, date):
        return datetime(v.year, v.month, v.day, tzinfo=timezone.utc)
    if isinstance(v, str):
        try:
            return config.iso_to_dt(v)
        except Exception:
            return None
    return None


def map_custom_to_customer(entry: Any) -> models.Customer:
    """Map a beancount Custom entry into a models.Customer instance.

    The mapping rules:
      - title/name: use detected title (payee/what/name) as Customer.name (required)
      - customer_id: meta.customer_id coerced to int -> mapped to id
      - email/address: mapped from meta keys if present

    Raises ValueError if required fields (name) are missing or invalid.
    """
    meta = entry_meta_map(entry)
    title = detect_entry_title(entry)
    if not title:
        raise ValueError("Missing title/name for customer entry")
    cid = coerce_int(meta.get("customer_id"))
    data = {
        "id": cid,
        "name": title,
        "email": meta.get("email"),
        "address": meta.get("address"),
    }
    # Use Pydantic model validation to coerce/validate datetimes etc.
    return models.Customer.model_validate(data)


def map_custom_to_creditor(entry: Any) -> models.Creditor:
    """Map a beancount Custom entry into a models.Creditor instance.

    Maps typical meta: creditor_id -> id, email, address, phone, tax_id, payment_instructions, default_currency.
    Uses entry date as created_at when available.
    """
    meta = entry_meta_map(entry)
    title = detect_entry_title(entry)
    if not title:
        raise ValueError("Missing title/name for creditor entry")
    cid = coerce_int(meta.get("creditor_id"))
    created = coerce_date_to_dt(getattr(entry, "date", None) or meta.get("created_at"))
    data = {
        "id": cid,
        "name": title,
        "email": meta.get("email"),
        "address": meta.get("address"),
        "phone": meta.get("phone"),
        "tax_id": meta.get("tax_id"),
        "payment_instructions": meta.get("payment_instructions"),
        "default_currency": meta.get("default_currency"),
        "created_at": created,
    }
    # Remove None values so model defaults are applied where appropriate
    clean = {k: v for k, v in data.items() if v is not None}
    return models.Creditor.model_validate(clean)


def map_custom_to_payment_account(entry: Any) -> models.PaymentAccount:
    """Map a beancount Custom entry into a models.PaymentAccount instance.

    Expected meta: creditor_id, type, label, identifier, bank_name, currency, is_default
    """
    meta = entry_meta_map(entry)
    # PaymentAccount requires creditor_id and type
    creditor_id = coerce_int(meta.get("creditor_id"))
    ptype = meta.get("type") or meta.get("account_type")
    if creditor_id is None or not ptype:
        raise ValueError("Missing creditor_id or type for payment account")
    is_default = coerce_bool(meta.get("is_default")) or False
    created = coerce_date_to_dt(getattr(entry, "date", None) or meta.get("created_at"))
    data = {
        "creditor_id": creditor_id,
        "type": ptype,
        "label": meta.get("label"),
        "identifier": meta.get("identifier"),
        "bank_name": meta.get("bank_name") or meta.get("bank"),
        "currency": meta.get("currency"),
        "beancount_account": meta.get("beancount_account"),
        "is_default": is_default,
        "metadata": {k: v for k, v in meta.items() if k not in ("creditor_id", "type", "label", "identifier", "bank_name", "bank", "currency", "is_default", "beancount_account")},
        "created_at": created,
    }
    return models.PaymentAccount.model_validate(data)


def extract_transaction_entries(entries: List[Any]) -> List[Any]:
    """Return entries that are beancount Transaction entries."""
    return [e for e in entries if e.__class__.__name__ == "Transaction"]


def map_transaction_to_invoice(
    entry: Any,
    sidecar_dir: Path | None = None,
) -> models.Invoice:
    """Map a beancount Transaction entry into a models.Invoice instance.

    The transaction narration should match "Invoice INV-NNNN".
    Metadata fields: invoice_id, customer_id, due_at, invoice_data, creditor_id, status.
    Postings determine currency.
    Invoice lines are loaded from the JSON sidecar file referenced by invoice_data.

    Args:
        entry: A beancount Transaction entry.
        sidecar_dir: Base directory for resolving relative invoice_data paths.
                     If None, invoice_data is treated as an absolute or cwd-relative path.

    Raises:
        ValueError: If required metadata (customer_id) is missing or sidecar cannot be loaded.
    """
    meta = entry_meta_map(entry)

    customer_id = coerce_int(meta.get("customer_id"))
    if customer_id is None:
        raise ValueError("Missing customer_id in invoice transaction metadata")

    invoice_id = coerce_int(meta.get("invoice_id"))
    creditor_id = coerce_int(meta.get("creditor_id"))
    status = meta.get("status", "draft")
    if not isinstance(status, str):
        status = str(status)

    created_at = coerce_date_to_dt(getattr(entry, "date", None))
    due_at = coerce_date_to_dt(meta.get("due_at"))

    # Determine currency from the first posting
    currency = "SEK"
    postings = getattr(entry, "postings", []) or []
    if postings and postings[0].units:
        currency = postings[0].units.currency

    # Load invoice lines from JSON sidecar
    lines: List[Dict[str, Any]] = []
    invoice_data_path = meta.get("invoice_data")
    if invoice_data_path and isinstance(invoice_data_path, str):
        path = Path(invoice_data_path)
        if sidecar_dir is not None:
            path = sidecar_dir / path
        if path.exists():
            with open(path) as f:
                sidecar = json.load(f)
            lines = sidecar.get("lines", [])

    narration = getattr(entry, "narration", None) or ""

    data = {
        "id": invoice_id,
        "customer_id": customer_id,
        "creditor_id": creditor_id,
        "status": status,
        "created_at": created_at,
        "due_at": due_at,
        "description": narration,
        "currency": currency,
        "lines": lines,
    }
    clean = {k: v for k, v in data.items() if v is not None}
    return models.Invoice.model_validate(clean)
