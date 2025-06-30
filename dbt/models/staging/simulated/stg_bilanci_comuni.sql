{{ config(
    materialized='view',
    schema='main_stg',
    tags=["simulated"]
) }}

SELECT
  codice_comune,
  nome_comune,
  anno,
  entrate_tributarie,
  spese_correnti,
  entrate_tributarie - spese_correnti AS saldo
FROM {{ ref('raw_bilanci_comunali') }}
