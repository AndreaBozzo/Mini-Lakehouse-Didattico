select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select categoria
from "warehouse"."main"."stg_siope_real"
where categoria is null



      
    ) dbt_internal_test