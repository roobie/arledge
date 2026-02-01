import click
import json
import sys
from . import db, models, config


@click.group()
def cli():
    """Ledger CLI"""
    pass


@cli.command()
def init_db():
    """Initialize the database."""
    db.init_db()
    click.echo("Initialized database at ledger.db", err=True)


@cli.group()
def customer():
    """Customer commands"""
    pass


@customer.command("create")
@click.option("--model", "model_json", default="", help='JSON object for Customer')
@click.option("--model-file", "model_file", type=click.Path(exists=True), default=None, help='Path to JSON file containing Customer')
def customer_create(model_json, model_file):
    """Create a customer from a JSON model or file. Prints created customer JSON to stdout."""
    if model_file:
        try:
            with open(model_file, "r", encoding="utf-8") as f:
                model_json = f.read()
        except Exception as e:
            click.echo(f"Failed to read model file: {e}", err=True)
            sys.exit(2)
    if not model_json:
        click.echo("Provide --model JSON or --model-file", err=True)
        sys.exit(2)
    try:
        c = models.Customer.model_validate_json(model_json)
    except Exception as e:
        click.echo(f"Invalid customer JSON: {e}", err=True)
        sys.exit(2)
    created = db.create_customer(c)
    # Actionable output: created customer as JSON on stdout
    click.echo(json.dumps(config.dump_model(created), ensure_ascii=False))


@customer.command("list")
def customer_list():
    customers = db.list_customers()
    if not customers:
        click.echo("No customers", err=True)
        return
    out = [config.dump_model(c) for c in customers]
    click.echo(json.dumps(out, ensure_ascii=False))


@cli.group()
def creditor():
    """Creditor (us) commands"""
    pass


@creditor.command("create")
@click.option("--model", "model_json", default="", help='JSON object for Creditor')
@click.option("--model-file", "model_file", type=click.Path(exists=True), default=None, help='Path to JSON file containing Creditor')
def creditor_create(model_json, model_file):
    """Create a creditor from a JSON model or file. Prints created creditor JSON to stdout."""
    if model_file:
        try:
            with open(model_file, "r", encoding="utf-8") as f:
                model_json = f.read()
        except Exception as e:
            click.echo(f"Failed to read model file: {e}", err=True)
            sys.exit(2)
    if not model_json:
        click.echo("Provide --model JSON or --model-file", err=True)
        sys.exit(2)
    try:
        cred = models.Creditor.model_validate_json(model_json)
    except Exception as e:
        click.echo(f"Invalid creditor JSON: {e}", err=True)
        sys.exit(2)
    created = db.create_creditor(cred)
    click.echo(json.dumps(config.dump_model(created), ensure_ascii=False))


@creditor.command("list")
def creditor_list():
    creds = db.list_creditors()
    if not creds:
        click.echo("No creditors", err=True)
        return
    out = [config.dump_model(c) for c in creds]
    click.echo(json.dumps(out, ensure_ascii=False))


@creditor.command("view")
@click.argument("creditor_id", type=int)
def creditor_view(creditor_id):
    c = db.get_creditor(creditor_id)
    if not c:
        click.echo("Creditor not found", err=True)
        sys.exit(2)
    click.echo(json.dumps(config.dump_model(c), ensure_ascii=False))


@creditor.group()
def account():
    """Creditor inbound payment accounts"""
    pass


@account.command("create")
@click.option("--model", "model_json", default="", help='JSON object for PaymentAccount')
@click.option("--model-file", "model_file", type=click.Path(exists=True), default=None, help='Path to JSON file containing PaymentAccount')
def account_create(model_json, model_file):
    """Create a payment account from a JSON model or file. Prints created account JSON to stdout."""
    if model_file:
        try:
            with open(model_file, "r", encoding="utf-8") as f:
                model_json = f.read()
        except Exception as e:
            click.echo(f"Failed to read model file: {e}", err=True)
            sys.exit(2)
    if not model_json:
        click.echo("Provide --model JSON or --model-file", err=True)
        sys.exit(2)
    try:
        pa = models.PaymentAccount.model_validate_json(model_json)
    except Exception as e:
        click.echo(f"Invalid payment account JSON: {e}", err=True)
        sys.exit(2)
    created = db.create_payment_account(pa)
    click.echo(json.dumps(config.dump_model(created), ensure_ascii=False))


