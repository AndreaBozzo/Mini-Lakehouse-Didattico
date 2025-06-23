
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select entrate_tributarie
from "warehouse"."main_stg"."stg_bilanci_comuni"
where entrate_tributarie is null



  
  
      
    ) dbt_internal_test