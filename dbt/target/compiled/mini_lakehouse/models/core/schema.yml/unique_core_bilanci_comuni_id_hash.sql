
    
    

select
    id_hash as unique_field,
    count(*) as n_records

from "warehouse"."main"."core_bilanci_comuni"
where id_hash is not null
group by id_hash
having count(*) > 1


