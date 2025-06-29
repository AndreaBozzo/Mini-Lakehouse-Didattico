
  
    
    

    create  table
      "warehouse"."main_main_core"."core_bilanci_comuni__dbt_tmp"
  
    as (
      -- File: dbt/models/core/simulated/core_bilanci_comuni.sql


SELECT
    md5(cast(coalesce(cast(codice_comune as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(anno as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS id_hash,
    CAST(codice_comune AS INT) AS codice_comune,
    CAST(nome_comune AS TEXT) AS nome_comune,
    CAST(anno AS INT) AS anno,
    CAST(entrate_tributarie AS BIGINT) AS entrate_tributarie,
    CAST(spese_correnti AS BIGINT) AS spese_correnti,

    -- Flag se valori critici sono null
    CASE 
        WHEN entrate_tributarie IS NULL OR spese_correnti IS NULL THEN TRUE
        ELSE FALSE
    END AS flag_dato_incompleto,

    -- Indicatore euristico qualità (semplificato per coerenza col mart)
    100
    - 50 * CASE WHEN entrate_tributarie IS NULL THEN 1 ELSE 0 END
    - 50 * CASE WHEN spese_correnti IS NULL THEN 1 ELSE 0 END
    AS indicatore_affidabilita

FROM "warehouse"."main_stg"."stg_bilanci_comuni"
WHERE 
    codice_comune IS NOT NULL
    AND anno IS NOT NULL
    );
  
  