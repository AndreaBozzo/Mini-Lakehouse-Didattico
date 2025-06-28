select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      -- tests/core/check_anno_range.sql
WITH invalid AS (
  SELECT * 
  FROM "warehouse"."main_main_core"."core_bilanci_comuni"
  WHERE anno < 1900
    OR anno > EXTRACT(year FROM CURRENT_TIMESTAMP)
)
SELECT * FROM invalid
      
    ) dbt_internal_test