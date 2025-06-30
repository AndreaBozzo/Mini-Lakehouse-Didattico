--audit_base.sql
SELECT
    codice_comune,
    anno,
    COUNT(*) AS n_righe
FROM {{ ref('core_bilanci_comuni') }}
GROUP BY codice_comune, anno
HAVING COUNT(*) > 1
ORDER BY n_righe DESC
