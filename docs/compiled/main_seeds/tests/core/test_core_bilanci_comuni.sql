-- tests/core/test_core_bilanci_comuni.sql
-- Fallisce se la tabella core_bilanci_comuni è vuota
SELECT 1 AS error
WHERE NOT EXISTS (
  SELECT 1 FROM "warehouse"."main_main_core"."core_bilanci_comuni"
)