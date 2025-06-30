from pathlib import Path
from typing import Dict

import pandas as pd
import yaml


def parse_dbt_schema(schema_path: Path) -> Dict[str, Dict]:
    """
    Estrae metadati da uno schema.yml dbt: colonne, tipi, chiavi primarie per modello.
    """
    with schema_path.open("r", encoding="utf-8") as f:
        content = yaml.safe_load(f)

    if not isinstance(content, dict) or "models" not in content:
        raise ValueError(f"File {schema_path} non contiene un blocco 'models' valido.")

    result = {}
    for model in content["models"]:
        name = model["name"].split(".")[-1]  # Rimuove prefisso schema se presente
        columns = {}
        pk = []

        for col in model.get("columns", []):
            col_name = col["name"]
            if "type" not in col:
                raise ValueError(
                    f"Colonna '{col_name}' in model '{name}' è priva di 'type'"
                )
            col_type = col["type"]
            columns[col_name] = col_type

            tests = col.get("tests", [])
            if isinstance(tests, list):
                if "unique" in tests or any(
                    isinstance(t, dict) and "unique" in t for t in tests
                ):
                    pk.append(col_name)

        result[name] = {"columns": columns, "primary_key": list(set(pk))}

    return result


def normalize_model_name(name: str) -> str:
    """
    Rimuove prefissi comuni dai nomi modello per facilitarne il matching con i file CSV.
    """
    return name.replace("main_marts__", "")


def find_all_schema_files(base_dir: Path) -> list[Path]:
    """
    Trova tutti gli schema.yml all'interno di base_dir ricorsivamente.
    """
    return list(base_dir.rglob("schema.yml"))


def validate_export_schema(csv_path: Path, base_models_dir: Path) -> bool:
    """
    Valida lo schema di un file CSV confrontandolo con tutti gli schema.yml trovati.
    """
    all_schema_files = find_all_schema_files(base_models_dir)

    all_schema_info = {}
    for path in all_schema_files:
        try:
            parsed = parse_dbt_schema(path)
            all_schema_info.update(parsed)
        except Exception as e:
            print(f"⚠️ Errore parsing {path}: {e}")

    csv_name = normalize_model_name(csv_path.stem)

    matches = [
        info
        for name, info in all_schema_info.items()
        if name == csv_name or normalize_model_name(name) == csv_name
    ]

    if not matches:
        print(f"⚠️ Nessuno schema trovato per {csv_path.stem}")
        return False

    expected = matches[0]
    expected_cols = set(expected["columns"].keys())

    df = pd.read_csv(csv_path, nrows=5)
    actual_cols = set(df.columns)

    missing = expected_cols - actual_cols
    extra = actual_cols - expected_cols

    if missing:
        print(f"❌ Colonne mancanti in {csv_path.name}: {sorted(missing)}")
    if extra:
        print(f"⚠️ Colonne inattese in {csv_path.name}: {sorted(extra)}")

    return not missing
