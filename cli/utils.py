# cli/utils.py

import subprocess
import sys
from pathlib import Path

from rich.console import Console

console = Console()

# Palette colori Rich
PALETTE = {
    "accent": "bold magenta",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "dim": "dim",
}


def run_step(
    name: str,
    command: str,
    working_dir: str = ".",
    check: bool = True,
):
    """
    Esegue un comando shell con output formattato via Rich.

    Args:
        name: Etichetta del comando (es. "Run", "Test", ecc.).
        command: Comando da eseguire (es. "dbt run").
        working_dir: Directory di lavoro.
        check: Se True, solleva errore su exit code ≠ 0.
    """
    console.rule(f"[{PALETTE['accent']}]⏳ {name}")
    try:
        subprocess.run(
            command,
            shell=True,
            check=check,
            cwd=working_dir,
        )
        console.print(f"[{PALETTE['success']}]✅ {name} completato.")
    except subprocess.CalledProcessError:
        console.print(f"[{PALETTE['error']}]❌ Errore durante: {name}")
        sys.exit(1)


def ensure_duckdb_path_exists():
    """Crea la directory data/warehouse se non esiste."""
    Path("data/warehouse").mkdir(parents=True, exist_ok=True)
