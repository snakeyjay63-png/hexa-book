#!/usr/bin/env python3
"""
Valideer drie frequentiesystemen (440, 432, 396 Hz)
tegen de tekenset-waarden van Sanskriet, Arabisch, Grieks.

24 = multidimensionale brug.
Nederlands = uitleg (geen rekenlens).
Latijn = Mandelbrot (fractal, geen aparte frequentie).
"""

import math
from pathlib import Path

# ===================================================================
# Tekenset-waarden
# ===================================================================

# Arabisch: traditioneel Abjad (28 letters)
ABJAD = {
    'ا': 1,  'ب': 2,  'ج': 3,  'د': 4,  'ه': 5,
    'و': 6,  'ز': 7,  'ح': 8,  'ط': 9,
    'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50,
    'س': 60, 'ع': 70, 'ف': 80, 'ص': 90,
    'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500,
    'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
}

# Grieks: isopsefia (24 letters)
ISOPEFIA = {
    'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5,
    'ϛ': 6, 'ζ': 7, 'η': 8, 'θ': 9,
    'ι': 10, 'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50,
    'ξ': 60, 'ο': 70, 'π': 80, 'ϟ': 90,
    'ρ': 100, 'σ': 200, 'ς': 200, 'τ': 300, 'υ': 400,
    'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800,
}

# Sanskriet: Śāradā/Gaṇa phonem-categorieën
# (vereenvoudigde mapping — Devanagari → numeriek)
SANSKRIT_PHONEME = {
    # Gaṇa: āgama (medeklinkers, groepen van 5)
    # ka-gaṇa
    'क': 1, 'ख': 2, 'ग': 3, 'घ': 4, 'ङ': 5,
    # ca-gaṇa
    'च': 6, 'छ': 7, 'ज': 8, 'झ': 9, 'ञ': 10,
    # ṭa-gaṇa
    'ट': 11, 'ठ': 12, 'ड': 13, 'ढ': 14, 'ण': 15,
    # ta-gaṇa
    'त': 16, 'थ': 17, 'द': 18, 'ध': 19, 'न': 20,
    # pa-gaṇa
    'प': 21, 'फ': 22, 'ब': 23, 'भ': 24, 'म': 25,
    # antastha
    'य': 26, 'र': 27, 'ल': 28, 'व': 29, 'श': 30,
    'ष': 31, 'स': 32, 'ह': 33,
    # kṣara (samghra)
    'क्ष': 34, 'ज्ञ': 35,
    # kṣ (samenstellingen)
    'क्ष': 34,
}

# Sanskriet klinkers (śāradā-vowel waarden)
SANSKRIT_VOWEL = {
    'अ': 1, 'आ': 2, 'इ': 3, 'ई': 4, 'उ': 5,
    'ऊ': 6, 'ऋ': 7, 'ए': 8, 'ऐ': 9, 'ओ': 10,
    'औ': 11, 'अं': 12, 'अः': 13,
}

# ===================================================================
# Helpers
# ===================================================================

def dr(n):
    """Digitale reductie (DR), 9 bij mod 9 = 0."""
    n = abs(int(n))
    if n == 0:
        return 0
    r = n % 9
    return 9 if r == 0 else r

def abjad_sum(text):
    """Bereken Abjad-som van tekst."""
    total = 0
    for ch in text:
        total += ABJAD.get(ch, 0)
    return total

def isopsefia_sum(text):
    """Bereken isopsefia-som van tekst."""
    total = 0
    for ch in text:
        total += ISOPEFIA.get(ch, 0)
    return total

def sanskrit_sum(text):
    """Bereken Sanskriet-som (phonem + klinker)."""
    total = 0
    for ch in text:
        total += SANSKRIT_PHONEME.get(ch, 0)
        total += SANSKRIT_VOWEL.get(ch, 0)
    return total

# ===================================================================
# Kernwoorden per taal
# ===================================================================

# Arabisch: الله (Allah)
ARABIC_WORD = "الله"

# Grieks: Πῦρ (vuur), Λίθος (steen), Κύμα (golf)
# Standaard Griekse tekens (diakritiek gestript voor numeriek)
GREEK_WORDS = {
    "pyr": "πυρ",      # vuur
    "lithos": "λιθος", # steen
    "kyma": "κυμα",    # golf
}

