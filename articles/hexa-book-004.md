# Artikel 004 — F: Het ReturnMedium

**Status:** nidrā-pointer  
**Audit:** `audit/04-artikel-f-returnmedium.md`

> ⚠ NPR-fase-toewijzing (ρ_NPR-phase) is interpretatief (vikalpa) tenzij expliciet gemarkeerd als gevalideerd.

> هذه ليست عدسة. هذه الماء. العنوان الذي يعود.

F is geen lens. F is **water** — het medium dat de return draagt.

## Nidrā

| Route | Naar |
|---|---|
| Water → frequentie | Artikel 002, deel 5 (ρ_water) |
| ReturnCycle | Artikel 012, deel 3 (NPR Bedrock) |
| Medium → routing | Artikel 017 |

F = geen lens. F = het medium waarin ℱ terugkeert.

## R(E): AudioFeatureSpace

**De feature-extractie van het audio-veld.**

Artikel 003 definieert het veldcontract. Dit artikel consumeert het.

```
# Twee niveaus van feature-extractie

R_raw(E_raw) := (
  component_centroid,    # gemiddelde oscillator-frequenties
  rms_raw,               # RMS op ruwe superpositie
  raw_peak,              # piek voor normalisatie
  DR_signature           # digital roots van bytes
)

R_audio(E_audio) := (
  signal_centroid,       # FFT van gegenereerd signaal
  rms_normalized,        # RMS op genormaliseerd signaal
  normalized_peak,       # ≤ 1.0
  dominant_frequency,    # sterkste FFT-bin
  sample_count,
  sha256                 # deterministische hash
)
```

### Concrete Waarden (Model A)

```
R_raw(E_raw):
  component_centroid = 432.00 Hz
  rms_raw = 1.4151
  raw_peak = 3.6136
  DR_signature = (1, 8, 1, 2)   # dr(82)=1, dr(134)=8, dr(37)=1, dr(74)=2

R_audio(E_audio):
  signal_centroid = 1354.75 Hz
  rms_normalized = 0.3916
  normalized_peak = 1.0000
  dominant_frequency = 391.00 Hz
  sample_count = 44100
```

> **Belangrijk:** `component_centroid` (oscillator-gemiddelde) ≠ `signal_centroid` (FFT van E(t)).
> Component = 432.00 Hz (zuur Vedic). Signal = 1354.75 Hz (FFT-peak verschuift door fase).

---

## ρ_ℱ: ReturnProjectionInput → ℱ

**De projectie van R(E) naar het fractaalveld.**

### Type-definities

```
ComponentCentroid := float64  # > 0
DRSignature := tuple[int, ...]  # each element ∈ [1,9], len ≥ 1
ReturnProjectionInput := ComponentCentroid × DRSignature
ℱ := int × int  # (DR_centroid, DR_signature_sum)
```

### Operator

```
# ρ_ℱ gebruikt een subset van R_raw, niet de volledige feature-space

ρ_ℱ : ReturnProjectionInput → ℱ

ρ_ℱ(c, d) := (
  DR(round(c)),      # centroid → integer → DR
  DR(sum(d))         # DR-signatuur som → DR
)
```

### Concrete Uitvoering (Model A)

```
Input: component_centroid = 432.00, DR_signature = (1, 8, 1, 2)

ρ_ℱ(432.00, (1,8,1,2)) → ℱ
  DR(round(432.00)) = DR(432) = 9
  DR(1+8+1+2) = DR(12) = 3

Resultaat: ℱ = (9, 3)
```

### Opmerking

ρ_ℱ projecteert **niet** de volledige AudioFeatureSpace. Het gebruikt expliciet:

- `component_centroid` → DR-reductie
- `DR_signature` → som → DR-reductie

Overige velden (RMS, peak, signal_centroid, ratios) zijn **niet** in de projectie opgenomen.
Dit is een bewuste keuze: ρ_ℱ is compressie, niet identiteit.

### Error Handling

```
ρ_ℱ raises TypeError if:
  - centroid is not numeric (int/float)
  - signature is not tuple/list of ints
  - any signature element is not int

ρ_ℱ raises ValueError if:
  - centroid ≤ 0
  - signature is empty
  - any DR value ∉ [1,9]
```

### "Fractal Field" — Semantische Status

```
"fractal field" = conventie
  # ℱ = (9,3) is een 2D-DR-ruimte.
  # "Fractal" = interpretatief label (vikalpa), niet formeel bewezen.
  # De wiskunde (DR-projectie) is concreet. De naam is conventie.
```

