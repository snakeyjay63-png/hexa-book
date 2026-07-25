#!/usr/bin/env python3
"""
gen_taal_md.py — Genereer taal-specifieke .md bestanden.

Ondersteunde talen: sanskriet, grieks, arabisch, latijn
Output: charveld/taalen/<taal>.md
"""

import os
import sys

BASE_FREQ = 432.0
REF = 81.75


def byte_to_freq(byte_val):
    return round(BASE_FREQ * byte_val / REF, 2)


def hexa4(byte_val):
    return byte_val & 0x0F


def klankveld(byte_val):
    return byte_val % 64


# ──────────────────────────────────────────────
# TAAL DEFINITIES
# ──────────────────────────────────────────────

TALEN = {
    "sanskriet": {
        "taal": "Sanskriet (Devanagari)",
        "chars": 49,
        "bits": 7,
        "combinaties": 128,
        "slack": 79,
        "unicode_range": "U+0900–U+097F",
        "tekens": [
            # Vocalen (11)
            ("अ", 0x0905, "a (kṛṣṇa a)"),
            ("आ", 0x0906, "ā"),
            ("इ", 0x0907, "i"),
            ("ई", 0x0908, "ī"),
            ("उ", 0x0909, "u"),
            ("ऊ", 0x090A, "ū"),
            ("ऋ", 0x0910, "ṛ"),
            ("ए", 0x0912, "e"),
            ("ऐ", 0x0913, "ai"),
            ("ओ", 0x0914, "o"),
            ("औ", 0x0915, "au"),
            # Medeklinkers - Vyanjana (33)
            # Varjaja (tongpunt)
            ("क", 0x0915, "ka"),
            ("ख", 0x0916, "kha"),
            ("ग", 0x0917, "ga"),
            ("घ", 0x0918, "gha"),
            ("ङ", 0x0919, "ṅa"),
            # Tālavya (tongwortel)
            ("च", 0x091A, "ca"),
            ("छ", 0x091B, "cha"),
            ("ज", 0x091C, "ja"),
            ("झ", 0x091D, "jha"),
            ("ञ", 0x091E, "ña"),
            # Mūrdhanya (tongrug)
            ("ट", 0x091F, "ṭa"),
            ("ठ", 0x0920, "ṭha"),
            ("ड", 0x0921, "ḍa"),
            ("ढ", 0x0922, "ḍha"),
            ("ण", 0x0923, "ṇa"),
            # Dantya (tand)
            ("त", 0x0924, "ta"),
            ("थ", 0x0925, "tha"),
            ("द", 0x0926, "da"),
            ("ध", 0x0927, "dha"),
            ("न", 0x0928, "na"),
            # Oṣṭhya (lip)
            ("प", 0x092A, "pa"),
            ("फ", 0x092B, "pha"),
            ("ब", 0x092C, "ba"),
            ("भ", 0x092D, "bha"),
            ("म", 0x092E, "ma"),
            # Antaḥstha (in-between)
            ("य", 0x092F, "ya"),
            ("र", 0x0930, "ra"),
            ("ल", 0x0932, "la"),
            ("व", 0x0935, "va"),
            # Upadhmānīya / Sṛśṇavīya
            ("श", 0x0936, "śa"),
            ("ष", 0x0937, "ṣa"),
            ("स", 0x0938, "sa"),
            ("ह", 0x0939, "ha"),
            # Speciale tekens (5)
            ("क्ष", 0x0915, "kṣa (conjunct)"),
            ("ज्ञ", 0x091C, "jña (conjunct)"),
            ("ः", 0x0903, "visarga"),
            ("ं", 0x0902, "anusvāra"),
            ("ँ", 0x0901, "chandrabindu"),
            ("्", 0x094D, "halant (virāma)"),
        ],
        "voorbeeld": {
            "woord": "अग्नि",
            "naam": "agni (vuur)",
            "letters": ["अ", "ग", "्न", "ि"],
            "bytes": [0x0905, 0x0917, 0x094D, 0x093F],
        },
    },

    "grieks": {
        "taal": "Grieks",
        "chars": 24,
        "bits": 5,
        "combinaties": 32,
        "slack": 8,
        "unicode_range": "U+0370–U+03FF",
        "tekens": [
            ("Α", 0x0391, "Alpha"),
            ("Β", 0x0392, "Beta"),
            ("Γ", 0x0393, "Gamma"),
            ("Δ", 0x0394, "Delta"),
            ("Ε", 0x0395, "Epsilon"),
            ("Ζ", 0x0396, "Zeta"),
            ("Η", 0x0397, "Eta"),
            ("Θ", 0x0398, "Theta"),
            ("Ι", 0x0399, "Iota"),
            ("Κ", 0x039A, "Kappa"),
            ("Λ", 0x039B, "Lambda"),
            ("Μ", 0x039C, "Mu"),
            ("Ν", 0x039D, "Nu"),
            ("Ξ", 0x039E, "Xi"),
            ("Ο", 0x039F, "Omicron"),
            ("Π", 0x03A0, "Pi"),
            ("Ρ", 0x03A1, "Rho"),
            ("Σ", 0x03A3, "Sigma"),
            ("Τ", 0x03A4, "Tau"),
            ("Υ", 0x03A5, "Upsilon"),
            ("Φ", 0x03A6, "Phi"),
            ("Χ", 0x03A7, "Chi"),
            ("Ψ", 0x03A8, "Psi"),
            ("Ω", 0x03A9, "Omega"),
        ],
        "voorbeeld": {
            "woord": "Λόγος",
            "naam": "Logos (woord/reden)",
            "letters": ["Λ", "ό", "γ", "ο", "ς"],
            "bytes": [0x039B, 0x03BF, 0x03B3, 0x03BF, 0x03C3],
        },
    },

    "arabisch": {
        "taal": "Arabisch (Abjad)",
        "chars": 28,
        "bits": 5,
        "combinaties": 32,
        "slack": 4,
        "unicode_range": "U+0600–U+06FF",
        "tekens": [
            # Abjad volgorde (traditioneel)
            ("ا", 0x0627, "alif (1)"),
            ("ب", 0x0628, "bāʾ (2)"),
            ("ت", 0x062A, "tāʾ (300)"),
            ("ث", 0x0630, "thāʾ (3)"),
            ("ج", 0x062C, "jīm (3000)"),
            ("ح", 0x062D, "ḥāʾ (8)"),
            ("خ", 0x062E, "khāʾ (600)"),
            ("د", 0x062F, "dāl (4)"),
            ("ذ", 0x0632, "dhal (700)"),
            ("ر", 0x0631, "rāʾ (200)"),
            ("ز", 0x0633, "zāy (20)"),
            ("س", 0x0633, "sīn (60)"),
            ("ش", 0x0634, "shīn (300)"),
            ("ص", 0x0635, "ṣād (90)"),
            ("ض", 0x0636, "ḍād (700)"),
            ("ط", 0x0637, "ṭāʾ (6)"),
            ("ظ", 0x0638, "ẓāʾ (500)"),
            ("ع", 0x0639, "ʿayn (70)"),
            ("غ", 0x063A, "ghayn (1000)"),
            ("ف", 0x0641, "fāʾ (80)"),
            ("ق", 0x0642, "qāf (100)"),
            ("ك", 0x0643, "kāf (900)"),
            ("ل", 0x0644, "lām (40)"),
            ("م", 0x0645, "mīm (40)"),
            ("ن", 0x0646, "nūn (50)"),
            ("ه", 0x0647, "hāʾ (5)"),
            ("و", 0x0648, "wāw (600)"),
            ("ي", 0x064A, "yāʾ (10)"),
        ],
        "voorbeeld": {
            "woord": "سلام",
            "naam": "salām (vrede)",
            "letters": ["س", "ل", "ا", "م"],
            "bytes": [0x0633, 0x0644, 0x0627, 0x0645],
        },
    },

    "latijn": {
        "taal": "Klassiek Latijn",
        "chars": 23,
        "bits": 5,
        "combinaties": 32,
        "slack": 9,
        "unicode_range": "U+0041–U+005A (klassiek subset)",
        "tekens": [
            # Klassiek Latijn (geen J of U — gebruik I/V)
            ("A", 0x0041, "A"),
            ("B", 0x0042, "B"),
            ("C", 0x0043, "C"),
            ("D", 0x0044, "D"),
            ("E", 0x0045, "E"),
            ("F", 0x0046, "F"),
            ("G", 0x0047, "G"),
            ("H", 0x0048, "H"),
            ("I", 0x0049, "I / J"),
            ("K", 0x004B, "K"),
            ("L", 0x004C, "L"),
            ("M", 0x004D, "M"),
            ("N", 0x004E, "N"),
            ("O", 0x004F, "O"),
            ("P", 0x0050, "P"),
            ("Q", 0x0051, "Q"),
            ("R", 0x0052, "R"),
            ("S", 0x0053, "S"),
            ("T", 0x0054, "T"),
            ("V", 0x0056, "V / U"),
            ("X", 0x0058, "X"),
            ("Y", 0x0059, "Y"),
            ("Z", 0x005A, "Z"),
        ],
        "voorbeeld": {
            "woord": "VITA",
            "naam": "Vita (leven)",
            "letters": ["V", "I", "T", "A"],
            "bytes": [0x0056, 0x0049, 0x0054, 0x0041],
        },
    },
}


