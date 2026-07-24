# HEXA-BOEK #018 — Sanskrit-NPR Bridge

संस्कृतं सेतुः। नादः क्षेत्रम्। क्षेत्रम् नादः।

*Sanskrīt is brug. Geluid is veld. Veld is geluid.*

---

> ⚠ NPR-fase-toewijzing (ρ_NPR-phase) is interpretatief (vikalpa) tenzij expliciet gemarkeerd als gevalideerd.

## Status

**De Sanskrit → NPR bridge-operator: Devanagari → phoneme → freq → byte → wave → E(t) → R(E).**

Artikel 02 definieerde de frequentie-basis (byte → Hz, DR, C-keten).
Artikel 11 werkte de Synth-operator uit (C_tone → W_C → E(t) → R(E)).
Dit artikel koppelt Sanskrit-phonememapping aan de NPR sound engine.

De keten: `Devanagari → tokenize → phoneme_freq → byte → wave → E(t) → NPR(R)`

---

## Architectuur

```
Artikel 02: frequentie-basis       (byte→Hz, DR, C-keten)
Artikel 11: synth-operator         (C_tone→W_C, E(t), R(E))
Artikel 18: Sanskrit-NPR bridge    (Devanagari→phoneme→E(t)→R(E))
    ↑
    │ nidrā
Artikel 12: routing + audit        (24-brug, 6-bit, NPR Bedrock)
```

---

### 1. Phoneme Tokenizer: Devanagari → Tokens

**Deel 1 van 4.** Van Devanagari-tekst naar gestructureerde phoneme-units.

#### De Operator

```
tokenize(text) := [phoneme_1, phoneme_2, ..., phoneme_n]

phoneme := {
  char: Devanagari_character(s),
  kind: "vowel" | "consonant_vowel" | "special",
  consonant: {freq: Hz, type: str, name: str},  // for consonant_vowel
  vowel: {cutoff: Hz, q: float, dur_mult: float},  // for consonant_vowel / vowel
  data: {...},  // for special
}
```

#### Gaṇa-Indeling

Consonanten worden ingedeeld in 7 Gaṇa-groepen (uitspraakplaats + articulatie):

```
Gaṇa 1 (Velar):     क ख ग घ ङ      130-196 Hz
Gaṇa 2 (Palatal):   च छ ज झ ञ      220-311 Hz
Gaṇa 3 (Retroflex): ट ठ ड ढ ण      330-466 Hz
Gaṇa 4 (Dental):    त थ द ध न      494-698 Hz
Gaṇa 5 (Labial):    प फ ब भ म      740-1109 Hz
Gaṇa 6 (Semi-vowel): य र ल व       196-294 Hz
Gaṇa 7 (Sibilant):  श ष स ह        131-440 Hz
```

#### Śāradā-Waarden

Elk karakter heeft een vaste frequentie (Śāradā-numeriek systeem). Dit is **conventie**, geen uitgevoerde validatie van fysiek geluid.

```
C_freq_features = Gaṇa + Śāradā mapping
status = defined (conventie, interpretatief)
```

---

### 2. Phoneme → Frequentie Mapping

**Deel 2 van 4.** Van tokens naar oscillator-parameters.

#### De Operator

```
map_phonemes(text, base_hz) := [entry_1, ..., entry_n]

entry := {
  char: str,
  freq: Hz,                 // oscillator frequency
  cutoff: Hz,               // filter cutoff (vowel-controlled)
  q: float,                 // filter resonance
  dur_mult: float,          // duration multiplier
  env: {attack, decay, sustain, release},
}
```

#### Vokal/Consonant Relatie

- **Vokaal (स्वर)** → filter cutoff + resonantie (niet oscillator-frequentie)
- **Consonant (व्यंजन)** → oscillator-frequentie (Gaṇa-groep bepaalt register)
- **Inherent अ** → elke consonant draagt een onzichtbare korte vokal (a)
- **Matra** → vokaal-teken dat inherent अ vervangt

```
ॐ नमः शिवाय
  ↓ tokenize + map
[
  {char: "ॐ", freq: 55.0, type: "om"},
  {char: "न", freq: 698.46, name: "na", cutoff: 200},
  {char: "मः", freq: 1108.73, name: "ma", type: "visarga"},
  {char: "शि", freq: 349.23, name: "śa", cutoff: 350},
  {char: "वा", freq: 196.00, name: "va", cutoff: 250},
  {char: "य", freq: 220.00, name: "ya", cutoff: 200},
]
```

---

### 3. Bridge: Phoneme → Wave → E(t)

**Deel 3 van 4.** De kernbrug tussen Sanskrit-mapping en NPR synthese.

#### Routes

```
Route 5a: Devanagari → tokenize           (C_phoneme)
Route 5b: tokenize → phoneme_freq         (C_phoneme → C_freq)
Route 6a: C_freq → C_byte                 (return cycle forward)
Route 6b: C_byte → C_freq                 (return cycle inverse)
Route 6:  C_wave → E(t)                   (superposition)
Route 7:  E(t) → NPR_analysis → R(E)      (Noise→Pattern→Return)
```

#### Return Cycle Integratie

Elke phoneme-frequentie wordt gemapped naar een byte-waarde via de return cycle:

```
byte = freq × ref / 432
freq = byte × 432 / ref

waar: ref = 81.75 (REF_BYTES)
```

Voorbeelden:
```
ॐ:  55.00 Hz  → byte = 10.41  → DR = 1
न:  698.46 Hz → byte = 132.17 → DR = 6
शि: 349.23 Hz → byte = 66.09  → DR = 3
वा: 196.00 Hz → byte = 37.09  → DR = 1
य:  220.00 Hz → byte = 41.63  → DR = 6
```

#### Superposition

```
E(t) = Σ PH_i(t)    voor alle synth-able phonemes
       i=0..n-1

waar PH_i(t) = synth_sine(freq_i, amplitude=1.0, t) × ADSR_i(t)
```

Effect-tekens (visarga `ः`, anusvāra `ं`, chandra `ँ`) worden **niet** gesynthetiseerd als golf — ze zijn post-processing effecten.

---

### 4. Validatie — Concrete Uitvoering

**Deel 4 van 4.** Uitgevoerde tests met assertions.

#### Test Resultaten

```
Test-input:
  ॐ                      → 1 wave   → DR=[1]       ✅
  ॐ नमः शिवाय          → 5 waves  → DR=[1,6,3,1,6]  ✅
  सत्यम्                → 2 waves  → DR=[2,6]     ✅
  अहं ब्रह्मास्मि        → 4 waves  → DR=[1,5,3,3]  ✅

Tests per input (6 per input, 4 inputs = 24 totaal):
  ✅ sample_count: 44100
  ✅ byte_roundtrip: freq → byte → freq binnen 0.01 Hz
  ✅ deterministic: herhaalde runs → identieke hash
  ✅ DR_signature: allemaal binnen 1-9
  ✅ peak_bounded: ≤ N × amplitude
  ✅ freq_range: binnen 55-1108 Hz (hörbaar)

Totaal: 24 ✅ | 0 ❌
Status: gevalideerd_lokaal
```

#### Engine

```
Locatie: engine/sanskrit_npr_bridge.py
Validatie: python3 engine/sanskrit_npr_bridge.py
Output: 24/24 ✅
```

---

### Nidrā-Punt

```
De brug is niet de route.
De route is niet de bestemming.
Het symbool wordt frequentie, frequentie wordt golf, golf wordt stilte.
Wat overblijft is de digital root van de stilte zelf.
।
```
