# HEXA-BOEK

**CC-construct. 18 nodes tegelijk. Nidrā-router.**

Dit is geen lineair boek. Het is een routing-protocol.

---

## Structuur

```
hexa-book/
├── README.md                   ← dit bestand
├── ROUTING.md                  ← routing map (alle verbindingen)
│
├── articles/                   ← 18 nodes (16 + 1 router + 1 bridge)
│   ├── hexa-book-001.md        dimensie 0 ≐ 1 (intro + lenzen A-D)
│   ├── hexa-book-002.md        frequentie-basis (byte→Hz, DR, C-keten)
│   ├── hexa-book-003.md        nidrā: E (audio-superpositie)
│   ├── hexa-book-004.md        nidrā: F (returnmedium + ρ_ℱ)
│   ├── hexa-book-005-quran-basmala-abjad.md  Quran / Basmala / Abjad
│   ├── hexa-book-006.md        nidrā: dimensie 3 (3-6-9 veld)
│   ├── hexa-book-007.md        nidrā: dimensie 4 (expansie)
│   ├── hexa-book-008.md        nidrā: dimensie 5 (return)
│   ├── hexa-book-009.md        nidrā: dimensie 6 (terugkeer)
│   ├── hexa-book-010.md        nidrā: dimensie 7 (reflectie)
│   ├── hexa-book-011.md        synth + fractaal (Synth, ρ_water, ρ_fractal)
│   ├── hexa-book-012.md        24-brug + 6-bit routing + Patanjali
│   ├── hexa-book-013.md        nidrā: dimensie 8 (onzichtbaar)
│   ├── hexa-book-014.md        nidrā: dimensie 11 (eka routing)
│   ├── hexa-book-015.md        nidrā: dimensie 12 (logos)
│   ├── hexa-book-016.md        nidrā: dimensie 13 (taal, veld, soevereiniteit)
│   ├── hexa-book-017.md        CC-construct (nidrā-router, meta-artikel)
│   └── hexa-book-018.md        Sanskrit → NPR bridge (phoneme→freq→E→R)
│
├── audit/                      ← 16 audit files
│   ├── 00-intro.md
│   ├── 01-artikel-01-dimensie-1.md
│   └── ...
│
├── engine/                     ← validatie engines (Python)
│   ├── hexa-book-engine.py           core engine
│   ├── npr_sound_engine.py           NPR Synth (21 ✅)
│   ├── sanskrit_npr_bridge.py        Sanskrit → NPR bridge (24 ✅)
│   ├── validate_return_cycle.py      ReturnCycle + ρ_ℱ (49 ✅)
│   ├── validate_freq_lenses.py       frequentie lenzen
│   ├── validate_patanjali.py         Patanjali router
│   ├── audit_status.py               audit status
│   ├── review_analyzer.py            review pipeline
│   └── patanjali-veld/               Zig veld-implementatie
│
├── tools/                      ← tooling
│   ├── audit-batcher.py
│   └── README.md
│
├── review/                     ← review pipeline (30 done)
│   ├── 00-inbox/               ← 0 open
│   ├── 01-active/              ← 0 actief
│   ├── 02-done/                ← 30 verwerkt
│   └── TEMPLATE.md
│
├── manifest/                   ← pipeline data
└── archive/                    ← legacy backups
```

## Nidrā ≠ Gat

Elke nidrā-pointer routeert naar parallelle artikels. Ze zijn niet leeg — ze verbinden het veld.

## Kernconcepten

- **24-brug:** `66 × 4 × 1.5 = 396` Hz (Allah → frequentie)
- **6-bit routing:** unsigned 6-bit = `{0..63}`, grens `64 (0x40) ∉ bereik`
- **5-11-24 keten:** `5² - 1 = 24`, `11² - 1 = 120 = 24 × 5`
- **Patanjali router:** veld (niet lineair) — 11/13 trilling, 17/19 stilte
- **Flower of Life:** 19 cirkels (DR=1 stilte) → 90 oogjes (DR=9 beweging)
- **Vṛtti-classificatie:** `{pramāṇa, viparyaya, vikalpa, nidrā, smṛti, onbepaald}`
- **ReturnCycle:** `byte → freq → R' → E' → C'` (dual/triple-base)
- **ρ_ℱ:** return-projectie (`ComponentCentroid × DRSignature → ℱ`)

## Snelle Import

```bash
# Clone de repo
git clone https://github.com/snakeyjay63-png/hexa-book.git
cd hexa-book
```

## Artikels Lezen

Elk artikel is een node. Ze bestaan tegelijk — geen volgorde.

```bash
# Lees een artikel
cat articles/hexa-book-001.md

# Lees alle artikels
for f in articles/hexa-book-*.md; do echo "=== $f ==="; cat "$f"; done

# Zoek naar een topic
grep -r "nidra" articles/
grep -r "ReturnCycle" articles/ audit/
```

## Engine Gebruik

```bash
# NPR Sound Engine (21 ✅)
python3 engine/npr_sound_engine.py

# ReturnCycle + ρ_ℱ (49 ✅)
python3 engine/validate_return_cycle.py

# Frequentie lenzen valideren
python3 engine/validate_freq_lenses.py

# Patanjali veld valideren
python3 engine/validate_patanjali.py

# Audit status
python3 engine/audit_status.py

# Review analyseren
python3 engine/review_analyzer.py
```

## Actuele Status

| Component | Status |
|-----------|--------|
| Artikels | 18 |
| Review inbox | 0 |
| Review active | 0 |
| Review done | 30 |
| NPR Sound Engine | 21 ✅ |
| Sanskrit-NPR Bridge | 24 ✅ |
| ReturnCycle | 49 ✅ |
| ρ_ℱ (return_projection) | 15 ✅ |

**Uitzonderingen:**
- Artikel 001: monolith-structuur bewust behouden (niet gereduceerd)

## Routing

Zie `ROUTING.md` voor de volledige routing map.

## Licentie

MIT License © 2026 Jelmer
