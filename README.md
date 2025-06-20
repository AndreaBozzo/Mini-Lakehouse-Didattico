# 🧊 Mini Lakehouse Didattico

> 📊 **Data Lakehouse minimale in locale** per progetti educativi e prototipazione rapida.  
> 🎯 Focus su **modellazione a livelli**, **validazione automatica** e **audit trasparente** con `dbt + DuckDB`.

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&style=flat)
![DuckDB](https://img.shields.io/badge/duckdb-local-yellow?logo=duckdb&style=flat)
![dbt-core](https://img.shields.io/badge/dbt-core-orange?logo=dbt&style=flat)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🧭 Table of Contents
- [⚙️ Stack](#️-stack)
- [🎯 Obiettivi](#-obiettivi)
- [📦 Dataset iniziale](#-dataset-iniziale)
- [📐 Architettura v010](#-architettura-v010)
- [🧪 Esecuzione base](#-esecuzione-base)
- [📁 Struttura progetto](#-struttura-progetto)
- [📌 Roadmap](#-roadmap)
- [📄 Licenza](#-licenza)
- [🙋‍♂️ Contatti](#-contatti)

---

## ⚙️ Stack

| Tecnologia | Descrizione |
|------------|-------------|
| [DuckDB](https://duckdb.org/) | Motore SQL OLAP embedded, veloce e leggero |
| [dbt-core](https://docs.getdbt.com/) | Modellazione e orchestrazione SQL |
| [`dbt-utils`](https://hub.getdbt.com/dbt-labs/dbt_utils/) | Macro utili standard |
| [`dbt-expectations`](https://hub.getdbt.com/calogica/dbt_expectations/) | Validazioni alla Great Expectations |
| [`dbt-date`](https://hub.getdbt.com/dbt-labs/dbt_date/) | Funzioni temporali |

---

## 🎯 Obiettivi

- Implementare una pipeline **trasparente**, **replicabile**, e **validabile**
- Modellazione a livelli: `staging → core → marts`
- Validazioni automatiche e **audit semplificato**
- Base flessibile per estensioni su altri dataset pubblici (ISTAT, OpenCUP, ecc.)

---

## 📦 Dataset iniziale

- Dati simulati da bilanci comunali italiani
- Input: file `.csv` in `data/raw/`
- Campi normalizzati: codice comune, voce, importo, anno

---

## 📐 Architettura v0.1.0

| Layer   | Modelli principali                          | Note |
|---------|---------------------------------------------|------|
| Staging | `stg_bilanci_comuni`                        | Pulizia, naming coerente |
| Core    | `core_bilanci_comuni`, `core_audit_flags`   | Calcoli derivati + flag anomalie |
| Marts   | `mart_finanza_locale`, `mart_audit_log`     | Output consolidati e log controllo |

---

## 🧪 Esecuzione base

```bash
poetry install
poetry run dbt deps
poetry run dbt run
poetry run dbt test


mini-lakehouse/
├── data/
│   └── raw/                    # CSV simulati
├── models/
│   ├── staging/                # Pulizia iniziale
│   ├── core/                   # Derivazioni e controlli
│   └── marts/                  # Output finale
├── tests/                      # Test dbt personalizzati
├── dbt_project.yml
├── pyproject.toml
└── README.md


📌 Roadmap
 Setup iniziale con DuckDB + dbt-core

 Modellazione bilanci pubblici simulati

 Audit con flag anomalie + validazioni dbt

 Estensione a dati reali (bilanci ISTAT / SIOPE)

 Dashboard leggibile da CSV / parquet prodotti

 Validazioni statistiche (es. distribuzioni importi, outlier)


 📄 Licenza
Questo progetto è distribuito sotto licenza MIT.

🙋‍♂️ Contatti
Andrea Bozzo
📧 andreabozzo92@gmail.com
[🔗 GitHub Profile](https://github.com/AndreaBozzo)
