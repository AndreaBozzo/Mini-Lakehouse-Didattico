-- tests/core/check_anno_range.sql
WITH invalid AS (
  SELECT * 
  FROM "warehouse"."main_main_core"."core_bilanci_comuni"
  WHERE anno < 1900
    OR anno > EXTRACT(year FROM CURRENT_TIMESTAMP)
)
SELECT * FROM invalid