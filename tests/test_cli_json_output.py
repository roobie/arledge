from click.testing import CliRunner
import json

from ledger import cli


def test_customer_create_outputs_valid_json():
    runner = CliRunner()
    # run in isolated filesystem so DB is created in temp dir
    with runner.isolated_filesystem():
        r = runner.invoke(cli.cli, ["database", "initialize"])
        assert r.exit_code == 0

        payload = {"name": "ACME", "email": "sales@acme.example", "address": "123 Road"}
        r = runner.invoke(
            cli.cli, ["customer", "create", "--model", json.dumps(payload)]
        )
        # Command should succeed
        assert r.exit_code == 0, r.output

        # output should contain valid JSON (actionable output)
        out = r.output
        # extract JSON object from output (should be the entire output)
        data = json.loads(out)
        assert isinstance(data, dict)
        assert data.get("name") == "ACME"
