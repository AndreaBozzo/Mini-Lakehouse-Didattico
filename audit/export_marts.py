# audit/export_marts.py

from pathlib import Path

import duckdb

EXPORT_BASE = Path("exports")
EXPORT_CSV = EXPORT_BASE / "csv"
EXPORT_PARQUET = EXPORT_BASE / "parquet"
DB_PATH = Path("dbt/data/warehouse/warehouse.duckdb")

EXPORT_CSV.mkdir(parents=True, exist_ok=True)
EXPORT_PARQUET.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(DB_PATH)

# Recupera le tabelle nello schema main_marts
tables = con.execute(
    """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'main_marts'
    """
).fetchall()

if not tables:
    print("⚠️  Nessuna tabella trovata in main_marts.")
else:
    for (table_name,) in tables:
        table_fqn = f"main_marts.{table_name}"
        csv_path = EXPORT_CSV / f"{table_name}.csv"
        parquet_path = EXPORT_PARQUET / f"{table_name}.parquet"

        print(f"📤 Esportazione {table_name}...")

        con.execute(
            f"COPY {table_fqn} TO '{csv_path}' (HEADER, DELIMITER ',')"
        )
        con.execute(
            f"COPY {table_fqn} TO '{parquet_path}' (FORMAT 'parquet')"
        )

    resolved_csv = EXPORT_CSV.resolve()
    resolved_parquet = EXPORT_PARQUET.resolve()
    print(
        "\n✅ Esportazione completata in:\n"
        f" - {resolved_csv}\n"
        f" - {resolved_parquet}"
    )

con.close()
