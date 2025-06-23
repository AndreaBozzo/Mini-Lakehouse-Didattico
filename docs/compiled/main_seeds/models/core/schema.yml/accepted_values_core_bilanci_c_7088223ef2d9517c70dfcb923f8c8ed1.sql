
    
    

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


