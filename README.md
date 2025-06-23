# 🧊 Mini Lakehouse Didattico

> 📊 **Data Lakehouse minimale in locale** per progetti educativi e prototipazione rapida.  
> 🎯 Focus su **modellazione a livelli**, **validazione automatica** e **audit trasparente** con `dbt + DuckDB`.

![dbt CI](https://github.com/AndreaBozzo/Mini-Lakehouse-Didattico/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&style=flat)
![DuckDB](https://img.shields.io/badge/duckdb-local-yellow?logo=duckdb&style=flat)
![dbt-core](https://img.shields.io/badge/dbt-core-orange?logo=dbt&style=flat)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

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

| Layer   | Modelli principali                          | Note |
|---------|---------------------------------------------|------|
| Staging | `stg_bilanci_comuni`                        | Pulizia, naming coerente |
| Core    | `core_bilanci_comuni`, `core_audit_flags`   | Calcoli derivati + flag anomalie |
| Marts   | `mart_finanza_locale`, `mart_audit_log`     | Output consolidati e log controlli |

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

```bash
mini-lakehouse/
├── audit/                  # Script esterni dbt (es. export_marts.py)
├── cli/                    # CLI pipeline interattiva con Typer
├── dbt/                    # Progetto dbt completo
├── models/                 # staging → core → marts
├── seeds/main/            # CSV seed di input
├── reports/               # coverage, log, audit
├── tests/                 # pytest + test CLI + coverage
├── Makefile
├── pyproject.toml
└── README.md
```

---

## 📄 Licenza

Distribuito sotto licenza MIT.

---

## 🙋‍♂️ Contatti

Andrea Bozzo  
📧 andreabozzo92@gmail.com  
[🔗 GitHub](https://github.com/AndreaBozzo)