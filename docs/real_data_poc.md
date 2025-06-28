# 📊 Proof of Concept – Dati Reali SIOPE

## Obiettivo

Dimostrare la compatibilità e robustezza dell'architettura Mini Lakehouse Didattico con dati pubblici reali (fonte: SIOPE – BDAP), integrando il flusso end-to-end per un comune pilota.

---

## 🏙️ Comune Pilota

- **Nome:** Milano
- **Codice Belfiore:** F205
- **Anno di riferimento:** 2016
- **Fonte:** OpenBDAP – SIOPE Entrate Mensili
- **File CSV usato:**  
  `data/public/siope_it/milano/2016---Lombardia---SIOPE-Movimenti-cumulati-mensili-di-Entrata.csv`

---

## 🔁 Flusso Modelli Implementato

| Livello       | Modello                         | Stato     |
|---------------|----------------------------------|-----------|
| Staging       | `stg_siope_reali`                | ✅ fatto  |
| Core          | `core_real_siope`                | ✅ fatto  |
| Marts         | `mart_siope_totali_mensili`      | ✅ fatto  |

---

## ⚙️ Estensione CLI

- Flag `--real-data` attivo nella pipeline CLI (`cli/pipeline.py`)
- Fallback automatico a modelli taggati `simulated` in caso di assenza reali
- Pipeline funziona correttamente in modalità `--real-data` sia interattiva che `ci-mode`

---

## 📈 Exposure Collegato

```yaml
- name: real_data_siope_flow
  type: analysis
  description: Analisi basata sui dati pubblici reali SIOPE del Comune di Milano.
  depends_on:
    - ref('mart_siope_totali_mensili')
  owner:
    name: Andrea Bozzo
    email: andreabozzo92@gmail.com
  maturity: medium
  meta:
    tool: duckdb + parquet
    dataset_sensibile: false
  url: http://localhost:8501/real_data
