-- models/raw/raw_bilanci.sql
select *
from read_csv_auto('../data/raw/bilanci_comunali_sample.csv', header=True)
