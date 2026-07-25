# hexa-book — Routing Map

> **Articles → Audits → Spikes → Engines → Reviews**
> De pipeline van concept naar validatie.

---

## Overzicht

```
articles/           ← Bron-content (4+1 per artikel, nidrā = cross-ref)
   │
   ├── hexa-book-002.md  ← frequentie-basis (byte→Hz, DR, C-keten)
   ├── hexa-book-011.md  ← synth + fractaal (Synth, ρ_water, ρ_fractal)
   ├── hexa-book-012.md  ← routing + audit (24-brug, 6-bit, NPR Bedrock)
   ├── hexa-book-017.md  ← CC-construct (nidrā-router, meta-artikel)
   ├── hexa-book-018.md  ← Sanskrit-NPR bridge (Devanagari→phoneme→E(t)→R(E))
   │
   ├── hexa-book-003.md  ← nidrā: E (audio-superpositie)
   ├── hexa-book-004.md  ← nidrā: F (returnmedium)
   ├── hexa-book-006.md  ← nidrā: dimensie 3 (3-6-9 veld)
   ├── hexa-book-007.md  ← nidrā: dimensie 4 (expansie)
   ├── hexa-book-008.md  ← nidrā: dimensie 5 (return zichtbaar)
   ├── hexa-book-009.md  ← nidrā: dimensie 6 (terugkeer vormt zich)
   ├── hexa-book-010.md  ← nidrā: dimensie 7 (reflectie)
   ├── hexa-book-013.md  ← nidrā: dimensie 8 (onzichtbaar)
   ├── hexa-book-014.md  ← nidrā: dimensie 11 (eka routing)
   ├── hexa-book-015.md  ← nidrā: dimensie 12 (logos)
   └── hexa-book-016.md  ← nidrā: dimensie 13 (taal, veld, soevereiniteit)
   │
   ▼
audit/              ← Audit per artikel
   │
   ├─► engine/audit_status.py     ← Live status scanner
   └─► engine/review_analyzer.py  ← Review pipeline
   │
   ▼
review/             ← Actieve reviews (inbox → active → archive)
   │
   ├─► engine/validate_freq_lenses.py  ← Frequentielens-validatie
   └─► tools/audit-batcher.py   ← Batch audit runner
```

## Nidrā — 4+1 Structuur

Elk artikel volgt het 4+1 patroon:
- **4 delen:** inhoudelijke secties
- **+1 nidrā:** verwijzing naar parallel artikel (niet wachtend)

Nidrā ≠ gat. Nidrā = terugkeer naar kern via ander perspectief.
```

---

## 1. Articles → Audits

Elk artikel krijgt een audit-bestand. Artikel 02 is opgesplitst in 02 + 11 + 12.

| Artikel | Onderwerp | Nidrā | Status |
|---------|-----------|-------|--------|
| `hexa-book-001.md` | Dimensie 1 | — | ✅ |
| `hexa-book-002.md` | frequentie-basis | → zie 11,12 | ✅ |
| `hexa-book-005.md` | Quran Basmala | — | ✅ |
| `hexa-book-011.md` | synth + fractaal | → zie 02 | ✅ |
| `hexa-book-012.md` | 24-brug + routing | → zie 02,11 | ✅ |
| `hexa-book-017.md` | CC-construct (nidrā-router) → alle 16 nodes | → alle artikels | ✅ |
| `hexa-book-018.md` | Sanskrit-NPR bridge (Devanagari→phoneme→E(t)→R(E)) | → 002, 011 | ✅ |

**Nidrā-pointers** (niet leeg — routeert naar parallel artikels):

| `hexa-book-003.md` | E: audio-superpositie | → 002, 001, 017 | ✅ |
| `hexa-book-004.md` | F: returnmedium | → 002, 012, 017 | ✅ |
| `hexa-book-006.md` | Dimensie 3: 3-6-9 veld | → 012, 017 | ✅ |
| `hexa-book-007.md` | Dimensie 4: expansie | → 011, 012, 001 | ✅ |
| `hexa-book-008.md` | Dimensie 5: return zichtbaar | → 012, 006, 001 | ✅ |
| `hexa-book-009.md` | Dimensie 6: terugkeer vormt zich | → 012 | ✅ |
| `hexa-book-010.md` | Dimensie 7: reflectie | → 001, 002, 017 | ✅ |
| `hexa-book-013.md` | Dimensie 8: onzichtbaar | → 001, 017, 002 | ✅ |
| `hexa-book-014.md` | Dimensie 11: eka routing | → 001, 012, 017 | ✅ |
| `hexa-book-015.md` | Dimensie 12: logos | → 002, 001, 017 | ✅ |
| `hexa-book-016.md` | Dimensie 13: taal, veld, soevereiniteit | → 001, 017, 012 | ✅ |

**Koppeling:** Audit filename → artikel nummer (`02-` = artikel 002).

---

## 2. Audits → Spikes

Audits die implementatie vereisen → spikes:

| Concept | Spike | Doel |
|---------|-------|------|
| 6-bit routing | `spikes/002-6bit-routing-zig/` | 64-slot address space, digital root, guna |
| 24-bridge | *(nog te maken)* | 24 als bridge tussen dimensies |
| Patanjali groot-klein | *(nog te maken)* | 0x3F boundary, routing |

### 6-Bit Routing (Spike 002)

```
64 slots (0-63)
   │
   ├─ digital root (1-9, 0=zero)
   ├─ guna (sattva / rajas / tamas)
   └─ 5 element boundaries: 25, 35, 49, 55, 63
       └─ water, fire, earth, air, ether
