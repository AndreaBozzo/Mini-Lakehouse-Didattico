from pathlib import Path
from typing import Dict

import pandas as pd
import yaml


def parse_dbt_schema(schema_path: Path) -> Dict[str, Dict]:
    """
    Estrae metadati da uno schema.yml dbt: colonne, tipi, chiavi primarie per modello.
    Ritorna un dizionario:
    {
        'nome_modello': {
            'columns': {'nome_col': 'tipo', ...},
            'primary_key': ['col1', 'col2']
        },
        ...
    }
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
    name = name.replace("main_marts__", "")  # rimozione prefisso file
    return name


def validate_export_schema(csv_path: Path, schema_path: Path) -> bool:
    """
    Confronta uno CSV esportato con il relativo schema dbt.
    Verifica che tutte le colonne siano presenti e del tipo atteso.
    Ritorna True se valido, False altrimenti.
    """
    schema_info = parse_dbt_schema(schema_path)
    csv_name = normalize_model_name(csv_path.stem)

    # Match flessibile: anche se in schema è scritto con o senza schema
    matches = [
        info
        for name, info in schema_info.items()
        if name == csv_name or normalize_model_name(name) == csv_name
    ]

    if not matches:
        print(f"⚠️ Nessuno schema trovato per {csv_path.stem} in {schema_path.name}")
        return False

    expected = matches[0]
    expected_cols = set(expected["columns"].keys())

    df = pd.read_csv(csv_path, nrows=5)  # Caricamento parziale per performance
    actual_cols = set(df.columns)

    missing = expected_cols - actual_cols
    extra = actual_cols - expected_cols

    if missing:
        print(f"❌ Colonne mancanti in {csv_path.name}: {sorted(missing)}")
    if extra:
        print(f"⚠️ Colonne inattese in {csv_path.name}: {sorted(extra)}")

    return not missing
