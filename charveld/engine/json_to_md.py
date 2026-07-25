#!/usr/bin/env python3
"""
json_to_md.py — Genereer taal-specifieke .md uit alfabet JSON.

Gebruik:
  python3 json_to_md.py <taal.json> [output.md]

Output:
  charveld/taalen/<taal>.md

Inhoud:
  - Frontmatter (taal, chars, bits, combinaties, slack)
  - Tabel: teken → bit → binary → byte → hex → freq → hexa4
  - Voorbeeld: woord → bytes → ipv4 → freqs
  - Wiskunde: bits per letter, combinaties, slack
"""

import json
import sys
import os


def hexa4(byte_val: int) -> int:
    """Hexa4 = (byte mod 6) — 4-bit blokken."""
    return byte_val % 6


def klankveld(byte_val: int) -> int:
    """Klankveld = byte mod 128 + 1 (1-based)."""
    return (byte_val % 128) + 1


def freq_vedic(byte_val: int, base: float = 432.0) -> float:
    """Vedic/Śāradā frequentie."""
    return base * (2 ** ((byte_val - 97) / 12))


def generate_md(json_path: str, output_path: str = None):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    taal = data["taal"]
    chars = data["chars"]
    bits = data["bits"]
    combinaties = data.get("combinaties", 2**bits)
    slack = data.get("slack", combinaties - chars)
    mapping = data["mapping"]
    example = data.get("ipv4_example", {})

    # Bepaal output pad
    if output_path is None:
        base = os.path.splitext(os.path.basename(json_path))[0]
        output_path = os.path.join(os.path.dirname(json_path), "..", "taalen", f"{base}.md")
        output_path = os.path.normpath(output_path)

    lines = []
    lines.append(f"---")
    lines.append(f"taal: {taal}")
    lines.append(f"chars: {chars}")
    lines.append(f"bits: {bits}")
    lines.append(f"combinaties: {combinaties}")
    lines.append(f"slack: {slack}")
    lines.append(f"base_freq: 432.0")
    lines.append(f"---")
    lines.append("")
    lines.append(f"# {taal} — Charveld Alfabet")
    lines.append("")
    lines.append("## Overzicht")
    lines.append("")
    lines.append(f"- **Tekenruimte:** {chars} tekens")
    lines.append(f"- **Bits per teken:** {bits}")
    lines.append(f"- **Combinaties:** {combinaties}")
    lines.append(f"- **Slack:** {slack} onbenut")
    lines.append(f"- **IPv4 blok:** 4 letters = 32-bit")
    lines.append(f"- **IPv6 blok:** 16 letters = 128-bit")
    lines.append("")
    lines.append("## Tekentabel")
    lines.append("")
    lines.append("| # | Teken | Bit | Binary | Byte | Hex | Freq (Hz) | Hexa4 | Klankveld |")
    lines.append("|---|-------|-----|--------|------|-----|-----------|-------|-----------|")

    for char, info in mapping.items():
        bit = info["bit"]
        binary = info["binary"]
        byte_val = info["byte"]
        hex_val = info["hex"]
        freq = info.get("freq_432", freq_vedic(byte_val))
        h4 = hexa4(byte_val)
        kv = klankveld(byte_val)

        lines.append(f"| {bit} | `{char}` | {bit} | `{binary}` | {byte_val} | {hex_val} | {freq:.2f} | {h4} | {kv} |")

    lines.append("")

    if example:
        lines.append("## Voorbeeld")
        lines.append("")
        woord = example["woord"]
        letters = example["letters"]
        bytes_list = example["bytes"]
        ipv4 = example["ipv4"]
        binary_str = example.get("binary", " ".join(f"{b:08b}" for b in bytes_list))
        hexa32 = example.get("hexa32", hex(sum(b << (24 - 8*i) for i, b in enumerate(bytes_list))))
        freqs = example["frequencies"]

        lines.append(f"**Woord:** `{woord}`")
        lines.append("")
        lines.append(f"- **Letters:** {', '.join(f'`{l}`' for l in letters)}")
        lines.append(f"- **Bytes:** {', '.join(map(str, bytes_list))}")
        lines.append(f"- **Hex:** `{binary_str}`")
        lines.append(f"- **IPv4:** `{ipv4}`")
        lines.append(f"- **Hexa32:** `{hexa32}`")
        lines.append(f"- **Frequenties:** {', '.join(f'{f:.2f}' for f in freqs)}")
        lines.append("")

    lines.append("## Wiskunde")
    lines.append("")
    lines.append(f"```")
    lines.append(f"Bits per teken : {bits}")
    lines.append(f"Chars          : {chars}")
    lines.append(f"Combinaties    : {combinaties} = 2^{bits}")
    lines.append(f"Slack          : {slack} = {combinaties} - {chars}")
    lines.append(f"IPv4 blok      : 4 chars × 8-bit = 32-bit")
    lines.append(f"IPv6 blok      : 16 chars × 8-bit = 128-bit")
    lines.append(f"```")
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 json_to_md.py <taal.json> [output.md]")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    generate_md(json_path, output_path)
