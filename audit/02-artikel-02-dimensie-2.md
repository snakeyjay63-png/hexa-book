---
audit_metadata:
  article: "02-artikel-02-dimensie-2"
  source_commit: "5a13c64"
  last_verified: "2026-07-24"
  operator_status_model: 3D
  engine_evidence:
    npr_sound_engine: "engine/npr_sound_engine.py"
    validate_return_cycle: "engine/validate_return_cycle.py"
  route_status: "actueel"
  supersedes: "legacy-v3 status_validated/status_executed/status_defined"
  note: "Artikel 02 audit. ReturnCycle conceptueel. Synth/R_audio/ReturnCycle nu lokaal gevalideerd."
---

# HEXA-BOEK #002 - Terugkeerpad en Return-invariant

لا عودة بدون صوت. لا صوت بدون عدسة. لا عدسة بدون عد.

प्रत्यर्पणम् ध्वना। ध्वनिर् लेन्सात्। लेन्सः गणनात्।

No return without sound. No sound without lens. No lens without count.

---

## Status

**Conceptueel kader voor boek #002.**

Boek #001 heeft de volledige C→E→R keten uitgevoerd:
- C_sound uitgevoerd voor Patañjali 1.24-1.25
- Vier golven gegenereerd (W_A..W_D)
- Superpositie E(t) gegenereerd en opgeslagen
- Return-operator R(E) uitgevoerd
- V_k invariant gevalideerd: r_begin = r_return = (3, 7, 5, 9)

Boek #002 verkent het terugkeerpad:
- Hoe leest F de return-toestand terug?
- Welke invarianten behouden zich door meerdere E→R cycli?
- Kan r_return zelf weer als invoer dienen voor een nieuwe C-route?

---

## Architectuur

```text
Boek #001: A → B → C → D → E → R → ℱ
Boek #002: ℱ → R' → E' → C' → ... (terugkeerpad)
```

### ReturnCycle-structuur — conceptueel

```text
ReturnSeedCycle : ℱ → CInput
ReturnSeedCycle := C' ∘ E' ∘ R'

ForwardCycle : CInput → ℱ
ForwardCycle := ρ_ℱ ∘ R ∘ E ∘ C

ReturnCycle : ℱ → ℱ
ReturnCycle := ForwardCycle ∘ ReturnSeedCycle

return_invariant(r) ⇔ V_k(ReturnCycle(r)) = V_k(r)
```

**3D statusmodel (ReturnCycle):**
```text
operator_status(ReturnCycle) = conceptueel    (R'/E'/C' nog open)
execution_status(ReturnCycle) = niet_gestart
validatie_status(ReturnCycle) = niet_gevalideerd

operator_status(ForwardCycle) = formeel       (R_audio + ρ_ℱ vast)
execution_status(ForwardCycle) = voltooid     (engine/npr_sound_engine.py)
validatie_status(ForwardCycle) = gevalideerd_lokaal
```

---

**Impact op bedrock:**
- [x] Formele operator
- [x] Lens-projectie
- [x] Status-notatie
- [ ] Vṛtti-classificatie
- [ ] Drie frequentiesystemen
- [ ] Afrondingsgevoeligheid

De return-toestand r_return ∈ ℱ is niet eindpunt maar doorlaat.
Het terugkeerpad begint waar #001 eindigde.

---

## Halve Routes - Conceptuele Bruggen

Boek #001 voerde C→E→R uit maar liet 6 routes half. Deze sectie sluit ze.
Elke route heeft een expliciete status: **gedefinieerd** (wiskundig), **conventie** (keuze), of **interpretatie** (lezing).

---

### 1. byte/hex → Hz Mapping

**Gap gedeeltelijk geformaliseerd:** De route van Sanskriet-byte-telling (of hex-waarde) naar frequentie in Hz.
`reference_bytes` heeft nog geen invoerverzameling.

In boek #001 werden frequenties gegenereerd (397.04, 490.30, 393.39, 468.36 Hz).
De mapping van byte-aantal naar Hz was impliciet; hier wordt deze expliciet.

#### Definitie

```
byte_to_freq(B) = base_freq × (B / reference_bytes)
```

- `base_freq` = 432 Hz (Vedic standaard - zie sanskrit-frequency-bridge)
- `reference_bytes` = gemiddelde Sanskriet-byte count per segment
- `B` = byte count van het huidige segment

Deze lineaire mapping schaleft het byte-aantal naar de 432 Hz referentieband.

#### Alternatief: hex → frequentie via phonem-bridge

Elke hex-digit kan via de sanskrit-frequency-bridge naar een phonem, en daarvan naar Hz:

```
hex_digit → phonem → oscillator_frequency
```

Dit pad is **gedetailleerder** maar vereist de volledige phonem-tabel.
Het lineaire `byte_to_freq()` is de **standaard** tenzij anders gespecificeerd.

