import os
from pathlib import Path

import duckdb
from rich.console import Console

console = Console()


def get_connection():
    """Da' connessione DuckDB usando DUCKDB_PATH, altrimenti default locale."""
    db_path = os.getenv("DUCKDB_PATH", "data/warehouse/warehouse.duckdb")
    return duckdb.connect(db_path)


def export_marts(csv_path: Path, parquet_path: Path):
    """Esporta tutte le tabelle nello schema 'main_marts' in formato CSV e Parquet."""
    csv_path.mkdir(parents=True, exist_ok=True)
    parquet_path.mkdir(parents=True, exist_ok=True)

    con = get_connection()

    tables = con.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main_marts'
    """
    ).fetchall()

    for (table_name,) in tables:
        df = con.execute(f"SELECT * FROM main_marts.{table_name}").fetch_df()

        console.print(f"📤 Esporto {table_name} …")

        csv_output = csv_path / f"{table_name}.csv"
        parquet_output = parquet_path / f"{table_name}.parquet"

        df.to_csv(csv_output, index=False)
        df.to_parquet(parquet_output, index=False)

    con.close()

    console.print("\n✅  Esportazione completata in:")
    console.print(f"   • {csv_path}")
    console.print(f"   • {parquet_path}")
