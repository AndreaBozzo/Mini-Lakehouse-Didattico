# tests/test_cli_pipeline.py
from typer.testing import CliRunner

from cli.pipeline import app

runner = CliRunner()


def test_cli_help_exit_zero():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Avvia la pipeline in modalità interattiva" in result.stdout
