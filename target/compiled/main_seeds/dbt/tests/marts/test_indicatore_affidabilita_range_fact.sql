-- tests/marts/test_indicatore_affidabilita_range_fact.sql
select *
from "warehouse"."main_main_marts"."fact_bilanci_comunali"
where indicatore_affidabilita < 0
   or indicatore_affidabilita > 100