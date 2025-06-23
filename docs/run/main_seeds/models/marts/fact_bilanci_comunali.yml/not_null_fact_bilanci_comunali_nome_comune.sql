
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select nome_comune
from "warehouse"."main_main_marts"."fact_bilanci_comunali"
where nome_comune is null



  
  
      
    ) dbt_internal_test