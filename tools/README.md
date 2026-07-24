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
