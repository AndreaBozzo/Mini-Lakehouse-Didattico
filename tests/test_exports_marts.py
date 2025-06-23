# tests/test_exports_marts.py


from audit import export_marts


def test_export_dirs_exist(tmp_path):
    csv_path = tmp_path / "csv"
    parquet_path = tmp_path / "parquet"

    export_marts.export_marts(csv_path=csv_path, parquet_path=parquet_path)

    assert csv_path.exists()
    assert parquet_path.exists()
