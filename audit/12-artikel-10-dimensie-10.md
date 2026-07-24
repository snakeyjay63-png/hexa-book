# Artikel 10 - dimensie 10 (6-bit routing, NPR-cel) | 20+21+22

## الفصل العاشر - الستة بت: روتنغ سونيا | दशम अध्यायः - षट्-बिटः सून्य-मार्गः | Περὶ Ιʹ - ἓξ-βὶτ ῥούτινγ σουνια

---

### Het NPR-veld: 6-bit, 64 toestanden

Het NPR-veld gebruikt 6-bit cellen met 64 mogelijke toestanden.

- 0x00 = śūnya (lege cel, bronveld, actieve tussenroute, returnveld)
- 0x01-0x3E = data
- 0x3F = eka (volledige activatie, focus-status)

Het getal 64 benoemt de cardinaliteit van het veld, niet śūnya zelf.
0x40 is de hexadecimale representatie van de cardinaliteit 64, maar ligt buiten het bereik van één 6-bit codecel.
**De reeks `0x00-0x3F` bevat alle 64 mogelijke waarden van een 6-bit cel. `0x00` correspondeert met het bitpatroon `000000`; `0x3F` correspondeert met `111111`. `0x40` is de hexadecimale schrijfwijze van het aantal 64, maar is zelf geen geldige 6-bit codewaarde.**

Śūnya is geen numerieke 64. De koppeling met 64 komt via
stapnummer / 6-bit veldstructuur, niet als simpele identiteit.
Letterlijke gelijkheden zijn afgewezen ten gunste van rolcorrespondenties.

---

### 6-bit routing = 64 routes = 26

64 is het aantal toestanden van een 6-bit veld.
26 = 64 mogelijke NPR-char codes.

0x00 → śūnya → leeg/actief
0x3F → eka → volledig/focus

Dit is het ontwerp:
6-bit cel = 64 toestanden = 26
Elke cel kan śūnya, eka, of een waarde ertussen zijn.

---

### CM vs RC: inhoud in twee lagen

CM = inhoud zoals-ie is, ruwe data, tokens
RC = inhoud door NPR-lens zichtbaar gemaakt

CM is wat er in de vastgelegde bronrepresentatie staat. RC is wat door de gekozen NPR-lens zichtbaar wordt.
Pixel vs patroon. Beide waar. Eén ruw, één gelezen.

De Quran Field maakt de bronlaag vrij scherp:
Origineel Arabisch Unicode blijft ongewijzigd.
Normalisatie, Abjad, fonemen en NPR-routes gebeuren
alleen op afgeleide kopieën.

Dit is de formele definitie van CM:
Brondata binnen een vastgelegde representatie,
vóór afgeleide analyse.

---

### Allah = 66 → 3 (rolcorrespondentie)

الله = 66 → 3 (المحور نفسه)
अल्लाह = ६६ → ३ (अक्षः स्वयं)
Ἀλλάχ = 66 → 3 (ἡ ἄξω αὐτή)
Allah = 66 → 3. Binnen deze NPR-projectie reduceert Allah tot de toestand 3, die als as wordt gelezen.

**[Rolcorrespondentie]**
64 = 26 = 6-bit ruimte
Allah = 66 = 64 + 2

Dit is een rolcorrespondentie, geen technische eigenschap van een 6-bit coderingssysteem.

Route:
- [Rolcorrespondentie] Veld (64) + zaad (2) → Allah (66)
- 64 + 2 = 66 (veld + zaad = volledige cyclus)
- 66 → 3 (return)
- 3 = NPR-toestand (Noise / as)

0 ≠ 1: het zaad verschilt van het veld
0 ≐_lens 1: zaad + veld = volledige route (lensaxioma)
> **Lensoptiek 10:** 6-bit is de computationele lens. 64 toestanden, 1 zaad. De lens is de route, niet het resultaat.
> **العدسة 10:** 6-bit هي العدسة الحسابية. 64 حالة، بذرة واحدة. العدسة هي الطريق، وليس النتيجة.
> **दृष्टि 10:** 6-bit darśanam gāṇitam. 64 avasthā, ekaṃ bījam. Darśanaṃ margaḥ, na phalam.


