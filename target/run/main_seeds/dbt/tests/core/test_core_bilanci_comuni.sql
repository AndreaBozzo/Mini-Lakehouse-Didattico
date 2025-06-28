select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      -- tests/core/test_core_bilanci_comuni.sql
-- Fallisce se la tabella core_bilanci_comuni è vuota
SELECT 1 AS error
WHERE NOT EXISTS (
  SELECT 1 FROM "warehouse"."main_main_core"."core_bilanci_comuni"
)
      
    ) dbt_internal_test