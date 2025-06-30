# audit/snapshot_test.py

import argparse
import tempfile
from pathlib import Path

from rich.console import Console
from typer import Exit

from audit.export_marts import export_marts_all
from audit.snapshot_utils import compare_snapshots, find_latest_snapshot_paths

console = Console()


def snapshot_test(ci_mode: bool = False):
    console.rule("[bold cyan]Snapshot Test: confronto con ultima snapshot")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_csv = Path(tmp_dir) / "csv"
        tmp_parquet = Path(tmp_dir) / "parquet"

        # Esportazione corrente
        export_marts_all(csv_path=tmp_csv, parquet_path=tmp_parquet)

        console.print("\n✅  Esportazione completata in:")
        console.print(f"   • {tmp_csv}")
        console.print(f"   • {tmp_parquet}")

        # Trova ultima snapshot
        latest_csv_snap, latest_parquet_snap = find_latest_snapshot_paths()
        if not latest_csv_snap or not latest_parquet_snap:
            console.print(
                "\n[bold red]❌ Nessuna snapshot precedente trovata. "
                "Crea prima una baseline con `make snapshot-create`."
            )
            raise Exit(1)

        # Confronto
        differences = compare_snapshots(tmp_csv, latest_csv_snap)

        if differences:
            console.print(
                "\n[bold yellow]⚠️  Differenze trovate tra l'esportazione attuale "
                "e la snapshot precedente:"
            )
            for diff in differences:
                console.print(f"  - {diff}")

            if ci_mode:
                raise Exit(2)
        else:
            console.print("\n✅ Nessuna differenza trovata nelle esportazioni.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Confronta esportazione corrente con snapshot precedente")
    )
    parser.add_argument(
        "--ci-mode",
        action="store_true",
        help="Attiva modalità CI: fallisce su differenze",
    )
    args = parser.parse_args()

    snapshot_test(ci_mode=args.ci_mode)
