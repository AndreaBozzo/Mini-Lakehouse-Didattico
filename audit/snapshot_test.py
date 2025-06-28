import hashlib
import sys
import tempfile
from pathlib import Path

from rich import box
from rich.console import Console
from rich.table import Table

from audit.export_marts import export_marts

console = Console()

SNAPSHOT_DIR = Path("snapshots/v0.3.0/real")


def get_latest_snapshot(subdir: str) -> Path | None:
    snapshot_base = SNAPSHOT_DIR / subdir
    if not snapshot_base.exists():
        return None
    candidates = [
        p
        for p in snapshot_base.iterdir()
        if p.is_dir() and p.name.startswith("snapshot_")
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.name)


def hash_file(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def compare_dirs(old_dir: Path, new_dir: Path) -> list[tuple[str, str, str]]:
    diffs = []
    for file in new_dir.glob("*.csv"):
        old_file = old_dir / file.name
        if not old_file.exists():
            diffs.append((file.name, "MISSING", "NEW"))
            continue
        old_hash = hash_file(old_file)
        new_hash = hash_file(file)
        if old_hash != new_hash:
            diffs.append((file.name, old_hash[:8], new_hash[:8]))
    return diffs


def main(ci_mode: bool = False):
    console.rule("[bold yellow]Snapshot Test: confronto con ultima snapshot")

    latest_csv = get_latest_snapshot("csv")
    latest_parquet = get_latest_snapshot("parquet")

    if not latest_csv or not latest_parquet:
        console.print("[red]❌ Nessuna snapshot precedente trovata.")
        sys.exit(1 if ci_mode else 0)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_csv = Path(tmpdir) / "csv"
        tmp_parquet = Path(tmpdir) / "parquet"
        export_marts(csv_path=tmp_csv, parquet_path=tmp_parquet)

        csv_diffs = compare_dirs(latest_csv, tmp_csv)
        parquet_diffs = compare_dirs(latest_parquet, tmp_parquet)

        if not csv_diffs and not parquet_diffs:
            console.print("[green]✅ Nessuna differenza trovata nelle esportazioni.")
        else:
            table = Table(title="Differenze rilevate", box=box.SIMPLE)
            table.add_column("File")
            table.add_column("Snapshot")
            table.add_column("Corrente")

            for name, old, new in csv_diffs + parquet_diffs:
                table.add_row(name, old, new)

            console.print("[red]❌ Differenze trovate tra snapshot e dati attuali:")
            console.print(table)
            if ci_mode:
                sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ci-mode",
        action="store_true",
        help="Termina con errore se vengono rilevate differenze",
    )
    args = parser.parse_args()
    main(ci_mode=args.ci_mode)
