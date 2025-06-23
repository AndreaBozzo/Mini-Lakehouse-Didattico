
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select id_hash
from "warehouse"."main_main_core"."core_bilanci_comuni"
where id_hash is null



  
  
      
    ) dbt_internal_test