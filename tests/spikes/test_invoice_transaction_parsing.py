"""Spike tests: parsing beancount transactions and mapping to Invoice model.

Validates that:
- Beancount transactions with invoice metadata parse correctly via load_string
- Transaction metadata (invoice_id, customer_id, due_at, etc.) round-trips
- Postings are accessible with correct account names, amounts, and currencies
- JSON sidecar files load and map to InvoiceLine instances
- Invoice totals auto-compute from lines
- Edge cases: missing sidecar, missing customer_id, multiple invoices
"""
import json
import textwrap
from decimal import Decimal
from pathlib import Path

import pytest
from beancount.loader import load_string

from ledger.beancount_spike import (
    extract_transaction_entries,
    map_transaction_to_invoice,
)
from ledger.models import Invoice, InvoiceLine


# -- Helpers --

# Accounts must be declared for load_string to avoid validation errors.
# This prefix is prepended to transaction snippets in tests.
ACCOUNT_PREAMBLE = textwrap.dedent("""\
    2020-01-01 open Assets:Receivable:ACME
    2020-01-01 open Income:Services
    2020-01-01 open Liabilities:VAT
""")


def _parse_invoice_snippet(snippet: str):
    """Parse a beancount snippet with account preamble, return (entries, errors)."""
    content = ACCOUNT_PREAMBLE + "\n" + textwrap.dedent(snippet)
    entries, errors, _ = load_string(content)
    return entries, errors


def _write_sidecar(tmp_path: Path, filename: str, data: dict) -> Path:
    """Write a JSON sidecar file and return its path."""
    p = tmp_path / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data))
    return p


# -- Tests: raw transaction parsing --


class TestTransactionParsing:
    """Verify beancount parses invoice transactions and exposes expected fields."""

    INVOICE_SNIPPET = """\
        2026-03-01 * "Invoice INV-0001"
          invoice_id: 1
          customer_id: 42
          due_at: 2026-03-31
          invoice_data: "invoices/data/inv-0001.json"
          Assets:Receivable:ACME        1250.00 SEK
          Income:Services              -1000.00 SEK
          Liabilities:VAT               -250.00 SEK
    """

    def test_transaction_parses_without_errors(self):
        entries, errors = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        assert not errors

    def test_transaction_entry_type(self):
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        txns = extract_transaction_entries(entries)
        assert len(txns) == 1
        assert txns[0].__class__.__name__ == "Transaction"

    def test_narration(self):
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        txn = extract_transaction_entries(entries)[0]
        assert txn.narration == "Invoice INV-0001"

    def test_metadata_types(self):
        """Beancount coerces metadata values: ints become Decimal, dates become date."""
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        txn = extract_transaction_entries(entries)[0]
        meta = txn.meta
        assert meta["invoice_id"] == Decimal("1")
        assert meta["customer_id"] == Decimal("42")
        assert str(meta["due_at"]) == "2026-03-31"
        assert meta["invoice_data"] == "invoices/data/inv-0001.json"

    def test_postings(self):
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        txn = extract_transaction_entries(entries)[0]
        assert len(txn.postings) == 3

        receivable = txn.postings[0]
        assert receivable.account == "Assets:Receivable:ACME"
        assert receivable.units.number == Decimal("1250.00")
        assert receivable.units.currency == "SEK"

        income = txn.postings[1]
        assert income.account == "Income:Services"
        assert income.units.number == Decimal("-1000.00")

        vat = txn.postings[2]
        assert vat.account == "Liabilities:VAT"
        assert vat.units.number == Decimal("-250.00")

    def test_date(self):
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        txn = extract_transaction_entries(entries)[0]
        assert str(txn.date) == "2026-03-01"


# -- Tests: mapping transaction to Invoice model --


