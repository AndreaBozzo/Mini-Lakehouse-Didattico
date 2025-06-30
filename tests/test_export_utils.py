# tests/test_export_utils.py

import tempfile
from pathlib import Path

import pandas as pd
import pytest
import yaml

from cli.export_utils import parse_dbt_schema, validate_export_schema


def test_parse_dbt_schema_extracts_columns_and_pk():
    schema_yaml = {
        "version": 2,
        "models": [
            {
                "name": "fct_sales",
                "columns": [
                    {"name": "id", "type": "integer", "tests": ["unique"]},
                    {"name": "amount", "type": "float"},
                    {"name": "region", "type": "text"},
                ],
            }
        ],
    }

    with tempfile.NamedTemporaryFile("w+", suffix=".yml", delete=False) as tmp:
        yaml.dump(schema_yaml, tmp)
        tmp_path = Path(tmp.name)

    result = parse_dbt_schema(tmp_path)

    assert "fct_sales" in result
    assert result["fct_sales"]["columns"]["id"] == "integer"
    assert result["fct_sales"]["primary_key"] == ["id"]


def test_validate_export_schema_success():
    # Simula uno schema dbt
    schema_yaml = {
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

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Salva schema
        schema_path = tmp_path / "schema.yml"
        with schema_path.open("w", encoding="utf-8") as f:
            yaml.dump(schema_yaml, f)

        # Crea CSV compatibile
        df = pd.DataFrame({"id": [1, 2], "amount": [100.0, 200.0]})
        csv_path = tmp_path / "main_marts__fct_sales.csv"
        df.to_csv(csv_path, index=False)

        assert validate_export_schema(csv_path, schema_path)


def test_validate_export_schema_missing_column():
    # Schema con 2 colonne
    schema_yaml = {
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

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Salva schema
        schema_path = tmp_path / "schema.yml"
        with schema_path.open("w", encoding="utf-8") as f:
            yaml.dump(schema_yaml, f)

        # CSV mancante di "amount"
        df = pd.DataFrame({"id": [1, 2]})
        csv_path = tmp_path / "fct_sales.csv"
        df.to_csv(csv_path, index=False)

        assert not validate_export_schema(csv_path, schema_path)


def test_parse_dbt_schema_raises_on_missing_type():
    schema_yaml = {
        "version": 2,
        "models": [
            {
                "name": "fct_invalid",
                "columns": [
                    {"name": "id"},  # manca 'type'
                ],
            }
        ],
    }

    with tempfile.NamedTemporaryFile("w+", suffix=".yml", delete=False) as tmp:
        yaml.dump(schema_yaml, tmp)
        tmp_path = Path(tmp.name)

    with pytest.raises(ValueError, match="priva di 'type'"):
        parse_dbt_schema(tmp_path)
