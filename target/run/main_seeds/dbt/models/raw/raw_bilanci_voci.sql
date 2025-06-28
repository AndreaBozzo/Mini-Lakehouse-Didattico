
  
  create view "warehouse"."main"."raw_bilanci_voci__dbt_tmp" as (
    

SELECT
  codice_comune,
  nome_comune,
  anno,
  codice_siope,
  descrizione_siope
FROM "warehouse"."main_seeds"."bilanci_voci_sample"
  );
