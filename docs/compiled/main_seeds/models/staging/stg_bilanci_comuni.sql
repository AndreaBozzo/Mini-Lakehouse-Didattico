

SELECT
  codice_comune,
  nome_comune,
  anno,
  entrate_tributarie,
  spese_correnti,
  entrate_tributarie - spese_correnti AS saldo
FROM "warehouse"."main"."raw_bilanci_comunali"