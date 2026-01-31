import click
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

@customer.command('create')
@click.option('--name', prompt=True)
@click.option('--email', default='')
@click.option('--address', default='')
def customer_create(name,email,address):
    cid = db.create_customer(name,email,address)
    click.echo(f"Created customer {cid}")

@customer.command('list')
def customer_list():
    customers = db.list_customers()
    if not customers:
        click.echo("No customers")
        return
    for c in customers:
        click.echo(f"{c['id']}: {c['name']} <{c['email']}>")
        
@cli.group()
def invoice():
    """Invoice commands"""
    pass

@invoice.command('create')
@click.option('--customer-id', required=True, type=int)
@click.option('--line', 'lines', multiple=True, help="Line in format desc,qty,unit_price,vat_rate. Repeatable.")
@click.option('--due-days', type=int, default=30)
@click.option('--description', default='')
def invoice_create(customer_id, lines, due_days, description):
    if not lines:
        click.echo("At least one --line is required")
        return
    parsed=[]
    for l in lines:
        parts = [p.strip() for p in l.split(',')]
        if len(parts) < 4:
            click.echo(f"Bad line format: {l}")
            return
        desc, qty, unit_price, vat = parts[0], parts[1], parts[2], parts[3]
        parsed.append({'description':desc, 'quantity':qty, 'unit_price':unit_price, 'vat_rate':vat})
    invoice_id = db.create_invoice(customer_id, parsed, status='issued', due_days=due_days, description=description)
    click.echo(f"Created invoice {db.format_invoice_number(invoice_id)} (id {invoice_id})")

@invoice.command('list')
def invoice_list():
    invs = db.list_invoices()
    if not invs:
        click.echo("No invoices")
        return
    for inv in invs:
        click.echo(f"{db.format_invoice_number(inv['id'])} - customer {inv['customer_id']} - {inv['status']} - {inv['created_at']}")
        
@invoice.command('view')
@click.argument('invoice_id', type=int)
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
    for l in inv['lines']:
        click.echo(f" - {l['description']}: {l['quantity']} x {l['unit_price']:.2f} VAT {l['vat_rate']}% -> line total {l['line_total']:.2f}")
    click.echo(f"Subtotal: {inv['subtotal']:.2f}")
    click.echo(f"Total VAT: {inv['total_vat']:.2f}")
    click.echo(f"Total: {inv['total']:.2f}")

@invoice.command('export')
@click.argument('invoice_id', type=int)
@click.option('--format', 'fmt', type=click.Choice(['json','text']), default='json')
@click.option('--path', default=None)
def invoice_export(invoice_id, fmt, path):
    if fmt == 'json':
        out = db.export_invoice_json(invoice_id, path=path)
        if not out:
            click.echo("Invoice not found")
            return
        click.echo(f"Exported to {out}")
    else:
        click.echo("Text export not implemented yet")