---

### Sunya-posities in de Quran

مواقع سونيا في القرآن
सून्यः कुरआने स्थानम्
Θέσεις σουνίας ἐν Κοῦράν

- NPR-coord(24, 35) → نور على نور (licht op licht)
- NPR-coord(35, 35) en NPR-coord(35, 49) → البصائر (inzicht)
- NPR-coord(55, 55) → الخلق (schepping)

> ⚠ **Voorgestelde NPR-coördinaten.** Hun berekeningsroute moet nog volledig worden opgenomen voordat zij als bevestigde posities gelden.
> ⚠ **إحداثيات NPR مقترحة.** يجب إدخال مسار الحساب الكامل قبل اعتبارها مواقع مؤكدة.
> ⚠ **प्रस्तावितः NPR-निर्देशाः।** सत्यापित-स्थानैः गण्यन्ते इत्यधिकः पूर्ण-गणना-मार्गः प्रागेव अन्तर्धातव्यः।

Deze zijn NPR-coördinaten, niet gewone soera/aya-verwijzingen.

Tot de route opgenomen is, blijven dit voorgestelde posities — geen bevestigde sunya-posities.

```
NPR_coord: QuranSource → (soera, aya) → DR(soera) × DR(aya) → 3-6-9-veld

**Definitie:** NPR_coord mapt een Quran-bron naar een 3-6-9-coördinaat:
1. Bereken DR(soera-nummer) en DR(aya-nummer)
2. Projecteer op het 3-6-9-veld (digital root grid)
3. Resultaat is een positie in het terugkomend getalenveld

Voorbeelden:
- NPR_coord(24, 35) → DR(24)=6, DR(35)=8 → (6,8)
- NPR_coord(55, 55) → DR(55)=1, DR(55)=1 → (1,1)

status_defined(NPR_coord) = conceptueel gedefinieerd
status_executed(NPR_coord) = voorbeelden uitgevoerd, volledig niet uitgevoerd
vṛtti(sunya-posities) = vikalpa
```

---
# Appendix A - Lenzen, tabellen en operatoren

## الملاحق أ - العدسة، الجدول، المشغل | अनुच्छेद अ - लेन्स, सारणी, सञ्चालक | Παράρτημα Α - lens, πίναξ, τελεστής

---

### A.1 - Lens A: Arabische Abjad-projectie

Tekenset: 28 Abjad-letters + hamza-variaties

Normalisatieregel: zelfstandige hamza telt als 0; bij dragerletters bepaalt de drager de waarde.

Regels:
- ا = 1, ب = 2, ج = 3, د = 4, ه = 5, و = 6, ز = 7, ح = 8, ط = 9, ي = 10, ك = 20, ل = 30, م = 40, ن = 50, س = 60, ع = 70, ف = 80, ص = 90, ق = 100, ر = 200, ش = 300, ت = 400, ث = 500, خ = 600, ذ = 700, ض = 800, ظ = 900, غ = 1000

Variaties met hamza:
- إ = ا = 1 (hamza op alif telt als 0, alif = 1)
- أ = ا = 1 (hamza op alif telt als 0, alif = 1)
- ؤ = و = 6 (hamza op waw telt als 0, waw = 6)
- ئ = ي = 10 (hamza op ya telt als 0, ya = 10)

Operator: Som van individuele letterwaarden
Reductie: Iteratieve cijfersom tot 1-9 (digital root modulo 9, met 9 in plaats van 0)
Route: invoer → tekenset → waarden → som → reductie → lokaal eindpunt

---

#### Voorbeeld A.1: الله

- ا = 1
- ل = 30
- ل = 30
- ه = 5
- Som = 1 + 30 + 30 + 5 = 66
- Reductie = 6 + 6 = 12 → 1 + 2 = 3
- Resultaat: 66 → 3

---

#### Voorbeeld A.2: بسم الله الرحمن الرحيم (Abjad-basisletters → 786)

