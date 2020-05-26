# flask_app_azure

## Testing documentation below:
---
layout: post
title:  "Plattform for innsikt og analyse (PIA)"
description: "Overordnet arkitektur for PIA"
author: "Merca Ovenrud, Ola Pukstad"
date:   2020-05-25 09:50:28 +0200
categories: Overordnet arkitektur
---

# Plattform for innsikt og analyse (PIA)

Plattform for innsikt og analyse er BKK konsernets løsning for lagring, tilrettelegging og analyse av data. Utviklingsmetodikk og kjernekomponenter er delte ressurser som forvaltes av avdeling for Teknologi og fornyelse.
[![Arkitekturskisse](/media/images/Arkitekturskisse.svg "Arkitekturskisse")](/media/images/Arkitekturskisse.svg "Arkitekturskisse")

## Utviklingsmetodikk

PIA arkitektur sikter mot et strategisk mål for kapabilitet, men beskriver og utvikler faktisk kapasitet etterhvert som det er nødvendig. Dvs. at det f.eks ikke beskrives en arkitektur for tekstanalyse, før dette er nødvendig for å løse et prosjekt. Forretningsområdene har ansvaret for å utvikle egne prosjekter innefor rammeverket av PIA og for å løfte eventuelle behov for arkitekturarbeid til arkitekturgruppen.

### Kildekode

Alle komponenter i PIA, både infrastruktur og dataflyter skal skrives som kode og sjekkes inn i passende repositories i GitHub. Retningslinjer for bruk av GitHub og branching strategi er beskrevet her.

### Sprint

Så lenge PIA er et prosjekt ligger hele porteføljen som et prosjekt i Azure DevOps Boards. Hvert delprosjekt har sine egne backlogs og sprinter.

### CI/CD

Det er tre dedikerte Subscriptions i Azure for PIA: Dev, Test og Produksjon. Alle komponeneter som skal kjøre i PIA Produksjon skal først utvikles i Dev og deployes gjennom Azure DevOps Pipelines.

## [Dataflyt](/overordnet/arkitektur/2020/05/25/plattform-for-innsikt-og-analyse-(PIA).html "Dataflyt")

PIA følger i hovedsak [lambda arkitektur (ekstern link)](https://docs.microsoft.com/en-us/azure/architecture/data-guide/big-data/#lambda-architecture), som består av 3 lag:

1. Kontinuerlig strømming av tidskritiske data rett til klient
2. Persistering av data
3. Servering av data

I en tradisjonelle lamda arkitektur foregår persistering som batch, men i PIA skrives alle streams parallelt til [rå-datalake](/dataflyt/readme.md#rå-datalake). Dette trigger Databricks til å prosessere denne inputen videre, så det vil være mer korrekt å si at persistering er en parallell og asynkron stream. Latency for denne prosessen vil være relativt lav, så en det bør vurderes om en ren hot-path er nødvendig.

## Serveringslag

Azure Synapse, API, Databricks

## Ingest

Det er flere alternative metoder for å skrive data til PIA:

- Funksjoner
- Web Jobs
- Event Hub
- Azure Data Factory
