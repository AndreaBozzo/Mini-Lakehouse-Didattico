SELECT
    CAST(codice_comune AS INT) AS codice_comune,
    TRIM(nome_comune) AS nome_comune,
    CAST(anno AS INT) AS anno,
    CAST(entrate_tributarie AS BIGINT) AS entrate,
    CAST(spese_correnti AS BIGINT) AS spese
FROM "warehouse"."main"."stg_bilanci_comuni"
WHERE 
    codice_comune IS NOT NULL
    AND anno IS NOT NULL
    AND entrate_tributarie IS NOT NULL
    AND spese_correnti IS NOT NULL