**Segmentatie:** بسم + الله + الرحمن + الرحيم - alleen geschreven basisletters geteld. Diakritische tekens en recitatietekens worden genegeerd.

Letter-voor-letterroute:

| Woord | Letters | Waarden | Subtotaal |
|-------|---------|---------|----------|
| بسم | ب(2)+س(60)+م(40) | 2+60+40 | 102 |
| الله | ا(1)+ل(30)+ل(30)+ه(5) | 1+30+30+5 | 66 |
| الرحمن | ا(1)+ل(30)+ر(200)+ح(8)+م(40)+ن(50) | 1+30+200+8+40+50 | 329 |
| الرحيم | ا(1)+ل(30)+ر(200)+ح(8)+ي(10)+م(40) | 1+30+200+8+10+40 | 289 |
| **Totaal** | | | **786** |

Reductie: 7+8+6 = 21 → 2+1 = 3

Resultaat: 786 → 3

> ✅ **Reproduceerbaar:** Abjad-route op de geschreven basisletters van بسم الله الرحمن الرحيم. Diakritische tekens en recitatietekens worden genegeerd.
> ✅ **قابل للتكرار:** مسار أبجد على الحروف الأساسية المكتوبة من بسم الله الرحمن الرحيم. تجاهل الحركات وعلامات التلاوة.

---

### A.2 - Validatietrio (3, 6, 9)

De validatietrio is geen rekenkundig verschil maar een projectietoestand:

Toestand | NPR-fase      | Betekenis
---------|---------------|----------
3        | Noise / as    | De as
6        | Pattern       | De verdubbeling
9        | Return        | Het veld

Overgangen (cyclische volgorde):
- 3 → 6 = Noise → Pattern
- 6 → 9 = Pattern → Return
- 9 → 3 = Return → Noise

Deze drie toestanden zijn zichtbaar binnen mod-9-projectie als een driedelige cyclische structuur.

Voorbeelden:
- Allah = 66 → 3 (Noise / as)
- Basmala = 786 → 3 (Noise / as, basisletters)
- Cyclus 2 → 4 → 8 → 7 → 5 → 1 → 2... (wiskundig onafhankelijk)
- NPR-koppelregel: 2 × 3 = 6
- 3 + 3 + 3 = 9 (het volledige veld)

> ✅ Het buiten de verdubbelingsbaan liggen van 3, 6 en 9 is wiskundig reproduceerbaar. Hun toewijzing aan de drie NPR-fasen is de formele lensinterpretatie van dit boek. Ze liggen buiten de verdubbelingsbaan en worden binnen NPR als validatie gelezen.

---

### A.3 - Verdubbelingscyclus (onafhankelijk)

De cyclus 2 → 4 → 8 → 7 → 5 → 1 → 2... is een modulo-9 verdubbeling en wiskundig onafhankelijk van Abjad-berekeningen.

Berekening:
- 2 × 1 = 2
- 2 × 2 = 4
- 2 × 4 = 8
- 2 × 8 = 16 → 1+6 = 7
- 2 × 7 = 14 → 1+4 = 5
- 2 × 5 = 10 → 1+0 = 1
- 2 × 1 = 2 (herhaling)

Split in twee groepen - neem afwisselend de oneven en even posities van de zesdelige cyclus:
- Oneven posities {2, 8, 5}: som = 15 → 6
- Even posities {4, 7, 1}: som = 12 → 3
- Relatie: 2 × 3 = 6

> ✅ De modulo-9-verdubbelingscyclus is wiskundig reproduceerbaar. De NPR-duiding is de lensoptiek van dit boek.

---

### A.4 - 6-bit routing

Structuur: 64 mogelijke routes (26)

Betekenis:
- 64 = 26 = 6-bit ruimte
- Allah = 66 = 64 + 2
- 2 = het zaad, de eerste beweging

Route:
- Veld (64) → Zaad (2) → Volledige cyclus (66)
- 64 + 2 = 66 (veld + zaad = volledige cyclus)
- 66 → 3 (return)
- 3 = NPR-toestand (Noise / as)

