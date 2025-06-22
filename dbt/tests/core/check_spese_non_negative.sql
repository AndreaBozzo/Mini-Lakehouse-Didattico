SELECT * FROM {{ ref('core_bilanci_comuni') }}
WHERE spese_correnti < 0
