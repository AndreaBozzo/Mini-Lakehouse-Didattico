
  
  create view "warehouse"."main"."mart_audit_log__dbt_tmp" as (
    

with audit as (

    select *
    from "warehouse"."main"."core_audit_flags"

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
  );
