-- models/marts/real/mart_siope_totali_mensili.sql


select
    codice_belfiore,
    denominazione_comune,
    anno,
    mese,
    titolo,
    categoria,
    sum(importo_accertato) as totale_accertato,
    sum(importo_incassato) as totale_incassato
from "warehouse"."main"."core_real_siope"
group by all
order by anno, mese, codice_belfiore