# 📦 CHANGELOG

## [v0.1.0] - 2025-06-20

Versione iniziale stabile del progetto **Mini Lakehouse Didattico**, focalizzata su modellazione dati, audit SQL e struttura replicabile tramite `dbt + DuckDB`.

---

### 🚀 Added

#### ▶️ Staging
- `stg_bilanci_comuni.sql`: normalizzazione del dataset raw dei bilanci comunali simulati
- `stg_bilanci_comuni.yml`: schema YAML con descrizioni e test `not_null`

#### ▶️ Core
- `core_bilanci_comuni.sql`: calcolo saldo per comune e anno (`entrate - spese`)
- `core_audit_flags.sql`: identificazione automatica anomalie con macro personalizzate:
  - variazioni percentuali fuori soglia
  - saldo negativo
  - valori nulli in colonne chiave

#### ▶️ Marts
- `mart_audit_log.sql`: log di tutti i record con almeno un flag di anomalia attivo
- `mart_finanza_locale.sql`: vista riassuntiva comune/anno con saldo e flag di anomalia

#### ▶️ Altro
- `Makefile`: automazioni base per setup, esecuzione dbt, e pulizia ambiente
- `README.md`: documentazione minimale coerente con architettura e obiettivi
- `pyproject.toml`: gestione ambiente e dipendenze con Poetry
- `packages.yml`: pacchetti dbt esterni (`dbt-utils`, `dbt-expectations`, `dbt-date`)

---

### ✏️ Changed

- Inizialmente previsti tre modelli `stg_bilanci_comuni_{cassa,competenza,residui}`: consolidati in uno solo per semplicità e coerenza con dataset attuale
- Obiettivi didattici adattati a un workflow minimale ma completo, per massimizzare comprensibilità e replicabilità

---

### 🛠 Fixed

- Rimozione test `dbt_utils.expression_is_true` e `row_count` non compatibili con DuckDB
- Corretto schema YAML `stg_bilanci_comuni.yml` dopo errori di parsing e ref non risolti
- Gestione macro non risolte in `core_audit_flags` tramite fallback a macro locali

---

### 🧪 Test & Validazione

- ✅ 15 test automatici attivi (`not_null`, macro expectations)
- ✅ Esecuzione locale verificata su DuckDB con `dbt run` e `dbt test`
- ✅ Tutti i modelli compilano e generano view/table correttamente

---

### 🔍 Note

- La versione `v0.1.0` rappresenta una base stabile e leggibile per l'evoluzione del progetto
- Ideale per studio e formazione su: staging, audit logico, qualità dati
- Pronta per estensioni future (più fonti, test incrociati, documentazione dbt, ecc.)

---

## 🪪 Licenza

MIT License
