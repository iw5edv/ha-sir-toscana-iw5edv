# Changelog

## 0.1 — SIR CFR Toscana (Fork by IW5EDV)

Prima versione del fork, basata su [m0m4x/ha-sir-toscana](https://github.com/m0m4x/ha-sir-toscana) **versione 0.2.2**.

### Coesistenza con l'integrazione originale

- Domain rinominato da `sir_toscana` a `sir_toscana_iw5edv` e cartella da `custom_components/sir_toscana` a `custom_components/sir_toscana_iw5edv`: il fork si installa accanto all'originale senza sovrascriverlo.
- Config entry, dispositivi, entità e coordinatori del fork sono registrati sotto il nuovo domain e non interferiscono con quelli dell'originale.
- Nome visualizzato: **SIR CFR Toscana (Fork by IW5EDV)**.

### Elenco delle stazioni

- L'elenco è acquisito dall'endpoint JSON del portale SIR (`actions.php?action=list&type_gauge=`), unendo la lista completa e quelle per tipologia. Le tabelle HTML `stazioni.php` restano come riserva per la singola tipologia.
- Corretto: se una tabella di monitoraggio non rispondeva (es. `pluvio`), le stazioni presenti solo in quella tabella sparivano dal menu senza alcuna segnalazione (es. Montecatini Terme, `TOS01001601`). La tabella `anemo` del portale risponde attualmente con HTTP 500.
- Le fonti non raggiungibili vengono registrate nel log di Home Assistant come warning.
- Le voci del menu riportano comune e provincia, per distinguere le stazioni con lo stesso nome (es. Sambuca, Roccastrada, Buonconvento).
- I nomi delle stazioni non riportano più i suffissi `(RADIO)`/`(GPRS)`.

### Metadati

- Manifest, `hacs.json`, README e istruzioni di pubblicazione aggiornati per il repository `iw5edv/ha-sir-toscana-iw5edv`.

---

## Storico del progetto originale (m0m4x/ha-sir-toscana)

### 0.2.2

- Rinominata l'integrazione da **SIR Toscana** a **SIR CFR Toscana** per identificare più chiaramente il servizio regionale.
- Aggiornati i metadati HACS e Home Assistant mantenendo invariati il domain `sir_toscana` e il repository.

### 0.2.1

- Aggiunto il secondo step del Config Flow per selezionare le tipologie di dati.
- Tutte le tipologie SIR supportate sono selezionabili: `anemo`, `radio`, `pluvio`, `termo`, `igro`, `idro`, `nivo`.
- Le opzioni mostrate dipendono dai blocchi realmente restituiti dalla stazione.
- Tutte le tipologie disponibili sono preselezionate per impostazione predefinita.
- Aggiunta `radio` alla discovery delle stazioni.
- Corretto il parsing della tabella idrometrica, dove il nome della stazione è preceduto dal nome del fiume.
- `radio.value` è esposto come Radianza in `W/m²` con device class `irradiance`.
- Mantenuta la compatibilità con le configurazioni precedenti prive di `data_types`.

### 0.1.1

Prima release pubblica dell'integrazione SIR Toscana.

- Config Flow tramite selezione della stazione.
- Risoluzione automatica del codice stazione.
- Sensori generati dinamicamente dal payload SIR.
- Polling tramite `DataUpdateCoordinator`, allineato a 15 minuti.
- Aggiornato il Config Flow al tipo `ConfigFlowResult` corrente.
- Associato il `ConfigEntry` al `DataUpdateCoordinator`.
- Aggiunta la device class Home Assistant per la direzione del vento.
- Reso `hacs.json` minimale e conforme alla documentazione corrente.
- Preparato il repository `m0m4x/ha-sir-toscana` per GitHub e HACS.
- Aggiunti `codeowners`, `integration_type`, `country` e link del progetto.
- Aggiunte le GitHub Actions ufficiali HACS e Hassfest.
- Aggiunti brand locali per Home Assistant 2026.3+.
- Migliorata la ricerca della stazione e la gestione dei nomi con suffissi RADIO/GPRS.
- Aggiunto il supporto alla tabella nivometrica nella ricerca delle stazioni.
- I nuovi campi che compaiono nel payload dopo il setup vengono aggiunti dinamicamente come sensori.
- I valori numerici generici vengono esposti come numeri, quando possibile.
- Evitata la generazione di statistiche long-term scorrette sulla direzione del vento.
- Migliorate tracciabilità e metadati delle entità.
