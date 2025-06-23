
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select codice_comune
from "warehouse"."main_stg"."stg_bilanci_comuni"
where codice_comune is null



  
  
      
    ) dbt_internal_test