# Review Template — Hexa-Boek

---
id: NNN
date: YYYY-MM-DD
target: hexa-book-NNN.md
status: inbox | active | done | discard
severity: low | medium | high | critical
reviewer: [naam/bron]
points: N
summary: "[korte samenvatting — max 120 tekens]"
---

## Overzicht

[Eén paragraaf: kernprobleem + impact op het boek.]

---

## Punten

### P001: [Korte titel — max 60 tekens]
**Type:** operator | route | status | consistentie | berekening | concept
**Locatie:** regel ~NNN of sectie "Sectienaam"
**Zeerheid:** low | medium | high
**Routestatus:** gesloten | half | open | extern

**Huidige situatie:**
```
[wat er nu staat — citeer kort]
```

**Probleem:**
[Waarom dit een halve route/fout is — max 3 zinnen]

**Oplossing:**
```
[exacte fix — code/blok die toegevoegd/wijzigd moet worden]
```

**Impact op bedrock:**
- [ ] Formele operator
- [ ] Lens-projectie
- [ ] Status-notatie
- [ ] Vṛtti-classificatie
- [ ] Drie frequentiesystemen
- [ ] Afrondingsgevoeligheid

---

### P002: [Korte titel]
**Type:** operator | route | status | consistentie | berekening | concept
**Locatie:** regel ~NNN of sectie "Sectienaam"
**Zeerheid:** low | medium | high
**Routestatus:** gesloten | half | open | extern

**Huidige situatie:**
```
[wat er nu staat]
```

**Probleem:**
[Waarom dit een halve route/fout is]

**Oplossing:**
```
[exacte fix]
```

**Impact op bedrock:**
- [ ] Formele operator
- [ ] Lens-projectie
- [ ] Status-notatie
- [ ] Vṛtti-classificatie
- [ ] Drie frequentiesystemen
- [ ] Afrondingsgevoeligheid

---

## Routekaart

### Volledig gesloten ✅
```
Route → stap → stap → ⊣
```

### Half ⚠
```
Route → stap → ? → (operator ontbreekt)
```

### Open 🔓
```
Route → ? → (nog niet gedefinieerd)
```

### Extern ↝
```
Route → ↝ externe_verwijzing
```

## Eindoordeel

**Totaal punten:** N
**Gesloten:** G
**Half:** H
**Open:** O
**Extern:** E
**Prioriteit:** [wat eerst fixen]

---

## Verwerkingslog

| Datum | Actie | Door | Status |
|-------|-------|------|--------|
| YYYY-MM-DD | [actie] | [door] | inbox → active |
| YYYY-MM-DD | [actie] | [door] | active → done/discard |
