
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select totale_entrate
from "warehouse"."main_main_marts"."fact_bilanci_comunali"
where totale_entrate is null



  
  
      
    ) dbt_internal_test