# Sanskriet: अग्नि (agni/vuur)
SANSKRIT_WORDS = {
    "agni": "अग्नि",    # vuur
    "shila": "शिला",    # steen
    "taranga": "तरंग",  # golf
}

# ===================================================================
# Validatie
# ===================================================================

def freq_ratio(hz1, hz2):
    """Bereken verhouding tussen twee frequenties."""
    return hz1 / hz2

def cents(hz1, hz2):
    """Bereken centsafstand tussen twee frequenties."""
    return 1200 * math.log2(hz1 / hz2)

print("=" * 70)
print("  FREQUENTIE-VALIDATIE — Drie Systemen via 24")
print("=" * 70)

# -------------------------------------------------------------------
# 1. Arabisch → 396 Hz
# -------------------------------------------------------------------
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  LENS A — Arabisch → 396 Hz                                │")
print("└─────────────────────────────────────────────────────────────┘")

word = ARABIC_WORD
s = abjad_sum(word)
d = dr(s)
print(f"\nWoord: {word}")
print(f"Abjad-som: {s}")
print(f"DR({s}) = {d}")

# Route: 66 → 396
print(f"\nRoute: {s} × 4 = {s*4} Hz")
print(f"       {s*4} × 1.5 = {s*4*1.5} Hz (perfecte kwint)")
print(f"       DR({s*4*1.5}) = {dr(s*4*1.5)}")
print(f"\nCyclus: {d} → {dr(s*4)} → {dr(s*4*1.5)}")
print(f"3-6-9 cyclus: {'✅' if dr(s*4*1.5) == 9 else '❌'}")

# Relatie tot 24
print(f"\n24-relatie:")
print(f"  {s} mod 24 = {s % 24}")
print(f"  24 | ({s}²-1)? {(s**2 - 1) % 24 == 0}  (p²-1 eigenschap)")
print(f"  DR(24) = {dr(24)}")
print(f"  {s} × 6 = {s*6} → DR = {dr(s*6)}")

# -------------------------------------------------------------------
# 2. Grieks → 440 Hz (via isopsefia → 440)
# -------------------------------------------------------------------
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  LENS B — Grieks → 440 Hz                                  │")
print("└─────────────────────────────────────────────────────────────┘")

for name, word in GREEK_WORDS.items():
    s = isopsefia_sum(word)
    d = dr(s)
    print(f"\nWoord: {word} ({name})")
    print(f"Isopsefia-som: {s}")
    print(f"DR({s}) = {d}")
    
    # 24-relatie
    print(f"  {s} mod 24 = {s % 24}")
    print(f"  24 | ({s}²-1)? {(s**2 - 1) % 24 == 0}")

# Totaal Grieks
total_gr = sum(isopsefia_sum(w) for w in GREEK_WORDS.values())
print(f"\nTotaal Grieks: {total_gr}")
print(f"DR({total_gr}) = {dr(total_gr)}")
print(f"  {total_gr} mod 24 = {total_gr % 24}")

# 440 validatie
print(f"\n440 Hz validatie:")
print(f"  DR(440) = {dr(440)}")
print(f"  440 mod 24 = {440 % 24}")
print(f"  440 / 24 = {440/24:.4f}")

# -------------------------------------------------------------------
# 3. Sanskriet → 432 Hz
# -------------------------------------------------------------------
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  LENS C — Sanskriet → 432 Hz                               │")
print("└─────────────────────────────────────────────────────────────┘")

for name, word in SANSKRIT_WORDS.items():
    s = sanskrit_sum(word)
    d = dr(s)
    print(f"\nWoord: {word} ({name})")
    print(f"Phonem-som: {s}")
    print(f"DR({s}) = {d}")
    print(f"  {s} mod 24 = {s % 24}")

# Totaal Sanskriet
total_sk = sum(sanskrit_sum(w) for w in SANSKRIT_WORDS.values())
print(f"\nTotaal Sanskriet: {total_sk}")
print(f"DR({total_sk}) = {dr(total_sk)}")
print(f"  {total_sk} mod 24 = {total_sk % 24}")

