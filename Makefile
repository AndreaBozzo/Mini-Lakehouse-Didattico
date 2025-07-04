# Makefile – Mini Lakehouse Didattico

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

.PHONY: help install deps seed run test dbt-clean build export-marts audit-log \
        docs coverage quality-report check lint format all cli ci-pipeline \
        activate clean

# ──────────────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "Mini Lakehouse Didattico – Makefile commands"
	@echo ""
	@echo "  make install         → Installa dipendenze"
	@echo "  make deps            → dbt deps"
	@echo "  make seed            → mkdir data/warehouse + dbt seed"
	@echo "  make run             → dbt run (dipende da seed)"
	@echo "  make test            → dbt test"
	@echo "  make dbt-clean       → dbt clean + rimozione manuale"
	@echo "  make build           → clean → deps → seed → run → test"
	@echo "  make export-marts    → esporta marts via script Python"
	@echo "  make audit-log       → esegue audit_log.py"
	@echo "  make docs            → dbt docs generate"
	@echo "  make coverage        → pytest con coverage"
	@echo "  make quality-report  → Ruff JSON report"
	@echo "  make check           → ruff, black, isort, safety"
	@echo "  make lint            → solo ruff"
	@echo "  make format          → black, isort, ruff --fix"
	@echo "  make all             → build → export-marts → audit-log → docs → check"
	@echo "  make cli             → pipeline interattiva (typer)"
	@echo "  make ci-pipeline     → pipeline in modalità CI"
	@echo "  make activate        → mostra path venv Poetry"
	@echo "  make clean           → pulisce cache locali"
	@echo ""

install:
	poetry install

deps:
	@echo "[dbt deps] Installing packages…"
	$(DBT_DEPS)

seed:
	@echo "[seed] Ensuring data/warehouse exists…"
	ifeq ($(OS),Windows_NT)
		@mkdir data/warehouse
	else
		@mkdir -p data/warehouse
	endif
	@echo "[dbt seed] Loading seeds…"
	$(DBT_SEED)

run: seed
	@echo "[dbt run] Compiling and materializing…"
	$(DBT_RUN)

test:
	@echo "[dbt test] Running tests…"
	$(DBT_TEST)

dbt-clean:
	@echo "[dbt clean] Automatic clean…"
	-@$(DBT_CLEAN)
	@echo "[dbt clean] Manual removal of target/ and dbt_packages/…"
ifeq ($(OS),Windows_NT)
	@powershell -NoProfile -Command "Remove-Item -Recurse -Force '$(DBTDIR)\target'; Remove-Item -Recurse -Force '$(DBTDIR)\dbt_packages'"
else
	@rm -rf $(DBTDIR)/target $(DBTDIR)/dbt_packages
endif

build: dbt-clean deps seed run test
	@echo "[build] ✅ Build completo."

export-marts:
	@echo "[export-marts] Esportazione dati marts…"
	poetry run python audit/export_marts.py

audit-log:
	@echo "[audit-log] Running audit/audit_log.py…"
	poetry run python audit/audit_log.py

docs:
	@echo "[docs] Generazione documentazione dbt…"
	poetry run dbt docs generate --project-dir $(DBTDIR) --profiles-dir $(PROFILESDIR)
	@echo "[docs] Disabilitazione Jekyll per GitHub Pages…"
	@touch $(DBTDIR)/docs/.nojekyll

coverage:
	@echo [coverage] Running pytest with coverage...
	@mkdir -p reports/htmlcov || powershell -Command "New-Item -ItemType Directory -Force -Path reports/htmlcov" >$null
	@poetry run pytest --cov=. \
		--cov-report=html:reports/htmlcov \
		--cov-report=xml:reports/coverage.xml || true

quality-report:
	@echo "[quality-report] Generating Ruff JSON report…"
	@poetry run python -c "import os; os.makedirs('reports', exist_ok=True)"
	@poetry run ruff check . --output-format json > reports/ruff.json

check:
	@echo "[check] Lint, format-check e security…"
	poetry run ruff check .
	poetry run black --check .
	poetry run isort --check-only .
	poetry run safety check || true

lint:
	@echo "[lint] Ruff only…"
	poetry run ruff check .

format:
	@echo "[format] Applicazione formattazione…"
	poetry run black .
	poetry run isort .
	ruff format .
	ruff check . --fix --show-fixes
cli:
	@echo "[cli] Avvio pipeline interattiva…"
	poetry run python cli/pipeline.py interactive

ci-pipeline:
	@echo "[ci-pipeline] Avvio pipeline CI…"
	poetry run python cli/pipeline.py ci-mode

activate:
	@echo "[activate] Poetry venv path…"
	poetry env info --path

clean:
	@echo "[clean] Rimozione cache locali…"
	@rm -rf __pycache__ .ruff_cache .pytest_cache .mypy_cache .venv .dbt_modules export reports
update-readme:
	poetry run python scripts/update_readme.py