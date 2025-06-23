# tests/test_cli.py
import os

import pytest
from typer.testing import CliRunner

from cli.pipeline import app

runner = CliRunner()


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Salta l'interattivo in CI")
def test_interactive_exit():
    # Simula la scelta "11" per uscire subito
    result = runner.invoke(app, ["interactive"], input="11\n")
    assert result.exit_code == 0
    assert "Uscita" in result.stdout


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert (
        "Mini Lakehouse Pipeline Interattiva" in result.stdout
        or "Usage" in result.stdout
    )


def test_ci_mode():
    result = runner.invoke(app, ["ci-mode"])
    # esce dopo il primo step, codice 1 o 0 a seconda dello script
    assert result.exit_code in (0, 1)