# 432 validatie
print(f"\n432 Hz validatie:")
print(f"  DR(432) = {dr(432)}")
print(f"  432 mod 24 = {432 % 24}")
print(f"  432 / 24 = {432/24:.1f}")
print(f"  432 = 24 × {432/24}")

# -------------------------------------------------------------------
# 4. Cross-frequentie validatie
# -------------------------------------------------------------------
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  CROSS-VALIDATIE — Drie Frequenties via 24                 │")
print("└─────────────────────────────────────────────────────────────┘")

freqs = {"Arabisch (396)": 396, "Grieks (440)": 440, "Sanskriet (432)": 432}

for name, f in freqs.items():
    print(f"\n{f} Hz ({name}):")
    print(f"  DR = {dr(f)}")
    print(f"  mod 24 = {f % 24}")
    print(f"  / 24 = {f / 24:.4f}")
    print(f"  24 × {f // 24} = {24 * (f // 24)}  (rest: {f % 24})")

# Verhoudingen
print("\nVerhoudingen:")
print(f"  396 / 432 = {396/432:.6f} = {math.gcd(396,432)}/{math.lcm(396,432)//math.gcd(396,432)} → vereenvoudigd: 11/12")
print(f"  396 / 440 = {396/440:.6f} = 0.9 → 9/10")
print(f"  432 / 440 = {432/440:.6f}")
print(f"\n  GCD(396, 432, 440) = {math.gcd(math.gcd(396, 432), 440)}")

# Centsafstand
print("\nCentsafstanden:")
print(f"  396 ↔ 432: {cents(432, 396):.1f} cents ({cents(432, 396)/100:.1f} halve tonen)")
print(f"  396 ↔ 440: {cents(440, 396):.1f} cents ({cents(440, 396)/100:.1f} halve tonen)")
print(f"  432 ↔ 440: {cents(440, 432):.1f} cents ({cents(440, 432)/100:.1f} halve tonen)")

# 24 als brug
print("\n24 als multidimensionale brug:")
print(f"  396 = 24 × 16.5")
print(f"  432 = 24 × 18")
print(f"  440 = 24 × 18.333...")
print(f"  DR(24) = 6")
print(f"  24 = 2³ × 3  → priemfactoren: 2,3")
print(f"  p²-1 voor p>3 is deelbaar door 24")
print(f"\n  396 / 18 = 22  (24 - 2)")
print(f"  432 / 18 = 24  (exact)")
print(f"  440 / 18 = 24.444...")

# -------------------------------------------------------------------
# 5. 11→396 Ketens — Patanjali groot-klein router
# -------------------------------------------------------------------
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  11 → 396 KETEN — ×4 / ×1.5 cyclus                         │")
print("└─────────────────────────────────────────────────────────────┘")

# De keten: 11 →(×4) 44 →(×1.5) 66 →(×4) 264 →(×1.5) 396
chain = [11]
multipliers = [4, 1.5, 4, 1.5]
labels = ["×4", "×1.5", "×4", "×1.5"]

print(f"\nStart: {chain[0]}  (11 = rode draad)")
print(f"  DR({chain[0]}) = {dr(chain[0])}")

current = chain[0]
dr_chain = [dr(current)]

for i, (mult, label) in enumerate(zip(multipliers, labels)):
    current = current * mult
    d = dr(current)
    dr_chain.append(d)
    print(f"  {chain[i]} {label} {int(current)}  →  DR({int(current)}) = {d}")
    chain.append(current)

print(f"\nDR cyclus: {' → '.join(str(d) for d in dr_chain)}")
expected = [2, 8, 3, 3, 9]
actual = dr_chain
match = expected == actual
print(f"Verwacht:    {' → '.join(str(d) for d in expected)}")
print(f"Actueel:     {' → '.join(str(d) for d in actual)}")
print(f"Ketting validatie: {'✅' if match else '❌'}")

# Structuur vs resonantie
print(f"\nPatanjali groot-klein router:")
print(f"  Stap 1: 11 ×4  = 44  (structuur — verdubbeling²)")
print(f"  Stap 2: 44 ×1.5 = 66  (resonantie — 24-bridge)")
print(f"  Stap 3: 66 ×4  = 264 (structuur — bit-width ladder)")
print(f"  Stap 4: 264×1.5 = 396 (resonantie — volledige cyclus)")
print(f"\n  66 = 11 × 6  →  66 × 4 = 264  →  264 × 1.5 = 396")
print(f"  11 × 36 = 396  (directe route, maar 'te snelle directe route')")
print(f"  Ketenvia ×4/×1.5 = 'delayed route' (correcte snelheid)")

