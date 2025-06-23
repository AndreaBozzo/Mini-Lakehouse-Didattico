# audit/export_marts.py

from pathlib import Path

import duckdb

EXPORT_BASE = Path("exports")
EXPORT_CSV = EXPORT_BASE / "csv"
EXPORT_PARQUET = EXPORT_BASE / "parquet"
DB_PATH = Path("dbt/data/warehouse/warehouse.duckdb")


def export_marts(
    db_path: Path = DB_PATH,
    csv_path: Path = EXPORT_CSV,
    parquet_path: Path = EXPORT_PARQUET,
):
    csv_path.mkdir(parents=True, exist_ok=True)
    parquet_path.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(db_path)

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
            csv_file = csv_path / f"{table_name}.csv"
            parquet_file = parquet_path / f"{table_name}.parquet"

            print(f"📤 Esportazione {table_name}...")

            con.execute(f"COPY {table_fqn} TO '{csv_file}' (HEADER, DELIMITER ',')")
            con.execute(f"COPY {table_fqn} TO '{parquet_file}' (FORMAT 'parquet')")

        print(
            "\n✅ Esportazione completata in:\n"
            f" - {csv_path.resolve()}\n"
            f" - {parquet_path.resolve()}"
        )

    con.close()


if __name__ == "__main__":
    export_marts()
