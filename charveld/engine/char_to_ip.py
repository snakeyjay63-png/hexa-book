#!/usr/bin/env python3
"""
charveld — TeKEN → BITVELD → KLANKVELD → NETWERK
=================================================
Elk teken van elke taal → IPv4/IPv6 address → frequentieveld.

Route: char → byte → 4-bit hexa → klankveld(64) → IPv4(32) → IPv6(128) → 4 richtingen
"""

import json, struct, socket, sys, os

# 3 frequentiesystemen
FREQ_SYSTEMS = {
    "440": {"name": "ISO/Latin", "base": 440.0, "ref": 81.75},
    "432": {"name": "Vedic/Śāradā", "base": 432.0, "ref": 81.75},
    "396": {"name": "Arabic/Abjad", "base": 396.0, "ref": 81.75},
}

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def byte_to_freq(byte_val, ref=81.75, base=432.0):
    """byte → frequentie via referentie."""
    return base * byte_val / ref


def char_to_hexa4(byte_val):
    """byte → 4-bit hexa waarde (0-15)."""
    return byte_val & 0x0F  # lowest 4 bits


def char_to_klankveld(byte_val):
    """byte → klankveld (64 bands)."""
    return byte_val % 64


def chars_to_ipv4(chars):
    """4 chars → IPv4 address."""
    if len(chars) != 4:
        raise ValueError(f"IPv4 needs 4 chars, got {len(chars)}")
    octets = [ord(c) & 0xFF for c in chars]
    return f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}"


def chars_to_ipv6(chars):
    """16 chars → IPv6 address (8 × 16-bit words)."""
    if len(chars) != 16:
        raise ValueError(f"IPv6 needs 16 chars, got {len(chars)}")
    words = []
    for i in range(0, 16, 2):
        word = (ord(chars[i]) << 8) | (ord(chars[i+1]) & 0xFF)
        words.append(f"{word:04x}")
    return ":".join(words)


def klankveld_lichaam(freq_hz):
    """Bepaal of frequentie binnen Mendelsche limieten valt.
    
    Lichaam als filter:
    - horen: 20Hz – 20kHz
    - maken: 80Hz – 1kHz
    
    Retourneert dict met hoorbaar/makbaar status.
    """
    hoorbaar = 20 <= freq_hz <= 20000
    maakbaar = 80 <= freq_hz <= 1000
    
    return {
        "freq": freq_hz,
        "hoorbaar": hoorbaar,
        "maakbaar": maakbaar,
        "filter": "lichaam",
    }


def char_to_token(char):
    """Char → 24-bit token: 23-bit vibratie + 1-bit vertraging.
    
    char → 1 token
    ── 23-bit : vibratie (klank, frequentie, data)
       1-bit  : vertraging (weg naar sunya)
    totaal   : 24-bit (3 bytes)
    """
    byte_val = ord(char)
    utf8_bytes = char.encode('utf-8')
    
    # 23-bit vibratie: byte_val (16-bit) + ticks (3-bit) + hexa4 (4-bit)
    # ticks = utf8 bytes (1-4) → 3-bit (max 7)
    ticks = len(utf8_bytes)
    h4 = byte_val & 0x0F
    
    # 23-bit payload: [byte(16) | ticks(3) | hexa4(4)]
    vibratie = (byte_val << 7) | (ticks << 4) | h4
    
    # 1-bit vertraging: altijd aanwezig (de weg terug naar sunya)
    vertraging = 1  # 1 = de stilte die er altijd is
    
    # 24-bit token
    token = (vibratie << 1) | vertraging
    
    return {
        "char": char,
        "byte": byte_val,
        "hex": f"0x{byte_val:04x}",
        "vibratie_23": vibratie,
        "vertraging_1": vertraging,
        "token_24": token,
        "token_binary": f"{token:024b}",
        "ticks": ticks,
        "utf8_bytes": len(utf8_bytes),
        "hexa4": h4,
    }


