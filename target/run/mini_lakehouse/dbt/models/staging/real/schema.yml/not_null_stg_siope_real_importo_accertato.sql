select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select importo_accertato
from "warehouse"."main"."stg_siope_real"
where importo_accertato is null



      
    ) dbt_internal_test