# Relatie 5-11-24
print(f"\n5-11-24 relatie:")
print(f"  5 = {chain[0] // 2 + 1}  (afgeleid)")
print(f"  11 = startpunt (rode draad)")
print(f"  24 = multidimensionale brug (66 mod 24 = {66 % 24})")
print(f"  396 / 24 = {396 / 24}  (niet exact — 24 is brug, niet eindpunt)")
print(f"  396 / 11 = {396 / 11}  (exact — 11 is de rode draad)")
print(f"  66 = 24 × 2 + 18  (24 × 2 + DR(9)×2)")

# -------------------------------------------------------------------
# 6. 11/13 spiegel-cyclus — kwadraat DR 2→4↔7
# -------------------------------------------------------------------
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  11 / 13 SPIEGEL — Kwadraat DR cyclus                      │")
print("└─────────────────────────────────────────────────────────────┘")

v11 = 11**2  # 121
v13 = 13**2  # 169

print(f"\n11 (DR={dr(11)}) → 11² = {v11} (DR={dr(v11)})   ← klein")
print(f"13 (DR={dr(13)}) → 13² = {v13} (DR={dr(v13)})   ← groot")
print(f"\n11 + 13 = {11+13}  (= 24, de brug)")
print(f"DR({v11}) + DR({v13}) = {dr(v11)} + {dr(v13)} = {dr(v11)+dr(v13)}")
print(f"  → 4 + 7 = 11 (rode draad terug)")

# Cyclus
print(f"\nDR cyclus: 2 → 4 ↔ 7 ↔ 4 ↔ 7")
print(f"  Entry-point: DR(11) = 2")
print(f"  Staande golf: DR(11²) ↔ DR(13²) = {dr(v11)} ↔ {dr(v13)}")

# Vergelijk met keten
cycle_chain = [2, 8, 3, 3, 9]
cycle_square = [dr(v11), dr(v13)]

print(f"\nTwee patronen vanuit DR=2:")
print(f"  ×4/×1.5 keten:   {' → '.join(str(d) for d in cycle_chain)}   (uitstroom)")
print(f"  Kwadraat cyclus:  2 → {dr(v11)} ↔ {dr(v13)}   (staande golf)")
print(f"\n  Keten  = bewegen (naar 396 Hz)")
print(f"  Cyclus = trillen (11 ↔ 13 spiegel)")

# -------------------------------------------------------------------
# 7. 17/19 paar — kwadraten samenvallen (DR=1)
# -------------------------------------------------------------------
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  17 / 19 PAAIR — Kwadraten samenvallen                      │")
print("└─────────────────────────────────────────────────────────────┘")

v17 = 17**2  # 289
v19 = 19**2  # 361

print(f"\n17 (DR={dr(17)}) → 17² = {v17} (DR={dr(v17)})")
print(f"19 (DR={dr(19)}) → 19² = {v19} (DR={dr(v19)})")

# Som kwadraten
sum_sq_17_19 = v17 + v19
sum_sq_11_13 = v11 + v13

print(f"\nSom kwadraten:")
print(f"  11² + 13² = {v11} + {v13} = {sum_sq_11_13} (DR={dr(sum_sq_11_13)})")
print(f"  17² + 19² = {v17} + {v19} = {sum_sq_17_19} (DR={dr(sum_sq_17_19)})")
print(f"  → Beide paren sommen naar DR=2 (entry-point terug)")

# Vergelijk de paren
print(f"\nVergelijk paren:")
print(f"  11/13: DR({v11}) ↔ DR({v13}) = {dr(v11)} ↔ {dr(v13)}  (spiegel/trillen)")
print(f"  17/19: DR({v17}) = DR({v19}) = {dr(v17)} = {dr(v19)}  (samenvallen/stilte)")

