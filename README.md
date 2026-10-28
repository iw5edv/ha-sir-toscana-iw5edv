# SIR CFR Toscana per Home Assistant — Fork by IW5EDV

[![GitHub release](https://img.shields.io/github/v/release/iw5edv/ha-sir-toscana-iw5edv?display_name=tag)](https://github.com/iw5edv/ha-sir-toscana-iw5edv/releases)
[![HACS validation](https://github.com/iw5edv/ha-sir-toscana-iw5edv/actions/workflows/validate.yml/badge.svg)](https://github.com/iw5edv/ha-sir-toscana-iw5edv/actions/workflows/validate.yml)
[![hassfest](https://github.com/iw5edv/ha-sir-toscana-iw5edv/actions/workflows/hassfest.yml/badge.svg)](https://github.com/iw5edv/ha-sir-toscana-iw5edv/actions/workflows/hassfest.yml)

> [!IMPORTANT]
> **Questo repository è un fork** dell'integrazione **[SIR CFR Toscana](https://github.com/m0m4x/ha-sir-toscana) di [m0m4x](https://github.com/m0m4x)**, basato sulla **versione 0.2.2** dell'originale.
>
> Versione del fork: **0.1** — manutenuto da **IW5EDV**. Distribuito con la stessa licenza MIT dell'originale; tutto il merito del lavoro di base va all'autore originale.

## Modifiche rispetto all'originale

### 1. Elenco delle stazioni più affidabile

Nell'originale l'elenco delle stazioni del menu veniva ricavato leggendo sette pagine HTML del portale SIR (`stazioni.php?type=…`, una per tipologia di sensore) ed estraendo i dati dal JavaScript contenuto nelle pagine. Se una di queste pagine non rispondeva, l'errore veniva ignorato in silenzio e **spariscono dal menu tutte le stazioni presenti solo in quella tabella**. Ad esempio **Montecatini Terme (`TOS01001601`)**, che compare solo nella tabella dei pluviometri, poteva non essere selezionabile. Inoltre la tabella `anemo` del portale risponde attualmente con errore HTTP 500.

Nel fork:

- l'elenco viene letto dall'endpoint JSON usato dalle mappe del portale SIR (`actions.php?action=list&type_gauge=…`), unendo la lista completa e quelle per ogni tipologia;
- se la lista JSON di una tipologia non è disponibile, viene letta la tabella HTML corrispondente, come nell'originale;
- ogni fonte non raggiungibile viene segnalata come **warning nel log** di Home Assistant invece di essere ignorata;
- i nomi delle stazioni non riportano più i suffissi `(RADIO)` / `(GPRS)`.

### 2. Comune e provincia nel menu

Diverse stazioni hanno lo stesso nome (Sambuca, Roccastrada, Buonconvento, Dicomano, Villafranca…). Ogni voce del menu riporta ora comune (se diverso dal nome) e provincia:

```text
Montecatini Terme (PT) — TOS01001601
Sambuca (Barberino Tavarnelle, FI) — TOS03004911
Sambuca (San Casciano in Val di Pesa, FI) — TOS11000057
```

### 3. Installabile insieme all'originale

Il fork usa un domain e una cartella propri, quindi **può essere installato accanto all'integrazione originale senza conflitti**:

| | Originale | Fork |
|---|---|---|
| Nome | SIR CFR Toscana | SIR CFR Toscana (Fork by IW5EDV) |
| Domain | `sir_toscana` | `sir_toscana_iw5edv` |
| Cartella | `custom_components/sir_toscana` | `custom_components/sir_toscana_iw5edv` |

Config entry, dispositivi ed entità delle due integrazioni restano separati. Una stessa stazione può essere configurata in entrambe: Home Assistant aggiunge automaticamente un suffisso (es. `_2`) agli `entity_id` del secondo dispositivo.

> Le stazioni configurate con l'integrazione originale non vengono migrate: per usarle con il fork vanno aggiunte di nuovo da **Aggiungi integrazione → SIR CFR Toscana (Fork by IW5EDV)**.

Il dettaglio delle modifiche è nel [CHANGELOG](CHANGELOG.md).

---

Custom integration per Home Assistant per acquisire i **dati in tempo reale della rete meteo-idrologica regionale** pubblicati dal **Servizio Idrologico Regionale (SIR) della Regione Toscana**.

L'integrazione acquisisce automaticamente l'elenco delle stazioni disponibili dal portale SIR della Regione Toscana. L'utente seleziona la stazione dal Config Flow e il relativo codice `TOS...` viene memorizzato come identificativo stabile. I valori restituiti dal servizio pubblico SIR vengono quindi esposti come sensori Home Assistant.

> **Progetto indipendente e non ufficiale.** Non è sviluppato, approvato o supportato dalla Regione Toscana o dal SIR.

## Installazione con HACS

Premi il pulsante seguente per aprire direttamente questo repository in HACS:

[![Apri SIR CFR Toscana (Fork by IW5EDV) in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=iw5edv&repository=ha-sir-toscana-iw5edv&category=integration)

In alternativa: **HACS → ⋮ → Custom repositories**, URL `https://github.com/iw5edv/ha-sir-toscana-iw5edv`, tipo **Integration**.

Dopo aver scaricato l'integrazione da HACS e riavviato Home Assistant, premi:

[![Aggiungi SIR CFR Toscana (Fork by IW5EDV) a Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=sir_toscana_iw5edv)

Il primo pulsante aggiunge/apre il repository in HACS. Il secondo avvia il Config Flow di **SIR CFR Toscana (Fork by IW5EDV)** dopo che la custom integration è stata installata.

## Funzionalità

- configurazione da interfaccia Home Assistant tramite Config Flow;
- selezione delle tipologie di dati disponibili per ciascuna stazione;
- elenco delle stazioni acquisito automaticamente dal portale SIR;
- selezione della stazione tramite menu Home Assistant;
- nessuna necessità di conoscere o digitare il codice `TOS...`;
- polling del servizio pubblico SIR ogni 15 minuti;
- una sola richiesta HTTP per stazione a ogni ciclo di aggiornamento;
- creazione automatica dei sensori presenti nel JSON della stazione;
- aggiunta dinamica di nuovi sensori se il SIR introduce nuovi campi nel payload;
- un dispositivo Home Assistant distinto per ogni stazione;
- supporto a più stazioni;
- nomi, unità e device class Home Assistant per le principali grandezze note;
- nessuna API key richiesta.

## Esempio: Prato Università

Nel Config Flow è possibile selezionare:

```text
Prato Università (Prato, PO) — TOS01001205
```

L'integrazione acquisisce i dati da:

```text
https://www.sir.toscana.it/monitoraggio/actions.php?action=station&id=TOS01001205
```

La stazione Prato Università è presente nelle tabelle di monitoraggio SIR per più grandezze meteorologiche.

## Nomi dei sensori

I nomi delle entità seguono il più possibile la terminologia utilizzata nelle visualizzazioni del portale SIR.

Esempi:

```text
Velocità vento
Direzione vento
Temperatura
Umidità aria
Radiazione diretta
Precipitazioni cumulate 15 minuti
Precipitazioni cumulate 1 ora
Precipitazioni cumulate 3 ore
Precipitazioni cumulate 6 ore
Precipitazioni cumulate 12 ore
Precipitazioni cumulate 24 ore
Precipitazioni cumulate 36 ore
Tempo di ritorno precipitazione 1 ora
Precipitazioni step 00–03 (24 h)
```

I timestamp vengono esposti come entità diagnostiche, ad esempio:

```text
Data rilevazione vento
Data rilevazione temperatura
Data rilevazione umidità aria
Data rilevazione precipitazioni
```

I campi tecnici `id` e `speed_label` non vengono creati come entità.

## Configurazione

1. Aprire **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**.
2. Cercare **SIR CFR Toscana (Fork by IW5EDV)**.
3. Selezionare la stazione desiderata dall'elenco.

Ogni voce mostra il nome pubblicato dal SIR, il comune (se diverso dal nome), la provincia e il relativo codice identificativo:

```text
Prato Università (Prato, PO) — TOS01001205
Montecatini Terme (PT) — TOS01001601
```

![Selezione della stazione SIR CFR Toscana](docs/images/config-flow-station.png)

Il codice viene salvato internamente come identificativo stabile della stazione, mentre il nome pubblicato dal SIR viene utilizzato come nome del dispositivo Home Assistant.

### Selezione delle tipologie di dati

Dopo la scelta della stazione, il Config Flow interroga il relativo endpoint SIR e propone **tutte le macro-tipologie supportate effettivamente presenti nel payload**.

![Selezione delle tipologie di dati SIR](docs/images/config-flow-data-types.png)

Le tipologie gestite sono:

- `anemo` — Anemometria / vento;
- `radio` — Radiometria / radianza, in `W/m²`;
- `pluvio` — Pluviometria / precipitazioni;
- `termo` — Termometria / temperatura;
- `igro` — Igrometria / umidità relativa;
- `idro` — Idrometria / livelli e portate;
- `nivo` — Nivometria / neve.

Tutte le tipologie disponibili sono preselezionate; l'utente può deselezionare quelle che non desidera esporre in Home Assistant.

La richiesta HTTP al SIR continua a restituire l'intero payload della stazione. La selezione determina quali sezioni vengono trasformate in entità Home Assistant.

Le configurazioni create con versioni precedenti, prive del campo `data_types`, mantengono il comportamento precedente ed espongono tutte le sezioni restituite dal SIR.

### Dispositivo e sensori

Al termine della configurazione Home Assistant crea un dispositivo distinto per la stazione, con i sensori relativi alle tipologie selezionate e le entità diagnostiche disponibili.

![Esempio del dispositivo SIR CFR Toscana in Home Assistant](docs/images/device-overview.png)

## Aggiornamento dei dati

L'integrazione interroga il servizio pubblico SIR ogni **15 minuti** tramite `DataUpdateCoordinator`.

Tutte le entità della stessa stazione utilizzano lo stesso payload, evitando una richiesta separata per ciascun sensore.

## Origine dei dati

Portale del Servizio Idrologico Regionale:

```text
https://www.sir.toscana.it/
```

Tabelle di monitoraggio in tempo reale:

```text
https://www.sir.toscana.it/monitoraggio/stazioni.php
```

Endpoint della singola stazione:

```text
https://www.sir.toscana.it/monitoraggio/actions.php?action=station&id=CODICE_STAZIONE
```

Elenco delle stazioni (JSON, usato dalle mappe del portale):

```text
https://www.sir.toscana.it/monitoraggio/actions.php?action=list&type_gauge=TIPOLOGIA
```

La ricerca delle stazioni unisce la lista completa (`type_gauge` vuoto) e le liste per anemometria, radiometria, pluviometria, termometria, igrometria, idrometria e nivometria. Se la lista JSON di una tipologia non è disponibile, viene letta la corrispondente tabella `stazioni.php`. Le fonti non raggiungibili sono segnalate come warning nel log di Home Assistant.

## Dati in tempo reale e validazione

Il SIR specifica che i dati pubblicati nelle sezioni di monitoraggio sono **acquisiti in tempo reale (ora solare) e non sottoposti a validazione**.

Questi valori non devono quindi essere confusi con eventuali serie storiche successivamente sottoposte a controllo, verifica o validazione dall'ente competente.

L'integrazione mantiene i timestamp nel formato fornito dalla fonte e non attribuisce ai dati un livello di validazione diverso da quello dichiarato dal SIR.

## Sensori dinamici

Il payload JSON viene analizzato senza presupporre che tutte le stazioni dispongano della stessa sensoristica.

Per ogni sezione del JSON della stazione vengono create entità per tutti i valori scalari, ad eccezione dei campi tecnici esclusi esplicitamente (`id` e `speed_label`).

I campi noti ricevono nomi leggibili, unità, device class e icone Home Assistant appropriate. I campi non ancora documentati vengono comunque acquisiti con un nome derivato dalla sezione e dal campo sorgente.

> L'integrazione considera come dati della stazione il payload JSON restituito da `actions.php?action=station`. Le tabelle riepilogative del portale possono mostrare elaborazioni aggiuntive, come massimi giornalieri o raffiche, che non fanno parte di quel payload e non vengono ancora importate come sensori.

## Installazione manuale

1. Scaricare questo repository.
2. Copiare:

   ```text
   custom_components/sir_toscana_iw5edv
   ```

   dentro:

   ```text
   /config/custom_components/sir_toscana_iw5edv
   ```

3. Riavviare Home Assistant.
4. Aprire **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**.
5. Cercare **SIR CFR Toscana (Fork by IW5EDV)**.
6. Selezionare la stazione desiderata.

## Limitazioni

- La disponibilità e la correttezza dei dati dipendono dal servizio pubblico SIR Toscana.
- Gli endpoint utilizzati sono servizi web pubblici del portale, ma questo progetto non li presenta come API ufficialmente documentate e stabili.
- Una modifica del portale SIR potrebbe richiedere un aggiornamento dell'integrazione.
- Per i campi non documentati viene volutamente evitata qualsiasi reinterpretazione del significato o dell'unità di misura.
- La consultazione nivometrica può essere stagionale secondo le indicazioni pubblicate dal SIR.

## Licenza

MIT.

## Disclaimer

I dati appartengono alle rispettive fonti istituzionali. Questa integrazione è esclusivamente un client non ufficiale per visualizzare in Home Assistant informazioni rese pubblicamente disponibili dal Servizio Idrologico Regionale della Regione Toscana.
