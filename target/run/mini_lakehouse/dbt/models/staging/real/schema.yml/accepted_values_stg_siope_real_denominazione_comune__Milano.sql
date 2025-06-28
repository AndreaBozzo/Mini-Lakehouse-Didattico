select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        denominazione_comune as value_field,
        count(*) as n_records

    from "warehouse"."main"."stg_siope_real"
    group by denominazione_comune

)

select *
from all_values
where value_field not in (
    'Milano'
)



      
    ) dbt_internal_test