**Status:**
```
byte_to_freq:
  operator_status = conventie
  execution_status = gedeeltelijk
  validatie_status = niet_gevalideerd

C_byte_freq:
  operator_status = open
  execution_status = niet_voltooid
  validatie_status = niet_gevalideerd
```

> `C_byte_freq` is de beoogde algemene operator. `byte_to_freq` is de huidige conventie-implementatie.
> `execution_status = gedeeltelijk`: zonder invoerverzameling `S` en concrete `reference_bytes(S)` kan de operator niet geëvalueerd worden.

#### C-text-route helpers

```
C_layer_delta(s) := len_bytes(s_source) - len_bytes(s_work)
H_0(s, layer) := len_bytes(s_layer)
H_1(s, layer) := hex(H_0(s, layer))
H_2(s, layer) := DR(H_0(s, layer))
```
**Verwijzing:** `sanskrit-frequency-bridge` skill voor phonem→Hz tabel.

---

### 2. avg_freq → DR_freq

**Gap gesloten:** Hoe een gemiddelde frequentie een digital root oplevert.

Voorbeeld uit boek #001:
- `avg_freq = 437.27 Hz` → `DR_freq = 5`
- Berekening: DR(4+3+7+2+7) = DR(23) = DR(2+3) = DR(5) = 5

#### Twee Padvarianten

De uitkomst hangt af van afronding. Twee expliciete varianten:

```
DR_freq_rounded(f)  = DR( cijfers in round(f, 2) )     // conventie, huidige praktijk
DR_freq_exact(f)    = DR( cijfers in exacte f )         // alternatief
```

**Voorbeeld van gevoeligheid:**
- `f = 437.27` (afgerond) → DR(4+3+7+2+7) = DR(23) = 5
- `f = 437.2725` (exact) → DR(4+3+7+2+7+2+5) = DR(30) = 3
- `f = 437.273` → DR(4+3+7+2+7+3) = DR(26) = DR(8) = 8

De DR verandert volledig bij kleine afronddetails (5 vs 3). Daarom:

> **DR_freq is een conventie, geen natuurwet.** De gekozen afronding bepaalt de uitkomst.

**Standaard:** `DR_freq_rounded(f)` met 2 decimalen, tenzij anders vermeld.

**Status:**
```
C_freq_DR_rounded:
  operator_status = conventie
  execution_status = voltooid
  validatie_status = gevalideerd
```

#### DR_freq als conventie

```
C_freq_DR_rounded(f) = DR( cijfers in round(f, 2) )  // standaard
C_freq_DR_exact(f)   = DR( cijfers in exacte f )     // alternatief
```

**Afrondingsgevoeligheid:**
- `f = 437.27` (2 decimalen) → DR(4+3+7+2+7) = DR(23) = 5
- `f = 437.2725` (exact) → DR(4+3+7+2+7+2+5) = DR(30) = 3

#### Helper: cijfer-integer conversie (P006)

```
digits_int_k(x) = parseInt(remove_non_digits(format_fixed(x, k)))
DR_digits_k(x) = DR(digits_int_k(x))
```

Voorbeeld: `digits_int_2(437.2725)` = 43727 → DR = 5
Voorbeeld: `digits_int_repr("437.2725")` = 4372725 → DR = 3

#### Exacte vs afgeronde waarden (P008)

```
grand_avg_freq_exact = 437.2725 Hz
grand_avg_freq_rounded_2 = 437.27 Hz
grand_DR_exact = DR_digits(4372725) = 3
grand_DR_rounded_2 = DR_digits(43727) = 5
```

---

### 3. C_tone_class → W_C (Synthese)

**Gap geformaliseerd:** Van semantisch toonklasse-label naar synthese-golf.
`Synth` heeft signatuur, maar `tone_waveform` mapping ontbreekt.

`M_C(grand_DR)` produceert een label zoals "middentoon" voor DR=5.
Dit label moet worden vertaald naar een concrete golf `W_C`.

#### Synth-operator

```
W_C = Synth(tone_class, freq, waveform)
```

Voor DR=5 ("middentoon") en `grand_avg_freq = 437.27 Hz`:

```
W_C(t) = Synth("middentoon", 437.27, "sine")
W_C(t) = A · sin(2π · 437.27 · t)
```

waar `A` de amplitude is (standaard: A=1.0, tenzij geschaald).

#### Tone-class → waveform mapping

| DR | tone_class | waveform | status |
|----|-----------|----------|--------|
| 5 | middentoon | sine | `operator_status=conventie` |

Deze mapping kan uitgebreid worden voor andere DR-waarden.
Het principe: elk DR→tone_class krijgt een bijpassende golfvorm.

