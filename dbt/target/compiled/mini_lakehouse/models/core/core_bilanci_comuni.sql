with fonte as (
    select
        codice_comune,
        initcap(nome_comune) as nome_comune,
        anno,
        entrate_tributarie,
        spese_correnti,
        entrate_tributarie - spese_correnti as saldo_corrente
    from "warehouse"."main"."stg_bilanci_comuni"
    where anno >= 2000
)

select * from fonte