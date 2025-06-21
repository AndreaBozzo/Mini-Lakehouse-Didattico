-- models/raw/raw_bilanci.sql
SELECT * FROM read_csv_auto('dbt/data/raw/bilanci_comunali_sample.csv', HEADER=TRUE)
