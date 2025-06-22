{{ config(materialized='table') }}

with base as (
    select
        anno,
        codice_comune,
        nome_comune,
        codice_siope,
        descrizione_siope,
        sum(valore) as totale_entrate
    from {{ ref('core_movimenti_bilancio') }}
    where tipologia = 'entrata'
    group by 1, 2, 3, 4, 5
)

select * from base