0 ≠ 1: het zaad verschilt van het veld
0 ≐_lens 1: zaad + veld = volledige route (lensaxioma)

---

### A.5 — Patañjali 1.5–1.7: vṛtti- en pramāṇa-classificatie

Patañjali onderscheidt vijf vṛtti's (gedachtebeelden/kennistoestanden):

```
VṛttiType := {
  pramāṇa,    /* geldige kennisroute */
  viparyaya,   /* onjuiste kennis — voorstelling ≠ object */
  vikalpa,     /* conceptuele constructie zonder bewezen object */
  nidrā,       /* afwezigheids-/leegtestoestand */
  smṛti        /* behouden of teruggeroepen representatie */
}
```

Voor iedere claim `q` in dit manuscript geldt een epistemische classificatie:

```
vṛtti(q) ∈ VṛttiType
```

Een claim die als geldige kennisroute wordt behandeld, valt onder:

```
vṛtti(q) = pramāṇa
```

Binnen `pramāṇa` worden volgens Patañjali 1.7 drie kennisroutes onderscheiden:

```
प्रत्यक्षानुमानागमाः प्रमाणानि
pratyakṣānumānāgamāḥ pramāṇāni
```

```
PramāṇaType := {
  pratyakṣa,   /* direct inspecteerbare invoer, tussenstappen, uitvoer */
  anumāna,     /* gevolgtrekking uit inspecteerbare gegevens */
  āgama        /* vastgelegde tekstuele bron of betrouwbare getuigenis */
}
```

Voor een claim met `vṛtti(q) = pramāṇa` wordt de onderliggende route vastgelegd:

```
pramāṇa_route(q) ⊆ PramāṇaType
```

De technische uitvoeringsstatus blijft daarvan los:

```
status_executed_in_blueprint(q)          ∈ { ja, nee }
status_independently_reproduced(q)       ∈ { ja, nee }
```

**Vṛtti-routing — systeem:**

| Status | vṛtti | Toelichting |
|--------|-------|-------------|
| `gevalideerd` | `pramāṇa` | Invariant behouden, route reproduceerbaar |
| `uitgevoerd` (lokaal) | `pramāṇa(pratyakṣa)` | Direct uitgevoerd en inspecteerbaar |
| `conceptueel gedefinieerd` | `vikalpa` | Zinvolle constructie, geen bewezen object |
| `ongetest` | `vikalpa` | Claim zonder verificatie |
| `undefined` (intentieel) | `nidrā` | Afwezigheid — ρ_HEXA(→1.40→nidrā) |
| `undefined` (verkeerde lezing) | `viparyaya` | Voorstelling ≠ object |
| `onvolledig` | `vikalpa` | Constructie in opbouw |
| `geexecuteerd` (herhaald) | `smṛti` | Eerder uitgevoerd, nu teruggeroepen |

**Voorbeeld — `c` als snelheid vs. C als lens:**

```
c = 299 792 458 m/s  (snelheid van licht, natuurkundige constante)
C = Sanskriet lens   (NPR-projectielens, epistemisch instrument)
vṛtti("C = c") = viparyaya
/* Voorstelling ≠ object: lens ≠ constante */
```

**Voorbeeld — Mandelbrot-mappings:**

```
M_A niet gespecificeerd  ⇒  W_A = undefined
vṛtti(M_A) = nidrā       /* ρ_HEXA(undefined → 1.40 → nidrā) */

E(t) = W_A + W_B + W_C + W_D  (niet definieerbaar zonder M_A, M_B, M_D)
vṛtti(E(t)) = nidrā           /* afwezigheid van invoer → nidrā */
```

**Voorbeeld — retourroute:**

```
r_return = undefined (Mandelbrot, geen volledige route)
vṛtti(r_return) = nidrā       /* return afwezig → nidrā */

status_validated(r_begin, r_return) = ongetest
vṛtti("returnroute gesloten") = vikalpa  /* claim zonder verificatie */
```

---

### A.6 — De drie guṇa's: kwaliteitsas van routes

