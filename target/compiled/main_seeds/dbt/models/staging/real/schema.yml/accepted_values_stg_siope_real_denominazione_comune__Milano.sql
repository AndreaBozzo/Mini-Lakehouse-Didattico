
    
    

with all_values as (

    select
        denominazione_comune as value_field,
        count(*) as n_records

    from "warehouse"."main_stg"."stg_siope_real"
    group by denominazione_comune

)

select *
from all_values
where value_field not in (
    'Milano'
)


