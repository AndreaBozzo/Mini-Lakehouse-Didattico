import duckdb
import polars as pl
from pathlib import Path

# Autodifesa contro moduli falsi
if not hasattr(duckdb, "connect"):
    raise ImportError("Modulo duckdb non valido: manca 'connect'. Verifica conflitti nel progetto.")

# Path coerenti
RAW_PATH = Path("data/raw/bilanci_comunali_sample.csv")
DB_PATH = Path("data/warehouse/warehouse.duckdb")

# Ingestione CSV in DuckDB
if __name__ == "__main__":
    df = pl.read_csv(RAW_PATH)
    df = df.rename({col: col.lower() for col in df.columns})
    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE OR REPLACE TABLE raw_bilanci AS SELECT * FROM df")

    # ✅ Debug: verifica contenuto
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
