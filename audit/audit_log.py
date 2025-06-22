import duckdb
import pandas as pd
from datetime import datetime
from rich.console import Console
from rich.table import Table
from pathlib import Path

# Config
DB_PATH = "dbt/data/warehouse/warehouse.duckdb"
OUTPUT_DIR = Path("audit/exports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
console = Console()

def estrai_anomalie():
    con = duckdb.connect(DB_PATH)
    query = """
        SELECT * FROM main.core_audit_flags
        WHERE flag_var_entrate OR flag_var_spese OR flag_saldo_negativo OR flag_valori_nulli
    """
    df = con.execute(query).fetch_df()
    con.close()
    return df

def stampa_sintesi(df: pd.DataFrame):
    table = Table(title="📊 Sintesi Anomalie nei Bilanci", show_lines=True)
    table.add_column("Tipo", style="cyan", justify="left")
    table.add_column("Conteggio", style="magenta", justify="right")

    for col in ["flag_var_entrate", "flag_var_spese", "flag_saldo_negativo", "flag_valori_nulli"]:
        count = df[col].sum()
        table.add_row(col, str(count))

    table.add_row("Totale righe anomale", str(len(df)), style="bold yellow")
    console.print(table)

def esporta_csv(df: pd.DataFrame):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"anomalie_bilanci_{ts}.csv"
    df.to_csv(output_path, index=False)
    console.print(f"[green]✅ CSV esportato:[/green] {output_path}")

if __name__ == "__main__":
    console.print("[bold]🔍 Avvio estrazione anomalie dai bilanci...[/bold]\n")
    df_anomalie = estrai_anomalie()

    if df_anomalie.empty:
        console.print("[green]✅ Nessuna anomalia rilevata.[/green]")
    else:
        stampa_sintesi(df_anomalie)
        esporta_csv(df_anomalie)
        console.print("[bold]🔍 Estrazione completata![/bold]")