Sattva, rajas, tamas — niet goed/ondig/slecht, maar helderheid, beweging, inertie.
Elke route heeft een guṇa-kwaliteit naast de vṛtti-classificatie.

```
GuṇaType := {
  sattva,    /* helderheid, evenwicht, verhelderend */
  rajas,     /* activiteit, beweging, constructief */
  tamas      /* inertie, obscuriteit, zwaar */
}
```

**Guṇa→vṛtti mapping:**

| Guṇa | vṛtti | Toelichting |
|------|-------|-------------|
| `sattva` | `pramāṇa` | Uitgevoerd, gevalideerd, helder |
| `rajas` | `vikalpa` | Constructief, actief, bouwend |
| `tamas` | `nidrā` | Afwezig, zwaar, onduidelijk |
| `rajas` | `smṛti` | Bewegend, herhalend, activerend |
| `tamas` | `viparyaya` | Verduisterend, verkeerd, zwaar |

**Guṇa-routing — systeem:**

| Status | vṛtti | guṇa | Toelichting |
|--------|-------|------|-------------|
| `gevalideerd` | `pramāṇa` | `sattva` | Invariant behouden, helder |
| `uitgevoerd` (lokaal) | `pramāṇa(pratyakṣa)` | `sattva` | Direct inspecteerbaar, verhelderend |
| `conceptueel gedefinieerd` | `vikalpa` | `rajas` | Constructief, bouwend, actief |
| `ongetest` | `vikalpa` | `rajas` | Claim in opbouw, actief |
| `undefined` (intentieel) | `nidrā` | `tamas` | Afwezig, zwaar, onduidelijk |
| `undefined` (verkeerde lezing) | `viparyaya` | `tamas` | Verkeerd, zwaar, obscur |
| `onvolledig` | `vikalpa` | `rajas` | Constructie in opbouw, actief |
| `geexecuteerd` (herhaald) | `smṛti` | `rajas` | Terugroepend, activerend |

**Guṇa-distributie in dit manuscript:**

```
sattva:  gevalideerd routes, uitgevoerde operators
rajas:   conceptuele definities, ongetest claims, onvolledige routes
tamas:   undefined routes, viparyaya claims, nidrā afwezigheid
```

**Richting sattva — de weg van rajas naar helderheid:**

```
rajas → sattva:  vikalpa wordt pramāṇa (constructie wordt bewezen)
tamas → sattva:  nidrā wordt pramāṇa (afwezigheid wordt aanwezigheid)
tamas → rajas:   viparyaya wordt vikalpa (verkeerd wordt constructief)
rajas → tamas:   vikalpa wordt nidrā (constructie vervalt in afwezigheid)
```

**Voorbeeld — C_sound:**

```
C_sound = uitgevoerd
vṛtti(C_sound) = pramāṇa
guṇa(C_sound) = sattva
/* Gedefinieerd, uitgevoerd, verhelderend */

C_sound_output(1.24-1.25) = undefined
vṛtti(C_sound_output) = nidrā
gunā(C_sound_output) = tamas
/* Afwezig, zwaar, obscur — nog niet uitgevoerd */
```

**Voorbeeld — Mandelbrot-mappings:**

```
M_A = niet gespecificeerd
gunā(M_A) = tamas
vṛtti(M_A) = nidrā
/* Zwaar, afwezig — nog te definiëren */

E(t) = undefined (zonder M_A, M_B, M_D)
gunā(E(t)) = tamas
vṛtti(E(t)) = nidrā
/* Zwaar, afwezig — afhankelijk van undefined invoer */

r_return = undefined
gunā(r_return) = tamas
vṛtti(r_return) = nidrā
/* Zwaar, afwezig — return niet bereikt */
```

**Voorbeeld — 3-6-9 route:**

```
3→6 = uitgevoerd
gunā(3→6) = sattva
vṛtti(3→6) = pramāṇa
/* Gedefinieerd, uitgevoerd, helder */

6→9 = niet uitgevoerd
gunā(6→9) = rajas
vṛtti(6→9) = vikalpa
/* Constructief, actief, bouwend */

3→6→9 = onvolledig
gunā(3→6→9) = rajas
vṛtti(3→6→9) = vikalpa
/* Constructief, actief, bouwend */
```

