import json
from click.testing import CliRunner

from ledger import cli


def assert_valid_json(result):
    assert result.exit_code == 0, result.output
    try:
        data = json.loads(result.output)
    except Exception as e:
        raise AssertionError(f"Output is not valid JSON: {e}\nOutput was:\n{result.output}")
    return data


def test_cli_json_endpoints():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # init DB
        r = runner.invoke(cli.cli, ["database", "initialize"])
        assert r.exit_code == 0

        # Create customer
        payload_cust = {"name": "ACME", "email": "sales@acme.example", "address": "123 Road"}
        r = runner.invoke(cli.cli, ["customer", "create", "--model", json.dumps(payload_cust)])
        cust = assert_valid_json(r)
        assert cust.get("name") == "ACME"
        cid = cust.get("id")
        assert isinstance(cid, int)

        # Customer list
        r = runner.invoke(cli.cli, ["customer", "list"])
        lst = assert_valid_json(r)
        assert isinstance(lst, list)

        # Create creditor
        payload_cred = {"name": "MeCo", "email": "me@co.example"}
        r = runner.invoke(cli.cli, ["creditor", "create", "--model", json.dumps(payload_cred)])
        cred = assert_valid_json(r)
        cred_id = cred.get("id")

        # Creditor list
        r = runner.invoke(cli.cli, ["creditor", "list"])
        clist = assert_valid_json(r)
        assert isinstance(clist, list)

        # Creditor view
        r = runner.invoke(cli.cli, ["creditor", "view", str(cred_id)])
        cview = assert_valid_json(r)
        assert cview.get("id") == cred_id

        # Create payment account
        pa_payload = {"creditor_id": cred_id, "type": "bank", "identifier": "IBAN123"}
        r = runner.invoke(cli.cli, ["creditor", "account", "create", "--model", json.dumps(pa_payload)])
        pa = assert_valid_json(r)
        pa_id = pa.get("id")

        # Account list
        r = runner.invoke(cli.cli, ["creditor", "account", "list", "--creditor-id", str(cred_id)])
        alist = assert_valid_json(r)
        assert isinstance(alist, list)

        # Create invoice
        inv_payload = {
            "customer_id": cid,
            "creditor_id": cred_id,
            "lines": [{"description": "Service", "quantity": 1, "unit_price": "1000.00", "vat_rate": "25"}],
        }
        r = runner.invoke(cli.cli, ["invoice", "create", "--model", json.dumps(inv_payload)])
        inv = assert_valid_json(r)
        inv_id = inv.get("id")
        # Money fields must be culture-invariant strings with two decimals
        assert isinstance(inv.get("lines"), list)
        first_line = inv["lines"][0]
        assert isinstance(first_line.get("unit_price"), str)
        assert first_line.get("unit_price") == "1000.00"

        # Invoice list
        r = runner.invoke(cli.cli, ["invoice", "list"])
        ilist = assert_valid_json(r)
        assert isinstance(ilist, list)

        # Invoice view
        r = runner.invoke(cli.cli, ["invoice", "view", str(inv_id)])
        iview = assert_valid_json(r)
        assert iview.get("id") == inv_id
        # View should also present monetary values as two-decimal strings
        assert isinstance(iview.get("lines"), list)
        vline = iview["lines"][0]
        assert isinstance(vline.get("unit_price"), str)
        assert vline.get("unit_price") == "1000.00"

        # Top-level schema command
        r = runner.invoke(cli.cli, ["schema", "customer"])
        schema = assert_valid_json(r)
        assert isinstance(schema, dict)

        # Per-command --json-schema
        r = runner.invoke(cli.cli, ["customer", "create", "--json-schema"])
        cschema = assert_valid_json(r)
        assert isinstance(cschema, dict)
