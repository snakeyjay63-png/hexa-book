#!/usr/bin/env python3
"""
Artikel XXX — [Naam]

Kopieer dit bestand als gen_XXX.py en vul de parameters in.
De geometrie komt uit de tekst — geen template, elke artikel is uniek.
"""

import hashlib
import math
import os

# ── Config ──
ARTICLE_FILE = "hexa-book-XXX.md"          # Bron bestand (in dezelfde map)
OUTPUT_FILE  = "../audit/XX-naam.art.html" # Output (relatief tot articles/)

# ── Lees de tekst ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE    = os.path.join(SCRIPT_DIR, ARTICLE_FILE)
OUTPUT     = os.path.join(SCRIPT_DIR, OUTPUT_FILE)

def read_article():
    with open(ARTICLE, encoding='utf-8') as f:
        return f.read()

# ── Basis berekeningen ──
def text_hash(text, n=8):
    """Unieke hash van de tekst."""
    h = hashlib.sha256(text.encode()).hexdigest()
    return int(h[:n], 16)

def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def freq_from_dr(dr):
    """Midden C + dr semitonen."""
    return 130.81 * (2 ** ((dr - 1) / 12))

# ── Hier begint jouw logica ──
# Verander dit per artikel. De parameters hieronder zijn voorbeelden.
# Elke artikel moet iets unieks berekenen uit de tekst.

def compute_geometry(text):
    """
    Bereken visuele parameters uit de tekst.

    Tips:
    - Hash → basis waarden
    - Woorden tellen, lijnen tellen, specifieke tekens zoeken
    - Digital root voor 3-6-9 patroon
    - Secties tellen → lagen
    - Trefwoorden → kleuren, vormen

    Return een dict met:
      dr, freq, segments, radius, rotation,
      hue, sat, light, layers, sparks, speed
    """
    h = text_hash(text)
    dr = digital_root(h)

    # ── Pas dit aan per artikel ──
    # Voorbeeld:
    lines = text.split('\n')
    sections = [l for l in lines if l.startswith('## ')]
    words = text.split()

    # Elke artikel kan hier eigen logica hebben
    segments = max(3, dr * 2)
    radius = 120 + (h % 80)
    rotation = h % 360
    hue = h % 360
    sat = 50 + (h >> 8) % 40
    light = 40 + (h >> 16) % 20

    # 3-6-9 lagen
    layers = [i for i in [3, 6, 9] if i <= dr or dr == 9]
    if not layers:
        layers = [dr]

    sparks = len(words) % 12 + 3
    speed = 0.2 + (dr * 0.05)

    return {
        'dr': dr, 'freq': freq_from_dr(dr),
        'segments': segments, 'radius': radius,
        'rotation': rotation, 'hue': hue,
        'sat': sat, 'light': light,
        'layers': layers, 'sparks': sparks,
        'speed': speed,
    }

# ── SVG generatie ──
def gen_svg(g):
    """Genereer SVG geometrie."""
    cx, cy = 250, 250
    hue, sat, light = g['hue'], g['sat'], g['light']
    parts = []

    # Polygon lagen
    for i, layer in enumerate(g['layers']):
        r = g['radius'] - (i * 25)
        pts = []
        for j in range(g['segments']):
            angle = (2 * math.pi * j / g['segments']) + (g['rotation'] * math.pi / 180) + (i * 0.1)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            pts.append("%.1f,%.1f" % (x, y))
        stroke = "hsl(%d,%d%%,%d%%)" % (hue, sat, light + i * 5)
        opacity = 0.8 - i * 0.15
        pts_str = " ".join(pts)
        parts.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="1.5" opacity="%s"/>' % (pts_str, stroke, opacity))

    # Centrale punt
    parts.append('<circle cx="%d" cy="%d" r="4" fill="hsl(%d,%d%%,%d%%)"/>' % (cx, cy, hue, sat, light + 15))

    # Vonken
    for i in range(g['sparks']):
        angle = 2 * math.pi * i / g['sparks']
        r = g['radius'] + 20 + (i * 5)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        parts.append('<circle cx="%.1f" cy="%.1f" r="2" fill="hsl(%d,%d%%,%d%%)" opacity="0.6"/>' % (x, y, hue, sat, light + 10))

    return "\n".join(parts)

# ── HTML output ──
def gen_html(g, text):
    lines = text.split("\n")
    title = lines[0].lstrip("# ").strip() if lines else "Artikel"
    svg = gen_svg(g)
    rot_time = "%.1f" % (10 / max(g['speed'], 0.1))

    return """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s | Hexa-Boek</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #06060a; color: #d4d4e0;
  font-family: 'Instrument Sans', -apple-system, sans-serif;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-height: 100vh; overflow: hidden;
}
.geometry {
  position: relative; width: 500px; height: 500px;
  animation: rotate %ss linear infinite;
}
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.metadata {
  position: absolute; bottom: 40px; text-align: center;
  font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
  color: hsl(%d, %d%%, %d%%); opacity: 0.6;
}
.metadata .title {
  font-size: 1.2rem; margin-bottom: 8px;
  color: hsl(%d, %d%%, %d%%);
}
.metadata .params {
  display: flex; gap: 16px; justify-content: center;
}
</style>
</head>
<body>
<div class="geometry">
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
%s
</svg>
</div>
<div class="metadata">
<div class="title">%s</div>
<div class="params">
  <span>DR: %d</span>
  <span>FREQ: %.1fHz</span>
  <span>SEG: %d</span>
  <span>LAYERS: %s</span>
  <span>SPARKS: %d</span>
</div>
</div>
</body>
</html>""" % (
    title, rot_time,
    g['hue'], g['sat'], g['light'],
    g['hue'], g['sat'], g['light'] + 15,
    svg, title,
    g['dr'], g['freq'], g['segments'],
    ", ".join(map(str, g['layers'])),
    g['sparks'],
)

# ── Main ──
def main():
    text = read_article()
    g = compute_geometry(text)
    print("Artikel %s" % ARTICLE_FILE)
    print("  DR: %d | FREQ: %.1fHz | SEG: %d" % (g['dr'], g['freq'], g['segments']))
    print("  Layers: %s | Sparks: %d" % (g['layers'], g['sparks']))
    print("  Kleur: hsl(%d, %d%%, %d%%)" % (g['hue'], g['sat'], g['light']))
    html = gen_html(g, text)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print("→ %s" % OUTPUT)

if __name__ == '__main__':
    main()
