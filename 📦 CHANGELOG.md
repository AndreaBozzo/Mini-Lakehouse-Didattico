
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

- Variabili per `DBTDIR` e `PROFILESDIR` per eseguire dbt in modo parametrizzato.
- Target aggiuntivi: `deps`, `run`, `test`, `build`, `export-marts`, `audit-log`.
- `build` esegue clean → deps → seed → run → test in un solo comando.

**Script di build cross-platform:**

- `build.sh` e `build.ps1` per workflow semplice su Linux/Mac e Windows.

**Rifinitura `.vscode/settings.json`:**

- Auto-detect ambiente virtuale Poetry.
- Formatter SQL con `innoverio.vscode-dbt-power-user`.

**Aggiornamenti `pyproject.toml`:**

- Dipendenze confermate e aggiornate: `dbt-core`, `dbt-duckdb`, `duckdb`, `polars`, `pyarrow`.
- Tool qualità: `black`, `isort`, `ruff`, `pytest`, `safety`.

### 📊 Marts + Export & Audit

- Aggiunti `flag_dato_incompleto` e `indicatore_affidabilita` in `core_bilanci_comuni.sql` per auditabilità dei dati.
- Propagazione dei flag e aggregazione score in `fact_bilanci_comunali.sql` con `BOOL_OR` e `AVG`.
- Creazione di `models/marts/fact_bilanci_comunali.yml` per documentazione YAML separata.
- Implementato `audit/export_marts.py` per esportazione automatica dei marts in CSV e Parquet.
- Aggiornati `schema.yml` in `core/` e `marts/` con test `not_null`, `accepted_values` e test range.
- Aggiunti test SQL manuali in `tests/core/` e `tests/marts/` per validazione range `indicatore_affidabilita` e non-empty.
- Migliorata CI (`ci.yml`) per includere clean interno a `dbt`, full build e `export-marts`.
- Eliminati test `dbt_utils.expression_is_true` problematici su DuckDB, sostituiti con test SQL manuali.
- Verifica e ottimizzazione Makefile, includendo supporto per VScode tasks.

### 📌 Note

- Le feature più avanzate di auditing (drift detection, report automatici, dashboard dinamici) saranno affrontate in Step 5 e Step 6.
- Il formato CSV e Parquet dei marts è ora standardizzato in `audit/exports`.
- Mantieni aggiornato il file `profiles.yml` per l’ambiente CI e locale.
