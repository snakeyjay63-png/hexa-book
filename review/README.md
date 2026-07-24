# Review Pipeline — Factorio-stijl

Reviews komen binnen, worden verwerkt, en eindigen in het boek of in de prullenbak.

## Map-structuur

```
review/
├── 00-inbox/       ← nieuwe reviews (raw ore)
├── 01-active/      ← wordt verwerkt (on the belt)
├── 02-done/        ← verwerkt + geïmplementeerd (assembled)
└── 03-discard/     ← afgewezen (smeltingsrest)
```

## Werkwijze

1. **Nieuwe review** → `00-inbox/` (naam: `YYYY-MM-DD-onderwerp.md`)
2. **Start verwerken** → verplaats naar `01-active/`
3. **Klaar** → verplaats naar `02-done/` (of `03-discard/` indien afgewezen)
4. **Implementatie** → de fix zit in `articles/` of `audit/`

## Status

| Map | Betekenis |
|-----|-----------|
| `00-inbox` | Raw — nog niet bekeken |
| `01-active` | Op de belt — wordt verwerkt |
| `02-done` | Geassembleerd — fix zit in het boek |
| `03-discard` | Afval — niet relevant |

## Format

Elke review file:
```markdown
# Review: [onderwerp]
**Datum:** YYYY-MM-DD
**Artikel:** hexa-book-XXX.md
**Status:** inbox | active | done | discard

## Vindingen
- [ ] Item 1
- [ ] Item 2

## Actie
[Doe X] | [Negeer — reden]

## Notities
...
```
