
    
    

with all_values as (

    select
        mese as value_field,
        count(*) as n_records

    from "warehouse"."main_main_marts"."mart_siope_totali_mensili"
    group by mese

)

select *
from all_values
where value_field not in (
    '1','2','3','4','5','6','7','8','9','10','11','12'
)


