-- File: dbt/models/core/simulated/core_movimenti_bilancio.sql
{{ config(materialized='view', schema='main_core', tags=["simulated"]) }}

SELECT
  codice_comune,
  nome_comune,
  anno,
  codice_siope AS tipologia,
  descrizione_siope AS descrizione
FROM {{ ref('stg_movimenti_bilancio') }}
