# audit/export_marts.py
from __future__ import annotations

import os
import sys
from pathlib import Path

import duckdb

EXPORT_CSV = Path("exports/csv")
EXPORT_PARQUET = Path("exports/parquet")
_DEFAULT_DB = Path("data/warehouse/warehouse.duckdb")
DB_PATH = Path(os.getenv("DUCKDB_PATH", _DEFAULT_DB))


def export_marts(
    db_path: Path = DB_PATH,
    *,
    # nuovi parametri “ufficiali”
    csv_dir: Path | None = None,
    parquet_dir: Path | None = None,
    # alias legacy per compatibilità test / script vecchi
    csv_path: Path | None = None,
    parquet_path: Path | None = None,
) -> None:
    """
    Esporta tutte le tabelle nello schema `main_marts`
    in CSV (HEADER) e Parquet.
    """
    # compatibilità: se qualcuno passa ancora csv_path/parquet_path li usiamo
    if csv_dir is None:
        csv_dir = csv_path or EXPORT_CSV
    if parquet_dir is None:
        parquet_dir = parquet_path or EXPORT_PARQUET

    if not db_path.exists():
        sys.exit(f"❌  DuckDB file non trovato: {db_path}")

    csv_dir.mkdir(parents=True, exist_ok=True)
    parquet_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(db_path)

    tables: list[tuple[str]] = con.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main_marts'
        """
    ).fetchall()

    if not tables:
        print("⚠️  Nessuna tabella trovata in main_marts.")
    else:
        for (table,) in tables:
            fqn = f"main_marts.{table}"
            csv_file = csv_dir / f"{table}.csv"
            parquet_file = parquet_dir / f"{table}.parquet"

            print(f"📤 Esporto {table} …")
            con.execute(f"COPY {fqn} TO '{csv_file}' (HEADER, DELIMITER ',')")
            con.execute(f"COPY {fqn} TO '{parquet_file}' (FORMAT 'parquet')")

        print(
            "\n✅  Esportazione completata in:\n"
            f"   • {csv_dir.resolve()}\n"
            f"   • {parquet_dir.resolve()}"
        )

    con.close()


if __name__ == "__main__":  # pragma: no cover
    export_marts()
