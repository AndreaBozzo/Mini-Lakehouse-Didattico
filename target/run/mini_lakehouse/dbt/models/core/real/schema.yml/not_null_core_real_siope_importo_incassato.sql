select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select importo_incassato
from "warehouse"."main"."core_real_siope"
where importo_incassato is null



      
    ) dbt_internal_test