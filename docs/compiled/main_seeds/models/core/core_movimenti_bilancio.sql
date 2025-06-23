

SELECT
  codice_comune,
  nome_comune,
  anno,
  codice_siope AS tipologia,
  descrizione_siope AS descrizione
FROM "warehouse"."main_stg"."stg_movimenti_bilancio"