@account.command("list")
@click.option("--creditor-id", type=int, default=None)
def account_list(creditor_id):
    rows = db.list_payment_accounts(creditor_id=creditor_id)
    if not rows:
        click.echo("No payment accounts", err=True)
        return
    out = [config.dump_model(r) for r in rows]
    click.echo(json.dumps(out, ensure_ascii=False))


@cli.group()
def invoice():
    """Invoice commands"""
    pass


@invoice.command("create")
@click.option("--model", "model_json", default="", help='JSON object for Invoice')
@click.option("--model-file", "model_file", type=click.Path(exists=True), default=None, help='Path to JSON file containing Invoice')
def invoice_create(model_json, model_file):
    """Create an invoice from a JSON model or file. Prints created invoice JSON to stdout."""
    if model_file:
        try:
            with open(model_file, "r", encoding="utf-8") as f:
                model_json = f.read()
        except Exception as e:
            click.echo(f"Failed to read model file: {e}", err=True)
            sys.exit(2)
    if not model_json:
        click.echo("Provide --model JSON or --model-file", err=True)
        sys.exit(2)
    try:
        inv = models.Invoice.model_validate_json(model_json)
    except Exception as e:
        click.echo(f"Invalid invoice JSON: {e}", err=True)
        sys.exit(2)
    created = db.create_invoice(inv)
    # Include invoice id and invoice_number in actionable JSON
    out = config.dump_model(created)
    out["invoice_number"] = db.format_invoice_number(created.id)
    click.echo(json.dumps(out, ensure_ascii=False))


@invoice.command("list")
def invoice_list():
    invs = db.list_invoices()
    if not invs:
        click.echo("No invoices", err=True)
        return
    out = [config.dump_model(inv) for inv in invs]
    click.echo(json.dumps(out, ensure_ascii=False))


@invoice.command("view")
@click.argument("invoice_id", type=int)
def invoice_view(invoice_id):
    inv = db.get_invoice(invoice_id)
    if not inv:
        click.echo("Invoice not found", err=True)
        sys.exit(2)
    click.echo(json.dumps(config.dump_model(inv), ensure_ascii=False))


@invoice.command("export")
@click.argument("invoice_id", type=int)
@click.option("--format", "fmt", type=click.Choice(["json", "text"]), default="json")
@click.option("--path", default=None)
def invoice_export(invoice_id, fmt, path):
    if fmt == "json":
        out = db.export_invoice_json(invoice_id, path=path)
        if not out:
            click.echo("Invoice not found", err=True)
            sys.exit(2)
        # actionable output: exported filepath on stdout
        click.echo(out)
    else:
        click.echo("Text export not implemented yet", err=True)
        sys.exit(2)


@cli.command()
def instructions():
    """Print instructions for agentic systems on interacting with the CLI."""
    text = """Instructions for agentic systems interacting with the ledger CLI

Initialization and basic commands:
- Initialize DB: python -m ledger init-db
- Create customer: python -m ledger customer create --name "Name" --email "email" --address "address"
- Create invoice: python -m ledger invoice create --customer-id <id> --line "desc,qty,unit_price,vat_rate" --line ...
  * VAT rates supported: 25, 12, 6, 0 (Sweden standard rates)
- List invoices: python -m ledger invoice list
- View invoice details: python -m ledger invoice view <id>
- Export invoice (machine-friendly JSON): python -m ledger invoice export <id> --format json --path <file>

Agent interaction guidelines:
- Prefer non-destructive reads before writes; confirm destructive actions with a human operator.
- Verify customer existence via `python -m ledger customer list` before creating invoices.
- Use JSON export for programmatic parsing; the JSON contains invoice_number (INV-0001...), lines, subtotal, total_vat, total.
- Monetary units: SEK. unit_price is specified in SEK as decimal (e.g., 199.99).
- Invoice numbers are sequential and deterministic based on DB id (INV-0001 for id=1).
- Logging: capture stdout/stderr and ledger.db after operations to record state changes.
- Exit codes: 0 on success, non-zero on error; parse outputs accordingly.

Best practices for automation:
- Run commands in an isolated environment to avoid concurrent DB writes.
- Acquire a lock on ledger.db when performing multiple dependent operations.
- When creating invoices, emit the JSON export immediately after creation to confirm final state.
"""
    click.echo(text, err=True)
