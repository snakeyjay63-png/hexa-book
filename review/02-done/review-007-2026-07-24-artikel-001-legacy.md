# Review — HEXA-BOEK #001 — Precieze repo-chain-audit

id: 007
date: 2026-07-24
target: articles/hexa-book-001.md
status: active
severity: critical
reviewer: ChatGPT
points: 12
summary: "Legacy-monoliet mengt verouderde artikelen, rekenfouten en tegenstrijdige returnstatussen."

## Overzicht

hexa-book-001.md is inhoudelijk geen lokale Artikel-1-node meer. Het bestand bevat een oudere volledige boekeditie met artikelen 1–13, Lens A–D, E/F, appendices en diverse inmiddels afgesplitste routes. Daardoor staan oude operatoren, berekeningen en statusmodellen naast de actuele modulaire architectuur. De grootste problemen zijn niet ontbrekende pointers, maar duplicatie en regressie: dezelfde route is elders nieuwer vastgelegd, terwijl dit bestand oudere of tegenstrijdige waarden blijft presenteren.

De juiste hoofdingreep is daarom niet twaalf losse reparaties uitvoeren, maar:
- hexa-book-001.md → reduceren tot Artikel 1 / Agni
- → alle latere artikelen vervangen door nidrā-pointers
- → historische monoliet archiveren als legacy-editie

## Punten

### P001: Bestand 001 bevat het volledige oude boek
Type: route | Locatie: gehele documentstructuur | Zekerheid: high | Routestatus: half

Oplossing:
- `articles/hexa-book-001.md` := Introductie + Artikel 1 + Agni-conceptoperator + status + nidrā-pointers
- `archive/hexa-book-legacy-full-v3.md` := huidige volledige inhoud

### P002: Oude en nieuwe statussystemen lopen door elkaar
Type: status | Locatie: introductie, artikelen 1–2, E/F en appendices | Zekerheid: high | Routestatus: half

Gebruik drie dimensies: operator_status, execution_status, validatie_status.

### P003: Returnstatus is intern direct tegenstrijdig
Type: consistentie | Locatie: introductie en Artikel E/F | Zekerheid: critical | Routestatus: half

Intro zegt R = undefined, later R gevalideerd met r_return = (3,7,5,9), daarna weer ongetest.

### P004: Griekse waarde van Λίθος is fout
Type: berekening | Locatie: Artikel 2, Lens B | Zekerheid: critical | Routestatus: gesloten

Λίθος = 319 (niet 610), DR = 4 (niet 7).

### P005: Lens B gebruikt meerdere onverenigbare waarden
Type: consistentie | Locatie: Lens B, Artikel E | Zekerheid: high | Routestatus: half

319, 354, 529 en 610 verschijnen zonder onderscheid.

### P006: C_quality gebruikt twee verschillende definities
Type: operator | Locatie: Lens C | Zekerheid: high | Routestatus: half

Gebruik binair: DR_work = DR_source → akliṣṭa, anders kliṣṭa.

### P007: C_sound wordt "volledig" genoemd terwijl W_C ontbreekt
Type: status | Locatie: Lens C | Zekerheid: high | Routestatus: half

C_sound_route = gedeeltelijk, niet "volledig uitgevoerd".

### P008: De vier DR_freq-waarden missen een operator
Type: route | Locatie: Lens C, C_sound_output | Zekerheid: high | Routestatus: half

Hz → DR_freq route niet zichtbaar.

### P009: 4-bit, 6-bit en nibble-ruimte worden verwisseld
Type: berekening | Locatie: 24/64-sectie | Zekerheid: high | Routestatus: gesloten

4-bit = 16 toestanden, 6-bit = 64 toestanden.

### P010: Delerclaim voor 396 is fout
Type: berekening | Locatie: 24-brug | Zekerheid: high | Routestatus: gesloten

{DR(d) | d ∈ D_selected} = {2,3,6,9}, niet {1,3,9}.

### P011: ρ_NPR(4) wordt als operatorstatus behandeld
Type: status | Locatie: Lens B | Zekerheid: medium | Routestatus: half

ρ_NPR = operator, ρ_NPR(4) = waarde.

### P012: "Lens F — Nederlandstalig" breekt vier-lenzenarchitectuur
Type: concept | Locatie: Artikel 13 | Zekerheid: high | Routestatus: gesloten

F = returnveld, niet Nederlandse lens.

## Eindoordeel

Totaal punten: 12
Gesloten: 12/12 ✅
- P001-P004: opgelost door splitsing + archivering
- P005-P012: opgelost door splitsing (al correct in gesplitste artikelen)

Prioriteit: Splits eerst het legacy-monoliet van de actuele Artikel-1-node. ✅ GEREED.

---

## Verwerkingslog

| Datum | Actie | Door | Status |
|-------|-------|------|--------|
| 2026-07-24 | Review geïmporteerd | hexa-engine | inbox → active |
| 2026-07-24 | P001: Legacy monoliet gearchiveerd (`archive/hexa-book-legacy-full-v3.md`) | hexa-engine | ✅ |
| 2026-07-24 | P001: hexa-book-001.md gereduceerd naar Artikel 1 + nidrā-pointers (3820→375 regels) | hexa-engine | ✅ |
| 2026-07-24 | P002: Statussysteem geüpgraded naar 3-dimensie (operator/execution/validatie) | hexa-engine | ✅ |
| 2026-07-24 | P003: Returnstatus harmoniseerd (alleen 'ongetest' in intro; E/F in aparte artikelen) | hexa-engine | ✅ |
| 2026-07-24 | P004: Λίθος = 319 (niet 610) — al correct in gesplitste artikel 002 | hexa-engine | ✅ (extern) |
| 2026-07-24 | P009: 4-bit/6-bit — al correct in gesplitste artikelen | hexa-engine | ✅ (extern) |
| 2026-07-24 | P010: 396 delerclaim — al correct in gesplitste artikelen | hexa-engine | ✅ (extern) |
| 2026-07-24 | P012: Lens F — al correct in gesplitste artikelen | hexa-engine | ✅ (extern) |
| 2026-07-24 | P005: Lens B waarden — opgelost door splitsing (artikel 002 heeft consistente waarden) | hexa-engine | ✅ (extern) |
| 2026-07-24 | P006: C_quality definitie — opgelost door splitsing (artikel 002 heeft binair DR_work=DR_source) | hexa-engine | ✅ (extern) |
| 2026-07-24 | P007: C_sound status — opgelost door splitsing (artikel 002 heeft correcte gedeeltelijke status) | hexa-engine | ✅ (extern) |
| 2026-07-24 | P008: DR_freq operator — opgelost door splitsing (artikel 002 heeft DR_freq_rounded + DR_freq_exact) | hexa-engine | ✅ (extern) |
| 2026-07-24 | P011: ρ_NPR(4) waarde-status — opgelost door splitsing (artikel 002 heeft correcte notatie) | hexa-engine | ✅ (extern) |
