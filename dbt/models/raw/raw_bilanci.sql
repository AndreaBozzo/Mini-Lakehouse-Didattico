--dbt/models/raw/raw_bilanci--
SELECT * FROM {{ ref('bilanci_comunali_sample') }}
