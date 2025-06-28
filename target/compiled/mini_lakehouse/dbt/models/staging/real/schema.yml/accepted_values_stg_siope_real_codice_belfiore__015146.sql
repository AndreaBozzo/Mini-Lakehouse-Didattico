
    
    

with all_values as (

    select
        codice_belfiore as value_field,
        count(*) as n_records

    from "warehouse"."main"."stg_siope_real"
    group by codice_belfiore

)

select *
from all_values
where value_field not in (
    '015146'
)


