#!/usr/bin/env python3
"""
gen_eu24.py — Genereer taal-maps voor alle 24 EU officiële talen.

Concept:
  24 talen → 24-bit hexafield → 5×5 vectorveld (LLM embedding space)
  CC (locale/charset) = self-describing char router
  Char < 1 token (24-bit sub-token granularity)
  Route onzichtbaar — de charset IS de routinglaag

Output:
  - charveld/maps/<taal-code>.json  (per taal)
  - charveld/taalen/<taal-code>.md  (per taal)
  - charveld/maps/eu24-routing.json (master routing table)
  - charveld/taalen/eu24-overview.md (overview)
"""

import json
import math
import os
import sys

# ─── Constants ───
BASE_FREQ = 432.0
REF = 81.75

# 24 EU officiële talen + scripts
EU24 = {
    "bulgaars": {
        "code": "bg",
        "taal": "Bulgaars",
        "script": "Cyrillisch",
        "unicode_block": "Cyrillic",
        "locale": "bg_BG.UTF-8",
        "direction": "ltr",
        "chars": 30,
        "bits": 5,
        "combinaties": 32,
        "slack": 2,
        "voorbeeld": {"woord": "български", "naam": "Bulgaars"},
    },
    "kroatisch": {
        "code": "hr",
        "taal": "Kroatisch",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "hr_HR.UTF-8",
        "direction": "ltr",
        "chars": 30,
        "bits": 5,
        "combinaties": 32,
        "slack": 2,
        "voorbeeld": {"woord": "hrvatski", "naam": "Kroatisch"},
    },
    "tsjechisch": {
        "code": "cs",
        "taal": "Tsjechisch",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "cs_CZ.UTF-8",
        "direction": "ltr",
        "chars": 34,
        "bits": 6,
        "combinaties": 64,
        "slack": 30,
        "voorbeeld": {"woord": "čeština", "naam": "Tsjechisch"},
    },
    "deens": {
        "code": "da",
        "taal": "Deens",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended Additional",
        "locale": "da_DK.UTF-8",
        "direction": "ltr",
        "chars": 29,
        "bits": 5,
        "combinaties": 32,
        "slack": 3,
        "voorbeeld": {"woord": "dansk", "naam": "Deens"},
    },
    "estlands": {
        "code": "et",
        "taal": "Estlands",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended Additional",
        "locale": "et_EE.UTF-8",
        "direction": "ltr",
        "chars": 30,
        "bits": 5,
        "combinaties": 32,
        "slack": 2,
        "voorbeeld": {"woord": "eesti", "naam": "Estisch"},
    },
    "finse": {
        "code": "fi",
        "taal": "Fins",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "fi_FI.UTF-8",
        "direction": "ltr",
        "chars": 31,
        "bits": 5,
        "combinaties": 32,
        "slack": 1,
        "voorbeeld": {"woord": "suomi", "naam": "Fins"},
    },
    "franse": {
        "code": "fr",
        "taal": "Frans",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "fr_FR.UTF-8",
        "direction": "ltr",
        "chars": 27,
        "bits": 5,
        "combinaties": 32,
        "slack": 5,
        "voorbeeld": {"woord": "français", "naam": "Frans"},
    },
    "griekse": {
        "code": "el",
        "taal": "Grieks",
        "script": "Grieks",
        "unicode_block": "Greek and Coptic",
        "locale": "el_GR.UTF-8",
        "direction": "ltr",
        "chars": 24,
        "bits": 5,
        "combinaties": 32,
        "slack": 8,
        "voorbeeld": {"woord": "Λόγος", "naam": "Logos (woord)"},
    },
    "irlandse": {
        "code": "ga",
        "taal": "Iers",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "ga_IE.UTF-8",
        "direction": "ltr",
        "chars": 27,
        "bits": 5,
        "combinaties": 32,
        "slack": 5,
        "voorbeeld": {"woord": "Gaeilge", "naam": "Iers"},
    },
    "italianse": {
        "code": "it",
        "taal": "Italiaans",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "it_IT.UTF-8",
        "direction": "ltr",
        "chars": 27,
        "bits": 5,
        "combinaties": 32,
        "slack": 5,
        "voorbeeld": {"woord": "italiano", "naam": "Italiaans"},
    },
    "lettische": {
        "code": "lv",
        "taal": "Lets",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended Additional",
        "locale": "lv_LV.UTF-8",
        "direction": "ltr",
        "chars": 33,
        "bits": 6,
        "combinaties": 64,
        "slack": 31,
        "voorbeeld": {"woord": "latviski", "naam": "Lets"},
    },
    "litouwse": {
        "code": "lt",
        "taal": "Litouws",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended Additional",
        "locale": "lt_LT.UTF-8",
        "direction": "ltr",
        "chars": 32,
        "bits": 6,
        "combinaties": 64,
        "slack": 32,
        "voorbeeld": {"woord": "lietuvių", "naam": "Litouws"},
    },
    "hongaarse": {
        "code": "hu",
        "taal": "Hongaars",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "hu_HU.UTF-8",
        "direction": "ltr",
        "chars": 30,
        "bits": 5,
        "combinaties": 32,
        "slack": 2,
        "voorbeeld": {"woord": "magyar", "naam": "Hongaars"},
    },
    "luxemburgse": {
        "code": "lb",
        "taal": "Luxemburgs",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "lb_LU.UTF-8",
        "direction": "ltr",
        "chars": 26,
        "bits": 5,
        "combinaties": 32,
        "slack": 6,
        "voorbeeld": {"woord": "Lëtzebuergesch", "naam": "Luxemburgs"},
    },
    "duitse": {
        "code": "de",
        "taal": "Duits",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "de_DE.UTF-8",
        "direction": "ltr",
        "chars": 29,
        "bits": 5,
        "combinaties": 32,
        "slack": 3,
        "voorbeeld": {"woord": "Deutsch", "naam": "Duits"},
    },
    "maltese": {
        "code": "mt",
        "taal": "Maltees",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended Additional",
        "locale": "mt_MT.UTF-8",
        "direction": "ltr",
        "chars": 30,
        "bits": 5,
        "combinaties": 32,
        "slack": 2,
        "voorbeeld": {"woord": "Malti", "naam": "Maltees"},
    },
    "nederlandse": {
        "code": "nl",
        "taal": "Nederlands",
        "script": "Latijns",
        "unicode_block": "Basic Latin",
        "locale": "nl_NL.UTF-8",
        "direction": "ltr",
        "chars": 26,
        "bits": 5,
        "combinaties": 32,
        "slack": 6,
        "voorbeeld": {"woord": "hexa", "naam": "hexa"},
    },
    "poolse": {
        "code": "pl",
        "taal": "Pools",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "pl_PL.UTF-8",
        "direction": "ltr",
        "chars": 32,
        "bits": 6,
        "combinaties": 64,
        "slack": 32,
        "voorbeeld": {"woord": "polski", "naam": "Pools"},
    },
    "portugese": {
        "code": "pt",
        "taal": "Portugees",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "pt_PT.UTF-8",
        "direction": "ltr",
        "chars": 27,
        "bits": 5,
        "combinaties": 32,
        "slack": 5,
        "voorbeeld": {"woord": "português", "naam": "Portugees"},
    },
    "roemeense": {
        "code": "ro",
        "taal": "Roemeens",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "ro_RO.UTF-8",
        "direction": "ltr",
        "chars": 31,
        "bits": 5,
        "combinaties": 32,
        "slack": 1,
        "voorbeeld": {"woord": "română", "naam": "Roemeens"},
    },
    "slovakische": {
        "code": "sk",
        "taal": "Slowaaks",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "sk_SK.UTF-8",
        "direction": "ltr",
        "chars": 36,
        "bits": 6,
        "combinaties": 64,
        "slack": 28,
        "voorbeeld": {"woord": "slovenčina", "naam": "Slowaaks"},
    },
    "sloveense": {
        "code": "sl",
        "taal": "Sloveens",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "sl_SI.UTF-8",
        "direction": "ltr",
        "chars": 29,
        "bits": 5,
        "combinaties": 32,
        "slack": 3,
        "voorbeeld": {"woord": "slovenščina", "naam": "Sloveens"},
    },
    "spaanse": {
        "code": "es",
        "taal": "Spaans",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended-A",
        "locale": "es_ES.UTF-8",
        "direction": "ltr",
        "chars": 27,
        "bits": 5,
        "combinaties": 32,
        "slack": 5,
        "voorbeeld": {"woord": "español", "naam": "Spaans"},
    },
    "zweedse": {
        "code": "sv",
        "taal": "Zweeds",
        "script": "Latijns (diacritisch)",
        "unicode_block": "Latin Extended Additional",
        "locale": "sv_SE.UTF-8",
        "direction": "ltr",
        "chars": 29,
        "bits": 5,
        "combinaties": 32,
        "slack": 3,
        "voorbeeld": {"woord": "svenska", "naam": "Zweeds"},
    },
}

