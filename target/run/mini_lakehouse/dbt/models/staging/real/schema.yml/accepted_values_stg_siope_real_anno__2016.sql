select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        anno as value_field,
        count(*) as n_records

    from "warehouse"."main"."stg_siope_real"
    group by anno

)

select *
from all_values
where value_field not in (
    '2016'
)



      
    ) dbt_internal_test