{{ config(materialized='view') }}

SELECT
  codice_comune,
  nome_comune,
  anno,
  codice_siope AS tipologia,
  descrizione_siope AS descrizione
FROM {{ ref('stg_movimenti_bilancio') }}
