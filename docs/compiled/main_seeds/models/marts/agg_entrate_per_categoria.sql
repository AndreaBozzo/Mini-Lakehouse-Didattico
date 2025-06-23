

with joined as (
    select
        mv.codice_comune,
        mv.anno,
        mv.tipologia    as categoria,
        mv.descrizione  as descrizione,
        cb.entrate_tributarie
    from "warehouse"."main_core"."core_movimenti_bilancio" as mv
    join "warehouse"."main_main_core"."core_bilanci_comuni" as cb
      on mv.codice_comune = cb.codice_comune
     and mv.anno = cb.anno
)

select
    categoria,
    descrizione,
    count(*)               as numero_movimenti,
    sum(entrate_tributarie) as totale_entrate
from joined
group by categoria, descrizione
order by totale_entrate desc