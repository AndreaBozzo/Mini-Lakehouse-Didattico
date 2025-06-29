-- File: dbt/models/marts/simulated/fact_bilanci_comunali.sql
{{ config(materialized='table', schema='main_marts', contracts=true) }}

SELECT
    codice_comune,
    nome_comune,
    anno,

    SUM(entrate_tributarie) AS totale_entrate,
    SUM(spese_correnti) AS totale_spese,
    SUM(entrate_tributarie - spese_correnti) AS saldo,

    -- Propagazione flag: almeno una riga con flag attivo
    BOOL_OR(flag_dato_incompleto) AS flag_dato_incompleto,

    -- Media affidabilità sulle righe aggregate
    ROUND(AVG(indicatore_affidabilita), 2) AS indicatore_affidabilita

FROM {{ ref('core_bilanci_comuni') }}
GROUP BY codice_comune, nome_comune, anno
ORDER BY anno, codice_comune
