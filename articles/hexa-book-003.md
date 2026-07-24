# Artikel 003 — E: Het Audio-Veld (Canoniek Contract)

**Status:** veld-contract  
**Audit:** `audit/03-artikel-e-audio.md`

> ⚠ NPR-fase-toewijzing (ρ_NPR-phase) is interpretatief (vikalpa) tenzij expliciet gemarkeerd als gevalideerd.

> لا تعدّ الخطوة الخامسة عدسة خامسة. إنها الحقل الصوتي حيث تتلاقى العدسات الأربع.

De vijfde stap is geen vijfde lens. Het is het **audio-veld** waar de vier lenzen samenkomen.

---

## Canoniek Veldcontract

Dit artikel definieert het gedeelde typecontract tussen producers en consumers.

### Type-definities

```text
Wave := float64[n]                    # Enkele sinusgolf
SignalRaw := float64[n]               # Ruwe superpositie (geen amplitude-beperking)
SignalAudio := float64[n], peak ≤ 1  # Genormaliseerde audio
```

### Core Operators

```text
E_raw : List[Wave] → SignalRaw
  # Superpositie: E_raw(t) = Σ W_i(t)
  # Geen amplitude-beperking — puur lineair

Normalize : SignalRaw → SignalAudio
  # E_audio(t) = E_raw(t) / max(1, peak(E_raw))
  # Voorkomt clipping bij WAV-opslag

E_audio := Normalize(E_raw)
  # De productie-/opslagrepresentatie
```

### Feature Extractors

```text
R_raw : SignalRaw → RawFeatureSpace
  # centroid, rms, peak, sha256 op ruwe signalen

R_audio : SignalAudio → AudioFeatureSpace
  # signal_centroid (FFT), normalized_peak, dominant_freq
```

### Semantische Conventie

```text
ℰ := E_raw          # Mathematisch veldobject (theorie, analyse)
E_audio := Normalize(ℰ)  # Productie-/opslagrepresentatie (praktijk)
```

**Reden:** `ℰ` is het pure superpositie-veld. `E_audio` is de clip-veilige versie.

---

## Routing

```text
Producers:
  Artikel 011 / Model A Synth        → produceert E_raw, E_audio
  Artikel 018 / Sanskrit Bridge       → produceert E_raw, E_audio

Canoniek Veld:
  Artikel 003 / E-contract            ← dit artikel

Consumers:
  Artikel 004 / ρ_ℱ + ReturnCycle     → consumeert R_raw(E_raw)
```

### Implementatie Status

| Operator | Artikel | Engine | Status |
|---|---|---|---|
| `C_sound` | 011 | `npr_sound_engine.py` | ✅ `gevalideerd_lokaal` |
| `E_raw` | 011 | `superposition()` | ✅ gesloten |
| `E_audio` | 011 | `superposition()` | ✅ gesloten |
| `R_raw` | 004 | `npr_sound_engine.py` | ✅ gesloten |
| `R_audio` | 004 | `npr_sound_engine.py` | ✅ gesloten |
| `ρ_ℱ` | 004 | `validate_return_cycle.py` | ✅ `gevalideerd_lokaal` |

---

## Nidrā

| Route | Naar |
|---|---|
| Audio → frequentie | Artikel 002, deel 1-3 |
| Vier lenzen (A,B,C,D) | Artikel 001, lens-projectie |
| Superpositie → CC | Artikel 017 |
| Synth-executie | Artikel 011 |
| Return + ρ_ℱ | Artikel 004 |

E = geen lens. E = het veld waarin A, B, C, D tegelijk klinken.

---

*Nidrā ≠ gat. Nidrā = canoniek contract.*
