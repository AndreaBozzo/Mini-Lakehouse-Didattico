import os
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from cli.core import audit_log, export_marts, post_checks, run_pipeline
from cli.export_utils import validate_export_schema
from cli.utils import PALETTE, ensure_duckdb_path_exists, run_step

# Forza UTF-8 anche nei child-process dbt su Windows
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

app = typer.Typer()
console = Console()


@app.command()
def run(real_data: bool = False, ci_mode: bool = False, verbose: bool = False):
    """Esegue la pipeline ETL (run dbt + test + docs)."""
    ensure_duckdb_path_exists()
    run_pipeline(real_data, ci_mode, verbose)
    console.print(f"[{PALETTE['warning']}]ℹ️ Per visualizzare la documentazione:")
    console.print(f"[{PALETTE['accent']}]poetry run python cli/pipeline.py docs-serve")


@app.command()
def docs_serve():
    """Avvia il server della documentazione dbt."""
    run_step("Docs Serve", "poetry run dbt docs serve --port 8000", check=False)


@app.command()
def export(real_data: bool = False, ci_mode: bool = False, verbose: bool = False):
    """Esporta i marts in CSV e Parquet, con validazione schema."""
    ensure_duckdb_path_exists()
    export_marts(real_data, ci_mode, verbose)

    export_dir = Path("exports/csv")
    possible_paths = [
        Path("dbt/models/marts/real/schema.yml"),
        Path("dbt/models/marts/simulated/schema.yml"),
    ]

    schema_path = next((p for p in possible_paths if p.exists()), None)
    if not schema_path:
        console.print(
            f"[{PALETTE['error']}]❌ Nessun file schema.yml trovato nei path attesi."
        )
        raise typer.Exit(code=1)

    if not export_dir.exists():
        console.print(f"[{PALETTE['error']}]❌ Export non trovato in: {export_dir}")
        raise typer.Exit(code=1)

    console.rule(f"[{PALETTE['accent']}]🧪 Validazione Schema CSV")
    failures = 0
    for csv_file in export_dir.glob("*.csv"):
        if not validate_export_schema(csv_file, schema_path):
            failures += 1

    if failures > 0:
        console.print(
            f"[{PALETTE['error']}]❌ {failures} file non conformi allo schema."
        )
        if ci_mode:
            raise typer.Exit(code=1)
    else:
        console.print(f"[{PALETTE['success']}]✅ Tutti i file validati con successo.")


@app.command()
def audit(ci_mode: bool = False):
    """Confronta gli snapshot attuali con quelli precedenti."""
    audit_log(ci_mode)


@app.command()
def ci_mode(real_data: bool = False):
    """Esegue l'intera pipeline in modalità CI."""
    console.print(Panel.fit("> Esecuzione in modalità CI"))
    ensure_duckdb_path_exists()

    run_pipeline(real_data=real_data, ci_mode=True)
    export_marts(real_data=real_data, ci_mode=True)
    audit_log(ci_mode=True)
    post_checks()


@app.command()
def interactive():
    """Avvia la pipeline in modalità interattiva."""
    ensure_duckdb_path_exists()
    console.print(Panel.fit("> Mini Lakehouse Pipeline Interattiva"))

    options = {
        "1": "Run pipeline",
        "2": "Export marts",
        "3": "Audit log",
        "4": "Coverage",
        "5": "Quality Report",
        "6": "Esci",
        "7": "Tutti i passaggi",
    }

    table = Table(title="Passaggi disponibili", header_style=PALETTE["accent"])
    table.add_column("Opzione", justify="center")
    table.add_column("Descrizione")
    for key, descr in options.items():
        table.add_row(key, descr)
    console.print(table)

    while True:
        choice = Prompt.ask(f"[{PALETTE['accent']}]Seleziona un'opzione")
        match choice:
            case "1":
                real = Confirm.ask("Usare dati reali?")
                verbose = Confirm.ask("Output dettagliato?")
                run(real_data=real, verbose=verbose)
            case "2":
                real = Confirm.ask("Usare dati reali?")
                verbose = Confirm.ask("Output dettagliato?")
                export(real_data=real, verbose=verbose)
            case "3":
                audit()
            case "4":
                post_checks()
            case "5":
                real = Confirm.ask("Usare dati reali?")
                verbose = Confirm.ask("Output dettagliato?")
                run(real_data=real, verbose=verbose)
                export(real_data=real, verbose=verbose)
                audit()
                post_checks()
            case "6":
                console.print(f"[{PALETTE['dim']}]Uscita.")
                sys.exit(0)
            case "7":
                real = Confirm.ask("Usare dati reali?")
                verbose = Confirm.ask("Output dettagliato?")
                run(real_data=real, verbose=verbose)
                export(real_data=real, verbose=verbose)
                audit()
                post_checks()
            case _:
                console.print(f"[{PALETTE['warning']}]⚠️ Scelta non valida.")


@app.command()
def snapshot():
    """Confronta i file CSV attuali con l'ultima snapshot salvata."""
    run_step("Snapshot check", "poetry run python -m audit.snapshot_test")


if __name__ == "__main__":
    app()
