from pathlib import Path

import duckdb
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "dbt" / "data" / "raw" / "bilanci_comunali_sample.csv"
DB_PATH = ROOT / "dbt" / "data" / "warehouse" / "warehouse.duckdb"


if not hasattr(duckdb, "connect"):
    raise ImportError(
        "Modulo duckdb non valido: manca 'connect'. Verifica conflitti nel progetto."
    )


def to_title_case(nome: str) -> str:
    """Capitalizzazione stile Title Case."""
    return " ".join(word.capitalize() for word in nome.lower().split())


if __name__ == "__main__":
    df = pl.read_csv(RAW_PATH)
    df = df.rename({col: col.lower() for col in df.columns})

    df = df.with_columns(
        [
            pl.col("nome_comune")
            .map_elements(to_title_case, return_dtype=pl.Utf8)
            .alias("nome_comune")
        ]
    )

    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE OR REPLACE TABLE raw_bilanci AS SELECT * FROM df")

    print("\n✅ Verifica: tabelle nel DB")
    tables = con.sql("SHOW TABLES").fetchall()
    print("Tabelle trovate:", tables)

    if ("raw_bilanci",) in tables:
        print("\n📋 Schema 'raw_bilanci':")
        print(con.sql("DESCRIBE raw_bilanci").fetchdf())

        print("\n🔍 Prime righe:")
        print(con.sql("SELECT * FROM raw_bilanci LIMIT 5").fetchdf())
    else:
        print("\n❌ Tabella 'raw_bilanci' non trovata.")

    con.close()
