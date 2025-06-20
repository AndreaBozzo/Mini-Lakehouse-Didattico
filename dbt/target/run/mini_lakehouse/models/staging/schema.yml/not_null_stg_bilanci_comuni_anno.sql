
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select anno
from "warehouse"."main"."stg_bilanci_comuni"
where anno is null



  
  
      
    ) dbt_internal_test