class TestMapTransactionToInvoice:
    """Verify map_transaction_to_invoice produces correct Invoice instances."""

    INVOICE_SNIPPET = """\
        2026-03-15 * "Invoice INV-0005"
          invoice_id: 5
          customer_id: 10
          creditor_id: 3
          due_at: 2026-04-15
          status: "sent"
          invoice_data: "inv-0005.json"
          Assets:Receivable:ACME        2500.00 SEK
          Income:Services              -2000.00 SEK
          Liabilities:VAT               -500.00 SEK
    """

    SIDECAR_DATA = {
        "invoice_id": 5,
        "lines": [
            {
                "description": "Consulting",
                "quantity": "2",
                "unit_price": "1000.00",
                "vat_rate": "25",
            },
        ],
    }

    def test_basic_mapping_with_sidecar(self, tmp_path):
        entries, errors = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        assert not errors
        _write_sidecar(tmp_path, "inv-0005.json", self.SIDECAR_DATA)

        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn, sidecar_dir=tmp_path)

        assert isinstance(inv, Invoice)
        assert inv.id == 5
        assert inv.customer_id == 10
        assert inv.creditor_id == 3
        assert inv.status == "sent"
        assert inv.description == "Invoice INV-0005"
        assert inv.currency == "SEK"

    def test_dates_are_coerced(self, tmp_path):
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        _write_sidecar(tmp_path, "inv-0005.json", self.SIDECAR_DATA)

        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn, sidecar_dir=tmp_path)

        assert inv.created_at is not None
        assert inv.created_at.year == 2026
        assert inv.created_at.month == 3
        assert inv.created_at.day == 15
        assert inv.due_at is not None
        assert inv.due_at.year == 2026
        assert inv.due_at.month == 4

    def test_lines_from_sidecar(self, tmp_path):
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        _write_sidecar(tmp_path, "inv-0005.json", self.SIDECAR_DATA)

        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn, sidecar_dir=tmp_path)

        assert len(inv.lines) == 1
        line = inv.lines[0]
        assert isinstance(line, InvoiceLine)
        assert line.description == "Consulting"
        assert line.quantity == Decimal("2")
        assert line.unit_price == Decimal("1000.00")
        assert line.vat_rate == Decimal("25")

    def test_totals_auto_computed(self, tmp_path):
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        _write_sidecar(tmp_path, "inv-0005.json", self.SIDECAR_DATA)

        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn, sidecar_dir=tmp_path)

        # 2 * 1000 = 2000 net, 25% vat = 500, total = 2500
        assert inv.subtotal == Decimal("2000.00")
        assert inv.total_vat == Decimal("500.00")
        assert inv.total == Decimal("2500.00")

    def test_multiple_lines(self, tmp_path):
        sidecar = {
            "invoice_id": 5,
            "lines": [
                {
                    "description": "Consulting",
                    "quantity": "1",
                    "unit_price": "1000.00",
                    "vat_rate": "25",
                },
                {
                    "description": "Travel expenses",
                    "quantity": "1",
                    "unit_price": "500.00",
                    "vat_rate": "0",
                },
            ],
        }
        entries, _ = _parse_invoice_snippet(self.INVOICE_SNIPPET)
        _write_sidecar(tmp_path, "inv-0005.json", sidecar)

        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn, sidecar_dir=tmp_path)

        assert len(inv.lines) == 2
        # 1000 * 1.25 + 500 * 1.0 = 1750
        assert inv.subtotal == Decimal("1500.00")
        assert inv.total_vat == Decimal("250.00")
        assert inv.total == Decimal("1750.00")

    def test_currency_from_postings(self, tmp_path):
        snippet = """\
            2026-03-01 * "Invoice INV-0010"
              invoice_id: 10
              customer_id: 1
              invoice_data: "inv-0010.json"
              Assets:Receivable:ACME        1000.00 EUR
              Income:Services              -1000.00 EUR
        """
        sidecar = {
            "invoice_id": 10,
            "lines": [
                {"description": "Work", "quantity": "1", "unit_price": "1000.00", "vat_rate": "0"}
            ],
        }
        # Need EUR accounts
        content = textwrap.dedent("""\
            2020-01-01 open Assets:Receivable:ACME
            2020-01-01 open Income:Services
        """) + "\n" + textwrap.dedent(snippet)
        entries, errors, _ = load_string(content)
        assert not errors
        _write_sidecar(tmp_path, "inv-0010.json", sidecar)

        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn, sidecar_dir=tmp_path)
        assert inv.currency == "EUR"


