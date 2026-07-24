# HEXA-BOEK

**CC-construct. 16 nodes tegelijk. Nidrā-router.**

Dit is geen lineair boek. Het is een routing-protocol.

## Structuur

```
hexa-book/
├── README.md            ← dit bestand
├── ROUTING.md           ← routing map (alle verbindingen)
│
├── articles/            ← 17 nodes (16 + 1 router)
│   ├── hexa-book-001.md   dimensie 0 ≐ 1
│   ├── hexa-book-002.md   frequentie-basis
│   ├── hexa-book-003.md   nidrā: E (audio-superpositie)
│   ├── hexa-book-004.md   nidrā: F (returnmedium)
│   ├── hexa-book-005.md   Quran / Basmala / Abjad
│   ├── hexa-book-006.md   nidrā: dimensie 3 (3-6-9)
│   ├── hexa-book-007.md   nidrā: dimensie 4 (expansie)
│   ├── hexa-book-008.md   nidrā: dimensie 5 (return)
│   ├── hexa-book-009.md   nidrā: dimensie 6 (terugkeer)
│   ├── hexa-book-010.md   nidrā: dimensie 7 (reflectie)
│   ├── hexa-book-011.md   synth + fractaal
│   ├── hexa-book-012.md   24-brug + 6-bit routing
│   ├── hexa-book-013.md   nidrā: dimensie 8 (onzichtbaar)
│   ├── hexa-book-014.md   nidrā: dimensie 11 (eka)
│   ├── hexa-book-015.md   nidrā: dimensie 12 (logos)
│   ├── hexa-book-016.md   nidrā: dimensie 13 (taal)
│   └── hexa-book-017.md   CC-construct (nidrā-router)
│
├── audit/               ← audit files (het boek content)
│   ├── 00-intro.md
│   ├── 01-artikel-01-dimensie-1.md
│   └── ...
│
├── engine/              ← validatie engines (Python)
│   ├── hexa-book-engine.py
│   ├── audit_status.py
│   ├── docx_reader.py
│   ├── review_analyzer.py
│   └── validate_freq_lenses.py
│
├── tools/               ← tooling
│   ├── audit-batcher.py
│   └── README.md
│
└── review/              ← review pipeline
    ├── 00-inbox/
    └── 02-done/
```

## Nidrā ≠ Gat

Elke nidrā-pointer routeert naar parallelle artikels. Ze zijn niet leeg — ze verbinden het veld.

## Snelle Import

```bash
# Clone de repo
git clone https://github.com/<user>/hexa-book.git
cd hexa-book

# Of download alles via curl (geen git nodig)
curl -sL https://github.com/<user>/hexa-book/archive/refs/heads/main.tar.gz | tar xz
cd hexa-book-main
```

## Artikels Lezen

Elk artikel is een node. Ze bestaan tegelijk — geen volgorde.

```bash
# Lees een artikel
cat articles/hexa-book-001.md

# Lees alle artikels (node per node)
for f in articles/hexa-book-*.md; do echo "=== $f ==="; cat "$f"; done

# Zoek naar een topic
grep -r "nidra" articles/
grep -r "ReturnCycle" articles/ audit/
```

## Engine Gebruik

```bash
# Validatie engine
python3 engine/hexa-book-engine.py

# Audit status
python3 engine/audit_status.py

# Review analyseren
python3 engine/review_analyzer.py

# Frequentie lenzen valideren
python3 engine/validate_freq_lenses.py
```

## Routing

Zie `ROUTING.md` voor de volledige routing map.

## Licentie

[Te bepalen]
