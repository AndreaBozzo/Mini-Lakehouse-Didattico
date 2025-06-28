select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select denominazione_comune
from "warehouse"."main"."stg_siope_real"
where denominazione_comune is null



      
    ) dbt_internal_test