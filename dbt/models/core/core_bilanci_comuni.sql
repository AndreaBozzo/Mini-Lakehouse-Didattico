with fonte as (
    select
        codice_comune,
        nome_comune,  -- rimosso initcap
        anno,
        entrate_tributarie,
        spese_correnti,
        entrate_tributarie - spese_correnti as saldo_corrente
    from {{ ref('stg_bilanci_comuni') }}
    where anno >= 2000
)

select * from fonte
