-- File: dbt/models/marts/simulated/mart_finanza_locale.sql
{{ config(materialized='table', contracts=true, tags=["simulated"]) }}

with bilanci as (

    select
        codice_comune,
        nome_comune,
        anno,
        entrate_tributarie,
        spese_correnti,
        entrate_tributarie - spese_correnti as saldo
    from {{ ref('core_bilanci_comuni') }}

),

audit as (

    select
        codice_comune,
        anno,
        flag_var_entrate,
        flag_var_spese,
        flag_saldo_negativo,
        flag_valori_nulli,
        flag_var_entrate or flag_var_spese or flag_saldo_negativo or flag_valori_nulli as flag_anomalia
    from {{ ref('core_audit_flags') }}

),

finale as (

    select
        b.codice_comune,
        b.nome_comune,
        b.anno,
        b.entrate_tributarie,
        b.spese_correnti,
        b.saldo,
        coalesce(a.flag_anomalia, false) as flag_anomalia
    from bilanci b
    left join audit a
      on b.codice_comune = a.codice_comune
     and b.anno = a.anno

)

select * from finale
