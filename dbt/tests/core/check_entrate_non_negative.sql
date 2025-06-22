SELECT * FROM {{ ref('core_bilanci_comuni') }}
WHERE entrate_tributarie < 0
