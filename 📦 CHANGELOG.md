## 📦 Changelog v0.2.0 (in sviluppo)

### ✅ Fix principali

- **Corretto bug critico su `packages.yml`**: causava fallimenti in `dbt deps` per uso errato del campo `name:` non supportato da `dbt-core 1.9.x`.

  ```yaml
  packages:
    - package: dbt-labs/dbt_utils
      version: 1.3.0
    - package: metaplane/dbt_expectations
      version: 0.10.9
    - package: godatadriven/dbt_date
      version: 0.14.1
  ```

- Risolto errore `No dbt_project.yml` nel CI: causato da directory di esecuzione sbagliata. Corretto con `--project-dir dbt --profiles-dir dbt` e `working-directory: dbt` in GitHub Actions.
- Fix blocco file su Windows (dbt-utils): errore nel rename della cartella `dbt-utils-1.3.0` dovuto a file in uso. Risolto chiudendo i processi e forzando la rimozione.
- Fix `NoneType` su `dbt_project.yml`: causato da archivi zip corrotti o configurazioni YAML errate. Ripristinato file e validazione.

**Struttura dbt ripristinata e funzionante:**

- `dbt_project.yml` e `profiles.yml` validi.
- `dbt clean`, `dbt deps`, `dbt run`, `dbt test` eseguibili senza errori.
- Tutti i modelli (raw, stg, core, marts, audit) compilano correttamente.

**CI corretta per DuckDB + dbt:**

- `warehouse.duckdb` ora generato correttamente durante il job.
- Corretto path assoluto nel `profiles.yml` CI.
- Fase `dbt run` ora precede `dbt test`, evitando `table does not exist`.

### 🔄 Migliorie Developer Experience

**Nuovo Makefile con target chiari e coerenti:**

- `check`, `format`, `run`, `install`, `dbt-run`, `dbt-test`, `dbt-clean`, `activate`, `clean`

**Aggiornato .vscode/settings.json:**

- Import di `polars` risolto.
- Auto-detect ambiente virtuale Poetry.
- Formatter SQL `innoverio.vscode-dbt-power-user`.

**Rifinito pyproject.toml:**

- Dipendenze aggiornate: `dbt-core`, `dbt-duckdb`, `duckdb`, `polars`, `pyarrow`.
- Inclusi tool di qualità: `black`, `isort`, `ruff`, `pytest`, `safety`.
- Configurazioni coerenti per `black`, `ruff`, `isort`.

**Fallback strategy Windows documentata:**

```powershell
poetry run dbt clean
Remove-Item -Recurse -Force dbt_packages .dbt package-lock.yml target
poetry run dbt deps
```

**Verifica con hash per packages.yml:**

```powershell
Get-FileHash -Algorithm SHA256 packages.yml
```

### 📌 Note

- dbt considera qualsiasi file `packages.yml`, anche se `packages.yaml` è corretto.
- dbt < 1.10 non supporta `name:` nei pacchetti, nonostante la documentazione ambigua.
- I path relativi nel profilo DuckDB devono essere risolti dal punto di vista della CI, non della macchina locale.
