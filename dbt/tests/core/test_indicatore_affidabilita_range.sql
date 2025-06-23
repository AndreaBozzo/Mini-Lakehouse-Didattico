-- tests/core/test_indicatore_affidabilita_range.sql
SELECT *
FROM {{ ref('core_bilanci_comuni') }}
WHERE indicatore_affidabilita < 0
   OR indicatore_affidabilita > 100