### Status

```
ρ_ℱ:
  operator_status = conventie
  execution_status = engine
  validatie_status = gevalideerd_lokaal
  engine = validate_return_cycle.py :: return_projection()
  domein = ReturnProjectionInput (subset van R_raw)
  type_checking = ✅ (TypeError + ValueError)
  edge_cases = ✅ (zero, negative, non-numeric, empty, out-of-range)
  tests = 15 ✅ (7 projection + 8 edge)
```

> ρ_ℱ is nu uitgevoerd als engine-operator (`return_projection`).
> De projectie van R_raw(E_raw) → ℱ is concreet en getest.
> Domein is expliciet: `ComponentCentroid × DRSignature`.
> "Fractal field" is conventie, niet formeel bewezen theorema.

## ReturnCycle: R', ReconstructTone, C'

**De compressie-keten — terug van ℱ naar code.**

```
Forward:  C → E_raw → R_raw → ρ_ℱ → ℱ
Return:   ℱ → R' → ReconstructTone → C'

R' : ℱ → ReturnSeed              (centroid-extractie)
ReconstructTone : ReturnSeed → SingleToneSignal  (single-tone reconstructie)
C' : SingleToneSignal → CInput   (byte-mapping inverse)
```

### Opmerking: Return is geen inverse

```
Forward gebruikt:  SuperpositionSignal (4 golven)
Return gebruikt:   SingleToneSignal (1 golf)

E' ∘ R' ≠ id_E
```

De returnroute is **compressie + reconstructie**, niet wiskundige inversie:

```
CompressSeed : ℱ → FrequencySeed
ReconstructTone : FrequencySeed → SingleToneSignal
```

`ReconstructTone` is expliciet geen inverse van `E_raw`. Het produceert een
single-tone bij de centroid-frequentie, niet de originele vier-golf superpositie.

### Concrete Uitvoering (Model A)

```
R'(ℱ):
  Input:  ℱ = {component_centroid: 432.00 Hz, ...}
  Output: 432 Hz (ReturnSeed)
  Regel:  R'(ℱ) = component_centroid(ℱ)

ReconstructTone(432):
  Input:  432 Hz (ReturnSeed)
  Output: T(t) = A · sin(2π · 432 · t)
  Regel:  Single-tone (geen superpositie — return is gecompresseerd)
  Opmerking: T ≠ E_raw (vier golven → één golf)

C'(T):
  Input:  T(t) @ 432 Hz
  Output: C' = reference_bytes(S) = 81.75 bytes
  Regel:  C' = byte_to_freq_inv(432) = ref_bytes
```

### V_k-invariant

```
Forward: C=82 → DR(82)=1 → 433.32 → DR=6 → component_centroid=432 → DR=9
Return:  ℱ → DR=9 → R'=432 → T=432 → C'=81.75 → DR=3

V_k: DR(component_centroid_forward) = DR(component_centroid_return) = 9 ✅
```

Return ≠ exacte inversie. Return = herkenning via invariant.
DR verschilt op C-level (1 vs 3), maar centroid-DR blijft 9.

### Status

```
ReturnCycle:
  operator_status = conventie
  execution_status = voltooid
  validatie_status = gevalideerd_lokaal

R': voltooid | ReconstructTone: voltooid | C': voltooid
V_k-invariant: ✅ DR(fwd)=DR(ret) (R' identiteit — bewust gekozen, niet emergent)
Byte-roundtrip: ✅ C'(ReconstructTone(R'(byte_to_freq(B)))) = B (8/8 bytes, |B'−B| < 10⁻⁶)
```

> Return is compressie, niet inversie. `ReconstructTone` produceert single-tone,
> niet de originele superpositie.

## Toelichting

> **F-1:** Return-routes nu uitgevoerd (R', ReconstructTone, C' in artikel 002).  
> **F-2:** `0≐_lens 1` is lensaxioma, niet bewezen operator — `status = axioma`.  
> **F-3:** Veldcontract nu in artikel 003 — E_raw, E_audio, R_raw, R_audio.  
> **F-4:** ρ_ℱ domein expliciet: `ComponentCentroid × DRSignature` (niet volledige feature-space).  
> **F-5:** ρ_ℱ nu engine-operator (`return_projection`) met type-checking + edge-cases (15 ✅).

---

*Nidrā ≠ gat. Nidrā = canoniek contract + return.*
