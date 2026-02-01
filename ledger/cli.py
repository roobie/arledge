import click
import json
from . import db


@click.group()
def cli():
    """Ledger CLI"""
    pass


@cli.command()
def init_db():
    """Initialize the database."""
    db.init_db()
    click.echo("Initialized database at ledger.db")


@cli.group()
def customer():
    """Customer commands"""
    pass


@customer.command("create")
@click.option("--name", prompt=True)
@click.option("--email", default="")
@click.option("--address", default="")
def customer_create(name, email, address):
    cid = db.create_customer(name, email, address)
    click.echo(f"Created customer {cid}")


@customer.command("list")
def customer_list():
    customers = db.list_customers()
    if not customers:
        click.echo("No customers")
        return
    for c in customers:
        click.echo(f"{c['id']}: {c['name']} <{c['email']}>")


@cli.group()
def creditor():
    """Creditor (us) commands"""
    pass


@creditor.command("create")
@click.option("--name", prompt=True)
@click.option("--address", default="")
@click.option("--email", default="")
@click.option("--phone", default="")
@click.option("--tax-id", default="")
@click.option("--payment-instructions", default="")
@click.option("--default-currency", default="SEK")
@click.option("--beancount-account", default="")
def creditor_create(name, address, email, phone, tax_id, payment_instructions, default_currency, beancount_account):
    cid = db.create_creditor(
        name,
        address=address or None,
        email=email or None,
        phone=phone or None,
        tax_id=tax_id or None,
        payment_instructions=payment_instructions or None,
        default_currency=default_currency,
        beancount_account=beancount_account or None,
    )
    click.echo(f"Created creditor {cid}")


@creditor.command("list")
def creditor_list():
    creds = db.list_creditors()
    if not creds:
        click.echo("No creditors")
        return
    for c in creds:
        click.echo(f"{c['id']}: {c['name']} ({c.get('default_currency','SEK')})")


@creditor.command("view")
@click.argument("creditor_id", type=int)
def creditor_view(creditor_id):
    c = db.get_creditor(creditor_id)
    if not c:
        click.echo("Creditor not found")
        return
    click.echo(f"Creditor {c['id']}: {c['name']}")
    click.echo(f"Address: {c.get('address')}")
    click.echo(f"Email: {c.get('email')}")
    click.echo(f"Phone: {c.get('phone')}")
    click.echo(f"Tax ID: {c.get('tax_id')}")
    click.echo(f"Default currency: {c.get('default_currency')}")
    click.echo(f"Beancount account: {c.get('beancount_account')}")


@creditor.group()
def account():
    """Creditor inbound payment accounts"""
    pass


@account.command("create")
@click.option("--creditor-id", required=True, type=int)
@click.option("--type", "acct_type", required=True, help="bank|paypal|card|other")
@click.option("--label", default="")
@click.option("--identifier", default="")
@click.option("--bank-name", default="")
@click.option("--currency", default="SEK")
@click.option("--beancount-account", default="")
@click.option("--default/--no-default", default=False)
@click.option("--metadata", default="", help="JSON string for provider-specific metadata")
def account_create(creditor_id, acct_type, label, identifier, bank_name, currency, beancount_account, default, metadata):
    try:
        meta = json.loads(metadata) if metadata else {}
    except Exception:
        click.echo("metadata must be valid JSON")
        return
    pa_id = db.create_payment_account(
        creditor_id,
        acct_type,
        label=label or None,
        identifier=identifier or None,
        bank_name=bank_name or None,
        currency=currency or None,
        beancount_account=beancount_account or None,
        is_default=bool(default),
        metadata=meta,
    )
    click.echo(f"Created payment account {pa_id} for creditor {creditor_id}")


@account.command("list")
@click.option("--creditor-id", type=int, default=None)
def account_list(creditor_id):
    rows = db.list_payment_accounts(creditor_id=creditor_id)
    if not rows:
        click.echo("No payment accounts")
        return
    for r in rows:
        default_mark = "(default)" if r.get("is_default") else ""
        click.echo(f"{r['id']}: creditor {r['creditor_id']} - {r['type']} {r.get('label')} {default_mark}")


@cli.group()
def invoice():
    """Invoice commands"""
    pass


@invoice.command("create")
@click.option("--customer-id", required=True, type=int)
@click.option(
    "--line",
    "lines",
    multiple=True,
    help="Line in format desc,qty,unit_price,vat_rate. Repeatable.",
)
@click.option("--due-days", type=int, default=30)
@click.option("--description", default="")
@click.option("--creditor-id", type=int, default=None, help="Optional creditor id to put on invoice")
def invoice_create(customer_id, lines, due_days, description, creditor_id):
    if not lines:
        click.echo("At least one --line is required")
        return
    parsed = []
    for l in lines:
        parts = [p.strip() for p in l.split(",")]
        if len(parts) < 4:
            click.echo(f"Bad line format: {l}")
            return
        desc, qty, unit_price, vat = parts[0], parts[1], parts[2], parts[3]
        parsed.append(
            {
                "description": desc,
                "quantity": qty,
                "unit_price": unit_price,
                "vat_rate": vat,
            }
        )
    invoice_id = db.create_invoice(
        customer_id,
        parsed,
        status="issued",
        due_days=due_days,
        description=description,
        creditor_id=creditor_id,
    )
    click.echo(
        f"Created invoice {db.format_invoice_number(invoice_id)} (id {invoice_id})"
    )


@invoice.command("list")
def invoice_list():
    invs = db.list_invoices()
    if not invs:
        click.echo("No invoices")
        return
    for inv in invs:
        click.echo(
            f"{db.format_invoice_number(inv['id'])} - customer {inv['customer_id']} - {inv['status']} - {inv['created_at']}"
        )


@invoice.command("view")
@click.argument("invoice_id", type=int)
def invoice_view(invoice_id):
    inv = db.get_invoice(invoice_id)
    if not inv:
        click.echo("Invoice not found")
        return
    click.echo(f"Invoice: {db.format_invoice_number(inv['id'])}")
    click.echo(f"Customer ID: {inv['customer_id']}")
    click.echo(f"Status: {inv['status']}")
    click.echo(f"Created: {inv['created_at']}")
    click.echo(f"Due: {inv['due_at']}")
    click.echo("Lines:")
    for l in inv["lines"]:
        click.echo(
            f" - {l['description']}: {l['quantity']} x {l['unit_price']:.2f} VAT {l['vat_rate']}% -> line total {l['line_total']:.2f}"
        )
    click.echo(f"Subtotal: {inv['subtotal']:.2f}")
    click.echo(f"Total VAT: {inv['total_vat']:.2f}")
    click.echo(f"Total: {inv['total']:.2f}")


@invoice.command("export")
@click.argument("invoice_id", type=int)
@click.option("--format", "fmt", type=click.Choice(["json", "text"]), default="json")
@click.option("--path", default=None)
def invoice_export(invoice_id, fmt, path):
    if fmt == "json":
        out = db.export_invoice_json(invoice_id, path=path)
        if not out:
            click.echo("Invoice not found")
            return
        click.echo(f"Exported to {out}")
    else:
        click.echo("Text export not implemented yet")


@cli.command()
def instructions():
    """Print instructions for agentic systems on interacting with the CLI."""
    text = f"""Instructions for agentic systems interacting with the ledger CLI

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
    click.echo(text)