```

**Koppeling met boek:**
- Artikel 002 (Dimensie 2) → beschrijft 6-bit routing concept
- Spike 002 → implementatie in Zig
- `0x3F` (63) = ether boundary = groot/klein grens

---

## 3. Spikes → Tokenfield

De NPR Tokenfield is de runtime-bridge tussen spikes en boek:

| Component | Locatie | Rol |
|-----------|---------|-----|
| Matrika-48 | `NPR-sandbox-tokenfield/src/matrika.zig` | Token → slot/tick/root |
| Vortex | `NPR-sandbox-tokenfield/src/vortex.zig` | CC-program, implosie/explosie |
| Router | `NPR-sandbox-tokenfield/src/router.zig` | 6-bit routing runtime |
| Geometry | `NPR-sandbox-tokenfield/src/geometry.zig` | Hex-grid, spatial |

### Tokenfield Bridge

```
Artikel concept (taal)
   │
   ▼
Spike prototype (Zig code)
   │
   ▼
Tokenfield runtime (matrika + vortex + router)
   │
   ▼
Engine validatie (Python)
```

---

## 4. Engines

Python scripts voor validatie:

| Engine | Doel |
|--------|------|
| `engine/audit_status.py` | Live audit status (zoals `git status`) |
| `engine/review_analyzer.py` | Review pipeline scanner |
| `engine/validate_freq_lenses.py` | Frequentielens validatie |
| `engine/sanskrit_npr_bridge.py` | Sanskrit → NPR bridge (24/24 ✅) |
| `tools/audit-batcher.py` | Batch audit runner (meerdere artikels) |

### Audit Status

```bash
cd hexa-book
python3 engine/audit_status.py
# → ✅/⚠️/❌ per audit bestand
```

### Opsplitsing Artikel 02

Artikel 02 (673 regels) was te groot → opgesplitst:
- **002:** frequentie-basis (byte→Hz, DR, C-keten) — 221 regels
- **011:** synth + fractaal (Synth, ρ_water, ρ_fractal) — 211 regels  
- **012:** 24-brug + 6-bit + NPR Bedrock — 280 regels

Nidrā = verwijzing tussen artikels. Niet wachtend, parallel.

### Audit Batcher

```bash
cd hexa-book
python3 tools/audit-batcher.py status           # huidige toestand
python3 tools/audit-batcher.py validate          # volledige validatie
python3 tools/audit-batcher.py role orchestrator review.md  # orchestrator rol
```

Batcher koppelt: artikel → audit → review → merge → article.

### Review Pipeline

```
review/00-inbox/        ← Nieuwe reviews
   │
   ▼
review/01-active/       ← Actieve reviews
   │
   ▼
review/02-archive/      ← Afgeronde reviews
```

---

## 5. Mathematische Validatie

### 24-Bridge

```
24 = 6 × 4
   = bits × dimensie

6-bit routing: 0-63 (0x3F)
24 → dimensie-bridge (tussen 1 en 2)
48 = 24 × 2 (matrika-48)
```

### Groot-Klein (Patanjali)

```
63 (0x3F) = ether = maximum 6-bit
   │
   ├─ < 63 → "klein" (binnen routing)
   └─ > 63 → "groot" (needs routing/compression)

