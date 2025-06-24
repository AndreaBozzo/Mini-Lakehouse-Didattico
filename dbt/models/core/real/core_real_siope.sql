-- models/core/real/core_real_siope.sql
{{ config(tags=["real"]) }}
with base as (
    select *
    from {{ ref('stg_siope_real') }}
),

final as (
    select
        codice_belfiore,
        denominazione_comune,
        anno,
        mese,
        titolo,
        categoria,
        importo_accertato,
        coalesce(importo_incassato, 0.0) as importo_incassato
    from base
)

select * from final
