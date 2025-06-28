# cli/pipeline.py

import os
import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

# Forza UTF-8 anche nei child-process dbt su Windows
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

app = typer.Typer()
console = Console()

# Palette colori
PALETTE = {
    "accent": "bold magenta",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "dim": "dim",
}


def ensure_duckdb_path_exists():
    # Crea data/warehouse nella root, non in dbt/data
    Path("data/warehouse").mkdir(parents=True, exist_ok=True)


def run_step(
    name: str,
    command: str,
    working_dir: str = ".",
    check: bool = True,
):
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


@app.command()
def interactive():
    """Avvia la pipeline in modalità interattiva"""
    ensure_duckdb_path_exists()

    console.print(Panel.fit("> Mini Lakehouse Pipeline Interattiva"))

    options = {
        "1": "Clean (dbt clean)",
        "2": "Deps (dbt deps)",
        "3": "Seed (dbt seed)",
        "4": "Run (dbt run)",
        "5": "Test (dbt test)",
        "6": "Docs (dbt docs generate)",
        "7": "Audit Export (export_marts.py)",
        "8": "Coverage (pytest + coverage)",
        "9": "Quality Report (ruff JSON)",
        "10": "Tutti i passaggi (build completo)",
        "11": "Esci",
    }

    table = Table(
        title="Passaggi disponibili",
        show_header=True,
        header_style=PALETTE["accent"],
    )
    table.add_column("Opzione", justify="center")
    table.add_column("Descrizione", justify="left")
    for key, descr in options.items():
        table.add_row(key, descr)
    console.print(table)

    while True:
        choice = Prompt.ask(f"[{PALETTE['accent']}]Seleziona un'opzione")
        match choice:
            case "1":
                run_step("Clean", "poetry run dbt clean", working_dir=".")
            case "2":
                run_step("Deps", "poetry run dbt deps", working_dir=".")
            case "3":
                run_step("Seed", "poetry run dbt seed", working_dir=".")
            case "4":
                run_step("Run", "poetry run dbt run", working_dir=".")
            case "5":
                run_step("Test", "poetry run dbt test", working_dir=".")
            case "6":
                run_step(
                    "Docs Generate", "poetry run dbt docs generate", working_dir="."
                )
            case "7":
                run_step(
                    "Audit Export",
                    "poetry run python audit/export_marts.py",
                    working_dir=".",
                )
            case "8":
                run_step("Coverage", "make coverage", working_dir=".")
            case "9":
                run_step("Quality Report", "make quality-report", working_dir=".")
            case "10":
                if Confirm.ask("Eseguire tutta la pipeline?"):
                    real_data = Confirm.ask("Usare dati reali?")
                    suffix = "tag:real" if real_data else "tag:simulated"
                    ensure_duckdb_path_exists()

                    full_pipeline = [
                        ("poetry run dbt clean", "Clean", "."),
                        ("poetry run dbt deps", "Deps", "."),
                        *([] if real_data else [("poetry run dbt seed", "Seed", ".")]),
                        (f"poetry run dbt run --select {suffix}", "Run", "."),
                        (f"poetry run dbt test --select {suffix}", "Test", "."),
                        ("poetry run dbt docs generate", "Docs Generate", "."),
                        (
                            "poetry run python audit/export_marts.py",
                            "Audit Export",
                            ".",
                        ),
                        ("make coverage", "Coverage", "."),
                        ("make quality-report", "Quality Report", "."),
                    ]
                    for cmd, desc, wd in full_pipeline:
                        run_step(desc, cmd, working_dir=wd)
            case "11":
                console.print(f"[{PALETTE['dim']}]Uscita.")
                sys.exit(0)
            case _:
                console.print(f"[{PALETTE['warning']}]⚠️ Scelta non valida.")


@app.command()
def ci_mode(real_data: bool = typer.Option(False, help="Usa dati reali (--real-data)")):
    """Esegue la pipeline completa in modalità CI"""
    console.print(Panel.fit("> Esecuzione in modalità CI"))
    ensure_duckdb_path_exists()

    suffix = "tag:real" if real_data else "tag:simulated"

    ci_commands = [
        ("poetry run dbt clean", "Clean", "."),
        ("poetry run dbt deps", "Deps", "."),
        *([] if real_data else [("poetry run dbt seed", "Seed", ".")]),
        (f"poetry run dbt run --select {suffix}", "Run", "."),
        (f"poetry run dbt test --select {suffix}", "Test", "."),
        ("poetry run dbt docs generate", "Docs Generate", "."),
        ("poetry run python audit/export_marts.py", "Audit Export", "."),
        ("make coverage", "Coverage", "."),
        ("make quality-report", "Quality Report", "."),
    ]

    for cmd, desc, wd in ci_commands:
        run_step(desc, cmd, working_dir=wd)


if __name__ == "__main__":
    app()