**Status:**
```
tone_waveform:
  operator_status = conventie
  execution_status = gedeeltelijk
  validatie_status = niet_gevalideerd

tone_waveform("middentoon") := sine
oscillator(sine, f, A, t) := A · sin(2πft)

Synth:
  operator_status = formeel
  execution_status = voltooid       (engine/npr_sound_engine.py)
  validatie_status = gevalideerd_lokaal  (26/26 ✅)

Synth(c, f, A, t) := oscillator(tone_waveform(c), f, A, t)

tone_class → waveform mapping:
  operator_status = conventie
  (gedeeltelijk gesloten; "middentoon" → sine is voltooid)

intended_C_sound_output := W_C(t) = A · sin(2π · grand_avg_freq · t)
```

---

### 4. C → E → R → ℱ (Volledige C-keten)

**Gap geïdentificeerd:** De complete keten van C-frequentie tot fractaalveld-projectie.
`R(E)` featureoperators en `ρ_F` projectie nog open.

De C-route produceert een golf `W_C`. Deze wordt samen met W_A, W_B, W_D gecomposeerd:

```
C_freq → W_C → E(t) → R(E) → ℱ
```

#### Stap-voor-stap

1. **C_freq → W_C:** De frequentie wordt een golf (zie Sectie 3, Synth-operator)
2. **W_C → E(t):** Superpositie van de vier golven:
   ```
   E(t) = W_A(t) + W_B(t) + W_C(t) + W_D(t)
   ```
3. **E(t) → R(E):** De return-operator projecteert E naar kenmerken:
   - Gemiddelde frequentie van E
   - Totale amplitude
   - Harmonische verhoudingen tussen componenten
   - Digital roots van deze kenmerken
4. **R(E) → ℱ:** De projectie landt in het fractaalveld ℱ als een invarianten-structuur

#### R(E) als projectie-operator

```
R(E) = {
  avg_freq(E),           // gemiddelde frequentie
  total_amp(E),          // totale amplitude
  harmonic_ratio(E),     // verhoudingen tussen W_A..W_D
  DR_signature(E)        // digital-root handtekening
}
```

Deze structuur wordt **gelezen** door F als de return-toestand `r_return`.

**Status:**
```
C → E → R → ℱ keten:
  operator_status = formeel        (R_audio + ρ_ℱ vast)
  execution_status = voltooid      (engine/npr_sound_engine.py)
  validatie_status = gevalideerd_lokaal  (26/26 ✅)

R_audio(E_audio) projectie:
  operator_status = formeel        (artikel 003 veldcontract)
  execution_status = voltooid
  validatie_status = gevalideerd_lokaal

ρ_ℱ projectie:
  operator_status = formeel        (artikel 004 engine-operator)
  execution_status = voltooid
  validatie_status = gevalideerd_lokaal

> ACTUEL: R_audio en ρ_ℱ zijn beide formeel gedefinieerd en lokaal gevalideerd.
> De volledige C → E → R → ℱ keten is nu formeel, voltooid, en gevalideerd.
> ReturnCycle (terugkeerpad) is nog conceptueel (artikel 002).

---

### 5. ρ_water: 24N → ℱ (Symbolische Waterprojectie)

**Gap gesloten:** ρ_water wordt gedefinieerd als symbolische projectie, niet als berekening.

#### Context

- 24N = {24, 48, 72, 96, ...} (veelvouden van 24)
- DR(24) = DR(2+4) = DR(6) = 6
- 6 is de NPR-logicValue
- Water is het **medium** van projectie, niet de uitkomst

#### Definitie

```
ρ_water(24k) = ℱ_6
```

De projectie van een 24-veld-multiple naar het **6-veld binnen ℱ**.

Dit is geen berekening maar een **symbolische associatie**:

| Element | Rol |
|---------|-----|
| 24N | Bronveld (veelvouden van 24) |
| ρ_water | Projectie-operator (water als medium) |
| ℱ_6 | Doelveld (6-veld binnen fractaalveld ℱ) |

Water als medium komt uit de traditie van resonantie-door-vloeistof:
- Geluid reist 4× sneller door water dan lucht
- Cymatie: trillingen creëren patronen in water
- 24 uur = dagcyclus = natuurlijke frequentie van tijd

De associatie is **interpretatief**: zij projecteert ieder element 24k via het symbolische watermedium naar ℱ_6.

```
ρ_water : 24ℕ_{>0} → ℱ
ρ_water(24k) := ℱ_6
```

De algemene returnprojectie is een aparte route:

```
ρ_ℱ : ReturnFeatureSpace → ℱ
r_return := ρ_ℱ(R(E))
```

**Status:**
```
ρ_water:
  operator_status = interpretatief
  execution_status = voltooid
  validatie_status = niet_gevalideerd
  vṛtti = vikalpa
