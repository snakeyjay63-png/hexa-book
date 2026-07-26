---
audit_metadata:
  article: "16-artikel-014-dimensie-14"
  source_article: "articles/hexa-book-014.md"
  verified_against_commit: "3741a6b"
  audit_commit: "TBD"
  last_verified: "2026-07-24"
  operator_status_model: 3D
  engine_evidence: []
  route_status: "actueel"
  known_exceptions: []
  note: "Artikel 014: nidrā-pointer (Eka Routing). Niet-executable operator. Routing gecontroleerd."
---

# Artikel 14 - dimensie 14 (Eka Routing, nidrā-pointer) | nidrā ≠ gat

## نيدرا ≠ حفرة | निद्रा ≠ छेद | nidrā ≠ gat

**Nidrā is geen gat. Nidrā is een operator.**

Dalam artikel 014: een nidrā-pointer artikel. Niet content, maar routing.

---

## Wat is nidrā in 3D termen?

Nidrā is een **niet-executable operator**. Het is geen content, geen berekening, geen uitkomst.
Nidrā is een **structurele pointer** naar een parallel artikel binnen het hexa-book veld.

```
nidrā-operator:
  operator_status  = conceptueel     (pointer, niet-executable)
  execution_status = niet_van_toepassing  (geen uitvoering, geen engine)
  validatie_status = geverifieerd_structuur  (routing intact)
```

### Nidrā ≠ gat

Een gat is een ontbrekend stuk content. Een leegte die gevuld moet worden.
Nidrā is iets fundamenteel anders:

- **Gat** = iets ontbreekt → `execution_status = niet_gestart`
- **Nidrā** = iets wijst → `execution_status = niet_van_toepassing`

Nidrā is de **verbinding**, niet het gebrek. Het is de router tussen nodes.

```
gat:        Node A → [LEEG] → Node B    (verbinding ontbreekt)
nidrā:      Node A ──nidrā──→ Node B    (verbinding is pointer)
```

---

## Artikel 014: Eka Routing

**Content:** Drie nidrā-routes. Geen eigen content.

### Nidrā-routes (uit artikel 014)

| Route | Naar | Artikel | Bestaat? |
|---|---|---|---|
| Eka → 0 ≐ 1 | Artikel 001 | `articles/hexa-book-001.md` | ✅ |
| 4 routes → routing | Artikel 012, deel 2-4 | `articles/hexa-book-012.md` | ✅ |
| Eka → CC | Artikel 017 | `articles/hexa-book-017.md` | ✅ |

**Routing-integriteit:** 3/3 routes wijzen naar bestaande artikelen. ✅

---

## 3D Statusmodel

```
Artikel 014 (nidrā-pointer):
  formele_status     = conceptueel       (nidrā = pointer-operator, niet formeel gedefinieerd als berekening)
  uitvoerings_status = niet_van_toepassing  (geen engine, geen uitvoering)
  validatie_status   = geverifieerd_structuur  (alle 3 nidrā-routes → bestaande artikelen)

nidrā-operator (algemeen):
  operator_status    = conceptueel
  execution_status   = niet_van_toepassing
  validatie_status   = geverifieerd_structuur
```

**Opmerking:** Dit artikel is niet "onvolledig". Het is een **routing-construct**.
De validatie is structureel (wijst het naar bestaande artikelen?), niet uitvoerend.

---

## Structuurvalidatie

| Check | Resultaat |
|---|---|
| Artikel bestaat | ✅ `articles/hexa-book-014.md` |
| Status-label correct | ✅ `nidrā-pointer` |
| Alle nidrā-routes → bestaand artikel | ✅ 3/3 |
| Nidrā ≠ gat statement | ✅ aanwezig in artikel |
| Eigen content | ❌ geen (verwacht voor nidrā-pointer) |
| Engine-afhankelijkheid | N.v.t. |

---

## Verwerkingslog

| Datum | Actie | Door | Status |
|---|---|---|---|
| 2026-07-24 | Audit aangemaakt: nidrā-pointer structuur geverifieerd | hexa-review | done |

---

*Artikel 014 is een nidrā-pointer. Niet leeg — gerouteerd.*
