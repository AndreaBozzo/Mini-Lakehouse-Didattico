.DEFAULT_GOAL := help

help:
	@echo "Comandi disponibili:"
	@echo "  make install        → Installa dipendenze con Poetry"
	@echo "  make run            → Esegue ingest_csv.py via Poetry"
	@echo "  make dbt-run        → Esegue dbt run"
	@echo "  make dbt-test       → Esegue dbt test"
	@echo "  make dbt-clean      → Rimuove target e cache dbt"
	@echo "  make activate       → Mostra path attivazione venv"
	@echo "  make clean          → Rimuove cache e __pycache__"

install:
	poetry install

run:
	poetry run python ingest/ingest_csv.py

dbt-run:
	poetry run dbt run --project-dir dbt --profiles-dir dbt

dbt-test:
	poetry run dbt test --project-dir dbt --profiles-dir dbt

dbt-clean:
	poetry run dbt clean --project-dir dbt --profiles-dir dbt

activate:
	@echo "Per attivare virtualenv:"
	@poetry env info --path

clean:
	rm -rf __pycache__ .ruff_cache .pytest_cache .mypy_cache