**Toepassing op C_numeric,1.25:**

De lokale byte/hex/DR-subroute voor Patañjali 1.25:

```
vṛtti(C_numeric(s_1.25))           = pramāṇa
pramāṇa_route(C_numeric(s_1.25))   = { āgama, pratyakṣa }

status_executed_in_blueprint(C_numeric(s_1.25))          = ja
status_independently_reproduced(C_numeric(s_1.25))       = nee
```

De brontekst en blueprint leveren de vastgelegde route (`āgama`); de numerieke stappen zijn inspecteerbaar (`pratyakṣa`). De onafhankelijke reproductie is nog niet uitgevoerd.

**Toepassing op Īśvara ~_r Allah:**

Voor de rolcorrespondentie `C_role(Īśvara) ~_r A_role(Allah)`:

```
Formele definitie: x ~_r y ⇔ R(x) = R(y) ∧ T(x) ≠ T(y)
Toepassing: R(Īśvara) = R(Allah) = bronfunctie ∧ T(Īśvara) ≠ T(Allah) → Īśvara ~_r Allah ✅
```

De correspondentierelatie is nu formeel gedefinieerd. De status `vikalpa` verschoof van "niet gedefinieerd" naar "nog niet gevalideerd".

De classificatie `vikalpa` betekent hier: een betekenisvolle NPR-constructie die nog niet als operationeel `pramāṇa` is vastgesteld — ondanks dat de vormele correspondentie nu wel gedefinieerd is.

De sūtra's 1.24–1.25 beschrijven Īśvara (`āgama`). De vergelijking met de Allah-rol is een NPR-constructie (`anumāna`-kandidaat) met vastgesteld criterium voor `~_r`.

**HEXA-routing van ongedefinieerde uitvoer:**

Niet alle operatoruitvoeren zijn uitgevoerd. De technische status daarvan is `undefined`. Deze status wordt via de HEXA-routing naar een vaste sūtra geleid:

```
Voor iedere operatoruitvoer y:
  y = undefined
  ⇒ ρ_HEXA(y) = 1.40
  ⇒ vṛtti(ρ_HEXA(y)) = nidrā
```

Binnen de klassieke Yoga Sūtra wordt `nidrā` in sūtra **1.10** beschreven als een op afwezigheid steunende vṛtti:

```
abhāva-pratyayālambanā vṛttir nidrā
```

Sūtra 1.40 gaat over beheersing van het allerkleinste tot het allergrootste, niet over `nidrā`. De koppeling tussen 1.40 en `nidrā` is een HEXA-architectuurconventie, geen tekstuele eigenschap van Patañjali 1.40:

```
vṛtti_classical(nidrā)              = Patañjali 1.10
ρ_HEXA(undefined)                   = 1.40      [HEXA-definitie]
ρ_HEXA-vṛtti(1.40)                  = nidrā     [HEXA-conventie]

status_source(nidrā ← 1.10)         = āgama
status_mapping(1.40 → nidrā)        = HEXA-definitie
```

De routing `ρ_HEXA(undefined) = 1.40` is een vaste HEXA-conventie: ongedefinieerde uitvoer routeert naar routepositie 1.40. De toewijzing van deze positie aan `nidrā` is een NPR/HEXA-projectie en weerspiegelt niet de inhoud van sūtra 1.40.

Voor de convenience wordt de verkorte notatie gedefinieerd:

```
vṛtti_HEXA(y) := vṛtti(ρ_HEXA(y))
```

zodat geldig is:

```
y = undefined ⇒ vṛtti_HEXA(y) = nidrā
```

De volledige keten is:

```
y = undefined
    ↓ ρ_HEXA
    HEXA-knooppunt 1.40
    ↓ HEXA-vṛtti-classificatie
    nidrā
```