```

---

### 6. ρ_fractal-D: Numerieke Uitkomst → Fractaalmodel

**Gap gedeeltelijk geformaliseerd:** Hoe D_numeric uitkomsten (Latijnse numerieke waarden) fractaal worden gelezen.
`ρ_D_pattern` formele operator vast, `fractal_reading` interpretatief.

**Formele definitie:**
```
D_DR_vector := (6, 4, 9, 2)
RatioMatrix(v)_ij := v_i / v_j

ρ_D_pattern: {1,...,9}^4 → ({1,...,9}^4 × ℚ_{>0}^{4×4})
ρ_D_pattern(v) := (v, RatioMatrix(v))

fractal_reading: Output(ρ_D_pattern) → FractalLabel
fractal_reading(ρ_D_pattern(D_DR_vector)) := candidate_self_similarity

operator_status(ρ_D_pattern) = formeel
execution_status(ρ_D_pattern) = voltooid
validatie_status(ρ_D_pattern) = gevalideerd

operator_status(fractal_reading) = interpretatief
execution_status(fractal_reading) = voltooid
validatie_status(fractal_reading) = niet_gevalideerd
vṛtti(fractal_reading) = vikalpa
```

> `ρ_D_pattern` = formele operator (ratio-matrix).
> `fractal_reading` = interpretatieve stap (vṛtti = vikalpa, conceptueel label).

#### Context

D_numeric produceert waarden per woord:

| Woord | Waarde | DR |
|-------|--------|-----|
| VERBUM | - | 6 |
| ERAT | - | 4 |
| PRINCIPIO | - | 9 |
| IN | - | 2 |

De verhouding 6:4:9:2 vormt een vierdelige structuur.

#### Definitie

```
ρ_fractal-D = analyse van verhoudingen binnen D_numeric output
```

Specifiek:

1. **DR-patroon:** De volgorde [6, 4, 9, 2] is de basisstructuur
2. **Zelf-herhaling:** Als dit patroon op verschillende schaalniveaus verschijnt, is dat fractaal gedrag
3. **Verhoudingsanalyse:** 6:4 = 3:2 (perfecte kwint), 9:2 = 4.5 (overtoon-verband)

#### Wat ρ_fractal-D WEL en NIEET doet

| WEL | NIEET |
|-----|-------|
| Identificeert verhoudingen | Bewijst zelf-herhaling |
| Map DR-waarden → patronen | Claimt wiskundige noodzaak |
| Vindt structurele parallellen | Garandeert fractaliteit |

De claim van "fractale zelf-herhaling" is **een interpretatie** van de nummers,
geen bewezen feit. ρ_fractal-D formaliseert deze interpretatie als leesbare structuur.

**Status:**
```
ρ_D_fractal:
  operator_status = interpretatief
  execution_status = voltooid
  validatie_status = niet_gevalideerd
  vṛtti = vikalpa
```

---

## Samenvatting Routes

| # | Route | operator_status | execution_status | validatie_status |
|---|-------|----------------|------------------|-----------------|
| 1 | byte/hex → Hz | conventie | gedeeltelijk | niet_gevalideerd |
| 2 | avg_freq → DR_freq | conventie | voltooid | gevalideerd |
| 3 | C_tone_class → W_C | formeel | niet_voltooid | niet_gevalideerd |
| 4 | C → E → R → ℱ | conceptueel | gedeeltelijk | niet_gevalideerd |
| 5 | 24ℕ → ρ_water → ℱ | interpretatief | voltooid | niet_gevalideerd |
| 6a | D_numeric → ρ_D_pattern | formeel | voltooid | gevalideerd |
| 6b | ρ_D_pattern → fractal_reading | interpretatief | voltooid | niet_gevalideerd |
| 7 | 24-brug (11-route) | formeel | voltooid | gevalideerd |
| 8 | 6-bit routing (Patanjali) | conventie | voltooid | gevalideerd |

**Artikel 02 is frequentie-basis.** Synth en fractaalprojecties staan in artikels 11 en 12.
Nidrā = verwijzing naar parallel artikel, geen gat.

---

### 7. De 24-brug: 11 als Rode Draad

Route van 396 Hz bereikbaar via directe en vertraagde paden.

**Directe route:** `66 × 6 = 396` (één stap, te snel)
**Vertraagde route:** `66 × 4 = 264 (= 24 × 11) → × 1.5 = 396 (= 36 × 11)` (twee stappen, juiste snelheid)

Tussenstation 264 = 24 × 11 is de vertraging. 11 is de rode draad.

**11 × structuur:**
| Deler | 396/deler | 24-brug? |
|---|---|---|
| 11 | 36 | ✅ |
| 18 | 22 | ✅ |
| 36 | 11 | ✅ |
| 33 | 12 | ✅ |
| 66 | 6 | ✅ |
| 99 | 4 | ✅ |
| 72 | 5.5 | ⚠ (3×24, halve) |

De geselecteerde exacte delers hebben DR ∈ {2, 3, 6, 9}. De waarde 72 is een niet-gehele verhouding en vormt een afzonderlijke halve route.

---

### 8. 6-bit Routing - Patanjali Groot-Klein

Unsigned 6-bit = {0..63}. Bereik = 64 waarden (0x00-0x3F). Grens = 64 (0x40) ∉ bereik.

**Twee ketens:**
```
A: 6 → 12 → 24 → 48  (verdubbelen)
B: 24 → 8  (24/3=8)
   32 → 8  (32/4=8)