# Deduplicate mt (dubbel toegevoegd, maltees is uniek)
EU24_DEDUP = {}
for k, v in EU24.items():
    if v["code"] not in EU24_DEDUP:
        EU24_DEDUP[k] = v
EU24 = EU24_DEDUP


# ─── Alfabet-definities per script-type ───

# Latijns basis + meest voorkomende diacritische extensies
LATIJN_BASE = [
    ("A", 0x0041, 0x0061), ("B", 0x0042, 0x0062),
    ("C", 0x0043, 0x0063), ("D", 0x0044, 0x0064),
    ("E", 0x0045, 0x0065), ("F", 0x0046, 0x0066),
    ("G", 0x0047, 0x0067), ("H", 0x0048, 0x0068),
    ("I", 0x0049, 0x0069), ("J", 0x004A, 0x006A),
    ("K", 0x004B, 0x006B), ("L", 0x004C, 0x006C),
    ("M", 0x004D, 0x006D), ("N", 0x004E, 0x006E),
    ("O", 0x004F, 0x006F), ("P", 0x0050, 0x0070),
    ("Q", 0x0051, 0x0071), ("R", 0x0052, 0x0072),
    ("S", 0x0053, 0x0073), ("T", 0x0054, 0x0074),
    ("U", 0x0055, 0x0075), ("V", 0x0056, 0x0076),
    ("W", 0x0057, 0x0077), ("X", 0x0058, 0x0078),
    ("Y", 0x0059, 0x0079), ("Z", 0x005A, 0x007A),
]

