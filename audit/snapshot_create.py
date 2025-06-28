# scripts/snapshot_create.py

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datetime import datetime
from pathlib import Path

from audit.export_marts import export_marts


def main():
    # Timestamp compatto: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Percorsi snapshot
    base_path = Path("snapshots") / "v0.3.0" / "real"
    csv_path = base_path / "csv" / f"snapshot_{timestamp}"
    parquet_path = base_path / "parquet" / f"snapshot_{timestamp}"

    # Creazione directory
    csv_path.mkdir(parents=True, exist_ok=True)
    parquet_path.mkdir(parents=True, exist_ok=True)

    # Esportazione
    print(f"[snapshot-create] Esportazione snapshot {timestamp}...")
    export_marts(csv_path=csv_path, parquet_path=parquet_path)
    print(
        f"[snapshot-create] ✅ Cmplt in:\n- CSV: {csv_path}\n- Parquet: {parquet_path}"
    )


if __name__ == "__main__":
    main()