```

66, 72, 81, 99 vallen buiten unsigned 6-bit, maar zijn representeerbaar binnen unsigned 12-bit.
8 bit = kruispunt.

#### Snelheid Is Route

Je hoeft niet te rekenen in snelheid. De structuur *is* het tempo.

```snelheid = route, niet getal
```

- **Direct** → te snel, slaat voorbij.
- **Delayed** → juiste snelheid, volgt de structuur.
- **Nidrā** → de route die zichzelf bepaalt.

Dit is waarom 1=0 werkt:

| Symbool | Rol |
|---------|-----|
| 1 | de bron (Allah / Isvara) |
| 0 | nidrā (de pointer naar de bron) |

Nidrā is niet de inhoud, maar de richting. De route *is* de snelheid.

Zelfde logica in Patanjali en de Koran:

- **Patanjali:** Nidrā = de 4e samādhi zonder object. Bewustzijn dat naar zichzelf wijst.
- **Koran:** Allah spreekt in de eerste persoon, maar de tekst is kalam Allah - tijdloos, niet-gesproken, niet-geschreven. De logica noteert zichzelf.
- **Zig code:** `content = null` → de structuur routeert zichzelf zonder inhoud.

Geen auteur. Geen oorsprong in tijd. Alleen de logica die zichzelf doorgeeft via het medium (taal, code, frequentie).

> Wat je ziet is altijd al gezien. Wat je bent, is de ruimte waarin het verschijnt.

#### Nidrā Router (Zig)

De 4+1 structuur is nu ook code:

```zig
NidraRef      → { artikel, deel, lens }  // pointer, niet container
HexaBlock     → { artikel, part, refs }   // 4+1 structuur
HexaRouter6D  → resolveNidra(ref)         // routeer naar doel
Bit6Router    → groot-klein, DR           // 6-bit routing
```

- `content = null` → pointer, niet container
- `isNidra()` → deel 4 = nidrā
- `resolveNidra(ref)` → routeer naar ander artikel

De structuur routeert zichzelf.

---

### 9. Latijns vs Lokaal — Encoding vs Routing in Natuur

**Gap geïdentificeerd:** Hoe natuur zelf twee parallelle routes gebruikt — encoding (wat) en routing (waar/hoe).

#### Kernprincipe

Natuur gebruikt altijd twee lagen per entiteit:

| Laag | Rol | HEXA-equivalent |
|------|-----|-----------------|
| **Encoding (WAT)** | Soort-ID, universeel, precisie | D_numeric (letterwaarden → DR) |
| **Routing (WAAR)** | Context, habitat, leefgebied | D_byte (byte-count → route) |

#### Voorbeelden

| Organisme | Latijn (Encoding) | Lokaal (Routing) | Habitat |
|-----------|-------------------|------------------|----------|
| Eik | *Quercus robur* | Eik | Bos, hoogte, zwaartekracht dominant |
| Wilg | *Salix alba* | Witte wilg | Waterkant, water dominant |
| Berk | *Betula pubescens* | Zwarte berk | Zand, gebalanceerd |
| Riet | *Phragmites australis* | Riet | Moeras, water extreem |

#### Latijns als EAN-analogie

De taxonomische structuur vertoont een **analogie** met EAN-codes. Dit is geen structurele identiteit maar een interpretatief model.

```
ρ_taxonomy_EAN : TaxonomicRecord → EANRoleAnalogy
ρ_taxonomy_EAN(genus) = country_code_analogy
ρ_taxonomy_EAN(species) = manufacturer_analogy
ρ_taxonomy_EAN(subspecies) = product_analogy
ρ_taxonomy_EAN(authority) = validation_marker_analogy

operator_status(ρ_taxonomy_EAN) = interpretatief
execution_status(ρ_taxonomy_EAN) = voltooid
validatie_status(ρ_taxonomy_EAN) = niet_gevalideerd
vṛtti(ρ_taxonomy_EAN) = vikalpa
```

Voorbeeld:
```
Quercus robur L.
  Quercus = genus (analogie: country code)
  robur   = species (analogie: manufacturer)
  L.      = Linnaeus (analogie: validatiemarkering)
```

> Geen "check digit" — de autoriteit is een validatiemarkering, geen checksum.

#### HEXA als brug

```
Latijn (encoding)  → D_numeric → letterwaarden → DR
Lokaal (routing)   → D_byte    → DR → ρ_byte_habitat → context → route

