
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select flag_dato_incompleto
from "warehouse"."main_main_marts"."fact_bilanci_comunali"
where flag_dato_incompleto is null



  
  
      
    ) dbt_internal_test