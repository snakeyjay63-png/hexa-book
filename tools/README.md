# Hexa-Book Tools

## audit-batcher.py — Audit Pipeline Toestandsmachine

Audit punten → batches → coordinators → edits → merge → verifiëren.

### Gebruik

```bash
cd hexa-book

# Pipeline initialiseren
python3 tools/audit-batcher.py reset
python3 tools/audit-batcher.py role orchestrator review.md article.md

# Coördinators (parallel spawnen)
python3 tools/audit-batcher.py role coordinator B01
python3 tools/audit-batcher.py role coordinator B02
# ... etc

# Status & validatie
python3 tools/audit-batcher.py status
python3 tools/audit-batcher.py validate orchestrator
python3 tools/audit-batcher.py validate coordinator
python3 tools/audit-batcher.py validate
```

### Pipeline

```
audit.md
  │
  ├─ orchestrator (diepte 0): parseer → batches → manifest
  │   └─ 19 punten → 7 batches (max 3 per batch, non-overlapping)
  │
  ├─ coordinator[B01] (diepte 1): batch lezen → edits toepassen
  ├─ coordinator[B02] (diepte 1): batch lezen → edits toepassen
  ├─ ...
  └─ coordinator[B07] (diepte 1): batch lezen → edits toepassen
  │
  └─ validate: alle batches gecheckt
```

### Viveka — Positieherkenning

Elke agent gebruikt dezelfde tool. Tool herkent rol → vertelt wat er moet gebeuren.

```bash
python3 tools/audit-batcher.py role orchestrator review.md article.md
# → "Ik zie het hele beeld. Ik splijt in batches."

python3 tools/audit-batcher.py role coordinator B01
# → "Ik zie mijn batch. Ik maak de edits."
```

### Factoren

- **2-lagen max:** subagent limiet is diepte 1
- **Non-overlapping:** batches delen geen regelbereiken → parallel veilig
- **Max 3 per batch:** coordinator context blijft beheersbaar
- **Toestand in manifest:** elke rol updateert zichzelf → elke rol kan valideren

## zig-version.sh — Zig Versie-Manager

Wrapper rond zigtool. Automatiseert de hele Zig-lifecycle voor hexa-book.

### Gebruik

```bash
cd hexa-book

# Status: welke audits, welke Zig versie
bash tools/zig-version.sh status

# Test alle audits
bash tools/zig-version.sh test

# Converteer alle audits (bijv. Zig 0.13 → 0.16)
bash tools/zig-version.sh convert 0.13 0.16

# Clean binaries
bash tools/zig-version.sh clean
```

### Workflow bij nieuwe Zig versie

```
1. bash tools/zig-version.sh status           # check huidige staat
2. bash tools/zig-version.sh convert 0.13 0.16  # converteer
3. handmatig fixen                             # deep changes
4. bash tools/zig-version.sh test             # validate
5. bash tools/zig-version.sh clean            # opruimen
```

## zigtool — Zig Versie-Converter

Automatiseert Zig 0.13 ↔ 0.16 migratie (oppervlakkige API-veranderingen).

### Gebruik

```bash
cd hexa-book

# 0.13 → 0.16
node tools/zigtool/convert.js --from 0.13 --to 0.16 audit/artikel.zig

# 0.16 → 0.13
node tools/zigtool/convert.js --from 0.16 --to 0.13 audit/artikel.zig -o old.zig

# Van stdin
cat audit/artikel.zig | node tools/zigtool/convert.js --from 0.13 --to 0.16 -
```

### Wat het doet

| Verandering | 0.13 | 0.16 |
|-------------|------|------|
| main() | `pub fn main() void` | `pub fn main() !void` |
| I/O | `std.os.linux.write/read` | `std.posix.write/read` |
| StdIo | `.Inherit`, `.Ignore` | `.inherit`, `.ignore` |
| Sleep | `.{ .ms = 10 }` | `10 * std.time.ns_per_ms` |
| ArrayList | `.deinit()` | `.deinit(gpa)` |

### Wat het NIET doet

Diepere veranderingen (`Child.init` → `spawn`, `std.Io` abstractie, `build.zig`) zijn handmatig werk.

### Workflow

```
1. converter draaien    → oppervlakkige fixes
2. handmatig fixen      → spawn, Io, build.zig
3. compileren           → fouten oplossen
4. testen              → werkend!
```

### Batch overzicht (review-001)

| Batch | Punten | Regels |
|-------|--------|--------|
| B01 | P001, P002, P003 | 21-102 |
| B02 | P004, P005, P006 | 103-184 |
| B03 | P007, P008, P009 | 185-248 |
| B04 | P010, P011, P012 | 249-297 |
| B05 | P013, P014, P015 | 298-340 |
| B06 | P016, P017, P018 | 341-390 |
| B07 | P019 | 391+ |
