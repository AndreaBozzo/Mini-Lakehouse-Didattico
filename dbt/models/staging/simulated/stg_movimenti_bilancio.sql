{{ config(
    materialized='view',
    schema='main_stg',
    tags=["simulated"]
) }}

SELECT
  codice_comune,
  nome_comune,
  anno,
  codice_siope,
  descrizione_siope
FROM {{ ref('raw_bilanci_voci') }}
