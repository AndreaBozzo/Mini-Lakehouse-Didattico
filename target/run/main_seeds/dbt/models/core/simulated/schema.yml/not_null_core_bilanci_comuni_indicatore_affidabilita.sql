select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select indicatore_affidabilita
from "warehouse"."main_main_core"."core_bilanci_comuni"
where indicatore_affidabilita is null



      
    ) dbt_internal_test