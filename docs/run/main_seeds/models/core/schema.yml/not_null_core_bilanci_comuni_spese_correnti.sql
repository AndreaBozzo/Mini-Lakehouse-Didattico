
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select spese_correnti
from "warehouse"."main_main_core"."core_bilanci_comuni"
where spese_correnti is null



  
  
      
    ) dbt_internal_test