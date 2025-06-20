{{ config(materialized='table') }}

with base as (

    select
        codice_comune,
        nome_comune,
        anno,
        entrate,
        spese,
        entrate - spese as saldo
    from {{ ref('core_bilanci_comuni') }}

),

lagged as (

    select
        *,
        lag(entrate) over (partition by codice_comune order by anno) as entrate_anno_prec,
        lag(spese) over (partition by codice_comune order by anno) as spese_anno_prec
    from base

),

audit as (

    select
        *,
        {{ test_delta_percentuale('entrate', 'entrate_anno_prec', 0.5) }} as flag_var_entrate,
        {{ test_delta_percentuale('spese', 'spese_anno_prec', 0.5) }} as flag_var_spese,
        case when saldo < 0 then true else false end as flag_saldo_negativo,
        case when entrate is null or spese is null then true else false end as flag_valori_nulli
    from lagged

)

select * from audit
