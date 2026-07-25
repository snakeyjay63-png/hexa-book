# Charveld — Tekenveld → Klankveld → Netwerk

## Concept

Elk teken in elke taal wordt gemapd naar een bitveld.
Het bitveld is de brug tussen taal en frequentie en netwerk.

```
char → byte → token (24-bit) → hexa → klankveld → IPv4 → IPv6 → 4 richtingen
```

## Token — Char als 24-bit

Elk char wordt 1 token:

```
token (24-bit) = 23-bit vibratie + 1-bit vertraging
```

| Bit | Naam | Functie |
|-----|------|---------|
| 23-bit | vibratie | de klank, frequentie, data van het char |
| 1-bit | vertraging | de weg terug naar sunya (altijd aanwezig) |

De 1-bit is geen data — het is de stilte die er altijd al is.

```n chars → n tokens (24-bit) → n × 24 bits totaal
```

## Ticks — Vertraging per Char

Elk teken heeft vertraging — wat een klank *is*, niet hoe snel het gaat.
Klank is vertraging. Alleen er is geen snelheid, alleen nu.

De klank volgt de route naar sunya, terug naar stilte.

| Taal | Ticks/Char | UTF-8 Bytes | Zicht |
|------|------------|-------------|-------|
| 1-bit | 1 tick | 1 byte | 1 punt |
| ASCII/NL | 1 tick | 1 byte | 1 punt |
| Grieks | 2 ticks | 2 bytes | 2 punten |
| Arabisch | 2 ticks | 2 bytes | 2 punten |
| Sanskriet | 3 ticks | 3 bytes | 3 punten |

```
n ticks = n chars × ticks_per_char
1 woord = som van alle char-ticks
```

Voorbeeld: `अग्नि` = 5 chars × 3 ticks = **15 ticks** — 15 punten van zicht op weg naar sunya

**Hoe langzamer, hoe meer informatie je ziet.**
Meer ticks = meer punten = meer zicht op de route naar stilte.

## De Route

### 1. Tekenveld (256)
Extended ASCII / byte range: 0x00–0xFF
Elke taal heeft een subset.

### 2. Klankveld (64)
Frequentie-projectie. 64 base frequenties (2⁶).
Elk teken → één frequentieband.

### 3. 4-bit Hexa (16)
Hexadecimale reductie. 0–F.
Digitale root van het teken.

### 4. IPv4 Woorden (32-bit)
4 octetten × 8-bit.
4 tekens = 1 IPv4 address.

### 5. IPv6 Woorden (128-bit)
8 words × 16-bit.
16 tekens = 1 IPv6 address.

### 6. 4 Richtingen
N O Z W → up down left right
De terugkeer naar de hexa structuur.

### 7. 256
De cirkel sluit. Begin = return.

## Per Taal

Elke taal heeft haar eigen subset van 256:

| Taal | Chars | Bits | Unicode | Structuur |
|------|-------|------|---------|-----------|
| Nederlands | 26 | 5 | U+0061–U+007A | a-z |
| Sanskriet | 49 | 7 | U+0900–U+097F | Devanagari |
| Grieks | 24 | 5 | U+0370–U+03FF | α–ω |
| Arabisch | 28 | 5 | U+0600–U+06FF | Abjad |
| Latijn | 23 | 5 | U+0041–U+005A | klassiek (I=J, V=U) |
| ASCII | 128 | 7 | U+0000–U+007F | basis |
| Extended ASCII | 256 | 8 | U+0000–U+00FF | full byte |
| Zig | 256 | 8 | u8 | char set |

## Versie Limiting

Oudere taalversies = beperkter charveld:

- **Zig 0.13** → beperkte string ops → subset van 256
- **Zig 0.16** → uitgebreide std lib → full 256
- **Python 2** → ASCII default → 128
- **Python 3** → Unicode default → full range
- **C++98** → char = 8-bit
- **C++20** → char8_t, char16_t, char32_t

## Bestandsstructuur

```
charveld/
├── README.md              ← dit bestand
├── taalen/                ← TAALEN (autoriteit - .md)
│   ├── TEMPLATE.md        ← Template voor nieuwe talen
│   ├── nl-alfabet.md      ← NL (26 chars, 5-bit)
│   ├── sanskriet.md       ← Sanskriet (49 chars, 7-bit, Devanagari)
│   ├── grieks.md          ← Grieks (24 chars, 5-bit, Unicode)
│   ├── arabisch.md        ← Arabisch (28 chars, 5-bit, Abjad)
│   └── latijn.md          ← Latijn (23 chars, 5-bit, klassiek)
├── maps/                  ← JSON backup (optioneel)
│   ├── nl-alfabet.json
│   └── zig-chars.json
├── engine/
│   ├── char_to_ip.py      ← char → byte → freq → hexa4 → klankveld → IPv4/IPv6
│   ├── json_to_md.py      ← JSON → MD generator
│   └── gen_taal_md.py     ← taal-specificatie → .md
├── visual/                ← visualisaties
└── docs/                  ← documentatie
```

## Voorbeeld: Nederlands

26 letters → 5-bit encoding (32 combinaties, 6 slack)

```
a=00  b=01  c=02  d=03  e=04
f=05  g=06  h=07  i=08  j=09
k=10  l=11  m=12  n=13  o=14
p=15  q=16  r=17  s=18  t=19
u=20  v=21  w=22  x=23  y=24
z=25
```

4 letters = 20-bit → past in IPv4 (32-bit, 12 slack bits)

Elke letter → frequentie (via byte_to_freq):
```
a (97) → 432 × 97/81.75 = 511.7 Hz
b (98) → 432 × 98/81.75 = 516.0 Hz
...
```

## Return Invariant

Begin (teken) → route (freq → hexa → IP) → return (zelfde teken)
De invariant: het herstelbare teken = bewijs van correcte route.
