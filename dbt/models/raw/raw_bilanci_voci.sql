{{ config(materialized='view') }}

SELECT
  codice_comune,
  nome_comune,
  anno,
  codice_siope,
  descrizione_siope
FROM {{ ref('bilanci_voci_sample') }}
