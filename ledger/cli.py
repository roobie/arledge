import click
import json
import sys
from . import db, models, config


@click.group()
def cli():
    """Ledger CLI

    Machine-actionable JSON is printed to stdout; human-facing messages
    and validation/file errors are printed to stderr. Validation and
    file-read errors exit with a non-zero code (the implementation
    currently uses ``sys.exit(2)`` for these error conditions).
    """
    pass


@cli.group()
def database():
    """Database commands"""
    pass


@database.command("initialize")
def initialize():
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
@click.option("--json-schema", "json_schema", is_flag=True, default=False, help='Print Pydantic JSON Schema for Customer and exit')
def customer_create(model_json, model_file, json_schema):
    """Create a customer from a JSON model or file. Prints created customer JSON to stdout."""
    if json_schema:
        click.echo(json.dumps(models.Customer.model_json_schema(), indent=2, ensure_ascii=False))
        return

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
@click.option("--json-schema", "json_schema", is_flag=True, default=False, help='Print Pydantic JSON Schema for Creditor and exit')
def creditor_create(model_json, model_file, json_schema):
    """Create a creditor from a JSON model or file. Prints created creditor JSON to stdout."""
    if json_schema:
        click.echo(json.dumps(models.Creditor.model_json_schema(), indent=2, ensure_ascii=False))
        return

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
@click.option("--json-schema", "json_schema", is_flag=True, default=False, help='Print Pydantic JSON Schema for PaymentAccount and exit')
def account_create(model_json, model_file, json_schema):
    """Create a payment account from a JSON model or file. Prints created account JSON to stdout."""
    if json_schema:
        click.echo(json.dumps(models.PaymentAccount.model_json_schema(), indent=2, ensure_ascii=False))
        return

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
@click.option("--json-schema", "json_schema", is_flag=True, default=False, help='Print Pydantic JSON Schema for Invoice and exit')
def invoice_create(model_json, model_file, json_schema):
    """Create an invoice from a JSON model or file. Prints created invoice JSON to stdout."""
    if json_schema:
        click.echo(json.dumps(models.Invoice.model_json_schema(), indent=2, ensure_ascii=False))
        return

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

Overview and machine I/O conventions:
- All machine-actionable outputs (created/listed models, schemas, export file paths) are printed to STDOUT as JSON or plain text.
- Human/informational messages, warnings and validation errors are printed to STDERR.
- Exit codes: `0` for success, non-zero for errors. Agents should check the exit code and parse STDOUT only on success.

How to provide model input (writes):
- Use `--model` to pass an inline JSON string, e.g.:
    `python -m ledger customer create --model '{"name":"ACME","email":"x@acme.test"}'`
- Or use `--model-file` to pass a path to a JSON file, e.g.:
    `python -m ledger customer create --model-file /tmp/customer.json`

How to discover JSON Schemas (important for agents):
- Per-command schema flag: add `--json-schema` to a create command to print that model's JSON Schema to STDOUT and exit.
    Example: `python -m ledger customer create --json-schema`
- Global schema command: `python -m ledger schema <name>` prints the named model's JSON Schema.
    Example: `python -m ledger schema customer`
    Supported names: `customer`, `creditor`, `account`, `payment-account`, `invoice`, `invoice-line`.

Common read operations (machine-friendly):
- List customers: `python -m ledger customer list`  # prints JSON array of customers to STDOUT
- View creditor: `python -m ledger creditor view <id>`  # prints Creditor JSON to STDOUT
- List payment accounts: `python -m ledger creditor account list [--creditor-id <id>]`
- Create invoice (write): use `--model` or `--model-file` with the `invoice create` command; created invoice JSON is printed to STDOUT and includes `invoice_number`.
- Export invoice JSON file: `python -m ledger invoice export <id> --format json --path <file>`  # prints exported filepath to STDOUT

Agent guidelines and best practices:
- Always fetch the model JSON Schema first (via `--json-schema` or `ledger schema`) to know required fields and types before constructing `--model` input.
- Parse STDOUT as JSON on success; treat STDERR as human-facing logs only.
- Prefer non-destructive reads (list/view) before writes. When performing multi-step operations, run them in an isolated working directory and use the export command to confirm final state.
- Avoid concurrent writes to the same `ledger.db`; acquire external locks if needed.

Examples (agent-friendly):
- Get the Customer schema:
    `python -m ledger customer create --json-schema`
    or
    `python -m ledger schema customer`
- Create a Customer using the schema-observed fields:
    `python -m ledger customer create --model '{"name":"ACME Ltd","email":"pay@acme.test"}'`

Notes:
- Monetary amounts in invoices are decimals (e.g., 199.99). Invoice line `unit_price` is expressed in currency units; the DB stores cents internally - i.e. the precision is .01 units.
- The CLI guarantees that JSON outputs are canonical via `ledger/config.dump_model()`; agents can rely on that for parsing.
"""
    click.echo(text, err=True)


@cli.command("schema")
@click.argument("name", type=str)
def schema(name):
    """Print Pydantic JSON Schema for a named model (customer, creditor, account, invoice).

    Example: `python -m ledger schema customer` prints the Customer JSON Schema to stdout.
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
        click.echo(
            "Unknown schema name. Available: customer, creditor, account, payment-account, invoice, invoice-line",
            err=True,
        )
        sys.exit(2)
    mdl = mapping[name]
    schema = mdl.model_json_schema()
    click.echo(json.dumps(schema, indent=2, ensure_ascii=False))
