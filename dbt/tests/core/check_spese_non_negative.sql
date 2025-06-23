-- tests/core/check_spese_non_negative.sql
WITH invalid AS (
  SELECT *
  FROM {{ ref('core_bilanci_comuni') }}
  WHERE spese_correnti < 0
)
SELECT * FROM invalid
