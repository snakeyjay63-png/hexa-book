# Engine Test Report — 2026-07-24

**Scope:** Digital Root correctness + Frequency validation
**Files tested:** `hexa-book-engine.py`, `validate_freq_lenses.py`
**Status:** Mostly correct, 1 float-handling concern, 1 task-description error

---

## 1. `digital_root()` — Engine Function Verification

The engine's `digital_root(n)` uses the standard mod-9 approach:
- `n % 9`, returning 9 for multiples of 9
- Floats are rounded to `int(round(n))` first

| Input    | Expected | Engine | Status  | Notes                              |
|----------|----------|--------|---------|------------------------------------|
| 66       | 3        | 3      | ✅      | Allah Abjad                        |
| 528      | **6**    | 6      | ✅      | Solfeggio — see note below         |
| 396      | 9        | 9      | ✅      | Solfeggio                          |
| 11       | 2        | 2      | ✅      |                                    |
| 529      | 7        | 7      | ✅      | Isopsefia ὁ θεός                   |
| 1071     | 9        | 9      | ✅      | Lens D                             |
| 440      | 8        | 8      | ✅      | A4 concert pitch                   |
| 432      | 9        | 9      | ✅      |                                    |

**All integer DR calculations are correct.**

---

## 2. Float Handling — `DR(437.2725)`

### Issue Found

The engine's grand average frequency from C_sound is **437.2700 Hz** (very close to the 437.2725 Hz referenced in the book).

**Engine behavior:**
```
digital_root(437.2725)
→ int(round(437.2725)) = 437
→ 437 % 9 = 5
→ Returns: 5
```

**Book/expected behavior (digit-sum approach):**
```
4+3+7+2+7+2+5 = 30 → 3+0 = 3
→ Returns: 3
```

**Result: MISMATCH** — Engine returns 5, expected digit-sum gives 3.

### Assessment

This is a design choice, not a bug per se. The standard mathematical digital root is defined on **integers**, and the engine's approach (round → mod-9) is the correct implementation of that definition. The "sum all digits including decimals" method is non-standard and would require explicit decimal handling.

**However**, if the book intends DR to operate on the full decimal representation (treating the decimal as just another digit), the engine needs a separate function like `digital_root_decimals(n)` that strips the decimal point and sums all digits.

**Severity:** Low — only affects float inputs. All integer DR calls in the engine are correct.

---

## 3. `validate_freq_lenses.py` — Output Verification

### Lens A: Arabisch → 396 Hz

| Check           | Result   | Status |
|-----------------|----------|--------|
| Allah Abjad sum | 66       | ✅     |
| DR(66)          | 3        | ✅     |
| 66 × 4 = 264 Hz | correct  | ✅     |
| 264 × 1.5 = 396 | correct  | ✅     |
| DR(396)         | 9        | ✅     |
| 3→3→9 cyclus    | ✅       | ✅     |
| 66 × 6 = 396    | correct  | ✅     |

### Lens B: Grieks → 440 Hz

| Check             | Result | Status |
|-------------------|--------|--------|
| πυρ isopsefia     | 580    | ✅     |
| λιθος isopsefia   | 319    | ✅     |
| κυμα isopsefia    | 461    | ✅     |
| Totaal Grieks     | 1360   | ✅     |
| DR(1360)          | 1      | ✅     |
| DR(440)           | 8      | ✅     |

### Lens C: Sanskriet → 432 Hz

| Check              | Result | Status |
|--------------------|--------|--------|
| अग्नि phonem-sum   | 24     | ✅     |
| शिला phonem-sum    | 58     | ✅     |
| तरंग phonem-sum    | 46     | ✅     |
| Totaal Sanskriet   | 128    | ✅     |
| DR(128)            | 2      | ✅     |
| DR(432)            | 9      | ✅     |
| 432 / 24 = 18.0    | exact   | ✅     |

### Cross-Validation

| Check                          | Result           | Status |
|--------------------------------|------------------|--------|
| DR(396)                        | 9                | ✅     |
| DR(440)                        | 8                | ✅     |
| DR(432)                        | 9                | ✅     |
| GCD(396, 432, 440)             | 4                | ✅     |
| 396/440 = 0.9 (9/10)           | correct          | ✅     |
| 396/432 = 11/12                | correct          | ✅     |
| 396↔432: 150.6 cents           | correct          | ✅     |
| 396↔440: 182.4 cents           | correct          | ✅     |
| 432↔440: 31.8 cents            | correct          | ✅     |

