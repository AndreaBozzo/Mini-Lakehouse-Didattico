# audit/snapshot_utils.py

import hashlib
from pathlib import Path
from typing import List, Optional, Tuple


def hash_file(path: Path) -> str:
    """Calcola l'hash SHA256 del file dato."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def find_latest_snapshot_paths() -> Tuple[Optional[Path], Optional[Path]]:
    """Trova le cartelle snapshot reali più recenti (csv e parquet)."""
    base_csv = Path("snapshots/v0.3.0/real/csv")
    base_parquet = Path("snapshots/v0.3.0/real/parquet")

    if not base_csv.exists() or not base_parquet.exists():
        return None, None

    latest_csv = max(base_csv.glob("snapshot_*"), default=None, key=lambda p: p.name)
    latest_parquet = max(
        base_parquet.glob("snapshot_*"), default=None, key=lambda p: p.name
    )

    return latest_csv, latest_parquet


def compare_snapshots(current_dir: Path, snapshot_dir: Path) -> List[str]:
    """Confronta file CSV tra le due cartelle e ritorna lista di differenze."""
    diffs = []
    current_files = list(current_dir.glob("*.csv"))

    for f in current_files:
        snap_file = snapshot_dir / f.name
        if not snap_file.exists():
            diffs.append(f"🆕 Nuovo file: {f.name}")
            continue

        curr_hash = hash_file(f)
        snap_hash = hash_file(snap_file)

        if curr_hash != snap_hash:
            diffs.append(f"🟡 File modificato: {f.name}")

    # Cerca file mancanti nella nuova esportazione
    snapshot_files = list(snapshot_dir.glob("*.csv"))
    snapshot_names = {f.name for f in snapshot_files}
    current_names = {f.name for f in current_files}
    missing = snapshot_names - current_names
    for name in missing:
        diffs.append(f"🔴 File mancante: {name}")

    return diffs
