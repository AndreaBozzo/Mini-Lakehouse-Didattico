
  
  create view "warehouse"."main"."stg_bilanci_comuni__dbt_tmp" as (
    

SELECT
  codice_comune,
  nome_comune,
  anno,
  entrate_tributarie,
  spese_correnti,
  entrate_tributarie - spese_correnti AS saldo
FROM raw_bilanci
  );
