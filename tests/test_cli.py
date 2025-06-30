import os
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
import yaml
from typer.testing import CliRunner

from cli.pipeline import app

runner = CliRunner()


def test_cli_help_output():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Avvia la pipeline in modalità interattiva" in result.stdout
    assert "Esegue la pipeline ETL" in result.stdout
    assert "Esporta i marts in CSV e Parquet" in result.stdout
    assert "Confronta i file CSV attuali con l'ultima snapshot salvata" in result.stdout


@pytest.mark.slow
@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Troppo lento in CI")
def test_ci_mode_executes():
    with patch("subprocess.run") as mock_run:
        result = runner.invoke(app, ["ci-mode"])
    assert result.exit_code in (0, 1)
    assert mock_run.called


@pytest.mark.slow
def test_interactive_minimal():
    prompt_responses = ["1", "n", "n", "6"]  # 1: Run pipeline, n/n, 6: Esci
    with (
        patch("cli.pipeline.Prompt.ask", side_effect=prompt_responses),
        patch("cli.pipeline.Confirm.ask", side_effect=lambda *_, **__: False),
        patch("subprocess.run") as mock_run,
    ):
        result = runner.invoke(app, ["interactive"])
    assert result.exit_code == 0
    assert mock_run.called


def test_run_command_executes():
    with patch("subprocess.run") as mock_run:
        result = runner.invoke(app, ["run", "--real-data"])
    assert result.exit_code in (0, 1)
    assert mock_run.called


def test_export_command_executes():
    with patch("subprocess.run") as mock_run:
        result = runner.invoke(app, ["export", "--real-data"])
    assert result.exit_code in (0, 1)
    assert mock_run.called


def test_audit_snapshot_missing():
    # Forza l'uscita come se non ci fosse snapshot
    with patch("cli.pipeline.audit_log", side_effect=lambda ci_mode=False: exit(1)):
        result = runner.invoke(app, ["audit"])
    assert result.exit_code == 1


def test_export_schema_validation_success(tmp_path: Path):
    # Prepara CSV compatibile con lo schema
    df = pd.DataFrame({"id": [1], "amount": [100.0]})
    csv_file = tmp_path / "main_marts__fct_sales.csv"
    df.to_csv(csv_file, index=False)

    # Crea schema.yml compatibile
    schema = {
        "version": 2,
        "models": [
            {
                "name": "fct_sales",
                "columns": [
                    {"name": "id", "type": "integer"},
                    {"name": "amount", "type": "float"},
                ],
            }
        ],
    }
    schema_path = tmp_path / "schema.yml"
    with schema_path.open("w", encoding="utf-8") as f:
        yaml.dump(schema, f)

    # Patch Path.exists e Path.glob per far puntare la CLI ai file temporanei
    with (
        patch("cli.pipeline.Path.glob", return_value=[csv_file]),
        patch("cli.pipeline.Path.exists", side_effect=lambda p=tmp_path: True),
        patch("cli.pipeline.Path.is_file", return_value=True),
        patch("cli.pipeline.Path.open", schema_path.open),
    ):
        result = runner.invoke(app, ["export"])

    assert result.exit_code == 0
    assert "Tutti i file validati con successo." in result.stdout


def test_export_schema_validation_failure():
    with (
        patch("cli.export_utils.validate_export_schema", return_value=False),
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.glob", return_value=[Path("bad.csv")]),
    ):
        result = runner.invoke(app, ["export", "--ci-mode"])
    assert result.exit_code == 1
    assert "file non conformi allo schema" in result.stdout
