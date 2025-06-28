
  
  create view "warehouse"."main_stg"."stg_movimenti_bilancio__dbt_tmp" as (
    

SELECT
  codice_comune,
  nome_comune,
  anno,
  codice_siope,
  descrizione_siope
FROM "warehouse"."main"."raw_bilanci_voci"
  );