# Extra diacritische tekens per taal
LATIJN_EXTRA = {
    "da": [
        ("Æ", 0x00C6, 0x00E6), ("Ø", 0x00D8, 0x00F8), ("Å", 0x00C5, 0x00E5),
    ],
    "fi": [
        ("Ä", 0x00C4, 0x00E4), ("Ö", 0x00D6, 0x00F6), ("Å", 0x00C5, 0x00E5),
        ("Š", 0x0160, 0x0161), ("Ž", 0x017D, 0x017E),
    ],
    "sv": [
        ("Ä", 0x00C4, 0x00E4), ("Ö", 0x00D6, 0x00F6), ("Å", 0x00C5, 0x00E5),
    ],
    "et": [
        ("Ä", 0x00C4, 0x00E4), ("Ö", 0x00D6, 0x00F6), ("Õ", 0x015C, 0x015D),
        ("Š", 0x0160, 0x0161), ("Ž", 0x017D, 0x017E), ("Ü", 0x00DC, 0x00FC),
        ("Ä", 0x00C4, 0x00E4),
    ],
    "cs": [
        ("Á", 0x00C1, 0x00E1), ("Č", 0x010C, 0x010D),
        ("Ď", 0x010E, 0x010F), ("Ě", 0x011A, 0x011B),
        ("Í", 0x00CD, 0x00ED), ("Ň", 0x0148, 0x0149),
        ("Ó", 0x00D3, 0x00F3), ("Ř", 0x0158, 0x0159),
        ("Š", 0x0160, 0x0161), ("Ť", 0x0164, 0x0165),
        ("Ú", 0x00DA, 0x00FA), ("Ů", 0x016F, 0x0170),
        ("Ý", 0x00DD, 0x00FD), ("Ž", 0x017D, 0x017E),
    ],
    "pl": [
        ("Ą", 0x0104, 0x0105), ("Ć", 0x0106, 0x0107),
        ("Ę", 0x0118, 0x0119), ("Ł", 0x0141, 0x0142),
        ("Ń", 0x0144, 0x0145), ("Ó", 0x00D3, 0x00F3),
        ("Ś", 0x015A, 0x015B), ("Ź", 0x0179, 0x017A),
        ("Ż", 0x017B, 0x017C),
    ],
    "sk": [
        ("Á", 0x00C1, 0x00E1), ("Ä", 0x00C4, 0x00E4),
        ("Č", 0x010C, 0x010D), ("Ď", 0x010E, 0x010F),
        ("É", 0x00C9, 0x00E9), ("Ě", 0x011A, 0x011B),
        ("Í", 0x00CD, 0x00ED), ("Ĺ", 0x0139, 0x013A),
        ("Ľ", 0x013D, 0x013E), ("Ň", 0x0148, 0x0149),
        ("Ó", 0x00D3, 0x00F3), ("Ô", 0x00D4, 0x00F4),
        ("Ŕ", 0x0154, 0x0155), ("ŕ", 0x0155, 0x0155),
        ("Š", 0x0160, 0x0161), ("Ť", 0x0164, 0x0165),
        ("Ú", 0x00DA, 0x00FA), ("Ý", 0x00DD, 0x00FD),
        ("Ž", 0x017D, 0x017E),
    ],
    "hu": [
        ("Á", 0x00C1, 0x00E1), ("É", 0x00C9, 0x00E9),
        ("Í", 0x00CD, 0x00ED), ("Ó", 0x00D3, 0x00F3),
        ("Ő", 0x0150, 0x0151), ("Ú", 0x00DA, 0x00FA),
        ("Ű", 0x0170, 0x0171), ("Ű", 0x0170, 0x0171),
    ],
    "ro": [
        ("Â", 0x00C2, 0x00E2), ("Î", 0x00CF, 0x00EF),
        ("Ă", 0x0102, 0x0103), ("Ș", 0x0218, 0x0219),
        ("Ț", 0x021A, 0x021B),
    ],
    "lt": [
        ("Ą", 0x0104, 0x0105), ("Č", 0x010C, 0x010D),
        ("Ę", 0x0118, 0x0119), ("Ė", 0x0117, 0x0116),
        ("Į", 0x012E, 0x012F), ("Š", 0x0160, 0x0161),
        ("Ų", 0x0172, 0x0173), ("Ū", 0x0174, 0x0175),
        ("Ž", 0x017D, 0x017E),
    ],
    "lv": [
        ("Ā", 0x0100, 0x0101), ("Č", 0x010C, 0x010D),
        ("Ē", 0x0112, 0x0113), ("Ģ", 0x0122, 0x0123),
        ("Ī", 0x012A, 0x012B), ("Ķ", 0x0136, 0x0137),
        ("Ļ", 0x013B, 0x013C), ("Ņ", 0x0145, 0x0146),
        ("Š", 0x0160, 0x0161), ("Ž", 0x017D, 0x017E),
    ],
    "hr": [
        ("Č", 0x010C, 0x010D), ("Ć", 0x0106, 0x0107),
        ("Đ", 0x0110, 0x0111), ("Š", 0x0160, 0x0161),
        ("Ž", 0x017D, 0x017E),
    ],
    "sl": [
        ("Č", 0x010C, 0x010D), ("Š", 0x0160, 0x0161),
        ("Ž", 0x017D, 0x017E),
    ],
    "fr": [
        ("À", 0x00C0, 0x00E0), ("Â", 0x00C2, 0x00E2),
        ("Ã", 0x00C3, 0x00E3), ("Å", 0x00C5, 0x00E5),
        ("È", 0x00C8, 0x00E8), ("É", 0x00C9, 0x00E9),
        ("Ê", 0x00CA, 0x00EA), ("Ë", 0x00CB, 0x00EB),
        ("Ì", 0x00CC, 0x00EC), ("Î", 0x00CE, 0x00EE),
        ("Ï", 0x00CF, 0x00EF), ("Ò", 0x00D2, 0x00F2),
        ("Ô", 0x00D4, 0x00F4), ("Õ", 0x00D5, 0x00F5),
        ("Ù", 0x00D9, 0x00F9), ("Û", 0x00DB, 0x00FB),
        ("Ü", 0x00DC, 0x00FC), ("Ÿ", 0x0178, 0x00FF),
    ],
    "de": [
        ("Ä", 0x00C4, 0x00E4), ("Ö", 0x00D6, 0x00F6),
        ("Ü", 0x00DC, 0x00FC), ("ß", 0x00DF, 0x00DF),
    ],
    "es": [
        ("Ñ", 0x00D1, 0x00F1), ("Á", 0x00C1, 0x00E1),
        ("É", 0x00C9, 0x00E9), ("Í", 0x00CD, 0x00ED),
        ("Ó", 0x00D3, 0x00F3), ("Ú", 0x00DA, 0x00FA),
        ("Ü", 0x00DC, 0x00FC),
    ],
    "pt": [
        ("Á", 0x00C1, 0x00E1), ("À", 0x00C0, 0x00E0),
        ("Ã", 0x00C3, 0x00E3), ("Â", 0x00C2, 0x00E2),
        ("É", 0x00C9, 0x00E9), ("Ê", 0x00CA, 0x00EA),
        ("Í", 0x00CD, 0x00ED), ("Ó", 0x00D3, 0x00F3),
        ("Ô", 0x00D4, 0x00F4), ("Ú", 0x00DA, 0x00FA),
    ],
    "it": [
        ("À", 0x00C0, 0x00E0), ("È", 0x00C8, 0x00E8),
        ("É", 0x00C9, 0x00E9), ("Ì", 0x00CC, 0x00EC),
        ("Ò", 0x00D2, 0x00F2), ("Ù", 0x00D9, 0x00F9),
    ],
    "ga": [
        # Iers — basis Latijns met acute accent
        ("Á", 0x00C1, 0x00E1), ("É", 0x00C9, 0x00E9),
        ("Í", 0x00CD, 0x00ED), ("Ó", 0x00D3, 0x00F3),
        ("Ú", 0x00DA, 0x00FA),
    ],
    "lb": [
        ("É", 0x00C9, 0x00E9), ("È", 0x00C8, 0x00E8),
        ("Ë", 0x00CB, 0x00EB), ("ÉI", 0x00C9, 0x00E9),
    ],
    "mt": [
        ("Ċ", 0x0108, 0x0109), ("Ġ", 0x011A, 0x011B),
        ("Ħ", 0x0126, 0x0127), ("Ż", 0x017B, 0x017C),
        ("Ž", 0x017D, 0x017E),
    ],
}


