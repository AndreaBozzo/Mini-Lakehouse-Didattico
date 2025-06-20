import duckdb
import polars as pl
from pathlib import Path

# ✅ Autodifesa contro moduli falsi
if not hasattr(duckdb, "connect"):
    raise ImportError("Modulo duckdb non valido: manca 'connect'. Verifica conflitti nel progetto.")

# ✅ Path coerenti
RAW_PATH = Path("data/raw/bilanci_comunali_sample.csv")
DB_PATH = Path("data/warehouse/warehouse.duckdb")

# ✅ Ingestione CSV in DuckDB
if __name__ == "__main__":
    df = pl.read_csv(RAW_PATH)
    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE OR REPLACE TABLE raw_bilanci AS SELECT * FROM df")
    con.close()
