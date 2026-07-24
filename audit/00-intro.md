---
audit_metadata:
  article: "00-intro"
  source_commit: "5a13c64"
  last_verified: "2026-07-24"
  operator_status_model: 3D
  engine_evidence:
    npr_sound_engine: "engine/npr_sound_engine.py"
    validate_return_cycle: "engine/validate_return_cycle.py"
  route_status: "actueel"
  supersedes: "legacy-v3 status_validated/status_executed/status_defined"
  note: "Introductie met 3D statusmodel. R_audio en ReturnCycle nu lokaal gevalideerd."
---

# 0 ≐ 1

## النار، الحجر، والتموج | अग्निः, शिला, तरंग | Πῦρ, Λίθος, Κύμα | 4 perspectieven op één stroom

نسخة ثالثة - الدائرة 3-6-9 | तृतीय संस्करण - ३-६-९ वलय | Τρίτη Έκδοση - Ὄλκισ ३-६-९ | Derde editie - De Wet van De Cirkel 3-6-9

بقلم Hexa | Hexa कृतम् | ὑπὸ Hexa | door Hexa

---

Dit boek bevat vier projectielenzen, één audio-superpositielaag en één returnmedium.
Alleen A-D zijn perspectieflenzen; E is de veldoperator; F is het returnveld.

Vier gelijktijdige perspectieven op één stroom:

Arabisch: de steen. De wiskunde die telt.
Sanskriet: de vibratie. De wiskunde die trilt.
Grieks: de vorm. De wiskunde die meet.
Latijn: de fractaal. De wiskunde die herhaalt.

Nederlands is geen vijfde rekenlens.
Nederlands is de metataal - de uitleg die de vier routes verbindt.

Dit zijn geen letterlijke vertalingen van elkaar.
Het zijn parallelle projecties - dezelfde bron door vier verschillende lenzen.
Elke taal heeft eigen regels, eigen tekensets, eigen reductie.

De informatie zit niet in één taal.
De informatie beweegt tussen de talen door sunya.
Sunya is leeg. Sunya is niet-leeg.

Lokaal: 0 ≠ 1
Volledig: 0 ≐_lens 1    (lensaxioma - operationeel gevalideerd pas na volledige E+R)

```
3D statusmodel (artikel 003 veldcontract):
  operator_status(R_audio)    = formeel
  operator_status(ρ_ℱ)        = formeel
  operator_status(ReturnCycle) = conceptueel
  execution_status(R_audio)    = voltooid
  validatie_status(R_audio)    = gevalideerd_lokaal
  validatie_status(ReturnCycle) = niet_gevalideerd
```

---

# Introductie 0 - Hoe dit boek rekent

Dit boek gebruikt niet één rekenlaag.

Binnen een lokale berekening blijven getallen, tekens en bewerkingen onderscheiden:

0 ≠ 1

Een letterwaarde moet controleerbaar zijn.
Een som moet binnen haar gekozen systeem kloppen.
Een functie mag niet ongemerkt door een andere functie worden vervangen.
Een hexadecimale reductie is niet hetzelfde als een decimale reductie, ook wanneer beide naar hetzelfde bronveld kunnen terugkeren.

Daarom draagt iedere uitkomst niet alleen een waarde, maar ook een route:

bron → differentiatie → representatie → bewerking → reductie → lokaal eindpunt

De waarde zonder route is onvolledig.

**Twee soorten eindpunten:**

- `r_local,i = reduce_i(...)` - het lokale eindpunt van een berekening (digitale reductie, byte-som, hex-projectie, etc.);
- `r_return = R(E) ∈ ℱ` - de volledige boekreturn via audio-superpositie en return-operator.

Een lokale digitale reductie is niet dezelfde return als de volledige E → R → ℱ route.

Het telsysteem is de lens.
De functie is de beweging door de lens.
Het lokaal eindpunt laat zien of de lokale berekening correct is.
De volledige boekreturn laat zien of de route haar samenhang heeft behouden.

Wanneer dit boek schrijft:

0 ≐_lens 1

betekent dit niet dat nul en één lokaal dezelfde numerieke waarde hebben.

Het lensaxioma leest nul en één op bronfunctieniveau als equivalent.

De volledige route toetst niet het bestaan van dit axioma,
maar onderzoekt of een vooraf vastgelegde returninvariant
tussen begin- en returntoestand behouden blijft.

Nul is het ongedifferentieerde bronveld.
Eén is de eerste lokale verschijning binnen dat veld.
Tijdens de route zijn zij verschillend.
In de volledige return worden zij als bron-equivalent gelezen.

Daarom geldt gelijktijdig:

lokaal: 0 ≠ 1
lensaxioma: 0 ≐_lens 1    (filosofische boekstelling)

**Twee niveaus van return:**

- `0 ≐_lens 1`: de centrale betekenis van het boek; axiomatische lensstelling;
- `3D statusmodel`: operationele status; drie dimensies per operator.

Deze versie heeft `E_audio_output` uitgevoerd.

