# Makefile migliorato per workflow dbt + Poetry

# ──────────────────────────────────────────────────────────────────────────────
# Variabili
DBTDIR       ?= dbt
PROFILESDIR  ?= dbt

# Comandi DBT semplificati
DBT_DEPS     = poetry run dbt deps --project-dir $(DBTDIR) --profiles-dir $(PROFILESDIR)
DBT_SEED     = poetry run dbt seed --project-dir $(DBTDIR) --profiles-dir $(PROFILESDIR)
DBT_RUN      = poetry run dbt run  --project-dir $(DBTDIR) --profiles-dir $(PROFILESDIR)
DBT_TEST     = poetry run dbt test --project-dir $(DBTDIR) --profiles-dir $(PROFILESDIR)
DBT_CLEAN    = poetry run dbt clean --project-dir $(DBTDIR) --profiles-dir $(PROFILESDIR)

# Default target
.DEFAULT_GOAL := help

# ──────────────────────────────────────────────────────────────────────────────
.PHONY: help install deps seed run test dbt-clean build \
        check format activate clean audit-log export-marts

help:
	@echo ""
	@echo "Mini Lakehouse Didattico – Makefile commands"
	@echo ""
	@echo "  make install         → Installa tutte le dipendenze (Poetry)"
	@echo "  make deps            → Installa i package dbt (dbt deps)"
	@echo "  make seed            → Carica i file seed in DuckDB (dbt seed)"
	@echo "  make run             → Esegue dbt run (dipende da seed)"
	@echo "  make test            → Esegue dbt test"
	@echo "  make dbt-clean       → Pulisce target/ e dbt_packages/ (dbt clean)"
	@echo "  make build           → clean → deps → seed → run → test"
	@echo "  make check           → Lint, format-check e security (ruff/black/isort/safety)"
	@echo "  make format          → Applica black, isort, ruff --fix"
	@echo "  make export-marts    → Esporta i marts in CSV/Parquet"
	@echo "  make audit-log       → Esegue script audit/audit_log.py"
	@echo "  make activate        → Mostra path del virtualenv Poetry"
	@echo "  make clean           → Rimuove cache & __pycache__ locali"
	@echo ""

install:
	poetry install

deps:
	@echo "[dbt deps] Installing packages…"
	$(DBT_DEPS)

seed:
	@echo "[dbt seed] Loading seeds…"
	$(DBT_SEED)

run: seed
	@echo "[dbt run] Compiling and materializing…"
	$(DBT_RUN)

test:
	@echo "[dbt test] Running tests…"
	$(DBT_TEST)

dbt-clean:
	@echo "[dbt clean] Cleaning…"
	$(DBT_CLEAN)

build: dbt-clean deps seed run test
	@echo "[build] ✅ Build completo."

check:
	@echo "[check] Lint, format-check e security…"
	poetry run ruff check .
	poetry run black --check .
	poetry run isort --check-only .
	poetry run safety check || true

format:
	@echo "[format] Applicazione formattazione…"
	poetry run black .
	poetry run isort .
	poetry run ruff check --fix .

audit-log:
	@echo "[audit-log] Eseguo audit/audit_log.py…"
	poetry run python audit/audit_log.py

export-marts:
	@echo "[export-marts] Esportazione dati marts…"
	poetry run python audit/export_marts.py

activate:
	@echo "[activate] Path virtualenv Poetry:"
	poetry env info --path

clean:
	@echo "[clean] Rimozione cache locali…"
	@python - <<'PYCODE'
import shutil, pathlib
paths = ['__pycache__', '.ruff_cache', '.pytest_cache', '.mypy_cache', '.venv', '.dbt_modules', 'export']
for p in paths:
    shutil.rmtree(pathlib.Path(p), ignore_errors=True)
PYCODE
