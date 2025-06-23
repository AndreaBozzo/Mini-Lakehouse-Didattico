-- tests/core/test_core_bilanci_comuni.sql
-- Fallisce se la tabella core_bilanci_comuni è vuota
SELECT 1 AS error
WHERE NOT EXISTS (
  SELECT 1 FROM {{ ref('core_bilanci_comuni') }}
)
