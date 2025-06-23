

with base as (

    select
        codice_comune,
        nome_comune,
        anno,
        entrate_tributarie,
        spese_correnti,
        entrate_tributarie - spese_correnti as saldo
    from "warehouse"."main_main_core"."core_bilanci_comuni"

),

lagged as (

    select
        codice_comune,
        nome_comune,
        anno,
        entrate_tributarie,
        spese_correnti,
        saldo,
        lag(entrate_tributarie) over (partition by codice_comune order by anno) as entrate_anno_prec,
        lag(spese_correnti) over (partition by codice_comune order by anno) as spese_anno_prec
    from base

),

audit as (

    select
        codice_comune,
        nome_comune,
        anno,
        entrate_tributarie,
        spese_correnti,
        saldo,
        entrate_anno_prec,
        spese_anno_prec,
        
    case
        when entrate_anno_prec is null then false
        when abs(entrate_tributarie - entrate_anno_prec) / nullif(entrate_anno_prec, 0) > 0.5 then true
        else false
    end
 as flag_var_entrate,
        
    case
        when spese_anno_prec is null then false
        when abs(spese_correnti - spese_anno_prec) / nullif(spese_anno_prec, 0) > 0.5 then true
        else false
    end
 as flag_var_spese,

        case when saldo < 0 then true else false end as flag_saldo_negativo,
        case when entrate_tributarie is null or spese_correnti is null then true else false end as flag_valori_nulli
    from lagged

)

select * from audit