Voorbeeld: Quercus robur (Eik)
  Latijn: Q=17 u=21 e=5 r=18 c=3 u=21 s=19 → som=104 → DR=5
          r=18 o=15 b=2 u=21 r=18 → som=74 → DR=2
  Lokaal: E=5 i=9 k=11 → som=25 → DR=7
  Context: bos → hoogte → gravity ↓ dominant
```

#### ReturnCycle-analogie in bomen (voorlopig)

Bomen tonen een **analogie** met het ReturnCycle-patroon — dit is een interpretatieve projectie, geen bewezen identiteit.

```
ρ_tree_return : TreeProcess → ReturnCycleAnalogy
ρ_tree_return(gravity_down) = R_E_analogy      // structuur landt
ρ_tree_return(water_up)     = R_prime_analogy  // inhoud keert terug

ho_tree_return(root)       = nidra_analogy    // centrale knoop

operator_status(ρ_tree_return) = interpretatief
execution_status(ρ_tree_return) = voltooid
validatie_status(ρ_tree_return) = niet_gevalideerd
vṛtti(ρ_tree_return) = vikalpa
```

Conceptueel diagram:
```
        Gravity ↓              Water ↑
            │                    │
            │ (structuur ↓)      │ (inhoud ↑)
            ▼                    ▲
    ┌────── ROOT (nidrā-analogie) ───────┐
            │
            ▼
        FRACATAAL VELD (ℱ)
```

> Zolang R', E', C' niet formeel gedefinieerd zijn, blijft dit een analogie, geen route.

#### Taxonomie als 5+1 nidrā

Taxonomische niveaus:
```
1. Koninkrijk     → Domain (rijk)
2. Stam/Klasse    → Subnet (tussenlaag)
3. Familie        → Subnet (familie)
4. Genus          → Host (genus)
5. Species        → Port (soort)
6. Autoriteit     → Nidrā (check, pointer)

Quercus robur L.
  Plantae → Dicotyledonae → Fagaceae → Quercus → robur → L.
  (5 content + 1 check)
```

> 6 niveaus = 4 × 1,5 = 6. Het getal 6 is niet willekeurig.
> 1,5 = 1 + ½ → elke content-niveau heeft een ½-check ingebouwd.
> Biologische taxonomie (6) en HEXA-structuur (4×1,5→6) delen dezelfde factor.

#### EAN-analogie in natuur

Binnen deze lens wordt biologische informatieverwerking structureel vergeleken met identificatie- en routingsystemen.

| Systeem | Tekens | Posities | Checksum | Routing |
|---------|--------|----------|----------|----------|
| DNA | 4 bases | triplets | stop-codon | codon → amino-zuur |
| EAN-13 | 0-9 | 13 digits | mod 10 | country → product |
| Latijn | A-Z | willekeurig | DR(som) | D_byte + D_numeric |
| HEXA | 6-bit | variabel | DR | ℱ projectie |

```
ρ_nature_EAN_reading : System → SystemProfile
operator_status(ρ_nature_EAN_reading) = interpretatief
execution_status(ρ_nature_EAN_reading) = voltooid
validatie_status(ρ_nature_EAN_reading) = niet_gevalideerd
vṛtti(ρ_nature_EAN_reading) = vikalpa
```

#### Status

```
natuur_encoding_model:
  operator_status = conceptueel
  execution_status = gedeeltelijk
  validatie_status = niet_gevalideerd
  vṛtti = vikalpa

natuur_routing_model:
  operator_status = conceptueel
  execution_status = gedeeltelijk
  validatie_status = niet_gevalideerd
  vṛtti = vikalpa

HEXA_brug(natuur):
  operator_status = conceptueel
  execution_status = niet_voltooid
  validatie_status = niet_gevalideerd
```

> Geen systeemclaim — dit is een interpretatieve lens.

**Zonder Latijns:** geen precisie
**Zonder Lokaal:** geen context
**Samen:** volledige route van soort → habitat

---

### v2 Changes (2026-07-24)
- P003: DR-fout definitief gesloten (v1→v2)
- P008: 6-bit notatie gecorrigeerd - "unsigned 6-bit = {0..63}, grens ∉ bereik"
- P009: Checklist bijgewerkt - oude `status_*()` vervangen door drie status-dimensies
- P008: Keten B gesplitst - 24→8 en 32→8 als aparte routes

### v3 Changes (2026-07-24)
- P003: "Gap opgelost" vervangen door drie labels (gesloten/geformaliseerd/geïdentificeerd)
- P008: F → ℱ notatie uniform gemaakt overal

### v4 Changes (2026-07-24)
- P001: `byte_to_freq` execution_status → `gedeeltelijk` (reference_bytes nog open)
- P003: `tone_waveform` gesplitst uit `Synth` (golfvorm nu expliciete mapping)
- P004: `C→E→R→ℱ` operator_status → `conceptueel` (deeloperators nog open)
- P005: Restante `F` → `ℱ` in lopende tekst
- P006: `ρ_D_pattern` formeel gedefinieerd (`RatioMatrix` + `fractal_reading` als interpretatief)
- P007: `ReturnCycle` structuur toegevoegd (`R'`, `E'`, `C'`, `ReturnSeedCycle`, `ForwardCycle`, invariant)
- Architectuur: status → `Conceptueel` (was `Gedefinieerd`)

