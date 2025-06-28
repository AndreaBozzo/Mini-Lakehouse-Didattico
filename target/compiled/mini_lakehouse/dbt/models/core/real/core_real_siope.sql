-- models/core/real/core_real_siope.sql

with base as (
    select *
    from "warehouse"."main"."stg_siope_real"
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