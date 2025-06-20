import duckdb
import polars as pl
from pathlib import Path

RAW_PATH = Path("data/raw/bilanci_comunali_sample.csv")
DB_PATH = Path("data/warehouse/warehouse.duckdb")

if not hasattr(duckdb, "connect"):
    raise ImportError("Modulo duckdb non valido: manca 'connect'. Verifica conflitti nel progetto.")

# Funzione di capitalizzazione tipo title case
def to_title_case(nome: str) -> str:
    return " ".join(word.capitalize() for word in nome.lower().split())

if __name__ == "__main__":
    df = pl.read_csv(RAW_PATH)
    df = df.rename({col: col.lower() for col in df.columns})

    df = df.with_columns([
        pl.col("nome_comune").map_elements(to_title_case).alias("nome_comune")
    ])

    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE OR REPLACE TABLE raw_bilanci AS SELECT * FROM df")

    print("\n✅ Verifica: tabelle nel DB")
    tables = con.sql("SHOW TABLES").fetchall()
    print("Tabelle trovate:", tables)

    if ('raw_bilanci',) in tables:
        print("\n📋 Schema 'raw_bilanci':")
        print(con.sql("DESCRIBE raw_bilanci").fetchdf())

        print("\n🔍 Prime righe:")
        print(con.sql("SELECT * FROM raw_bilanci LIMIT 5").fetchdf())
    else:
        print("\n❌ Tabella 'raw_bilanci' non trovata.")

    con.close()