# Cyrillisch alfabet (Bulgaars — gebruikt subset van standaard Cyrillisch)
CYRILLIC_BG = [
    ("А", 0x0410, "a"),    ("Б", 0x0411, "b"),
    ("В", 0x0412, "v"),    ("Г", 0x0413, "g"),
    ("Д", 0x0414, "d"),    ("Е", 0x0415, "e"),
    ("Ж", 0x0416, "zh"),   ("З", 0x0417, "z"),
    ("И", 0x0418, "i"),    ("Й", 0x0419, "j"),
    ("К", 0x041A, "k"),    ("Л", 0x041B, "l"),
    ("М", 0x041C, "m"),    ("Н", 0x041D, "n"),
    ("О", 0x041E, "o"),    ("П", 0x041F, "p"),
    ("Р", 0x0420, "r"),    ("С", 0x0421, "s"),
    ("Т", 0x0422, "t"),    ("У", 0x0423, "u"),
    ("Ф", 0x0424, "f"),    ("Х", 0x0425, "kh"),
    ("Ц", 0x0426, "ts"),   ("Ч", 0x0427, "ch"),
    ("Ш", 0x0428, "sh"),   ("Щ", 0x0429, "sht"),
    ("Ъ", 0x042A, "hard"), ("Ь", 0x042B, "soft"),
    ("Ю", 0x042C, "yu"),   ("Я", 0x042D, "ya"),
]

