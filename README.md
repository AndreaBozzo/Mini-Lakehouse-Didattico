# 🧊 Mini Lakehouse Didattico

Data Lakehouse minimale locale con stack moderno, focalizzato su:
- modellazione dati
- SQL avanzato
- audit e validazione
- tracciabilità e best practice con `dbt`

---

## ⚙️ Stack

- [DuckDB](https://duckdb.org/) – motore SQL analitico embedded
- [dbt-core](https://www.getdbt.com/) – orchestrazione e modellazione
- `dbt-utils`, `dbt-expectations`, `dbt-date` – macro standard e test

---

## 🎯 Obiettivi

- Implementare una pipeline replicabile e trasparente
- Applicare best practice nella modellazione a livelli (`staging → core → marts`)
- Dimostrare tecniche di audit automatico e controllo qualità su dati pubblici
- Creare una base solida e leggibile per progetti futuri

---

## 📦 Dataset iniziale

- Dati simulati da bilanci comunali italiani
- Input in formato `.csv` (cartella `data/raw`)
- Integrazione futura di più fonti (es. ISTAT)

---

## 📐 Architettura v0.1.0

| Layer   | Modelli principali                  | Note |
|---------|-------------------------------------|------|
| Staging | `stg_bilanci_comuni`               | Pulizia e normalizzazione |
| Core    | `core_bilanci_comuni`, `core_audit_flags` | Derivazioni + flag anomalie |
| Marts   | `mart_audit_log`, `mart_finanza_locale` | Output finale e log anomalie |

---

## 🧪 Esecuzione base

```bash
poetry install
poetry run dbt deps
poetry run dbt run
poetry run dbt test
