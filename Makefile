.DEFAULT_GOAL := help

help:
	@echo "Comandi disponibili:"
	@echo "  make install        → installa tutto con Poetry"
	@echo "  make run            → esegue ingest_csv.py via Poetry"
	@echo "  make dbt-run        → esegue dbt run"
	@echo "  make format         → esegue black + isort + ruff"
	@echo "  make activate       → mostra path attivazione venv"
	@echo "  make clean          → pulizia"

install:
	poetry install

run:
	poetry run python ingest/ingest_csv.py

dbt-run:
	poetry run dbt run --project-dir dbt --profiles-dir dbt

format:
	poetry run black . && poetry run isort . && poetry run ruff check .

activate:
	@echo "Per attivare virtualenv:"
	@poetry env info --path

clean:
	rm -rf __pycache__ .ruff_cache .pytest_cache .mypy_cache
