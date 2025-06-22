select *
from {{ ref('core_bilanci_comuni') }}
where anno < 2000