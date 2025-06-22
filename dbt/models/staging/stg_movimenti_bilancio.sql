{{ config(materialized='view') }}

select
    cast(codice_comune as int) as codice_comune,
    nome_comune,
    cast(anno as int) as anno,
    codice_siope,
    descrizione_siope,
    tipologia,
    cast(valore as bigint) as valore
from {{ ref('bilanci_voci_sample') }}
where codice_comune is not null and codice_siope is not null and valore is not null
