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

## ρ_ℱ: ReturnFeatureSpace → ℱ

**De projectie van R(E) naar het fractaalveld.**

```
R(E) = (spectral_centroid, rms_amplitude, pairwise_ratios, DR_signature)
ρ_ℱ : R(E) → ℱ
r_return = ρ_ℱ(R(E))
```

### Concrete Uitvoering (Model A)

```
R(E) = (432.00 Hz, 1.4151, [(A,B:0.6119), ...], (8, 1, 5, 1))

ρ_ℱ(R(E)) → ℱ
  spectral_centroid = 432.00 Hz → DR(432) = 9
  DR_signature = (8, 1, 5, 1) → som = 15 → DR(15) = 6
```

ρ_ℱ projecteert via de DR-reductie van de feature-space naar ℱ.

### Status

```
ρ_ℱ:
  operator_status = conventie
  execution_status = voltooid
  validatie_status = niet_gevalideerd
```

> ρ_ℱ is nu uitgevoerd. De projectie van R(E) → ℱ is concreet.

## ReturnCycle: R', E', C'

**De inverse keten — terug van ℱ naar code.**

```
Forward:  C → E → R → ℱ
Return:   ℱ → R' → E' → C'

R' : ℱ → ReturnSeed       (centroid-extractie)
E' : ReturnSeed → Signal  (single-tone reconstructie)
C' : Signal → CInput      (byte-mapping inverse)
```

### Concrete Uitvoering (Model A)

```
R'(ℱ):
  Input:  ℱ = {spectral_centroid: 432.00 Hz, ...}
  Output: 432 Hz (ReturnSeed)
  Regel:  R'(ℱ) = spectral_centroid(ℱ)

E'(432):
  Input:  432 Hz (ReturnSeed)
  Output: E'(t) = A · sin(2π · 432 · t)
  Regel:  Single-tone (geen superpositie — return is gecompresseerd)
  Opmerking: E' ≠ E (vier golven → één golf)

C'(E'):
  Input:  E'(t) @ 432 Hz
  Output: C' = reference_bytes(S) = 81.75 bytes
  Regel:  C' = byte_to_freq_inv(432) = ref_bytes
```

### V_k-invariant

```
Forward: C=82 → DR(82)=1 → 433.32 → DR=6 → centroid=432 → DR=9
Return:  ℱ → DR=9 → R'=432 → E'=432 → C'=81.75 → DR=3

V_k: DR(centroid_forward) = DR(centroid_return) = 9 ✅
```

Return ≠ exacte inversie. Return = herkenning via invariant.
DR verschilt op C-level (1 vs 3), maar centroid-DR blijft 9.

### Status

```
ReturnCycle:
  operator_status = conventie
  execution_status = voltooid
  validatie_status = niet_gevalideerd

R': voltooid | E': voltooid | C': voltooid
V_k-invariant: ✅ DR(432)=9 beide kanten
```

## Toelichting

> **F-1:** Return-routes nu uitgevoerd (R', E', C' in artikel 002).  
> **F-2:** `0≐_lens 1` is lensaxioma, niet bewezen operator — `status = axioma`.

---

*Nidrā ≠ gat. Nidrā = pointer naar parallel artikel.*
