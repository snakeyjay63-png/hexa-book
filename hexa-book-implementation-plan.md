# Hexa-Boek #001 — Implementatieplan

**Doel:** Het boek operationeel self-validating maken.
`status_validated(r_begin, r_return)` van `ongetest` → `gevalideerd` of `verworpen`.

---

## Frequentiestandaarden per Route

Elke rekenlens heeft zijn eigen frequentiestandaard:

| Route | Standaard | DR | Freq | Cyclus |
|---|---|---|---|---|
| Arabisch | Abjad | 3 | 396 Hz (66×6) | 3→6→9 |
| Latijns | ISO 16 | 8 | 440 Hz | 8 |
| Vedic | Śāradā | 9 | 432 Hz | 9 |

**Actieve standaard:** A4=432 Hz (Vedic) als universele schaal voor DR_FREQ_MAP.
440 Hz blijft als Latijnse conventie behouden — niet weggewerkt, maar gedocumenteerd.

**Arabisch 3-6-9 cyclus:**
- Bron: Allah = 66 (Abjad) → DR(66) = 3
- 66 × 4 = 264 Hz → DR(264) = 3 (DR behoud!)
- 264 × 1.5 = 396 Hz → DR(396) = 9 (perfecte kwint, cyclus voltooid)
- Factor 6 is de brug: 66 × 6 = 396

**Reden 432 Hz als universele schaal:**
432 Hz is de natuurlijke kosmische frequentie uit de Vedic/Sanskriet-traditie.
De schalingsfactor t.o.v. ISO 16 is 432/440 ≈ 0.9818.

---

## Huidige Status

| Onderdeel | Status |
|---|---|
| Lens A (Abjad → DR) | ✅ Uitgevoerd (الله, بسم الله الرحمن الرحيم) |
| Lens B (Isopsefia → DR) | ✅ Uitgevoerd (Πῦρ) |
| Lens C (C_role) | ✅ Semantisch |
| Lens C (C_numeric,1.25) | ✅ Lokaal uitgevoerd (DR=2) |
| Lens C (C_sound_output) | ❌ Undefined |
| Lens D (D_byte, D_numeric) | ✅ Uitgevoerd |
| Mappings M_A, M_B, M_C, M_D | ❌ Gedeclareerd, niet gedefinieerd |
| Golven W_A, W_B, W_C, W_D | ❌ Undefined |
| E(t) superpositie | ❌ Undefined |
| R(E) return-operator | ❌ Undefined |
| V_k invariant | ❌ Niet vastgelegd |
| status_validated | ❌ ongetest |

---

## Stap 1 — C_sound Uitvoeren

**Probleem:** Sanskriet klankroute blockt de hele E-route.
Zonder `C_sound_output` → `W_C = undefined` → `E(t) = undefined`.

**Te doen:**
1. Bepaal de exacte Sanskriet-brontekst met accentmarkeringen (Patañjali 1.24-1.25)
2. Werklaag (unaccented) + Bronlaag (accented) vaststellen
3. UTF-8-bytelengte meten → hexrepresentatie → DR
4. Routekwaliteit bepalen (akliṣṭa/kliṣṭa)
5. `C_sound_output` produceren
6. Resultaat opnemen in hexa-book-001.md

**Output:** `C_sound_output` is een numerieke waarde die via `M_C` naar `W_C` gaat.

---

## Stap 2 — Mappings Definieren (M_A, M_B, M_C, M_D)

**Probleem:** Hoe wordt een lenswaarde een golfparameter?
Nu zijn de mappings alleen gedeclareerd zonder omzettingsregels.

**Te doen:**
1. Definieer voor elke lens een expliciete mapping:
   - `M_A: P_A → (f_A, a_A, φ_A)` — Abjad-waarde → frequentie/amplitude/fase
   - `M_B: P_B → (f_B, a_B, φ_B)` — Isopsefia-waarde → frequentie/amplitude/fase
   - `M_C: P_C → (f_C, a_C, φ_C)` — C_sound_output → frequentie/amplitude/fase
   - `M_D: P_D → (f_D, a_D, φ_D)` — D_byte/D_numeric → frequentie/amplitude/fase

2. Elke mapping moet een reproduceerbare regel hebben, geen willekeurige keuze.

3. Beslis of de numerieke DR-waarde rechtstreeks frequentie bepaalt, of via een transformatie.

4. Documenteer de keuze in het boek.

**Output:** Vier expliciete mappings met parameterfuncties.

---

## Stap 3 — De Vier Golven Berekenen

**Te doen:**
1. Pas M_A op P_A → W_A(t) = a_A sin(2π f_A t + φ_A)
2. Pas M_B op P_B → W_B(t) = a_B sin(2π f_B t + φ_B)
3. Pas M_C op P_C → W_C(t) = a_C sin(2π f_C t + φ_C)
4. Pas M_D op P_D → W_D(t) = a_D sin(2π f_D t + φ_D)

**Output:** Vier golfparameters (f, a, φ) per lens.

---

## Stap 4 — E(t) Superpositie Genereren

**Te doen:**
1. Combineer W_A + W_B + W_C + W_D → E(t)
2. Genereer audio-output (MIDI of WAV)
3. Sla op als `E_audio-output`
4. Documenteer de samengestelde golf in het boek

**Output:** `E_audio-output` bestand + golfvorm-parameter in hexa-book-001.md

---

## Stap 5 — Return-Invariant Vastleggen (V_k)

**Te doen:**
1. Vooraf definiëren welke invariant `V_k` per route wordt gebruikt
2. `V_k(r_begin)` vastleggen vóór sonificatie
3. De invariant kan zijn:
   - `V_DR` = digitale wortel behoud
   - `V_interval` = frequentieverhouding behoud
   - `V_369` = 3-6-9 validatietrio behoud
4. Kies ÉÉN primary invariant (of meer, maar vóór uitvoer vastleggen)

**Output:** `V_k` gedefinieerd en `V_k(r_begin)` vastgelegd.

---

## Stap 6 — R(E) Return-Operator Uitvoeren

**Te doen:**
1. Definieer R: hoe leest de audio-output terug naar ℱ?
2. Pas R op E_audio-output → r_return
3. Bereken `V_k(r_return)`
4. Vergelijk: `V_k(r_begin) = V_k(r_return)`?

**Output:** `r_return` berekend, `status_validated` bijgewerkt.

---

## Stap 7 — Validatie & Documentatie

**Te doen:**
1. `status_validated` bijwerken: `gevalideerd` of `verworpen`
2. Alle tussenstappen in hexa-book-001.md opnemen
3. Artikel E updaten van "architectuur" naar "uitgevoerd"
4. Artikel F updaten met R(E) resultaat
5. Eindstatus: `status_validated(r_begin, r_return) = {gevalideerd|verworpen}`

**Output:** Self-validating boek. De wiskunde kan zichzelf toetsen.

---

## Afhankelijkheden

```
Stap 1 (C_sound) → Stap 2 (Mappings) → Stap 3 (Golven) → Stap 4 (E(t))
                                                                  ↓
Stap 5 (V_k) ─────────────────────────────────────────────────────→ Stap 6 (R(E))
                                                                        ↓
                                                                   Stap 7 (Validatie)
```

Stap 5 kan parallel met Stappen 1-4, mits `V_k` vóór Stap 6 is vastgelegd.

---

## Start

Volgende stap: **Stap 1 — C_sound uitvoeren.**