### Tekenset Sizes

| System                  | Count | DR   |
|------------------------|-------|------|
| Abjad                  | 28    | 1    |
| Isopsefia (Greek)      | 27    | ~24  |
| Sanskrit consonants    | 35    | —    |
| Sanskrit vowels        | 13    | —    |
| Sanskrit total         | 48    | 3    |

---

## 4. Task Description Error

The task stated:
> `DR(528)` should be 3 (5+2+8=15 → 1+5=6) — verify

This is self-contradictory: it claims DR should be 3, but the math shown (1+5) = **6**.

**Correct value: DR(528) = 6** (5+2+8=15, 1+5=6). Engine computes this correctly.

---

## 5. Engine Mappings (Stap 2) — Verification

| Lens | Input           | DR  | Freq    | Amplitude | Phase   | Status |
|------|-----------------|-----|---------|-----------|---------|--------|
| M_A  | Abjad 66        | 3   | 293.66  | 1.0000    | π/2     | ✅     |
| M_B  | Isopsefia 529   | 7   | 440.00  | 0.5000    | 3π/2    | ✅     |
| M_C  | C_sound grand   | 5   | 349.23  | 0.3333    | π       | ✅     |
| M_D  | D_numeric 1071  | 9   | 523.25  | 1.0000    | 2π      | ✅     |

All mappings derive correctly from the DR→(f, a, φ) conversion formula.

---

## Summary

| Category                    | Status     | Details                                      |
|-----------------------------|------------|----------------------------------------------|
| Integer DR calculations     | ✅ PASS    | All 8 test values correct                    |
| Float DR (437.2725)         | ⚠️ DESIGN  | Engine returns 5, digit-sum gives 3          |
| validate_freq_lenses output | ✅ PASS    | All lens validations consistent              |
| Cross-frequency ratios      | ✅ PASS    | Cents, GCD, ratios all correct               |
| Task description (DR 528)   | ❌ ERROR   | Task says 3, correct answer is 6             |

### Findings

1. **No bugs in integer digital_root** — The mod-9 implementation is correct and matches the standard definition.

2. **Float handling design choice** — `digital_root(437.2725)` returns 5 (via round→mod-9) vs. 3 (via full digit-sum). This is a valid implementation choice for the standard integer DR, but if the book requires decimal-aware DR, a separate function is needed.

3. **validate_freq_lenses.py runs cleanly** — All three frequency lenses (396/440/432 Hz) validate correctly against their respective character set sums.

4. **Grand average frequency is 437.27 Hz** — This is the C_sound output. It's close to 437.2725 Hz but not exact. The discrepancy likely comes from SLOT_FREQS approximations.

---

## Spike 019 Integration — 2026-07-24 14:45

### Changes
- Zig source gesynced naar `engine/patanjali-veld/src/` (Unicode versie)
- `validate_patanjali.py` gefixed:
  - `std.debug.print` → stderr (Zig behavior)
  - Unicode regex: `↔`, `×`, `→` support
- Parent `engine/validate_patanjali.py` gesynced

### Validation
```
  ✅ Entry DR=2
  ✅ Trilling 4↔7
  ✅ Stilte 1=1
  ✅ Beide naar entry
  ✅ Richting ×2=2
  ✅ Richting /2=5
  ✅ Cirkels=19 (DR=1)
  ✅ Oogjes=90 (DR=9)
  ✅ DR cyclus 2→8→3→3→9
```
**Result: 9/9 ✅ — Veld validatie geslaagd**

### Batch Reviews 03-15
- 13 reviews verwerkt (inbox → 02-done)
- P0 fixes artikelen 003-013:
  - X-2: NPR-fase disclaimer (interpretatief/vikalpa)
  - X-3: HEXA-buiten cross-ref (11,12,13 transcendentie-domein)
  - Per-artikel status labels (C_sound, J', H(x), Mandelbrot, six-cycle, etc.)
