# tests/test_snapshot_utils.py

import tempfile
from pathlib import Path

from audit.snapshot_utils import compare_snapshots, hash_file


def test_hash_file_and_compare_snapshots():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        file1 = tmp_path / "file1.csv"
        file2 = tmp_path / "file2.csv"
        file3 = tmp_path / "file3.csv"

        file1.write_text("a,b,c\n1,2,3\n")
        file2.write_text("a,b,c\n1,2,3\n")
        file3.write_text("a,b,c\n4,5,6\n")

        assert hash_file(file1) == hash_file(file2), "Hash uguali per file identici"
        assert hash_file(file1) != hash_file(
            file3
        ), "Hash diversi per contenuti diversi"

        snap1 = tmp_path / "snap1"
        snap2 = tmp_path / "snap2"
        snap3 = tmp_path / "snap3"
        snap1.mkdir()
        snap2.mkdir()
        snap3.mkdir()

        (snap1 / "test.csv").write_text("a,b\n1,2\n")
        (snap2 / "test.csv").write_text("a,b\n1,2\n")
        (snap3 / "test.csv").write_text("a,b\n9,9\n")

        assert compare_snapshots(snap1, snap2) == [], "Nessuna differenza attesa"
        assert compare_snapshots(snap1, snap3) != [], "Differenze attese"
