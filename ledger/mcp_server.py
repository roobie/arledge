"""Lightweight launcher for an MCP stdio server using the official `mcp` package.

This module keeps imports lazy so the rest of the CLI does not require the
`mcp` runtime unless the server command is invoked. It provides a simple
`start_mcp_stdio_server` function with a deterministic `dry_run` path useful
for unit tests.
"""

from __future__ import annotations
import sys
from typing import Optional


def start_mcp_stdio_server(
    name: Optional[str] = None, json_response: bool = True, dry_run: bool = False
):
    """Start an MCP stdio server using FastMCP.

    Parameters
    - name: Optional server name displayed in logs.
    - json_response: Hint for whether JSON responses are preferred (kept for API parity).
    - dry_run: If True, validate imports and configuration but do not block or start the server.
    """
    server_name = name or "Arledge MCP"
    if dry_run:
        print(
            f"MCP dry-run: name={server_name}, json_response={json_response}",
            file=sys.stderr,
        )
        return
    else:
        print(
            f"Starting MCP stdio server: name={server_name}, json_response={json_response}",
            file=sys.stderr,
        )

    try:
        # Lazy import the official FastMCP stdio implementation
        from mcp.server.fastmcp import FastMCP
    except Exception as e:
        print(f"Failed to import FastMCP from mcp package: {e}", file=sys.stderr)
        raise

    mcp = FastMCP(server_name)

    # Register a tiny health check tool so the server is minimally useful.
    @mcp.tool()
    def ping() -> str:  # pragma: no cover - trivial runtime helper
        """Health-check tool; returns the string 'pong'."""
        return "pong"

    # Lazy-import application modules to avoid introducing runtime deps
    from . import db, models, config

    @mcp.tool()
    def database_initialize() -> str:
        """Initialize the database (mirrors `ledger database initialize`)."""
        db.init_db()
        return "Initialized database at ledger.db"

    @mcp.tool()
    def customer_create(
        model: object | None = None,
        model_file: str | None = None,
        json_schema: bool = False,
    ):
        """Create a Customer.

        Accepts a decoded model (Pydantic model instance or dict) as `model` and
        lets the framework handle JSON decoding. If `model` is a dict it will be
        validated via `models.Customer.model_validate`. Alternatively, provide
        `model_file` to load JSON from disk.
        """
        if json_schema:
            return models.Customer.model_json_schema()

        model_obj = None
        if model is not None:
            # If framework passed a dict, validate it; if it's already a model, accept it
            if isinstance(model, dict):
                model_obj = models.Customer.model_validate(model)
            elif isinstance(model, models.Customer):
                model_obj = model
            else:
                # Try to coerce via model_validate (handles JSON-like inputs)
                model_obj = models.Customer.model_validate(model)
        elif model_file:
            try:
                with open(model_file, "r", encoding="utf-8") as f:
                    data = f.read()
            except Exception as e:
                raise RuntimeError(f"Failed to read model file: {e}")
            model_obj = models.Customer.model_validate_json(data)

        if model_obj is None:
            raise ValueError("Provide model (decoded) or model_file")

        created = db.create_customer(model_obj)
        return config.dump_model(created)

    @mcp.tool()
    def customer_list() -> list:
        """Return all customers as a list of JSON-serializable dicts."""
        customers = db.list_customers()
        return [config.dump_model(c) for c in customers]

    @mcp.tool()
    def creditor_create(
        model: object | None = None,
        model_file: str | None = None,
        json_schema: bool = False,
    ):
        """Create a Creditor from a decoded model or file; or return its JSON Schema."""
        if json_schema:
            return models.Creditor.model_json_schema()

        model_obj = None
        if model is not None:
            if isinstance(model, dict):
                model_obj = models.Creditor.model_validate(model)
            elif isinstance(model, models.Creditor):
                model_obj = model
            else:
                model_obj = models.Creditor.model_validate(model)
        elif model_file:
            try:
                with open(model_file, "r", encoding="utf-8") as f:
                    data = f.read()
            except Exception as e:
                raise RuntimeError(f"Failed to read model file: {e}")
            model_obj = models.Creditor.model_validate_json(data)

        if model_obj is None:
            raise ValueError("Provide model (decoded) or model_file")

        created = db.create_creditor(model_obj)
        return config.dump_model(created)

    @mcp.tool()
    def creditor_list() -> list:
        """Return all creditors as a list of JSON-serializable dicts."""
        creds = db.list_creditors()
        return [config.dump_model(c) for c in creds]

    @mcp.tool()
    def creditor_view(creditor_id: int):
        """Return a single creditor by id as a JSON-serializable dict."""
        c = db.get_creditor(creditor_id)
        if not c:
            raise ValueError("Creditor not found")
        return config.dump_model(c)

    @mcp.tool()
    def creditor_account_create(
        model: object | None = None,
        model_file: str | None = None,
        json_schema: bool = False,
    ):
        """Create a PaymentAccount from a decoded model or file; or return its JSON Schema."""
        if json_schema:
            return models.PaymentAccount.model_json_schema()

        model_obj = None
        if model is not None:
            if isinstance(model, dict):
                model_obj = models.PaymentAccount.model_validate(model)
            elif isinstance(model, models.PaymentAccount):
                model_obj = model
            else:
                model_obj = models.PaymentAccount.model_validate(model)
        elif model_file:
            try:
                with open(model_file, "r", encoding="utf-8") as f:
                    data = f.read()
            except Exception as e:
                raise RuntimeError(f"Failed to read model file: {e}")
            model_obj = models.PaymentAccount.model_validate_json(data)

        if model_obj is None:
            raise ValueError("Provide model (decoded) or model_file")

        created = db.create_payment_account(model_obj)
        return config.dump_model(created)

    @mcp.tool()
    def creditor_account_list(creditor_id: int | None = None) -> list:
        """List payment accounts; optionally filter by creditor_id."""
        rows = db.list_payment_accounts(creditor_id=creditor_id)
        return [config.dump_model(r) for r in rows]

    @mcp.tool()
    def invoice_create(
        model: object | None = None,
        model_file: str | None = None,
        json_schema: bool = False,
    ):
        """Create an Invoice from a decoded model or file; or return its JSON Schema."""
        if json_schema:
            return models.Invoice.model_json_schema()

        model_obj = None
        if model is not None:
            if isinstance(model, dict):
                model_obj = models.Invoice.model_validate(model)
            elif isinstance(model, models.Invoice):
                model_obj = model
            else:
                model_obj = models.Invoice.model_validate(model)
        elif model_file:
            try:
                with open(model_file, "r", encoding="utf-8") as f:
                    data = f.read()
            except Exception as e:
                raise RuntimeError(f"Failed to read model file: {e}")
            model_obj = models.Invoice.model_validate_json(data)

        if model_obj is None:
            raise ValueError("Provide model (decoded) or model_file")

        created = db.create_invoice(model_obj)
        out = config.dump_model(created)
        out["invoice_number"] = db.format_invoice_number(created.id)
        return out

    @mcp.tool()
    def invoice_list() -> list:
        """Return all invoices as a list of JSON-serializable dicts."""
        invs = db.list_invoices()
        return [config.dump_model(inv) for inv in invs]

    @mcp.tool()
    def invoice_view(invoice_id: int):
        """Return a single invoice by id as a JSON-serializable dict."""
        inv = db.get_invoice(invoice_id)
        if not inv:
            raise ValueError("Invoice not found")
        return config.dump_model(inv)

    @mcp.tool()
    def invoice_export(invoice_id: int, fmt: str = "json", path: str | None = None):
        """Export an invoice to JSON and return the exported file path."""
        if fmt != "json":
            raise ValueError("Only json export supported")
        out = db.export_invoice_json(invoice_id, path=path)
        if not out:
            raise ValueError("Invoice not found")
        return out

    @mcp.tool()
    def schema(name: str):
        """Return the Pydantic JSON Schema for a named model.

        Supported names: customer, creditor, account, payment-account, invoice, invoice-line
        """
        mapping = {
            "customer": models.Customer,
            "creditor": models.Creditor,
            "account": models.PaymentAccount,
            "payment-account": models.PaymentAccount,
            "invoice": models.Invoice,
            "invoice-line": getattr(models, "InvoiceLine", None),
        }
        if name not in mapping or mapping[name] is None:
            raise ValueError("Unknown schema name")
        return mapping[name].model_json_schema()

    @mcp.tool()
    def instructions():
        """Return brief agent-facing instructions describing CLI machine I/O conventions."""
        return (
            "Machine-actionable outputs are JSON on stdout. Use per-command model JSON or model_file. "
            "See CLI for full instructions."
        )

    print("✅ MCP stdio server has started", file=sys.stderr)
    # FastMCP.run() blocks, serving requests over stdin/stdout
    mcp.run()