def char_full_route(char, freq_mode="432"):
    """Volledige route voor één teken → char → token → frequentie → lichaam."""
    token = char_to_token(char)
    byte_val = token["byte"]
    fs = FREQ_SYSTEMS[freq_mode]
    freq = round(byte_to_freq(byte_val, fs["ref"], fs["base"]), 2)
    
    # Klankveld als lichaam-filter
    lichaam = klankveld_lichaam(freq)
    
    return {
        "char": token["char"],
        "byte": token["byte"],
        "hex": token["hex"],
        "token_24": token["token_24"],
        "token_binary": token["token_binary"],
        "vibratie_23": token["vibratie_23"],
        "vertraging_1": token["vertraging_1"],
        "hexa4": token["hexa4"],
        "klankveld": char_to_klankveld(byte_val),
        "freq": freq,
        "freq_system": fs["name"],
        "ticks": token["ticks"],
        "utf8_bytes": token["utf8_bytes"],
        "lichaam": lichaam,  # Mendelsche filter: horen/maken
    }


def woord_route(word, freq_mode="432"):
    """Volledige route voor woord."""
    n = len(word)
    char_routes = [char_full_route(c, freq_mode) for c in word]
    
    # Totaal ticks = som van alle char ticks
    total_ticks = sum(c["ticks"] for c in char_routes)
    
    result = {
        "woord": word,
        "letters": n,
        "chars": char_routes,
        "total_ticks": total_ticks,  # snelheid van het woord
    }
    
    # IPv4 als 4 letters
    if n >= 4:
        result["ipv4"] = chars_to_ipv4(word[:4])
    
    # IPv6 als 16 letters (pad indien nodig)
    if n >= 16:
        result["ipv6"] = chars_to_ipv6(word[:16])
    elif n < 16:
        padded = word.ljust(16, '\x00')
        result["ipv6"] = chars_to_ipv6(padded)
        result["ipv6_padded"] = True
    
    # 4 richtingen (N O Z W)
    directions = ["N", "O", "Z", "W"]
    result["directions"] = {}
    for i, d in enumerate(directions):
        if i * 4 + 3 < n:
            chunk = word[i*4:(i+1)*4]
            result["directions"][d] = {
                "chars": list(chunk),
                "ipv4": chars_to_ipv4(chunk),
                "freqs": [round(FREQ_SYSTEMS[freq_mode]["base"] * ord(c) / FREQ_SYSTEMS[freq_mode]["ref"], 2) 
                         for c in chunk],
            }
    
    return result


def taal_map(taal_name="nl"):
    """Laad taal map."""
    map_path = os.path.join(BASE, "maps", f"{taal_name}-alfabet.json")
    if os.path.exists(map_path):
        with open(map_path) as f:
            return json.load(f)
    return None


def main():
    """CLI: charveld conversie."""
    if len(sys.argv) < 2:
        print("Usage: char_to_ip.py <woord|char|taal> [freq_mode]")
        print("  char <c>     - route één teken")
        print("  word <w>     - route woord → IPv4/IPv6")
        print("  taal <name>  - laad taal map")
        print("  freq_mode: 440, 432, 396 (default: 432)")
        return
    
    mode = sys.argv[1]
    freq = sys.argv[3] if len(sys.argv) > 3 else "432"
    
    if mode == "char" and len(sys.argv) > 2:
        c = sys.argv[2]
        r = char_full_route(c, freq)
        print(json.dumps(r, indent=2))
    
    elif mode == "word" and len(sys.argv) > 2:
        w = sys.argv[2]
        r = woord_route(w, freq)
        print(json.dumps(r, indent=2, ensure_ascii=False))
    
    elif mode == "taal" and len(sys.argv) > 2:
        t = sys.argv[2]
        m = taal_map(t)
        if m:
            print(json.dumps(m, indent=2, ensure_ascii=False))
        else:
            print(f"Taal map niet gevonden: {t}")
    
    else:
        print("Zie usage.")


if __name__ == "__main__":
    main()
