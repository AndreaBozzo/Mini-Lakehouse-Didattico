SELECT *
FROM {{ ref('core_bilanci_comuni') }}
WHERE entrate < 0
