{% macro delta_percentuale_flag(col1, col2, soglia) %}
    case
        when {{ col2 }} is null then false
        when abs({{ col1 }} - {{ col2 }}) / nullif({{ col2 }}, 0) > {{ soglia }} then true
        else false
    end
{% endmacro %}