Bit-width ladder:
6 → 12 → 24 → 48  (doubling)
24 → 32 → 8       (compression)
crossover bij 8
```

### Frequentie Validatie

```
66 × 4 × 1.5 = 396  ← ISO 440 Hz bridge
24             ← bridge constant
11             ← rode draad
```

### 11→396 Ketens (Patanjali groot-klein)

```
11  (DR=2)  ← start (rode draad)
 ×4
44  (DR=8)  ← structuur (verdubbeling²)
 ×1.5
66  (DR=3)  ← resonantie (24-bridge)
 ×4
264 (DR=3)  ← structuur (bit-width ladder)
 ×1.5
396 (DR=9)  ← resonantie (volledige cyclus)
```

**DR cyclus:** `2 → 8 → 3 → 3 → 9`

**Patroon:** `×4 → ×1.5` herhaalt (structuur eerst, frequentie volgt).
- Directe route: `11 × 36 = 396` (te snel)
- Delayed route: `×4 → ×1.5 → ×4 → ×1.5` (juiste snelheid)

**Engine-validatie:** `engine/validate_freq_lenses.py` — sectie 5.
**Ketting test:** ✅ (verwacht `2→8→3→3→9` = actueel)

### 11/13 Spiegel-cyclus (Kwadraten)

```
11 (DR=2) → 11² = 121 (DR=4)   ← klein
13 (DR=4) → 13² = 169 (DR=7)   ← groot

11 + 13 = 24   ← brug
4  +  7 = 11   ← rode draad terug
```

**DR cyclus:** `2 → 4 ↔ 7 ↔ 4 ↔ 7` (staande golf)

**Twee patronen vanuit DR=2:**
| Keten (×4/×1.5) | `2 → 8 → 3 → 3 → 9` (uitstroom) |
| Kwadraat cyclus | `2 → 4 ↔ 7` (staande golf) |

Keten = bewegen (naar 396 Hz). Cyclus = trillen (11 ↔ 13 spiegel).

**Engine-validatie:** `engine/validate_freq_lenses.py` — sectie 7.

### 17/19 Paar — Kwadraten Samenvallen

```
17 (DR=8) → 17² = 289 (DR=1)
19 (DR=1) → 19² = 361 (DR=1)

17² + 19² = 650 (DR=2)  ← entry-point terug
11² + 13² = 290 (DR=2)  ← entry-point terug
```

**Tegenover 11/13:**

| Paar | Kwadraten | DR | Gedrag |
|------|-----------|----|--------|
| 11/13 | 121/169 | 4↔7 | spiegelbeeld / trillen |
| 17/19 | 289/361 | 1=1 | samenvallen / stilte |

**Terug-route via DR=1:**
```
1 → 11 (rode draad) → 5 (5-11-24 keten start)
```

**Volledige Patanjali cyclus:**
```
11 (DR=2) → entry
  ↓
11² ↔ 13² (4 ↔ 7) → trilling
  ↓
17² = 19² (1 = 1) → stilte
  ↓
1 → 11 → 5 → 24 → terug
```

11/13 trilt. 17/19 valt samen. Beide paren sommen naar DR=2. Stilte na trilling, terugkeer via rode draad.

**Engine-validatie:** `engine/validate_freq_lenses.py` — sectie 8.

### Flower of Life Geometrie (19 → 90)

```
Flower of Life: 1 + 6 + 12 = 19 cirkels (DR=1, stilte)
Halve oogjes:
  Binnenin: 3 × 24 = 72  (3 richtingen = 3 gunas)
  Rand: 18               (cirkel eromheen)
  Totaal: 72 + 18 = 90   (DR=9)
