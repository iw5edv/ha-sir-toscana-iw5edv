# Pubblicazione GitHub e HACS — Fork by IW5EDV

Questa cartella è già un repository git: contiene la storia dell'originale [m0m4x/ha-sir-toscana](https://github.com/m0m4x/ha-sir-toscana) fino alla versione `v0.2.2` e, sopra, il commit con le modifiche del fork (versione `0.1`).

## Dati del repository

| Campo | Valore |
|---|---|
| Owner | `iw5edv` |
| Nome | `ha-sir-toscana-iw5edv` |
| Fork di | `m0m4x/ha-sir-toscana` (v0.2.2) |
| Website | `https://www.sir.toscana.it/` |

Descrizione consigliata:

```text
Fork by IW5EDV di SIR CFR Toscana (m0m4x/ha-sir-toscana v0.2.2): integrazione Home Assistant per i dati in tempo reale della rete meteo-idrologica del SIR Toscana.
```

Topics consigliati:

```text
home-assistant
homeassistant
hacs
italy
toscana
sir-toscana
weather
meteorology
hydrology
```

## 1. Creare il fork su GitHub

1. Accedere a GitHub come `iw5edv` e aprire <https://github.com/m0m4x/ha-sir-toscana>.
2. Premere **Fork**.
3. In **Repository name** scrivere `ha-sir-toscana-iw5edv`.
4. Lasciare selezionato **Copy the main branch only** e premere **Create fork**.
5. Nelle **Settings** del fork abilitare **Issues** (nei fork sono disattivate per impostazione predefinita) e impostare Description, Website e Topics.

## 2. Caricare le modifiche

Dalla cartella del fork (`ha-sir-toscana-iw5edv`), in un terminale:

```bash
git remote add origin https://github.com/iw5edv/ha-sir-toscana-iw5edv.git
git push -u origin main
```

Il push è un normale avanzamento del ramo `main` del fork, perché il commit del fork si trova sopra la storia dell'originale.

Per ricevere in futuro gli aggiornamenti dell'originale è già configurato il remote `upstream`:

```bash
git fetch upstream
git merge upstream/main
```

## 3. Controlli GitHub

Aprire la scheda **Actions**, abilitare i workflow (nei fork sono disattivati finché non si conferma) e verificare che risultino verdi:

- HACS validation
- Validate with hassfest

La validazione HACS controlla anche Description, Topics e Issues del repository.

## 4. Prima release

Creare su GitHub una **Release**, non soltanto un tag:

```text
Tag: v0.1
Title: SIR CFR Toscana (Fork by IW5EDV) v0.1
```

Usare come note il contenuto della sezione `0.1` di `CHANGELOG.md`.

HACS usa le GitHub Releases per mostrare le versioni disponibili. Il tag deve corrispondere a `version` in `custom_components/sir_toscana_iw5edv/manifest.json`.

## 5. Installazione con HACS

Usare:

```text
https://my.home-assistant.io/redirect/hacs_repository/?owner=iw5edv&repository=ha-sir-toscana-iw5edv&category=integration
```

oppure aggiungere il repository a HACS come **Custom repository → Integration**.

Dopo l'installazione riavviare Home Assistant e aggiungere **SIR CFR Toscana (Fork by IW5EDV)**. Il fork può restare installato accanto all'integrazione originale.