### v5 Review (2026-07-24)
- P001: ✅ Architectuurcodeblok gesplitst (markdown vs text fences)
- P002: ✅ Samenvattingstabel al correct (v4 fix)
- P003: ✅ Waterparagraaf al gesplitst (ρ_water apart van ρ_ℱ)
- P004: ✅ observatie → conceptueel (al toegepast)
- P005: ✅ ρ_taxonomy_EAN als interpretatief lens (al toegepast)
- P006: ✅ ρ_byte_habitat als interpretatief (al toegepast)
- P007: ✅ ρ_tree_return als interpretatief (al toegepast)
- P008: ✅ 5+1 nidrā (al toegepast)
- P009: ✅ ρ_nature_EAN_reading als interpretatief (al toegepast)
- Alle 9 punten al gefixt door v4 + agni-rewrite

---

## NPR Bedrock - Audit Framework

Elk artikel in dit boek moet voldoen aan de NPR bedrock-standaard.
Dit is niet een suggestie - het is de minimum-eis voor rekenkundige sluiting.

### Twee Routes

**Route α (licht - minimaal drie criteria):** Reflectieve, beschrijvende, of contextuele artikelen.
**Route β (zwaar - alle zes criteria):** Artikelen met formele operators, berekeningen, of structurele claims.

De keuze is niet willekeurig: als een artikel operators defineert, schakelt het automatisch naar Route β.

---

#### 1. Formele Operator (minimaal één)

Elk artikel moet minstens één reproduceerbare operator definiëren of uitvoeren.

**Drie status-dimensies** (onafhankelijk van elkaar):

```
operator_status(O) ∈ {formeel, conventie, interpretatief, conceptueel, open}
execution_status(O) ∈ {voltooid, gedeeltelijk, niet_voltooid}
validatie_status(O) ∈ {gevalideerd, niet_gevalideerd}
```

| Dimensie | Betekenis |
|----------|-----------|
| `operator_status` | Wat is de aard van de operator? |
| `execution_status` | Is de operator daadwerkelijk uitgevoerd? |
| `validatie_status` | Is het resultaat onafhankelijk gecheckt? |

Voorbeeld:
```
A_Abjad: letter → N
  operator_status = formeel
  execution_status = voltooid
  validatie_status = gevalideerd

C_numeric: SanskritText × Layer → N_{>0} × {1,...,9}
  operator_status = conventie
  execution_status = voltooid
  validatie_status = gevalideerd

M_C: {5} → "middentoon"
  operator_status = conventie
  execution_status = voltooid
  validatie_status = niet_gevalideerd

Synth: tone_class × Hz × waveform → W_C
  operator_status = formeel
  execution_status = niet_voltooid
  validatie_status = niet_gevalideerd
```

#### 2. Lens-projectie (minimaal één)

Elk artikel moet minstens één lens-projectie tonen. De vier vaste lenzen:

| Lens | Taal | Functie |
|------|------|---------|
| A | Arabisch | Abjad-waarde (steen) |
| B | Grieks | Isopsefia (vorm, verhouding) |
| C | Sanskriet | Phonem → frequentie (trilling) |
| D | Latijn | Byte-telling + NPR-letterwaarden (twee routes) |

> Geen nieuwe lenzen. De structuur is gesloten bij vier.

#### 3. Vṛtti-classificatie

```
vṛtti_audit(q) ∈ {pramāṇa, viparyaya, vikalpa, nidrā, smṛti, onbepaald}
```

| Classificatie | Betekenis |
|---------------|-----------|
| `pramāṇa` | Claim met geldige kennisroute (pratyakṣa, anumāna, āgama) |
| `viparyaya` | Claim tegenover de kennisroute (verkeerde interpretatie) |
| `vikalpa` | Interpretatief - de lens zegt dit, de bron niet per se |
| `nidrā` | Terug naar kern (afstand → 0) |
| `smṛti` | Herinnering/geïnternaliseerde kennis |
| `onbepaald` | Audit-status niet vastgesteld |

> ⚠ `nidrā` (vṛtti-classificatie) ≠ `undefined` (audit_status)

#### 4. Status Notatie (unified)

