#!/usr/bin/env bash
set -e

# 1) Clean dbt via comando nativo
echo "[1/6] Cleaning dbt…"
pushd dbt >/dev/null
poetry run dbt clean --profiles-dir .
popd  >/dev/null

# 2) Install deps
echo "[2/6] Installing dbt deps…"
poetry run dbt deps --project-dir dbt --profiles-dir dbt

# 3) Seed
echo "[3/6] Seeding…"
poetry run dbt seed --project-dir dbt --profiles-dir dbt

# 4) Run
echo "[4/6] Running models…"
poetry run dbt run  --project-dir dbt --profiles-dir dbt

# 5) Test
echo "[5/6] Testing…"
poetry run dbt test --project-dir dbt --profiles-dir dbt

# 6) Export
echo "[6/6] Export marts…"
poetry run python audit/export_marts.py

echo "✅ Build completo!"
