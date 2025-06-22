from pathlib import Path

import duckdb
import polars as pl


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "dbt" / "seeds" / "bilanci_comunali_sample.csv"
DB_PATH = ROOT / "dbt" / "data" / "warehouse" / "warehouse.duckdb"


def to_title_case(nome: str) -> str:
    """Restituisce il testo in Title Case."""
    return " ".join(word.capitalize() for word in nome.lower().split())


def load_ingest_raw() -> pl.DataFrame:
    """Legge il CSV raw e normalizza i nomi delle colonne."""
    df = pl.read_csv(RAW_PATH)
    df = df.rename({col: col.lower() for col in df.columns})
    df = df.with_columns(
        pl.col("nome_comune")
        .map_elements(to_title_case, return_dtype=pl.Utf8)
        .alias("nome_comune")
    )
    return df


def ingest_to_duckdb(df: pl.DataFrame) -> None:
    """Crea o sostituisce la tabella raw_bilanci in DuckDB dal DataFrame."""
    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE OR REPLACE TABLE raw_bilanci AS SELECT * FROM df")
    con.close()


def preview_duckdb() -> None:
    """Stampa schema e prime righe di raw_bilanci per verifica."""
    con = duckdb.connect(str(DB_PATH))
    print("\n✅ Tabelle nel DB:")
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


if __name__ == "__main__":
    if not hasattr(duckdb, "connect"):
        raise ImportError(
            "Modulo duckdb non valido: manca 'connect'. "
            "Verifica conflitti nel progetto."
        )

    df_raw = load_ingest_raw()
    ingest_to_duckdb(df_raw)
    preview_duckdb()
