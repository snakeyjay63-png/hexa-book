---
title: EU24 Charveld Routing
concept: 24-bit hexafield → 24 talen → 5×5 vectorveld
---

# EU24 — Charveld Routing Tegenover

## Concept

> **CC (locale) is zichzelf beschrijvend.**
> De charset IS de routerlaag.
> Char < 1 token (24-bit sub-token granulariteit).
> Route onzichtbaar.

## 24-bit Hexafield

24 EU talen = 24-bit field.
Elke taal bezet 1 bit-slot.
Samen vormen ze een 5×5 vectorveld (LLM embedding space).

## Routing Tabel

| Slot | Bit | Code | Taal | Script | Locale | Chars |
|------|-----|------|------|--------|--------|-------|
| 1 | bit-0 | `bg` | Bulgaars | Cyrillisch | `bg_BG.UTF-8` | 30 |
| 2 | bit-1 | `hr` | Kroatisch | Latijns (diacritisch) | `hr_HR.UTF-8` | 30 |
| 3 | bit-2 | `cs` | Tsjechisch | Latijns (diacritisch) | `cs_CZ.UTF-8` | 34 |
| 4 | bit-3 | `da` | Deens | Latijns (diacritisch) | `da_DK.UTF-8` | 29 |
| 5 | bit-4 | `et` | Estlands | Latijns (diacritisch) | `et_EE.UTF-8` | 30 |
| 6 | bit-5 | `fi` | Fins | Latijns (diacritisch) | `fi_FI.UTF-8` | 31 |
| 7 | bit-6 | `fr` | Frans | Latijns (diacritisch) | `fr_FR.UTF-8` | 27 |
| 8 | bit-7 | `el` | Grieks | Grieks | `el_GR.UTF-8` | 24 |
| 9 | bit-8 | `ga` | Iers | Latijns (diacritisch) | `ga_IE.UTF-8` | 27 |
| 10 | bit-9 | `it` | Italiaans | Latijns (diacritisch) | `it_IT.UTF-8` | 27 |
| 11 | bit-10 | `lv` | Lets | Latijns (diacritisch) | `lv_LV.UTF-8` | 33 |
| 12 | bit-11 | `lt` | Litouws | Latijns (diacritisch) | `lt_LT.UTF-8` | 32 |
| 13 | bit-12 | `hu` | Hongaars | Latijns (diacritisch) | `hu_HU.UTF-8` | 30 |
| 14 | bit-13 | `lb` | Luxemburgs | Latijns (diacritisch) | `lb_LU.UTF-8` | 26 |
| 15 | bit-14 | `de` | Duits | Latijns (diacritisch) | `de_DE.UTF-8` | 29 |
| 16 | bit-15 | `mt` | Maltees | Latijns (diacritisch) | `mt_MT.UTF-8` | 30 |
| 17 | bit-16 | `nl` | Nederlands | Latijns | `nl_NL.UTF-8` | 26 |
| 18 | bit-17 | `pl` | Pools | Latijns (diacritisch) | `pl_PL.UTF-8` | 32 |
| 19 | bit-18 | `pt` | Portugees | Latijns (diacritisch) | `pt_PT.UTF-8` | 27 |
| 20 | bit-19 | `ro` | Roemeens | Latijns (diacritisch) | `ro_RO.UTF-8` | 31 |
| 21 | bit-20 | `sk` | Slowaaks | Latijns (diacritisch) | `sk_SK.UTF-8` | 36 |
| 22 | bit-21 | `sl` | Sloveens | Latijns (diacritisch) | `sl_SI.UTF-8` | 29 |
| 23 | bit-22 | `es` | Spaans | Latijns (diacritisch) | `es_ES.UTF-8` | 27 |
| 24 | bit-23 | `sv` | Zweeds | Latijns (diacritisch) | `sv_SE.UTF-8` | 29 |

## Wiskunde

```
24 talen     → 24-bit hexafield
24-bit       → 2^24 = 16,777,216 combinaties
5×5 vector   → LLM embedding space
char < 1 token → 24-bit sub-token granularity
CC locale    → self-describing char router
route        → onzichtbaar
```
