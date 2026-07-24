# Spike 019: Patanjali Router (Veld)

**Doel:** Patanjali router als FIELD modelleren — niet lineair. Alles bestaat tegelijk; de keten is de route door het veld.

## Bouwen & Draaien

```bash
zig build-exe -O ReleaseSmall src/main.zig
./main
```

## Tests

```bash
zig test src/digital_root.zig
zig test src/veld.zig
zig test src/flower_of_life.zig
```

## Resultaat

```
=== Patanjali-veld ===
Entry: 11 (DR=2)
Trilling: 11²↔13² (4↔7)
Stilte: 17²=19² (1=1)
Beide naar entry (DR=2): true

=== Richting (vanaf 1) ===
  ×2 (vooruit)  → DR(2)
  /2 (achteruit) → DR(5)

=== 11→396 Keten ===
   11 (start) → DR=2
   44 (×4) → DR=8
   66 (×1.5) → DR=3
  264 (×4) → DR=3
  396 (×1.5) → DR=9

DR cyclus: 2 → 8 → 3 → 3 → 9

=== Flower of Life ===
Cirkels: 19 (DR=1)
Oogjes: 90 (DR=9)
Sattva: 24, Tamas: 24, Rajas: 42

=== Veld compleet ===
```

## Structuur

| Bestand | Rol |
|---------|-----|
| `src/digital_root.zig` | DR veld (mod 9, /2=×5) |
| `src/veld.zig` | Patanjali-veld (11/13, 17/19, richting) |
| `src/flower_of_life.zig` | 19 cirkels, 90 oogjes, 3 gunas |
| `src/main.zig` | Validatie + keten |

## Concepten

- **2 en 5** zijn RICHTINGEN (×2 en /2) vanaf 1 — geen losse getallen
- **11/13** = trilling (DR: 4↔7, spiegel)
- **17/19** = stilte (DR: 1=1, samenvallen)
- **Rajas** = RAND/OVERGANG (18), niet buiten
- **Veld ≠ keten**: structuur is simultaan, keten is route erdoorheen

## Verdict

✅ **Geslaagd.** Veld gemodelleerd in Zig. Alle relaties bestaan tegelijk. Keten is de route, niet de structuur.
