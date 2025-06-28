
    
    

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


