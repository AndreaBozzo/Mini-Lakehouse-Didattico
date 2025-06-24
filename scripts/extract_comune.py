import argparse
from pathlib import Path

import pandas as pd


def extract_comune(csv_path: str, comune: str, anno: int):
    print(f"🔍 Caricamento CSV da: {csv_path}")
    chunksize = 50_000
    target_rows = []

    COLONNA_COMUNE = "Descrizione Ente BDAP"

    for chunk in pd.read_csv(csv_path, chunksize=chunksize, encoding="latin1", sep=";"):
        if COLONNA_COMUNE not in chunk.columns:
            print(f"❌ Colonna '{COLONNA_COMUNE}' not found. {list(chunk.columns)}")
            return
        # Variante più conservativa
        filtered = chunk[
            chunk[COLONNA_COMUNE]
            .str.upper()
            .str.contains(f"COMUNE DI {comune.upper()}")
        ]

        if not filtered.empty:
            target_rows.append(filtered)

    if not target_rows:
        print(f"❌ Nessun dato trovato per il comune '{comune}'")
        return

    df_final = pd.concat(target_rows)
    print(f"✅ Righe trovate: {len(df_final)}")
    target_dir = Path(f"data/public/siope_it/{comune.lower()}")
    target_dir.mkdir(parents=True, exist_ok=True)
    output_path = target_dir / f"{anno}.csv"
    df_final.to_csv(output_path, index=False, encoding="utf-8", sep=";")
    print(f"✅ File salvato in: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Estrai dati di un singolo comune dal CSV SIOPE completo."
    )
    parser.add_argument("--csv-path", required=True, help="Path del CSV SIOPE completo")
    parser.add_argument(
        "--comune", required=True, help="Nome del comune (es. 'milano')"
    )
    parser.add_argument("--anno", type=int, required=True, help="Anno (es. 2016)")
    args = parser.parse_args()

    extract_comune(args.csv_path, args.comune, args.anno)
