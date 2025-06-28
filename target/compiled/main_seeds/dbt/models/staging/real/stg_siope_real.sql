-- models/staging/real/stg_siope_real.sql

with source as (
    select *
    from read_csv_auto('data/public/siope_it/milano/2016.csv', delim=';', header=True)
),

renamed as (
    select
        '015146' as codice_belfiore,
        'Milano' as denominazione_comune,

        split_part("Anno/Mese calendario", '/', 1)::integer as anno,
        split_part("Anno/Mese calendario", '/', 2)::integer as mese,

        "Descrizione Titolo CG" as titolo,
        "Descrizione CG" as categoria,

        "Importo cumulato"::double as importo_accertato,
        NULL::double as importo_incassato

    from source
)

select * from renamed