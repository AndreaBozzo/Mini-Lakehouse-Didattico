## audit_log.py
# Script per estrarre e analizzare anomalie nei bilanci da `core_audit_flags`
import os
from datetime import datetime
from pathlib import Path

import duckdb
import pandas as pd
from rich.console import Console
from rich.table import Table

# Configurazione: percorso DB da variabile d'ambiente o default
DEFAULT_DB_PATH = "data/warehouse/warehouse.duckdb"
DB_PATH = os.environ.get("DUCKDB_PATH", DEFAULT_DB_PATH)
OUTPUT_DIR = Path("audit/exports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

console = Console()


def estrai_anomalie() -> pd.DataFrame:
    """
    Estrae tutte le righe con flag attivi da `core_audit_flags` del modello dbt.

    Restituisce:
        pd.DataFrame: Righe con almeno un'anomalia rilevata.
    """
    conn = duckdb.connect(DB_PATH)
    query = """
        SELECT *
        FROM main.core_audit_flags
        WHERE flag_var_entrate
           OR flag_var_spese
           OR flag_saldo_negativo
           OR flag_valori_nulli
    """
    df = conn.execute(query).fetch_df()
    conn.close()
    return df


def stampa_sintesi(df: pd.DataFrame) -> None:
    """
    Stampa una tabella di riepilogo con il conteggio per ogni tipo di flag di anomalia.

    Args:
        df (pd.DataFrame): DataFrame contenente le righe anomale.
    """
    table = Table(title="📊 Sintesi Anomalie nei Bilanci", show_lines=True)
    table.add_column("Tipo", style="cyan", justify="left")
    table.add_column("Conteggio", style="magenta", justify="right")

    for col in [
        "flag_var_entrate",
        "flag_var_spese",
        "flag_saldo_negativo",
        "flag_valori_nulli",
    ]:
        count = df[col].sum()
        table.add_row(col, str(count))

    table.add_row("Totale righe anomale", str(len(df)), style="bold yellow")
    console.print(table)


def esporta_csv(df: pd.DataFrame) -> None:
    """
    Esporta le anomalie in un file CSV timestampato nella cartella `audit/exports`.

    Args:
        df (pd.DataFrame): DataFrame contenente le anomalie da esportare.
    """
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
