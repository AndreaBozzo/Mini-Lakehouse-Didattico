
  
    
    

    create  table
      "warehouse"."main"."fatti_bilanci__dbt_tmp"
  
    as (
      SELECT
    codice_comune,
    nome_comune,
    anno,
    SUM(entrate) AS totale_entrate,
    SUM(spese) AS totale_spese,
    SUM(entrate - spese) AS saldo
FROM "warehouse"."main"."core_bilanci_comuni"
GROUP BY codice_comune, nome_comune, anno
ORDER BY anno, codice_comune
    );
  
  