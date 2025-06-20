SELECT *
FROM {{ ref('core_bilanci_comuni') }}
WHERE spese < 0