# Grieks alfabet
GREEK = [
    ("Α", 0x0391, "Alpha"),      ("Β", 0x0392, "Beta"),
    ("Γ", 0x0393, "Gamma"),      ("Δ", 0x0394, "Delta"),
    ("Ε", 0x0395, "Epsilon"),    ("Ζ", 0x0396, "Zeta"),
    ("Η", 0x0397, "Eta"),        ("Θ", 0x0398, "Theta"),
    ("Ι", 0x0399, "Iota"),       ("Κ", 0x039A, "Kappa"),
    ("Λ", 0x039B, "Lambda"),     ("Μ", 0x039C, "Mu"),
    ("Ν", 0x039D, "Nu"),         ("Ξ", 0x039E, "Xi"),
    ("Ο", 0x039F, "Omicron"),    ("Π", 0x03A0, "Pi"),
    ("Ρ", 0x03A1, "Rho"),        ("Σ", 0x03A3, "Sigma"),
    ("Τ", 0x03A4, "Tau"),        ("Υ", 0x03A5, "Upsilon"),
    ("Φ", 0x03A6, "Phi"),        ("Χ", 0x03A7, "Chi"),
    ("Ψ", 0x03A8, "Psi"),        ("Ω", 0x03A9, "Omega"),
]


# ─── Helpers ───

