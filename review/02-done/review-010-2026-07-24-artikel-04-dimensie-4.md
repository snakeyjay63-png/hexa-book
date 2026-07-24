# Review 010 — Artikel 4: Dimensie 4 (expansie, Mandelbrot)

**Datum:** 2026-07-24
**Audit-bron:** `audit/06-artikel-04-dimensie-4.md`
**Reviewer:** audit-batcher (batch 03-15)
**Status:** 🟡 ONBEHANDELD
**Route:** intake → audit → 00-inbox

---

## Audit-bron

Artikel 4 koppelt de Mandelbrot-set aan het HEXA-systeem via c=0 als bronpunt. Introduceert ρ_Mandelbrot-lens als NPR-projectie en verbindt Mandelbrot-0 met Null Island, 0.0.0.0, en ongedifferentieerd bronveld.

## Bevindingen

**Primaire operatoren:**
- `z_{n+1} = z_n² + c` — Mandelbrot-iteratie, `z_0 = 0`
- `M = {c ∈ ℂ : (z_n) blijft begrensd}` — formele Mandelbrot-definitie
- `ρ_Mandelbrot-lens(c) = leegte indien c ∉ M` — NPR-projectie
- `ρ_Mandelbrot-role(0_C) = bronpunt` — NPR-roltoewijzing
- `ρ_NPR-source(0) = ongedifferentieerd bronveld` — abstracte brontoestand
- Abjad-route: x → A_value(x) → DR(A_value(x))

**Structuur:**
- c=0 is wiskundig triviaal: z_n=0 voor alle n (absolute stabiliteit)
- Drie representaties van 0: HEXA (0.0.0.0), cartografisch (0°,0°), NPR (ongedifferentieerd)
- Lensaxioma: 0≐_lens 1 — de route sluit bij dezelfde bron
- Expansie vermenigvuldigt lenzen (Lensoptiek 4)

**Cross-referenties:**
- Artikel F (returnmedium) — 0.0.0.0 als returnpunt
- Artikel 3 (3-6-9) — Abjad-route door NPR-lens
- Artikel 10 (6-bit routing) — expansie → veld

## Validatiestatus

| Operator | Gedefinieerd | Uitgevoerd | Gevalideerd |
|----------|-------------|------------|-------------|
| Mandelbrot-definitie | ✅ formeel | ✅ wiskundig | ✅ standaard |
| ρ_Mandelbrot-lens | ⚠ interpretatief | ❌ nee | ❌ ongetest |
| ρ_Mandelbrot-role(0) | ⚠ interpretatief | ❌ nee | ❌ ongetest |
| ρ_NPR-source(0) | ⚠ interpretatief | ❌ nee | ❌ ongetest |
| 0≐_lens 1 | ✅ formeel | ⚠ deels | ❌ ongetest |

**Overkoepelend:** Mandelbrot is wiskundig correct. Alle NPR-projecties zijn interpretatief.

## Ontbrekende Elementen

1. **Mandelbrot→NPR mapping** — ρ_Mandelbrot-lens is niet operationeel
2. **Expansie-operator** — "vermenigvuldigt lenzen" is metafoor zonder formele operator
3. **Sonificatie** — Lensoptiek 4 vermeldt concrete sonificatie-operator als toekomstig
4. **Onafhankelijke reproductie** — NPR-projecties niet door derden verifieerd

## Routing Implicaties

- **vṛtti(Mandelbrot)** = `pramāṇa` — wiskundige standaard
- **vṛtti(ρ_Mandelbrot-lens)** = `vikalpa` — interpretatieve constructie
- **guṇa(Mandelbrot)** = `sattva` — helder, standaard
- **guṇa(ρ_Mandelbrot-lens)** = `rajas` — constructief
- **HEXA-route:** Expansie-laag, poort van 0 naar veld

## Classificatie

- **vṛtti(Artikel 4)** = `vikalpa` (wiskunde is pramāṇa, NPR-koppeling is vikalpa)
- **guṇa(Artikel 4)** = `rajas`

---

*Review gegenereerd via audit-batcher batch 03-15*
