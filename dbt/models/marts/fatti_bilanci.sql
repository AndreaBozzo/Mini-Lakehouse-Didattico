SELECT
    codice_comune,
    nome_comune,
    anno,
    SUM(entrate_tributarie) AS totale_entrate,
    SUM(spese_correnti) AS totale_spese,
    SUM(entrate_tributarie - spese_correnti) AS saldo
FROM {{ ref('core_bilanci_comuni') }}
GROUP BY codice_comune, nome_comune, anno
ORDER BY anno, codice_comune
