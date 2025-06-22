SELECT *
FROM {{ ref('core_bilanci_comuni') }}
WHERE anno < 2000 OR anno > 2025