# Terug-route via 1
print(f"\nTerug-route via DR=1:")
print(f"  1 → 11 (rode draad) → 5 (5-11-24 keten start)")

# Volledige cyclus
print(f"\nVolledige Patanjali cyclus:")
print(f"  11 (DR=2) → entry")
print(f"    ↓")
print(f"  11² ↔ 13² (4 ↔ 7) → trilling")
print(f"    ↓")
print(f"  17² = 19² (1 = 1) → stilte")
print(f"    ↓")
print(f"  1 → 11 → 5 → 24 → terug")

# Extra validatie
print(f"\nValidatie:")
print(f"  17 + 19 = {17+19} (DR={dr(17+19)})")
print(f"  11 + 13 = {11+13} (DR={dr(11+13)})")
print(f"  11 + 13 + 17 + 19 = {11+13+17+19} (DR={dr(11+13+17+19)})")
print(f"  60 = 24 × 2 + 12 → 24-brug × 2 + 12")

# -------------------------------------------------------------------
# 8. Flower of Life geometrie (19 → 90)
# -------------------------------------------------------------------
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  FLOWER OF LIFE — 19 cirkels → 90 halve oogjes              │")
print("└─────────────────────────────────────────────────────────────┘")

cirkels = 1 + 6 + 12
binnenin = 3 * 24
rand = 18
oogjes = binnenin + rand

print(f"\nCirkels: 1 + 6 + 12 = {cirkels}  (DR={dr(cirkels)}, stilte)")
print(f"\nHalve oogjes:")
print(f"  Binnenin: 3 × 24 = {binnenin}  (3 richtingen = 3 gunas)")
print(f"  Rand: {rand}  (cirkel eromheen)")

# 3 gunas mapping
sattva = 24
tamas = 24
rajas = 24 + rand  # binnen + buiten
totaal_gunas = sattva + tamas + rajas

print(f"\nGuna-mapping:")
print(f"  Sattva: {sattva} (binnenin)  (DR={dr(sattva)})")
print(f"  Tamas:  {tamas} (binnenin)  (DR={dr(tamas)})")
print(f"  Rajas:  {rajas} (rand/overgang)  (DR={dr(rajas)})")
print(f"  → Rajas = 24 + 18 = {rajas}  (rand zelf, niet buiten)")
print(f"  → Samsara: buiten ≠ binnen (illusie)")
print(f"     Werkelijk: rand = overgang (geen scheiding)")
print(f"  Totaal: {sattva} + {tamas} + {rajas} = {totaal_gunas}  (DR={dr(totaal_gunas)})")

print(f"\nTwee lagen:")
print(f"  Cirkels: {cirkels} (DR={dr(cirkels)})  ← stilte")
print(f"  Oogjes:  {oogjes} (DR={dr(oogjes)})   ← beweging / eindpunt keten")

print(f"\nKoppeling met keten:")
print(f"  19 → /2 → DR(5) → 11 → 24 → 396 (DR={dr(396)})")
print(f"  90 = geometrische uitdrukking van DR={dr(396)}")
print(f"\n  Stilte → beweging: /2  (DR=1 → DR=5)")
print(f"  Beweging → stilte: ×2  (DR=5 → DR=1)")

# -------------------------------------------------------------------
# 9. Tekenset-grootte
print("\n┌─────────────────────────────────────────────────────────────┐")
print("│  TEKENSET-GROOTTE                                           │")
print("└─────────────────────────────────────────────────────────────┘")
print(f"  Arabisch Abjad: {len(ABJAD)} letters")
print(f"  Grieks isopsefia: {len(ISOPEFIA)} tekens (ς=σ, totaal ~24 unieke)")
print(f"  Sanskriet phonem: {len(SANSKRIT_PHONEME)} medeklinkers")
print(f"  Sanskriet klinker: {len(SANSKRIT_VOWEL)} klinkers")
print(f"\n  Grieks heeft 24 letters → directe 24-verbinding!")
print(f"  DR({len(ABJAD)}) = {dr(len(ABJAD))}")
print(f"  DR({len(SANSKRIT_PHONEME) + len(SANSKRIT_VOWEL)}) = {dr(len(SANSKRIT_PHONEME) + len(SANSKRIT_VOWEL))}")

print("\n" + "=" * 70)