def utf8_bytes(codepoint):
    """Return UTF-8 byte representation as string."""
    char = chr(codepoint)
    return " ".join(f"0x{b:02x}" for b in char.encode("utf-8"))


def ipv4_from_bytes(byte_list):
    """First 4 bytes → IPv4. For multi-byte chars, use UTF-8 bytes."""
    # If bytes are Unicode codepoints > 255, convert to UTF-8
    utf8_bytes = []
    for bp in byte_list:
        if bp > 255:
            # Multi-byte: convert codepoint to UTF-8 bytes
            char = chr(bp)
            utf8_bytes.extend(char.encode("utf-8"))
        else:
            utf8_bytes.append(bp)
    
    b = utf8_bytes[:4]
    return f"{b[0]}.{b[1]}.{b[2]}.{b[3]}"


def generate_md(taal_key, output_path):
    taal = TALEN[taal_key]

    lines = []
    lines.append("---")
    lines.append(f"taal: {taal['taal']}")
    lines.append(f"chars: {taal['chars']}")
    lines.append(f"bits: {taal['bits']}")
    lines.append(f"combinaties: {taal['combinaties']}")
    lines.append(f"slack: {taal['slack']}")
    lines.append(f"base_freq: {BASE_FREQ}")
    lines.append(f"unicode_range: {taal['unicode_range']}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {taal['taal']} — Charveld Alfabet")
    lines.append("")
    lines.append("## Overzicht")
    lines.append("")
    lines.append(f"- **Tekenruimte:** {taal['chars']} tekens")
    lines.append(f"- **Bits per teken:** {taal['bits']}")
    lines.append(f"- **Combinaties:** {taal['combinaties']}")
    lines.append(f"- **Slack:** {taal['slack']} onbenut")
    lines.append(f"- **Unicode range:** {taal['unicode_range']}")
    lines.append(f"- **IPv4 blok:** 4 letters = 32-bit")
    lines.append(f"- **IPv6 blok:** 16 letters = 128-bit")
    lines.append("")
    lines.append("## Tekentabel")
    lines.append("")
    lines.append("| # | Teken | Naam | Unicode | UTF-8 Bytes | Hex | Freq (Hz) | Hexa4 | Klankveld |")
    lines.append("|---|-------|------|---------|-------------|-----|-----------|-------|-----------|")

    for idx, (char, cp, naam) in enumerate(taal["tekens"]):
        freq = byte_to_freq(cp)
        h4 = hexa4(cp)
        kv = klankveld(cp)
        u8 = utf8_bytes(cp)

        lines.append(
            f"| {idx} | {char} | {naam} | `U+{cp:04X}` | `{u8}` | "
            f"`0x{cp:04x}` | {freq:.2f} | {h4} | {kv} |"
        )

    lines.append("")

    # Voorbeeld
    vb = taal["voorbeeld"]
    lines.append("## Voorbeeld")
    lines.append("")
    lines.append(f"**Woord:** `{vb['woord']}` — *{vb['naam']}*")
    lines.append("")
    lines.append(f"- **Letters:** {', '.join(f'`{l}`' for l in vb['letters'])}")

    # Bytes
    byte_list = vb["bytes"]
    lines.append(f"- **Bytes:** {', '.join(f'0x{b:04x}' for b in byte_list)}")

    # UTF-8
    utf8_str = " ".join(
        " ".join(f"0x{b:02x}" for b in chr(bp).encode("utf-8"))
        for bp in byte_list
    )
    lines.append(f"- **UTF-8:** `{utf8_str}`")

    # IPv4 (eerste 4 bytes)
    ipv4 = ipv4_from_bytes(byte_list)
    lines.append(f"- **IPv4:** `{ipv4}`")

    # Frequenties
    freqs = [byte_to_freq(bp) for bp in byte_list]
    lines.append(f"- **Frequenties:** {', '.join(f'{f:.2f}' for f in freqs)}")
    lines.append("")

    # Wiskunde
    lines.append("## Wiskunde")
    lines.append("")
    lines.append("```")
    lines.append(f"Bits per teken : {taal['bits']}")
    lines.append(f"Chars          : {taal['chars']}")
    lines.append(f"Combinaties    : {taal['combinaties']} = 2^{taal['bits']}")
    lines.append(f"Slack          : {taal['slack']} = {taal['combinaties']} - {taal['chars']}")
    lines.append(f"IPv4 blok      : 4 chars × 8-bit = 32-bit")
    lines.append(f"IPv6 blok      : 16 chars × 8-bit = 128-bit")
    lines.append(f"```")
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ {output_path}")
    return output_path


if __name__ == "__main__":
    # Bepaal taalen directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    taalen_dir = os.path.join(base_dir, "taalen")
    os.makedirs(taalen_dir, exist_ok=True)

    if len(sys.argv) > 1:
        taal_keys = sys.argv[1:]
    else:
        taal_keys = list(TALEN.keys())

    for key in taal_keys:
        if key in TALEN:
            out = os.path.join(taalen_dir, f"{key}.md")
            generate_md(key, out)
        else:
            print(f"⚠ Onbekende taal: {key}")
