
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- tests/core/check_entrate_non_negative.sql
WITH invalid AS (
  SELECT *
  FROM "warehouse"."main_main_core"."core_bilanci_comuni"
  WHERE entrate_tributarie < 0
)
SELECT * FROM invalid
  
  
      
    ) dbt_internal_test