# -- Tests: edge cases --


class TestInvoiceMappingEdgeCases:

    def test_missing_customer_id_raises(self):
        snippet = """\
            2026-03-01 * "Invoice INV-0099"
              invoice_id: 99
              Assets:Receivable:ACME        100.00 SEK
              Income:Services              -100.00 SEK
        """
        entries, _ = _parse_invoice_snippet(snippet)
        txn = extract_transaction_entries(entries)[0]
        with pytest.raises(ValueError, match="Missing customer_id"):
            map_transaction_to_invoice(txn)

    def test_missing_sidecar_produces_empty_lines(self, tmp_path):
        """When sidecar file doesn't exist, invoice has no lines."""
        snippet = """\
            2026-03-01 * "Invoice INV-0099"
              invoice_id: 99
              customer_id: 1
              invoice_data: "nonexistent.json"
              Assets:Receivable:ACME        100.00 SEK
              Income:Services              -100.00 SEK
        """
        entries, _ = _parse_invoice_snippet(snippet)
        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn, sidecar_dir=tmp_path)
        assert inv.lines == []
        assert inv.subtotal == Decimal("0")
        assert inv.total == Decimal("0")

    def test_no_invoice_data_meta_produces_empty_lines(self):
        """When invoice_data metadata is absent, invoice has no lines."""
        snippet = """\
            2026-03-01 * "Invoice INV-0099"
              invoice_id: 99
              customer_id: 1
              Assets:Receivable:ACME        100.00 SEK
              Income:Services              -100.00 SEK
        """
        entries, _ = _parse_invoice_snippet(snippet)
        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn)
        assert inv.lines == []

    def test_status_defaults_to_draft(self):
        snippet = """\
            2026-03-01 * "Invoice INV-0099"
              invoice_id: 99
              customer_id: 1
              Assets:Receivable:ACME        100.00 SEK
              Income:Services              -100.00 SEK
        """
        entries, _ = _parse_invoice_snippet(snippet)
        txn = extract_transaction_entries(entries)[0]
        inv = map_transaction_to_invoice(txn)
        assert inv.status == "draft"

    def test_multiple_invoices_in_one_file(self, tmp_path):
        snippet = """\
            2026-03-01 * "Invoice INV-0001"
              invoice_id: 1
              customer_id: 10
              invoice_data: "inv-0001.json"
              Assets:Receivable:ACME        100.00 SEK
              Income:Services              -100.00 SEK

            2026-03-15 * "Invoice INV-0002"
              invoice_id: 2
              customer_id: 20
              invoice_data: "inv-0002.json"
              Assets:Receivable:ACME        200.00 SEK
              Income:Services              -200.00 SEK
        """
        for i, (iid, amt) in enumerate([(1, "100.00"), (2, "200.00")], start=1):
            _write_sidecar(tmp_path, f"inv-000{i}.json", {
                "invoice_id": i,
                "lines": [
                    {"description": f"Service {i}", "quantity": "1", "unit_price": amt, "vat_rate": "0"}
                ],
            })

        entries, errors = _parse_invoice_snippet(snippet)
        assert not errors
        txns = extract_transaction_entries(entries)
        assert len(txns) == 2

        inv1 = map_transaction_to_invoice(txns[0], sidecar_dir=tmp_path)
        inv2 = map_transaction_to_invoice(txns[1], sidecar_dir=tmp_path)
        assert inv1.id == 1
        assert inv1.customer_id == 10
        assert inv2.id == 2
        assert inv2.customer_id == 20