```

**3 Guna-mapping:**

| Guna | Oogjes | DR | Bereik |
|------|--------|----|-------|
| Sattva | 24 | 6 | binnenin |
| Tamas | 24 | 6 | binnenin |
| Rajas | 24 + 18 = 42 | 6 | **rand/overgang** |

**Totaal:** `24 + 24 + 42 = 90` ✅

Rajas reikt niet naar buiten. Rajas *is* de rand. De 18 is niet "buiten" — het is de overgang zelf.  
Samsara: buiten ≠ binnen ← illusie.  
Werkelijk: rand = overgang ← geen scheiding.

**Twee lagen:**
- Cirkels: `19` (DR=1) ← stilte
- Oogjes: `90` (DR=9)  ← beweging / eindpunt keten

**Koppeling met 11→396 keten:**
```
19 → /2 → DR(5) → 11 → 24 → 396 (DR=9)
90 = geometrische uitdrukking van DR=9
```

De Flower of Life bevat zowel stilte (19) als beweging (90).  
Stilte wordt beweging via `/2` (DR=1 → DR=5).  
Beweging wordt stilte via `×2` (DR=5 → DR=1).

**Engine-validatie:** `engine/validate_freq_lenses.py` — sectie 9.

---

## 6. Bestandsstructuur

```
hexa-book/
├── articles/               ← Bron-content (4+1 per artikel)
│   ├── hexa-book-001.md
│   ├── hexa-book-002.md    ← frequentie-basis (opgesplitst)
│   ├── hexa-book-005.md    ← Quran Basmala
│   ├── hexa-book-011.md    ← synth + fractaal (nieuw)
│   ├── hexa-book-012.md    ← routing + audit (nieuw)
│   └── hexa-book-018.md    ← Sanskrit-NPR bridge (nieuw)
│
├── audit/                  ← Audits (4-lagen: .md, .zig, .py, router)
│   ├── 01-artikel-01-dimensie-1.md
│   ├── 02-artikel-02-dimensie-2.md
│   ├── 02-artikel-02-dimensie-2.zig  ← Zig implementatie
│   └── 02-artikel-02-dimensie-2.py   ← MD↔Zig bridge
│
├── engine/                 ← Validatie scripts
│   ├── audit_status.py
│   ├── review_analyzer.py
│   ├── validate_freq_lenses.py
│   ├── nidra_router.py     ← nidrā graph + cross-ref validatie
│   └── sanskrit_npr_bridge.py
│
├── review/                 ← Review pipeline
│   ├── 00-inbox/
│   ├── 01-active/
│   └── 02-done/
│       ├── agni-02-artikel-02-dimensie-2.md
│       └── waarom-agni-02.md
│
├── tools/                  ← Hulpmiddelen
│   ├── audit-batcher.py    ← Batch audit runner
│   ├── zigtool/            ← Zig 0.13↔0.16 converter
│   └── zig-version.sh      ← Versie-manager (status/test/convert/clean)
│
├── ROUTING.md              ← Dit bestand
├── hexa-book-implementation-plan.md
└── hexa-book-patch.md
```

---

## 7. Koppelingen Naar Buiten

| Externe Map | Locatie |
|-------------|---------|
| 6-bit Zig Spike | `../spikes/002-6bit-routing-zig/` |
| Tokenfield | `../NPR-sandbox-tokenfield/` |
| NPR Sound Engine | `../skills/npr-sound-engine/` |
| Sanskrit Bridge | `../skills/sanskrit-frequency-bridge/` |
| Spike 020 | `../spikes/020-sanskrit-npr-bridge/` |

---

## 8. Direct vs. Delayed Routes

> **Direct = te snel. Delayed = juiste snelheid.**

| Type | Snelheid | Doel |
|------|----------|------|
| Direct | Onmiddellijk | Raw signal → taal |
| Delayed | 1 tick vertraging | Signal → matrika → taal |

In de tokenfield:
- Direct: byte → token (geen routing)
- Delayed: byte → token → slot → tick → root → output

---

## Status

- ✅ Articles → Audits: mapped
- ✅ Artikel 02 opgesplitst → 02 + 11 + 12 (4+1 nidrā)
- ✅ Audits → Spikes: 6-bit routing gekoppeld
- ✅ Spikes → Tokenfield: matrika/vortex/router mapped
- ✅ Engines: Python validatie scripts
- ✅ Agni-herschrijving artikel 02 → review/02-done/
- ✅ Audit-batcher 03–15 → 13 reviews in inbox
- ✅ Engine test: DR + freq validatie correct
- ✅ Spike bridge 002↔003: 6-bit↔tokenfield gedocumenteerd
- ⚠️ 24-bridge spike: in uitvoering (spike 021)
- ⚠️ Patanjali groot-klein spike: in uitvoering (spike 022)
- ✅ Agni rewrites op reviews 007–019: 14 files in review/02-done/
- ✅ Review pipeline: inbox → active → done
- ✅ 11→396 keten-validatie: toegevoegd aan engine + ROUTING.md
- ✅ NPR Sound Engine: synth-operator (artikel 011, 24/24 ✅)
- ✅ Sanskrit-NPR Bridge: engine + artikel 018 (24/24 ✅)
- ✅ zigtool: Zig 0.13↔0.16 converter in tools/
- ✅ zig-version.sh: versie-manager (status/test/convert/clean)
- ✅ nidra_router.py: cross-ref graph + validatie (17 artikels, 48 edges)
- ✅ audit bridge: MD↔Zig validatie per artikel (02 template)

---

*Laatst bijgewerkt: 2026-07-25 15:38 CET*
