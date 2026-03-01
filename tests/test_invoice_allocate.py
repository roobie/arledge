import json
from click.testing import CliRunner
from pathlib import Path

from arledge import cli


def test_invoice_allocate_and_seq():
    runner = CliRunner()
    with runner.isolated_filesystem():
        r = runner.invoke(cli.cli, ["init"]) 
        assert r.exit_code == 0
        # allocate before creating any invoices
        r = runner.invoke(cli.cli, ["invoice", "allocate"]) 
        assert r.exit_code == 0
        out = json.loads(r.output)
        assert out.get("id") == 1
        seq = Path(".arledge") / "invoice_seq"
        assert seq.exists()
        assert seq.read_text(encoding="utf-8").strip() == "2"
        # allocate again
        r = runner.invoke(cli.cli, ["invoice", "allocate"]) 
        assert r.exit_code == 0
        out2 = json.loads(r.output)
        assert out2.get("id") == 2
        assert seq.read_text(encoding="utf-8").strip() == "3"