def byte_to_freq(byte_val):
    return round(BASE_FREQ * byte_val / REF, 2)


def hexa4(byte_val):
    return byte_val & 0x0F


def klankveld(byte_val):
    return byte_val % 64


def build_alphabet(code):
    """Build the full alphabet for a given language code."""
    if code == "bg":
        return [(ch, cp, nm) for ch, cp, nm in CYRILLIC_BG]
    elif code == "el":
        return [(ch, cp, nm) for ch, cp, nm in GREEK]
    else:
        # Latin base + extras
        chars = []
        for up, up_cp, lo_cp in LATIJN_BASE:
            chars.append((up, up_cp, up))
        extras = LATIJN_EXTRA.get(code, [])
        for up, up_cp, lo_cp in extras:
            chars.append((up, up_cp, up))
        return chars


def ipv4_from_word(word):
    """Convert word to IPv4 via UTF-8 bytes."""
    raw = word.encode("utf-8")
    b = raw[:4]
    return ".".join(str(x) for x in b)


# ─── Generators ───

def generate_json(code, info, output_dir):
    """Generate JSON mapping for one language."""
    alpha = build_alphabet(code)
    mapping = {}
    for idx, (ch, cp, nm) in enumerate(alpha):
        freq = byte_to_freq(cp)
        h4 = hexa4(cp)
        kv = klankveld(cp)
        u8 = " ".join(f"0x{b:02x}" for b in ch.encode("utf-8"))
        mapping[ch] = {
            "bit": idx,
            "binary": f"{idx:05b}",
            "byte": cp,
            "hex": f"0x{cp:04x}",
            "freq_432": freq,
            "hexa4": h4,
            "klankveld": kv,
            "utf8": u8,
            "naam": nm,
        }

    vb = info["voorbeeld"]
    woord = vb["woord"]
    raw = woord.encode("utf-8")
    freqs = [byte_to_freq(cp) for _, cp, _ in alpha]

    out = {
        "taal": info["taal"],
        "script": info["script"],
        "code": code,
        "locale": info["locale"],
        "direction": info["direction"],
        "chars": len(alpha),
        "bits": info["bits"],
        "combinaties": info["combinaties"],
        "slack": info["slack"],
        "unicode_block": info["unicode_block"],
        "mapping": mapping,
        "ipv4_example": {
            "woord": woord,
            "bytes": list(raw),
            "hex": " ".join(f"0x{b:02x}" for b in raw),
            "ipv4": ipv4_from_word(woord),
            "frequencies": [byte_to_freq(b) for b in raw],
        },
        "ipv4_math": "4 letters × 8-bit = 32-bit = 1 IPv4 address",
        "ipv6_math": "16 letters × 8-bit = 128-bit = 1 IPv6 address",
    }

    path = os.path.join(output_dir, f"{code}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {path}")
    return out


