-- tests/core/check_spese_non_negative.sql
WITH invalid AS (
  SELECT *
  FROM "warehouse"."main_main_core"."core_bilanci_comuni"
  WHERE spese_correnti < 0
)
SELECT * FROM invalid