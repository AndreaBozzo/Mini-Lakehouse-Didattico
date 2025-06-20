SELECT
    {{ dbt_utils.generate_surrogate_key(['codice_comune', 'anno']) }} AS id_hash,
    CAST(codice_comune AS INT) AS codice_comune,
    nome_comune,
    CAST(anno AS INT) AS anno,
    CAST(entrate_tributarie AS BIGINT) AS entrate,
    CAST(spese_correnti AS BIGINT) AS spese
FROM {{ ref('stg_bilanci_comuni') }}
WHERE 
    codice_comune IS NOT NULL
    AND anno IS NOT NULL
    AND entrate_tributarie IS NOT NULL
    AND spese_correnti IS NOT NULL