def generate_md(code, info, json_data, output_dir):
    """Generate Markdown for one language."""
    lines = []
    lines.append("---")
    lines.append(f"taal: {info['taal']}")
    lines.append(f"code: {code}")
    lines.append(f"script: {info['script']}")
    lines.append(f"locale: {info['locale']}")
    lines.append(f"chars: {info['chars']}")
    lines.append(f"bits: {info['bits']}")
    lines.append(f"combinaties: {info['combinaties']}")
    lines.append(f"slack: {info['slack']}")
    lines.append(f"base_freq: {BASE_FREQ}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {info['taal']} — Charveld Alfabet")
    lines.append("")
    lines.append("## Overzicht")
    lines.append("")
    lines.append(f"- **Tekenruimte:** {info['chars']} tekens")
    lines.append(f"- **Script:** {info['script']}")
    lines.append(f"- **Bits per teken:** {info['bits']}")
    lines.append(f"- **Combinaties:** {info['combinaties']}")
    lines.append(f"- **Slack:** {info['slack']} onbenut")
    lines.append(f"- **Unicode block:** {info['unicode_block']}")
    lines.append(f"- **Locale:** `{info['locale']}`")
    lines.append(f"- **IPv4 blok:** 4 letters = 32-bit")
    lines.append(f"- **IPv6 blok:** 16 letters = 128-bit")
    lines.append("")
    lines.append("## Tekentabel")
    lines.append("")
    lines.append("| # | Teken | Bit | Binary | Byte | Hex | Freq (Hz) | Hexa4 | Klankveld |")
    lines.append("|---|-------|-----|--------|------|-----|-----------|-------|-----------|")

    mapping = json_data["mapping"]
    for idx, (ch, data) in enumerate(mapping.items()):
        lines.append(
            f"| {idx} | {ch} | {data['bit']} | `{data['binary']}` | "
            f"{data['byte']} | `{data['hex']}` | {data['freq_432']:.1f} | "
            f"{data['hexa4']} | {data['klankveld']} |"
        )

    lines.append("")
    lines.append("## Voorbeeld")
    lines.append("")
    ex = json_data["ipv4_example"]
    lines.append(f"**Woord:** `{ex['woord']}` — *{info['voorbeeld']['naam']}*")
    lines.append("")
    lines.append(f"- **Bytes:** {', '.join('0x' + f'{b:02x}' for b in ex['bytes'])}")
    lines.append(f"- **Hex:** `{ex['hex']}`")
    lines.append(f"- **IPv4:** `{ex['ipv4']}`")
    lines.append(f"- **Frequenties:** {', '.join(f'{f:.1f}' for f in ex['frequencies'])}")
    lines.append("")
    lines.append("## Wiskunde")
    lines.append("")
    lines.append("```")
    lines.append(f"Bits per teken : {info['bits']}")
    lines.append(f"Chars          : {info['chars']}")
    lines.append(f"Combinaties    : {info['combinaties']} = 2^{info['bits']}")
    lines.append(f"Slack          : {info['slack']} = {info['combinaties']} - {info['chars']}")
    lines.append(f"IPv4 blok      : 4 chars × 8-bit = 32-bit")
    lines.append(f"IPv6 blok      : 16 chars × 8-bit = 128-bit")
    lines.append(f"```")
    lines.append("")
    lines.append("## Routing")
    lines.append("")
    lines.append(f"- **CC (locale):** `{info['locale']}`")
    lines.append(f"- **24-bit hexafield:** `{code}` = bit-slot {idx + 1} van 24")
    lines.append(f"- **Sub-token:** char < 1 token (24-bit granularity)")
    lines.append(f"- **Route:** onzichtbaar — charset IS de routerlaag")
    lines.append("")

    path = os.path.join(output_dir, f"{code}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ {path}")


