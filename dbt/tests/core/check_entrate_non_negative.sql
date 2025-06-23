-- tests/core/check_entrate_non_negative.sql
WITH invalid AS (
  SELECT *
  FROM {{ ref('core_bilanci_comuni') }}
  WHERE entrate_tributarie < 0
)
SELECT * FROM invalid
