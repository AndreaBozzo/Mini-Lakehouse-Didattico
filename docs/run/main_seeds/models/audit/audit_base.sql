
  
  create view "warehouse"."main"."audit_base__dbt_tmp" as (
    SELECT
    codice_comune,
    anno,
    COUNT(*) AS n_righe
FROM "warehouse"."main_main_core"."core_bilanci_comuni"
GROUP BY codice_comune, anno
HAVING COUNT(*) > 1
ORDER BY n_righe DESC
  );
