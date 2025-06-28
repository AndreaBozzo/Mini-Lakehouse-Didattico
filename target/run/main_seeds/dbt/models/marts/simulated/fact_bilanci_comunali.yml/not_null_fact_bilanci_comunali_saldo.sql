select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select saldo
from "warehouse"."main_main_marts"."fact_bilanci_comunali"
where saldo is null



      
    ) dbt_internal_test