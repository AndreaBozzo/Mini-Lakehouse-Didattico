{{ config(materialized='view') }}

select
    codice_comune,
    nome_comune,
    anno,
    codice_siope,
    descrizione_siope,
    tipologia,
    valore
from {{ ref('stg_movimenti_bilancio') }}
