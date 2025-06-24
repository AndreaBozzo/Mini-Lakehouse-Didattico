import pandas as pd

df = pd.read_csv(
    "data/public/siope_it/lombardia/2016_entrate.csv", encoding="latin1", sep=";"
)
print(df["Descrizione Ente BDAP"].dropna().unique())
