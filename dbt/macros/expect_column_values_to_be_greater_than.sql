-- macros/expect_column_values_to_be_greater_than.sql
{% macro expect_column_values_to_be_greater_than(model, column_name, value) %}
    SELECT
        *
    FROM {{ model }}
    WHERE {{ column_name }} <= {{ value }}
{% endmacro %}