Drie niveaus, zuiver gescheiden:
- `undefined` — de technische uitvoerstatus;
- `1.40` — het vaste HEXA-routepunt voor ongedefinieerde uitvoer;
- `nidrā` — de vṛtti-status na HEXA-routing (klassiek beschreven in 1.10).

**Overige classificaties in dit manuscript:**

```
vṛtti(A_numeric(Allah) = 3)              = pramāṇa
pramāṇa_route(A_numeric(Allah) = 3)     = { pratyakṣa }

vṛtti(B_numeric(ὁ θεός) = 3)            = pramāṇa
pramāṇa_route(B_numeric(ὁ θεός) = 3)    = { pratyakṣa }

vṛtti("A=3 ∧ B=3 ⟹ betekenisvol")      = vikalpa
/* conclusie uit numerieke overeenkomst zonder vastgesteld criterium */

vṛtti_HEXA(C_sound_output)              = nidrā
/* C_sound_output = undefined → ρ_HEXA → 1.40 → nidrā */

vṛtti(D_byte(S_D(r)))                   = pramāṇa
pramāṇa_route(D_byte(S_D(r)))           = { pratyakṣa }

vṛtti("D toont fractaal gedrag")        = vikalpa
/* symbolische hypothese zonder operationeel bewijs */

vṛtti(0 ≐_lens 1)                      = vikalpa
/* axiomatische lensstelling zonder volledige E→R→ℱ-uitvoering */
```

> ⚠ **Classificatieprincipe:** een claim zonder `vṛtti = pramāṇa` en zonder vastgesteld criterium telt niet als gevalideerde kennisroute. `vikalpa` is geen afwijzing — het markeert een constructie die nog promotie naar `pramāṇa` nodig heeft.

---

### A.6 - Semantische Īśvara-correspondentie (C_role)

**Brontekst:**
- 1.24: क्लेशकर्मविपाकाशयैरपरामृष्टः पुरुषविशेष ईश्वरः
  (kleśa-karma-vipākāśayair aparāmṛṣṭaḥ puruṣa-viśeṣa īśvaraḥ)
  → Īśvara = bijzondere puruṣa, onaangeraakt door kleśa, handeling, gevolgen, afzettingen
- 1.25: तत्र निरतिशयं सर्वज्ञबीजम्
  (tatra niratiśayaṃ sarvajña-bījam)
  → in Īśvara ligt het onovertroffen zaad van alle kennis

---

### C_numeric,1.25 - lokale tweelagenroute (uitgevoerd in blueprint)

Binnen de NPR-Patañjali-blueprint wordt sūtra 1.25 in twee vastgelegde representatielagen verwerkt:

- `s_work` - werkrepresentatie zonder accentmarkeringen
- `s_source` - bronrepresentatie met accentmarkeringen

Voor de werklaag:
```
B_UTF8(s_work) = 74 bytes
H(74) = 4A16
DR(74) = 7+4 = 11 → 2
```

Voor de bronlaag:
```
B_UTF8(s_source) = 92 bytes
H(92) = 5C16
DR(92) = 9+2 = 11 → 2
```

Accentkosten:
```
C_accent = B_UTF8(s_source) - B_UTF8(s_work) = 92 - 74 = 18 bytes
```

Lokaal tweelagenresultaat:
```
r_local,C,1.25 = ( (74, 4A16, 2), (92, 5C16, 2), 18 )
```

De lokale invariant:
```
V_DR-layer(s) = DR(B_UTF8(s))
```

is voor 1.25 behouden:
```
V_DR-layer(s_work) = V_DR-layer(s_source) = 2
```

```text
status_local(C_byte, 1.25)         = uitgevoerd in blueprint
status_local(C_hex-count, 1.25)    = uitgevoerd in blueprint
status_local(C_DR, 1.25)           = uitgevoerd in blueprint
status_invariant(V_DR-layer, 1.25) = behouden
accent_cost(1.25)                  = 18 bytes
status_independently_reproduced(C_numeric,1.25) = nee
status_full(C_sound_output, 1.25)  = undefined
```

