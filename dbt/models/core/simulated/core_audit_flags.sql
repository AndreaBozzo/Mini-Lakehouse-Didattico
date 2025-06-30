-- File: dbt/models/audit/core_audit_flags.sql
{{ config(materialized='table', schema='main_core', tags=["simulated"]) }}

with base as (

    select
        codice_comune,
        nome_comune,
        anno,
        entrate_tributarie,
        spese_correnti,
        entrate_tributarie - spese_correnti as saldo
    from {{ ref('core_bilanci_comuni') }}

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
        {{ delta_percentuale_flag('entrate_tributarie', 'entrate_anno_prec', 0.5) }} as flag_var_entrate,
        {{ delta_percentuale_flag('spese_correnti', 'spese_anno_prec', 0.5) }} as flag_var_spese,

        case when saldo < 0 then true else false end as flag_saldo_negativo,
        case when entrate_tributarie is null or spese_correnti is null then true else false end as flag_valori_nulli
    from lagged

)

select * from audit
