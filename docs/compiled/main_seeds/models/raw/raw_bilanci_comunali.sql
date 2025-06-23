

SELECT
  codice_comune,
  -- Title-case “Roma” → “Roma”, “milano” → “Milano”
  upper(substring(nome_comune, 1, 1))
    || lower(substring(nome_comune, 2)) AS nome_comune,
  anno,
  entrate_tributarie,
  spese_correnti
FROM "warehouse"."main_seeds"."bilanci_comunali_sample"