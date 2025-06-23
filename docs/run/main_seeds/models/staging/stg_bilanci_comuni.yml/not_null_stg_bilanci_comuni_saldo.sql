
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select saldo
from "warehouse"."main_stg"."stg_bilanci_comuni"
where saldo is null



  
  
      
    ) dbt_internal_test