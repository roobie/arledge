"""Read-only beancount-backed store for arledge.

Provides functions mirroring the legacy DB read APIs but sourcing data from
beancount files and sidecar JSON files.

This module is intentionally read-only and uses beancount.loader.load_file to
parse ledger.beancount (which should include the includes/ files). It reuses
mapping helpers in src/arledge/beancount_spike.py to build Pydantic models.
"""
from __future__ import annotations
from typing import List, Optional
import json
from pathlib import Path

from . import config
from . import models
from .beancount_spike import (
    extract_custom_entries_from_loader_entries,
    map_custom_to_customer,
    map_custom_to_creditor,
    map_custom_to_payment_account,
    coerce_int,
)


def _load_ledger_entries() -> tuple[List[object], list, dict]:
    """Load the top-level ledger.beancount and return (entries, errors, options).

    The ledger file is resolved relative to config.get_basedir(). If there is no
    ledger.beancount file, return ([], [], {}).
    """
    base = config.get_basedir()
    ledger_file = base / "ledger.beancount"
    if not ledger_file.exists():
        return [], [], {}
    try:
        from beancount.loader import load_file

        entries, errors, options = load_file(str(ledger_file))
        return entries, errors, options
    except Exception:
        # Surface loader errors up to the caller via returned errors when possible
        # but avoid raising here; return empty and an error indicator
        return [], ["failed to load beancount ledger"], {}


def _entries_for_custom_type(custom_type: str) -> List[object]:
    entries, errors, opts = _load_ledger_entries()
    customs = extract_custom_entries_from_loader_entries(entries)
    # beancount Custom entries usually have a `type` attribute indicating the kind
    return [e for e in customs if getattr(e, "type", None) == custom_type]


# Customers

def list_customers() -> List[models.Customer]:
    es = _entries_for_custom_type("customer")
    res = []
    for e in es:
        try:
            res.append(map_custom_to_customer(e))
        except Exception:
            # skip entries that fail to map
            continue
    return res


def get_customer(customer_id: int) -> Optional[models.Customer]:
    for c in list_customers():
        if c.id == customer_id:
            return c
    return None


# Creditors

def list_creditors() -> List[models.Creditor]:
    """Return the latest mapping for each creditor id.

    If multiple custom entries for the same creditor_id exist, prefer the
    entry with the most recent date (or the later one in the ledger) so that
    updates appended to the include file are reflected.
    """
    es = _entries_for_custom_type("creditor")
    # Build mapping creditor_id -> entry (choose newest by date)
    latest: dict[int, object] = {}
    for e in es:
        try:
            meta = getattr(e, "meta", {}) or {}
            cid = coerce_int(meta.get("creditor_id"))
            if cid is None:
                # skip entries without id
                continue
            existing = latest.get(cid)
            if existing is None:
                latest[cid] = e
                continue
            # compare dates if available
            d_new = getattr(e, "date", None)
            d_old = getattr(existing, "date", None)
            # prefer entry with later date; if dates equal or missing prefer newer entry (e)
            if d_new is None:
                # keep existing
                continue
            if d_old is None or d_new >= d_old:
                latest[cid] = e
        except Exception:
            continue
    res: List[models.Creditor] = []
    for e in latest.values():
        try:
            res.append(map_custom_to_creditor(e))
        except Exception:
            continue
    # Sort by id ascending for determinism
    res.sort(key=lambda x: x.id or 0)
    return res


def get_creditor(creditor_id: int) -> Optional[models.Creditor]:
    for c in list_creditors():
        if c.id == creditor_id:
            return c
    return None


# Payment accounts

def list_payment_accounts(creditor_id: Optional[int] = None) -> List[models.PaymentAccount]:
    es = _entries_for_custom_type("payment_account")
    res = []
    for e in es:
        try:
            pa = map_custom_to_payment_account(e)
        except Exception:
            continue
        if creditor_id is not None and pa.creditor_id != creditor_id:
            continue
        res.append(pa)
    return res


# Invoices

def _load_invoice_sidecar(path_str: str) -> dict | None:
    base = config.get_basedir()
    p = Path(path_str)
    if not p.is_absolute():
        p = base / path_str
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def list_invoices() -> List[models.Invoice]:
    # Load ledger and search for Transaction entries with invoice_id in meta
    entries, errors, opts = _load_ledger_entries()
    result: List[models.Invoice] = []
    for e in entries:
        if e.__class__.__name__ == "Transaction":
            meta = getattr(e, "meta", {}) or {}
            inv_id = coerce_int(meta.get("invoice_id"))
            if inv_id is None:
                continue
            # build a minimal invoice mapping
            inv_data = {
                "id": inv_id,
                "customer_id": coerce_int(meta.get("customer_id")) or 0,
                "status": meta.get("status") or "draft",
                "created_at": None,
                "due_at": meta.get("due_at"),
                "description": getattr(e, "narration", None) or getattr(e, "description", None),
                "creditor_id": coerce_int(meta.get("creditor_id")),
                "currency": meta.get("currency") or "SEK",
                "lines": [],
            }
            # Load sidecar if present
            side = meta.get("invoice_data")
            if side:
                sc = _load_invoice_sidecar(side)
                if sc and isinstance(sc, dict):
                    inv_data["lines"] = sc.get("lines", [])
            try:
                inv = models.Invoice.model_validate(inv_data)
                result.append(inv)
            except Exception:
                continue
    # Sort by id descending to mimic DB ordering
    result.sort(key=lambda x: x.id or 0, reverse=True)
    return result


def get_invoice(invoice_id: int) -> Optional[models.Invoice]:
    for inv in list_invoices():
        if inv.id == invoice_id:
            return inv
    return None


def format_invoice_number(invoice_id: int) -> str:
    return f"INV-{invoice_id:04d}"


def export_invoice_json(invoice_id: int, path: Optional[str] = None) -> Optional[str]:
    inv = get_invoice(invoice_id)
    if not inv:
        return None
    data = config.dump_model(inv)
    data["invoice_number"] = format_invoice_number(inv.id)
    if path is None:
        path = f"invoice-{inv.id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path
