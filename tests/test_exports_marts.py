import duckdb

from audit import export_marts


def test_export_marts_outputs(tmp_path, monkeypatch):
    # Setup: crea db DuckDB temporaneo con una tabella dummy nello schema "main_marts"
    duckdb_path = tmp_path / "test.duckdb"
    con = duckdb.connect(str(duckdb_path))
    con.execute("CREATE SCHEMA IF NOT EXISTS main_marts")
    con.execute(
        """
        CREATE TABLE main_marts.mart_demo (
            id INTEGER,
            name TEXT
        )
    """
    )
    con.execute("INSERT INTO main_marts.mart_demo VALUES (1, 'Test'), (2, 'Demo')")

    # Override della variabile d'ambiente DUCKDB_PATH per usare il db temporaneo
    monkeypatch.setenv("DUCKDB_PATH", str(duckdb_path))

    # Directory di destinazione
    csv_path = tmp_path / "csv"
    parquet_path = tmp_path / "parquet"

    # Esegui export
    export_marts.export_marts(csv_path=csv_path, parquet_path=parquet_path)

    # Verifica che le directory siano state create
    assert csv_path.exists()
    assert parquet_path.exists()

    # Verifica che i file siano stati creati
    csv_files = list(csv_path.glob("*.csv"))
    parquet_files = list(parquet_path.glob("*.parquet"))
    assert len(csv_files) > 0
    assert len(parquet_files) > 0

    # Verifica che i file non siano vuoti
    for file in csv_files + parquet_files:
        assert file.stat().st_size > 0
