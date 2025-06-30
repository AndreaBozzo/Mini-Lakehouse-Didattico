# audit/export_marts.py
from __future__ import annotations

import os
from pathlib import Path
from typing import Collection

import duckdb

EXPORT_CSV = Path("exports/csv")
EXPORT_PARQUET = Path("exports/parquet")
_DEFAULT_DB = Path("data/warehouse/warehouse.duckdb")
DB_PATH = Path(os.getenv("DUCKDB_PATH", _DEFAULT_DB))


def export_schemas(
    db_path: Path,
    schemas: Collection[str],
    *,
    csv_dir: Path = EXPORT_CSV,
    parquet_dir: Path = EXPORT_PARQUET,
) -> None:
    """
    Esporta tutte le tabelle nei `schemas` indicati in CSV (HEADER) e Parquet.
    """
    if not db_path.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        duckdb.connect(db_path).close()

    csv_dir.mkdir(parents=True, exist_ok=True)
    parquet_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(db_path)

    # Genera query con filtri dinamici su schema
    placeholders = ", ".join(["?"] * len(schemas))
    query = f"""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema IN ({placeholders})
    """
    tables: list[tuple[str, str]] = con.execute(query, schemas).fetchall()

    if not tables:
        print(f"⚠️  Nessuna tabella trovata negli schemi: {', '.join(schemas)}")
    else:
        for schema, table in tables:
            fqn = f"{schema}.{table}"
            csv_file = csv_dir / f"{table}.csv"
            parquet_file = parquet_dir / f"{table}.parquet"

            print(f"📤 Esporto {fqn} …")
            con.execute(f"COPY {fqn} TO '{csv_file}' (HEADER, DELIMITER ',')")
            con.execute(f"COPY {fqn} TO '{parquet_file}' (FORMAT 'parquet')")

        print(
            "\n✅  Esportazione completata in:\n"
            f"   • {csv_dir.resolve()}\n"
            f"   • {parquet_dir.resolve()}"
        )

    con.close()


def export_marts_simulated() -> None:
    export_schemas(DB_PATH, schemas=["marts_simulated"])


def export_marts_real() -> None:
    export_schemas(DB_PATH, schemas=["marts_real"])


def export_marts_all(
    csv_path: Path = EXPORT_CSV, parquet_path: Path = EXPORT_PARQUET
) -> None:
    export_schemas(
        DB_PATH,
        schemas=["marts_real", "marts_simulated"],
        csv_dir=csv_path,
        parquet_dir=parquet_path,
    )


if __name__ == "__main__":  # pragma: no cover
    export_marts_simulated()
