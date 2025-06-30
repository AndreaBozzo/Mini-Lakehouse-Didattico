-- File: dbt/models/audit/mart_audit_log.sql
{{ config(materialized='view', schema='main_marts_simulated', tags=["simulated"]) }}

with audit as (

    select *
    from {{ ref('core_audit_flags') }}

),

anomalie as (

    select *
    from audit
    where
        flag_var_entrate = true
        or flag_var_spese = true
        or flag_saldo_negativo = true
        or flag_valori_nulli = true

)

select * from anomalie