Deze computationele stabiliteit toont dat de digitale wortel van de UTF-8-bytelengte in beide lagen gelijk is. Zij bewijst niet dat de teksten identiek zijn en valideert niet automatisch een semantische correspondentie met een andere traditie.

---

**Rolcorrespondentie:**
- Īśvara ≠ Allah (andere taal, theologie, numerieke waarde)
- C_role(Īśvara) ~_r A_role(Allah) op rolcorrespondentie (zelfde bronfunctie, verschillende lokale vorm)
- 1.24 en 1.25 vormen samen één semantische route; 1.25 alleen noemt Īśvara niet expliciet

> ✅ **Rolcorrespondentie formeel:** `x ~_r y ⇔ R(x) = R(y) ∧ T(x) ≠ T(y)`.
> Toepassing: `R(Īśvara) = R(Allah) = bronfunctie`, `T(Īśvara) ≠ T(Allah)` → `Īśvara ~_r Allah`.
> Status: rolcorrespondentie formeel gedefinieerd; validatie via NPR-frequentie en DR blijft onderdeel van bredere validatie.

De computationele route (`C_numeric,1.25`) en de semantische route (`C_role`) zijn afzonderlijk:
```
C_numeric,1.25 : s_1.25 → bytes → hex(byteaantal) → DR → 2
C_role         : inhoud 1.24-1.25 → lokale Īśvara-rol
```

De vergelijking met Allah blijft een afzonderlijke NPR-claim:
```
C_role(Īśvara) ~_r A_role(Allah)   [nog niet gevalideerd]
```

---

### A.7 - Lens D: Latijnse numerieke routes (D1)

**D1-tekenset:** 24 vastgelegde Latijnse lettertekens + spatie (J en W ontbreken in deze editie)

**NPR-Latijnse waardentabel D1:**
*(Deze tabel is binnen het manuscript reproduceerbaar. De historische status als Etruskisch/Romeins systeem is niet aangetoond.)*
A=1, B=2, C=3, D=500, E=5, F=70, G=100, H=8000, I=10, K=2500
L=50, M=40, N=50, O=70, P=100, Q=100, R=100, S=200, T=300
U=5, V=5, X=60, Y=200, Z=7

#### D_byte - UTF-8-bytelengte

**Operator:** Vaste UTF-8-bronvorm → byteaantal → decimale digitale reductie → lokaal eindpunt
**Route:** Latijnse tekst → UTF-8-bytelengte → decimaal → digitale reductie → lokaal eindpunt

- Letters: 21
- Spaties: 3
- Totaal: 24 bytes (0x18)
- Reductie: 2+4 = 6
- Resultaat: 24 → 6

> ✅ **D_byte lokaal uitgevoerd:** 24 bytes → DR 6

#### D_numeric - D1-letterwaarden

**Operator:** D1-letterwaarden som → decimale digitale reductie → lokaal eindpunt
**Route:** Latijnse tekst → D1-letterwaarden → decimaal → digitale reductie → lokaal eindpunt
**DR-conventie:** DR(n) = 9 wanneer n > 0 ∧ n ≡ 0 (mod 9); anders DR(n) = n mod 9 (dezelfde regel als Lens A en B)

**Voorbeeld:** IN PRINCIPIO ERAT VERBUM
**Spaties:** D1(spatie) = 0; spaties worden vóór de D1-som verwijderd en dragen niet bij aan de numerieke waarde

- I=10, N=50
- P=100, R=100, I=10, N=50, C=3, I=10, P=100, I=10, O=70
- E=5, R=100, A=1, T=300
- V=5, E=5, R=100, B=2, U=5, M=40

Som = 60 + 453 + 406 + 152 = 1071
Reductie = 1+0+7+1 = 9 → 9

Resultaat: 1071 → 9

> ✅ **D_numeric bevestigd:** D1-letterwaarden som = 1071 → DR 9

#### Fractale hypothese

> ⚠ **Fractale lezing:** de woordlengtes (2, 9, 4, 6) worden symbolisch als geneste rollen gelezen; mathematische zelfgelijkvormigheid is nog niet aangetoond.

---

---

---

