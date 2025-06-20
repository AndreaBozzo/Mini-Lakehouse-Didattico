## 📦 Changelog v0.2.0 (in sviluppo)

### ✅ Fix principali

* **Corretto bug critico su `packages.yml`**: il file conteneva campi `name:` non supportati da `dbt-core 1.9.x`. Questo causava fallimenti persistenti in `dbt deps` con errore di validazione YAML.

  * Sintassi corretta:

    ```yaml
    packages:
      - package: dbt-labs/dbt_utils
        version: 1.3.0
      - package: metaplane/dbt_expectations
        version: 0.10.9
      - package: godatadriven/dbt_date
        version: 0.14.1
    ```

* **Risolto errore `No dbt_project.yml` nel CI**: dovuto a posizione errata del file `dbt_project.yml` rispetto alla root del repository GitHub. Aggiunto `cwd: ./dbt` nel workflow GitHub Actions.

* **Blocco file su Windows**: dbt non riusciva a rinominare `dbt_packages/dbt-utils-1.3.0` a causa di file `integration_tests` ancora in uso. Risolto chiudendo processi e usando `rm -Force` mirato.

* **Errori `NoneType` su `dbt_project.yml`**: generati da zip parzialmente corrotti o da sostituzioni errate dei file YAML.

* **Reimpostata struttura del progetto dbt**:

  * `dbt_project.yml` e `profiles.yml` correttamente validati.
  * `dbt clean` e `dbt deps` funzionano senza errori.
  * `dbt run` eseguito con successo: tutti i 7 modelli compilati correttamente.

### 🔄 Migliorie DevEx

* Aggiunta procedura consigliata per risoluzione problemi su Windows:

  * `poetry run dbt clean`
  * `Remove-Item -Recurse -Force dbt_packages .dbt package-lock.yml target`
  * Controllare che `packages.yml` non contenga campi `name:`

* Usato `Get-FileHash` per verifica differenze effettive tra versioni del file `packages.yml`.

### 📌 Note

* Il problema è stato amplificato dal fatto che dbt carica **qualsiasi** `packages.yml` anche se `packages.yaml` era corretto.
* dbt < 1.10 **non supporta `name:` nei pacchetti**, nonostante documentazione ambigua.

---

Prossimo step: chiudere questa sezione nel changelog solo al momento del merge su `main`.
