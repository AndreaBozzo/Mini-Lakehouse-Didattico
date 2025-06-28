select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        flag_dato_incompleto as value_field,
        count(*) as n_records

    from "warehouse"."main_main_core"."core_bilanci_comuni"
    group by flag_dato_incompleto

)

select *
from all_values
where value_field not in (
    'True','False'
)



      
    ) dbt_internal_test