De returnoperator `R_audio` is in artikel 003 formeel gespecificeerd,
in artikel 004 als `ρ_ℱ` uitgewerkt, en lokaal gevalideerd via `validate_return_cycle.py`.

Daarom geldt binnen het formele boekmodel:

```
3D statusmodel (R_audio):
  operator_status    = formeel        (artikel 003 veldcontract)
  execution_status   = voltooid       (engine/npr_sound_engine.py)
  validatie_status   = gevalideerd_lokaal  (26/26 ✅)

3D statusmodel (ρ_ℱ):
  operator_status    = formeel        (artikel 004 engine-operator)
  execution_status   = voltooid       (engine/validate_patanjali.py)
  validatie_status   = gevalideerd_lokaal

3D statusmodel (ReturnCycle):
  operator_status    = conceptueel    (artikel 002, R'/E'/C' nog open)
  execution_status   = niet_gestart
  validatie_status   = niet_gevalideerd
```

**Drie status-dimensies (3D model):**
```
operator_status  ∈ { formeel, conventie, interpretatief, conceptueel, open }
execution_status ∈ { voltooid, gedeeltelijk, niet_gestart }
validatie_status ∈ { gevalideerd_lokaal, niet_gevalideerd, verworpen }
```
"Niet gevalideerd" betekent niet automatisch "ongelijk".

Dit boek beweegt door drie rekenlagen.

---

## 1. Lokale rekenkunde

Hier worden letters, getallen en functies volgens expliciete regels behandeld.
Een berekening is alleen geldig wanneer basis, operator en representatie zijn benoemd.

---

## 2. Lensrekenkunde

Dezelfde bron kan door verschillende systemen anders worden geprojecteerd.
Een Arabische, Sanskriet-, Griekse, decimale of hexadecimale route kan een ander lokaal resultaat geven.

Dat verschil is geen fout zolang de actieve lens zichtbaar blijft.

Een lens is alleen lokaal geldig wanneer haar regels expliciet en consequent worden toegepast.

---

## 3. Return-rekenkunde

De volledige betekenis ligt niet alleen in het begin- of eindgetal, maar in de behouden samenhang van de route.

De vraag is daarom niet uitsluitend:

Welk getal komt eruit?

De vraag is ook:

Via welke lens?
Met welke functie?
Wat bleef tijdens de transformatie invariant?
Keert de uitkomst terug naar de bronstructuur?

De 3-6-9-structuur is binnen dit boek een validatielaag van die beweging.
Zij is niet de bron zelf.
Zij maakt de driedelige route zichtbaar:

Noise → Pattern → Return

Vuur transformeert.
Steen positioneert.
Water draagt.
De lens projecteert.
De return sluit de stroom.

0 ≠ 1 lokaal.
0 ≐_lens 1 als lensaxioma.
Na volledige (E → R → ℱ) kan de status `gevalideerd` of `verworpen` worden toegekend.

##### Formele definitie van de gebruikte relaties

`x ≐_lens y` betekent: binnen de filosofische lens van dit boek worden `x` en `y` op het niveau van de bronfunctie als equivalent gelezen. Het is een axiomatische stelling, geen lokaal bewijs.

**3D statusmodel** betekent: de operationele status van een route. Drie dimensies per operator:

```
operator_status  ∈ { formeel, conventie, interpretatief, conceptueel, open }
execution_status ∈ { voltooid, gedeeltelijk, niet_gestart }
validatie_status ∈ { gevalideerd_lokaal, niet_gevalideerd, verworpen }
```

waar de voorwaarde na volledige route:

```
validatie_status = gevalideerd_lokaal   ⟺   V_k(r_begin) = V_k(r_return)
validatie_status = verworpen             ⟺   V_k(r_begin) ≠ V_k(r_return)
```

waar `V_k: X_k → Y_k` de vooraf gekozen returninvariant is per route `k`.

**Validatieprotocol:** voor iedere route `k` wordt de invariant `V_k` vóór sonificatie en return vastgelegd. Een invariant die pas na inspectie van het resultaat wordt gekozen, telt niet als operationele validatie.

Zolang geen volledige `r → P → W → E → R → ℱ`-route is uitgevoerd:
```
validatie_status(r_begin, r_return) = niet_gevalideerd
```

`x ≘ y` betekent: de returnroute tussen `x` en `y` is geopend, maar bron-equivalentie is nog niet vastgesteld.
> **Lensoptiek 0:** Dit boek is een lens. Niet de bron. De route die je door dit boek volgt, is je huidige filter. De bron is er altijd geweest.
> **العدسة 0:** هذا الكتاب عدسة. ليس المصدر. الطريق الذي تتبعه في هذا الكتاب هو فلترك الحالي. المصدر كان موجوداً دائماً.
> **दृष्टि 0:** Idaṃ pustakaṃ darśanaṃ. Nāyaṃ mūlam. Margo yaṃ idaṃ pustakam anuvartase, tvaṃ darśanam. Mūlam sadā asti.

---

