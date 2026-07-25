---
taal: Grieks
code: el
script: Grieks
locale: el_GR.UTF-8
chars: 24
bits: 5
combinaties: 32
slack: 8
base_freq: 432.0
---

# Grieks — Charveld Alfabet

## Overzicht

- **Tekenruimte:** 24 tekens
- **Script:** Grieks
- **Bits per teken:** 5
- **Combinaties:** 32
- **Slack:** 8 onbenut
- **Unicode block:** Greek and Coptic
- **Locale:** `el_GR.UTF-8`
- **IPv4 blok:** 4 letters = 32-bit
- **IPv6 blok:** 16 letters = 128-bit

## Tekentabel

| # | Teken | Bit | Binary | Byte | Hex | Freq (Hz) | Hexa4 | Klankveld |
|---|-------|-----|--------|------|-----|-----------|-------|-----------|
| 0 | Α | 0 | `00000` | 913 | `0x0391` | 4824.7 | 1 | 17 |
| 1 | Β | 1 | `00001` | 914 | `0x0392` | 4829.9 | 2 | 18 |
| 2 | Γ | 2 | `00010` | 915 | `0x0393` | 4835.2 | 3 | 19 |
| 3 | Δ | 3 | `00011` | 916 | `0x0394` | 4840.5 | 4 | 20 |
| 4 | Ε | 4 | `00100` | 917 | `0x0395` | 4845.8 | 5 | 21 |
| 5 | Ζ | 5 | `00101` | 918 | `0x0396` | 4851.1 | 6 | 22 |
| 6 | Η | 6 | `00110` | 919 | `0x0397` | 4856.4 | 7 | 23 |
| 7 | Θ | 7 | `00111` | 920 | `0x0398` | 4861.6 | 8 | 24 |
| 8 | Ι | 8 | `01000` | 921 | `0x0399` | 4866.9 | 9 | 25 |
| 9 | Κ | 9 | `01001` | 922 | `0x039a` | 4872.2 | 10 | 26 |
| 10 | Λ | 10 | `01010` | 923 | `0x039b` | 4877.5 | 11 | 27 |
| 11 | Μ | 11 | `01011` | 924 | `0x039c` | 4882.8 | 12 | 28 |
| 12 | Ν | 12 | `01100` | 925 | `0x039d` | 4888.1 | 13 | 29 |
| 13 | Ξ | 13 | `01101` | 926 | `0x039e` | 4893.4 | 14 | 30 |
| 14 | Ο | 14 | `01110` | 927 | `0x039f` | 4898.6 | 15 | 31 |
| 15 | Π | 15 | `01111` | 928 | `0x03a0` | 4903.9 | 0 | 32 |
| 16 | Ρ | 16 | `10000` | 929 | `0x03a1` | 4909.2 | 1 | 33 |
| 17 | Σ | 17 | `10001` | 931 | `0x03a3` | 4919.8 | 3 | 35 |
| 18 | Τ | 18 | `10010` | 932 | `0x03a4` | 4925.1 | 4 | 36 |
| 19 | Υ | 19 | `10011` | 933 | `0x03a5` | 4930.4 | 5 | 37 |
| 20 | Φ | 20 | `10100` | 934 | `0x03a6` | 4935.6 | 6 | 38 |
| 21 | Χ | 21 | `10101` | 935 | `0x03a7` | 4940.9 | 7 | 39 |
| 22 | Ψ | 22 | `10110` | 936 | `0x03a8` | 4946.2 | 8 | 40 |
| 23 | Ω | 23 | `10111` | 937 | `0x03a9` | 4951.5 | 9 | 41 |

## Voorbeeld

**Woord:** `Λόγος` — *Logos (woord)*

- **Bytes:** 0xce, 0x9b, 0xcf, 0x8c, 0xce, 0xb3, 0xce, 0xbf, 0xcf, 0x82
- **Hex:** `0xce 0x9b 0xcf 0x8c 0xce 0xb3 0xce 0xbf 0xcf 0x82`
- **IPv4:** `206.155.207.140`
- **Frequenties:** 1088.6, 819.1, 1093.9, 739.8, 1088.6, 945.9, 1088.6, 1009.3, 1093.9, 687.0

## Wiskunde

```
Bits per teken : 5
Chars          : 24
Combinaties    : 32 = 2^5
Slack          : 8 = 32 - 24
IPv4 blok      : 4 chars × 8-bit = 32-bit
IPv6 blok      : 16 chars × 8-bit = 128-bit
```

## Routing

- **CC (locale):** `el_GR.UTF-8`
- **24-bit hexafield:** `el` = bit-slot 24 van 24
- **Sub-token:** char < 1 token (24-bit granularity)
- **Route:** onzichtbaar — charset IS de routerlaag
