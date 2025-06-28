select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select totale_accertato
from "warehouse"."main"."mart_siope_totali_mensili"
where totale_accertato is null



      
    ) dbt_internal_test