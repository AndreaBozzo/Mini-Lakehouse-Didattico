# 🧊 Mini Lakehouse Didattico

> 📊 **Data Lakehouse minimale in locale** per progetti educativi e prototipazione rapida.  
> 🎯 Focus su **modellazione a livelli**, **validazione automatica** e **audit trasparente** con `dbt + DuckDB`.

![dbt CI](https://github.com/AndreaBozzo/Mini-Lakehouse-Didattico/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&style=flat)
![DuckDB](https://img.shields.io/badge/duckdb-local-yellow?logo=duckdb&style=flat)
![dbt-core](https://img.shields.io/badge/dbt-core-orange?logo=dbt&style=flat)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
[![Docs](https://img.shields.io/badge/docs-online-success?style=flat&logo=readthedocs)](https://andreabozzo.github.io/Mini-Lakehouse-Didattico/)

---

## 🧭 Table of Contents
- [⚙️ Stack](#️-stack)
- [🎯 Obiettivi](#-obiettivi)
- [📦 Dataset iniziale](#-dataset-iniziale)
- [🏗️ Architettura](#-architettura)
- [🧪 Esecuzione base](#-esecuzione-base)
- [🛠️ Comandi Makefile](#-comandi-makefile)
- [📁 Struttura progetto](#-struttura-progetto)
- [📄 Licenza](#-licenza)
- [🙋‍♂️ Contatti](#-contatti)

---

## ⚙️ Stack

| Tecnologia | Descrizione |
|------------|-------------|
| [DuckDB](https://duckdb.org/) | Motore SQL OLAP embedded |
| [dbt-core](https://docs.getdbt.com/) | Modellazione e orchestrazione SQL |
| [`dbt-utils`](https://hub.getdbt.com/dbt-labs/dbt_utils/) | Macro standard |
| [`dbt-date`](https://hub.getdbt.com/godatadriven/dbt_date/) | Macro temporali |
| [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/) | CLI interattiva avanzata |
| [Ruff](https://docs.astral.sh/ruff/) | Linter e formatter veloce |
| [Poetry](https://python-poetry.org/) | Gestione pacchetti Python |

---

## 🎯 Obiettivi

- Pipeline trasparente, riproducibile e validabile
- Modellazione a 3 livelli: `staging → core → marts`
- Validazioni automatiche + audit semplificato
- Base flessibile per dataset pubblici italiani (ISTAT, SIOPE, OpenCUP...)
- Supporto a esportazioni intelligenti da `marts/`
- CLI `pipeline.py` per uso locale o CI

---

## 📦 Dataset iniziale

- Dati simulati ispirati a bilanci comunali italiani
- Input: file `.csv` in `seeds/main/`
- Colonne chiave: codice comune, voce, importo, anno

---

## 🏗️ Architettura

<!-- AUTO-SECTION:DIAGRAM -->

```
flowchart TD
    subgraph Staging
        A1[stg_bilanci_comuni]
    end

    subgraph Core
        B1[core_bilanci_comuni]
        B2[core_audit_flags]
    end

    subgraph Marts
        C1[mart_finanza_locale]
        C2[mart_audit_log]
    end

    subgraph Audit
        D1[export_marts.py]
        D2[audit_log.py]
    end

    subgraph Seeds
        S1[seeds: bilanci.csv]
    end

    subgraph Exports
        E1[CSV]
        E2[Parquet]
    end

    subgraph Dev
        F1[dbt run, test, docs]
        F2[Developer - make & pre-commit]
    end

    S1 --> A1
    A1 --> B1
    B1 --> C1
    B2 --> C2
    B1 --> B2
    C1 --> D1
    C1 --> D2
    D1 --> E1
    D1 --> E2
    F2 --> F1
    F1 --> A1
```

<!-- END-SECTION:DIAGRAM -->

```
📊 Descrizione del diagramma

Il diagramma mostra il flusso di dati e processi all'interno del progetto dbt.
Rappresenta i livelli di modellazione (staging, core, marts), i processi di audit, i dati di input (seeds), le esportazioni (CSV, Parquet) e le attività di sviluppo (CLI, make, pre-commit).

Le frecce indicano la dipendenza e il flusso dati tra componenti.
I blocchi logici (subgraph) raggruppano le fasi principali del ciclo di vita del dato.
Questo schema facilita la comprensione dell’architettura complessiva da parte di sviluppatori e stakeholder.
```

---

## 🧪 Esecuzione base

```bash
make install
make build
make check
make export-marts
make audit-log
```

Oppure via CLI:

```bash
poetry run python cli/pipeline.py
```

---

## 🛠️ Comandi Makefile

| Comando         | Descrizione |
|----------------|-------------|
| `make install` | Installa tutto con Poetry |
| `make build`   | dbt deps + seed + run + test |
| `make check`   | Lint e format con Ruff |
| `make export-marts` | Esporta output intelligenti |
| `make audit-log` | Log controlli qualità |
| `make coverage` | Genera report copertura |
| `make all`     | Build + export + check |
| `make ci`      | Pipeline per CI |
| `make clean`   | Pulisce cache e target |

---

## 📁 Struttura progetto

<!-- AUTO-SECTION:STRUCTURE -->

```bash
├── -p
├── __init__.py
├── audit
│   ├── __init__.py
│   ├── audit_log.py
│   ├── audit_report.json
│   ├── audit_template.json
│   ├── export_marts.py
│   ├── exports
│   │   ├── __init__.py
│   │   ├── csv
│   │   ├── parquet
│   ├── snapshot_create.py
│   ├── snapshot_test.py
│   ├── snapshot_utils.py
├── build.sh
├── cli
│   ├── __init__.py
│   ├── pipeline.py
├── data
│   ├── public
│   │   ├── siope_it
│   ├── warehouse
│   │   ├── warehouse.duckdb
├── dbt
│   ├── dbt_packages
│   │   ├── dbt_date
│   │   ├── dbt_utils
│   ├── logs
│   │   ├── dbt.log
│   │   ├── dbt.log.1
│   ├── macros
│   │   ├── audit
│   │   ├── fix_duckdb_persist_docs.sql
│   ├── models
│   │   ├── audit
│   │   ├── core
│   │   ├── exposures
│   │   ├── marts
│   │   ├── raw
│   │   ├── staging
│   ├── seeds
│   │   ├── bilanci_comunali_sample.csv
│   │   ├── bilanci_voci_sample.csv
│   │   ├── schema.yml
│   ├── target
│   │   ├── compiled
│   │   ├── graph.gpickle
│   │   ├── graph_summary.json
│   │   ├── manifest.json
│   │   ├── partial_parse.msgpack
│   │   ├── run
│   │   ├── run_results.json
│   │   ├── semantic_manifest.json
│   ├── tests
│   │   ├── core
│   │   ├── marts
├── dbt.cmd
├── dbt_packages
│   ├── dbt_date
│   │   ├── CHANGELOG.md
│   │   ├── dbt_project.yml
│   │   ├── dev-requirements.txt
│   │   ├── images
│   │   ├── integration_tests
│   │   ├── LICENSE
│   │   ├── macros
│   │   ├── makefile
│   │   ├── packages.yml
│   │   ├── README.md
│   │   ├── supported_adapters.env
│   │   ├── tox.ini
│   ├── dbt_utils
│   │   ├── CHANGELOG.md
│   │   ├── CONTRIBUTING.md
│   │   ├── dbt_project.yml
│   │   ├── dev-requirements.txt
│   │   ├── docker-compose.yml
│   │   ├── docs
│   │   ├── integration_tests
│   │   ├── LICENSE
│   │   ├── macros
│   │   ├── Makefile
│   │   ├── pytest.ini
│   │   ├── README.md
│   │   ├── RELEASE.md
│   │   ├── run_functional_test.sh
│   │   ├── run_test.sh
│   │   ├── supported_adapters.env
│   │   ├── tox.ini
├── dbt_project.yml
├── docs
│   ├── architecture.mmd
│   ├── catalog.json
│   ├── compiled
│   │   ├── main_seeds
│   ├── graph.gpickle
│   ├── graph_summary.json
│   ├── index.html
│   ├── manifest.json
│   ├── partial_parse.msgpack
│   ├── real_data_poc.md
│   ├── run
│   │   ├── main_seeds
│   ├── run_results.json
│   ├── semantic_manifest.json
├── exports
│   ├── csv
│   │   ├── agg_entrate_per_categoria.csv
│   │   ├── fact_bilanci_comunali.csv
│   │   ├── mart_finanza_locale.csv
│   │   ├── mart_siope_totali_mensili.csv
│   ├── parquet
│   │   ├── agg_entrate_per_categoria.parquet
│   │   ├── fact_bilanci_comunali.parquet
│   │   ├── mart_finanza_locale.parquet
│   │   ├── mart_siope_totali_mensili.parquet
├── LICENSE.txt
├── logs
│   ├── dbt.log
├── Makefile
├── notebooks
├── package-lock.yml
├── packages.yml
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── README.md
├── reports
│   ├── coverage.xml
│   ├── htmlcov
│   │   ├── class_index.html
│   │   ├── coverage_html_cb_497bf287.js
│   │   ├── favicon_32_cb_58284776.png
│   │   ├── function_index.html
│   │   ├── index.html
│   │   ├── keybd_closed_cb_ce680311.png
│   │   ├── status.json
│   │   ├── style_cb_db813965.css
│   │   ├── z_209d042482f181b3_audit_log_py.html
│   │   ├── z_209d042482f181b3_export_marts_py.html
│   │   ├── z_209d042482f181b3_snapshot_create_py.html
│   │   ├── z_209d042482f181b3_snapshot_test_py.html
│   │   ├── z_209d042482f181b3_snapshot_utils_py.html
│   │   ├── z_434c77fc11d56e0c_pipeline_py.html
│   │   ├── z_73f802a1d358a589___init___py.html
│   │   ├── z_a44f0ac069e85531___init___py.html
│   │   ├── z_a44f0ac069e85531_test_cli_pipeline_py.html
│   │   ├── z_a44f0ac069e85531_test_cli_py.html
│   │   ├── z_a44f0ac069e85531_test_exports_marts_py.html
│   │   ├── z_de1a740d5dc98ffd_extract_comune_py.html
│   │   ├── z_de1a740d5dc98ffd_script_comuni_py.html
│   │   ├── z_de1a740d5dc98ffd_update_readme_py.html
│   ├── ruff.json
├── scripts
│   ├── __init__.py
│   ├── activate.ps1
│   ├── extract_comune.py
│   ├── script_comuni.py
│   ├── update_readme.py
├── snapshots
│   ├── v0.3.0
│   │   ├── real
├── target
│   ├── catalog.json
│   ├── compiled
│   │   ├── main_seeds
│   ├── graph.gpickle
│   ├── graph_summary.json
│   ├── index.html
│   ├── manifest.json
│   ├── partial_parse.msgpack
│   ├── run
│   │   ├── main_seeds
│   ├── run_results.json
│   ├── semantic_manifest.json
├── tests
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_cli_pipeline.py
│   ├── test_exports_marts.py
│   ├── test_snapshot_utils.py
├── 📦 CHANGELOG.md
```

<!-- END-SECTION:STRUCTURE -->

```markdown
---

## 📦 Changelog

<!-- AUTO-SECTION:CHANGELOG -->
_Non ancora disponibile. Il changelog verrà aggiornato automaticamente._
<!-- END-SECTION:CHANGELOG -->
---

## 📄 Licenza

Distribuito sotto licenza MIT.

---

## 🙋‍♂️ Contatti

Andrea Bozzo  
📧 andreabozzo92@gmail.com  
[🔗 GitHub](https://github.com/AndreaBozzo)