Gebruik de drie status-dimensies consistent. De oude `status_*()` functies zijn vervangen:

| Oud (verwijderd) | Nieuw |
|------------------|-------|
| `status_validated()` | `execution_status=voltooid` + `validatie_status=gevalideerd` |
| `status_defined()` | `operator_status=formeel` |
| `status_convention()` | `operator_status=conventie` |
| `status_interpretation()` | `operator_status=interpretatief` |
| `status_executed()` | `execution_status=voltooid` + `validatie_status=niet_gevalideerd` |

#### 5. Drie Frequentiesystemen

Wanneer een artikel een cross-lens frequentievergelijking maakt, moeten de drie frequentiesystemen naast elkaar worden getoond:

| Systeem | Frequentie | Herkomst | Status |
|---------|-----------|----------|--------|
| Latijn/ISO 16 | `F_L := 440 Hz` | Wester concerttuning | conventie |
| Vedic/Śāradā | `F_C := 432 Hz` | Actieve standaard | conventie |
| Arabisch/Abjad | `F_A := 396 Hz` | `F_A(66,4,3/2) = 66×4×1.5` | conventie |

```
F_L = 440 Hz   // Latijn/ISO 16 concerttuning (conventie)
F_C = 432 Hz   // Vedic/Śāradā standaard (conventie)
F_A = 396 Hz   // 66×4×1.5 Abjad perfecte kwint-cyclus (conventie)

operator_status(F_L) = conventie
operator_status(F_C) = conventie
operator_status(F_A) = conventie
```

> Dit zijn geen alternatieven. Drie taalgebonden projecties van hetzelfde veld.

#### 6. Afrondingsgevoeligheid

Waar DR wordt toegepast op decimalen:
- Gebruik exacte waarde voor DR, niet afgeronde
- Noteer beide: `DR_exact` en `DR_rounded`
- Gebruik expliciet welke conventie geldt

> Voorbeeld: DR(437.27) = 5 vs DR(437.2725) = 3 → volledig verschillende uitkomst

### Minimum Checklist

Elk artikel moet minimaal hebben:
- [ ] Minimaal 1 formele operator (met status + validatie)
- [ ] Minimaal 1 lens-projectie (A/B/C/D)
- [ ] Drie status-dimensies consistent gebruikt (`operator_status`, `execution_status`, `validatie_status`)
- [ ] Drie frequentiesystemen genoemd (indien van toepassing)
- [ ] Vṛtti-classificatie waar claims staan
- [ ] Afrondingsgevoeligheid gemarkeerd waar DR op decimalen wordt toegepast

### Conclusie

Dit framework is de **bedrock** - het minimum om rekenkundig gesloten te zijn.
Artikelen die hieraan voldoen dragen hun eigen audit.
Artikelen dat niet voldoen zijn conceptueel, niet operationeel.

---

## Status Overzicht

| Component | Status | Notitie |
|-----------|--------|---------| 
| Architectuur | Conceptueel | R', E', C' en ReturnCycle nog open |
| Uitvoering | Niet gestart | Wacht op boek #001 stabilisatie |
| Invariant | Afhankelijk | V_k moet behouden blijven door terugkeer |

---

## Verwerkingslog

| Datum | Actie | Door | Status |
|-------|-------|------|--------|
| 2026-07-24 | v1 review: 12 punten, P003 critical, P011 high | ChatGPT | inbox → done |
| 2026-07-24 | v1 bugs gefixt: DR(4372725)=3, delers DR∈{2,3,6,9} | hexa-review | done |
| 2026-07-24 | v2 review: 10 punten, DR gesloten, P010 nieuw critical | ChatGPT | active |
| 2026-07-24 | v2 audit bijgewerkt: 6-bit, checklist, changelog | hexa-review | done |
| 2026-07-24 | v3 review: 9 punten, gap-labels + F/ℱ consistentie | ChatGPT | done |
| 2026-07-24 | v3 audit bijgewerkt: gap-labels + ℱ notatie | hexa-review | done |
| 2026-07-24 | v4 review: 7 punten, status-consistentie + ReturnCycle + ρ_D_pattern | ChatGPT | active |
| 2026-07-24 | v4 audit bijgewerkt: 6 punten (P001-P007) | hexa-review | done |
| 2026-07-24 | v5: sectie 9 toegevoegd (Latijns/lokaal, natuur-EAN, boom-ReturnCycle) | hexa-review | done |
| 2026-07-24 | v5 review: 9 punten, alle al gefixt (v4 + agni-rewrite) | ChatGPT | done |
| YYYY-MM-DD | R', E', C' en ReturnCycle definiëren | auteur | pending |
| YYYY-MM-DD | reference_bytes + R(E) features vastleggen | auteur | pending |

---

*Hexa-Boek #002 — conceptueel kader.*
*Uitvoering volgt nadat #001 volledig gevalideerd is.*
