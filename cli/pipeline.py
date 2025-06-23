# cli/pipeline.py

import subprocess
import sys

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

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
    console.print(
        Panel.fit("[bold white on blue]🚀 Mini Lakehouse Pipeline Interattiva")
    )

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
    table.add_column("Opzione", style=None, justify="center")
    table.add_column("Descrizione", style=None, justify="left")
    for key, descr in options.items():
        table.add_row(key, descr)
    console.print(table)

    # lista dei comandi per “Tutti i passaggi”
    full_pipeline = [
        ("poetry run dbt clean", "Clean"),
        ("poetry run dbt deps", "Deps"),
        ("poetry run dbt seed", "Seed"),
        ("poetry run dbt run", "Run"),
        ("poetry run dbt test", "Test"),
        ("poetry run dbt docs generate", "Docs Generate"),
        ("poetry run python audit/export_marts.py", "Audit Export"),
        ("make coverage", "Coverage"),
        ("make quality-report", "Quality Report"),
    ]

    while True:
        choice = Prompt.ask(f"[{PALETTE['accent']}]Seleziona un'opzione")
        match choice:
            case "1":
                run_step("Clean", full_pipeline[0][0], working_dir="dbt")
            case "2":
                run_step("Deps", full_pipeline[1][0], working_dir="dbt")
            case "3":
                run_step("Seed", full_pipeline[2][0], working_dir="dbt")
            case "4":
                run_step("Run", full_pipeline[3][0], working_dir="dbt")
            case "5":
                run_step("Test", full_pipeline[4][0], working_dir="dbt")
            case "6":
                run_step("Docs Generate", full_pipeline[5][0], working_dir="dbt")
            case "7":
                run_step("Audit Export", full_pipeline[6][0])
            case "8":
                run_step("Coverage", full_pipeline[7][0])
            case "9":
                run_step("Quality Report", full_pipeline[8][0])
            case "10":
                if Confirm.ask("Eseguire tutta la pipeline?"):
                    for cmd, desc in full_pipeline:
                        wd = "dbt" if cmd.startswith("poetry run dbt") else "."
                        run_step(desc, cmd, working_dir=wd)
            case "11":
                console.print(f"[{PALETTE['dim']}]Uscita.")
                sys.exit(0)
            case _:
                console.print(f"[{PALETTE['warning']}]⚠️ Scelta non valida.")


@app.command()
def ci_mode():
    """Esegue la pipeline completa in modalità CI"""
    console.print(Panel.fit("[bold white on blue]🤖 Esecuzione in modalità CI"))

    ci_commands = [
        ("poetry run dbt clean", "Clean"),
        ("poetry run dbt deps", "Deps"),
        ("poetry run dbt seed", "Seed"),
        ("poetry run dbt run", "Run"),
        ("poetry run dbt test", "Test"),
        ("poetry run dbt docs generate", "Docs Generate"),
        ("poetry run python audit/export_marts.py", "Audit Export"),
        ("make coverage", "Coverage"),
        ("make quality-report", "Quality Report"),
    ]

    for cmd, desc in ci_commands:
        wd = "dbt" if cmd.startswith("poetry run dbt") else "."
        run_step(desc, cmd, working_dir=wd)


if __name__ == "__main__":
    app()
