select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select codice_belfiore
from "warehouse"."main"."stg_siope_real"
where codice_belfiore is null



      
    ) dbt_internal_test