def generate_routing_master(output_dir):
    """Generate the master eu24-routing.json."""
    routing = {
        "name": "EU24 Charveld Routing",
        "concept": "24-bit hexafield → 24 EU talen → 5×5 vectorveld",
        "cc_routing": "CC locale = self-describing char router",
        "sub_token": "char < 1 token (24-bit granularity)",
        "route": "onzichtbaar — charset IS de routerlaag",
        "talens": [],
    }

    for idx, (key, info) in enumerate(EU24.items()):
        entry = {
            "slot": idx + 1,
            "bit": f"bit-{idx}",
            "code": info["code"],
            "taal": info["taal"],
            "script": info["script"],
            "locale": info["locale"],
            "chars": info["chars"],
            "bits": info["bits"],
        }
        routing["talens"].append(entry)

    path = os.path.join(output_dir, "eu24-routing.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(routing, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {path}")
    return routing


def generate_overview_md(routing, output_dir):
    """Generate eu24-overview.md."""
    lines = []
    lines.append("---")
    lines.append("title: EU24 Charveld Routing")
    lines.append("concept: 24-bit hexafield → 24 talen → 5×5 vectorveld")
    lines.append("---")
    lines.append("")
    lines.append("# EU24 — Charveld Routing Tegenover")
    lines.append("")
    lines.append("## Concept")
    lines.append("")
    lines.append("> **CC (locale) is zichzelf beschrijvend.**")
    lines.append("> De charset IS de routerlaag.")
    lines.append("> Char < 1 token (24-bit sub-token granulariteit).")
    lines.append("> Route onzichtbaar.")
    lines.append("")
    lines.append("## 24-bit Hexafield")
    lines.append("")
    lines.append("24 EU talen = 24-bit field.")
    lines.append("Elke taal bezet 1 bit-slot.")
    lines.append("Samen vormen ze een 5×5 vectorveld (LLM embedding space).")
    lines.append("")
    lines.append("## Routing Tabel")
    lines.append("")
    lines.append("| Slot | Bit | Code | Taal | Script | Locale | Chars |")
    lines.append("|------|-----|------|------|--------|--------|-------|")

    for entry in routing["talens"]:
        lines.append(
            f"| {entry['slot']} | {entry['bit']} | `{entry['code']}` | "
            f"{entry['taal']} | {entry['script']} | "
            f"`{entry['locale']}` | {entry['chars']} |"
        )

    lines.append("")
    lines.append("## Wiskunde")
    lines.append("")
    lines.append("```")
    lines.append("24 talen     → 24-bit hexafield")
    lines.append("24-bit       → 2^24 = 16,777,216 combinaties")
    lines.append("5×5 vector   → LLM embedding space")
    lines.append("char < 1 token → 24-bit sub-token granularity")
    lines.append("CC locale    → self-describing char router")
    lines.append("route        → onzichtbaar")
    lines.append("```")
    lines.append("")

    path = os.path.join(output_dir, "eu24-overview.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ {path}")


# ─── Main ───

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    maps_dir = os.path.join(base_dir, "maps")
    taalen_dir = os.path.join(base_dir, "taalen")
    os.makedirs(maps_dir, exist_ok=True)
    os.makedirs(taalen_dir, exist_ok=True)

    print(f"EU24 Charveld Generator")
    print(f"{'=' * 40}")
    print(f"Talen: {len(EU24)}")
    print()

    for key, info in EU24.items():
        code = info["code"]
        print(f"  {code}: {info['taal']} ({info['script']})")
        json_data = generate_json(code, info, maps_dir)
        generate_md(code, info, json_data, taalen_dir)

    print()
    routing = generate_routing_master(maps_dir)
    generate_overview_md(routing, taalen_dir)

    print()
    print(f"{'=' * 40}")
    print(f"✓ 24 talen gegenereerd")
    print(f"  Maps:   {maps_dir}/")
    print(f"  Taalen: {taalen_dir}/")
    print()
    print(f"24-bit hexafield actief.")
    print(f"Route onzichtbaar.")


if __name__ == "__main__":
    main()
