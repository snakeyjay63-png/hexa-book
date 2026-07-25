---
taal: <Taal Naam>
chars: <aantal tekens>
bits: <bits per teken>
combinaties: <2^bits>
slack: <combinaties - chars>
base_freq: 432.0
---

# <Taal> — Charveld Alfabet

## Overzicht

- **Tekenruimte:** <chars> tekens
- **Bits per teken:** <bits>
- **Combinaties:** <combinaties>
- **Slack:** <slack> onbenut
- **IPv4 blok:** 4 letters = 32-bit
- **IPv6 blok:** 16 letters = 128-bit

## Tekentabel

| # | Teken | Bit | Binary | Byte | Hex | Freq (Hz) | Hexa4 | Klankveld |
|---|-------|-----|--------|------|-----|-----------|-------|-----------|
| 0 | `<char>` | 0 | `<binary>` | <byte> | <hex> | <freq> | <hexa4> | <klankveld> |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Voorbeeld

**Woord:** `<voorbeeld woord>`

- **Letters:** `<l1>`, `<l2>`, `<l3>`, `<l4>`
- **Bytes:** <b1>, <b2>, <b3>, <b4>
- **Hex:** `<binary string>`
- **IPv4:** <ipv4 address>
- **Hexa32:** <hex32>
- **Frequenties:** <f1>, <f2>, <f3>, <f4>

## Wiskunde

```
Bits per teken : <bits>
Chars          : <chars>
Combinaties    : <combinaties> = 2^<bits>
Slack          : <slack> = <combinaties> - <chars>
IPv4 blok      : 4 chars × 8-bit = 32-bit
IPv6 blok      : 16 chars × 8-bit = 128-bit
```
