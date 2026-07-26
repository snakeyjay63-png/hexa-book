#!/usr/bin/env python3
"""
Artikel 017 — Artikel E: Audio-superpositie

Geometrie afgeleid uit de tekst:
- 4 lenzen (A,B,C,D) → 4 golven
- Superpositie E(t) = samensmelting
- Golfpatroon → sinusvormige lagen
- NPR: Noise → Pattern → Return
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-003.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "17-e-audio.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f:
        return f.read()

def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    words = text.split()
    has_npr = "NPR" in text or "Noise" in text or "Pattern" in text or "Return" in text
    has_lenses = all(c in text for c in ["A_numeric", "B_numeric", "C_role", "D_byte"])
    nidra_links = sum(1 for n in ["004", "005", "006"] if n in text)
    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "has_npr": has_npr,
        "has_lenses": has_lenses, "nidra_links": nidra_links,
    }

def compute_geometry(e):
    cx, cy = 250, 250
    base_hue = 280  # paars = audio-veld

    # 4 golven (A,B,C,D)
    waves = []
    colors = [
        ("#e87040", "A"),   # rood
        ("#40c8e8", "B"),   # cyan
        ("#40e870", "C"),   # groen
        ("#e840c8", "D"),   # magenta
    ]
    for idx, (color, label) in enumerate(colors):
        pts = []
        phase = idx * math.pi / 2
        freq = 2 + idx * 0.5
        amp = 30 + idx * 10
        for x in range(500):
            y = cy + idx * 50 + amp * math.sin(2 * math.pi * freq * x / 500 + phase)
            pts.append("{:.1f},{:.1f}".format(x, y))
        waves.append({"points": " ".join(pts), "color": color, "label": label})

    # Superpositie E(t) — gemiddelde van de 4 golven
    super_pts = []
    for x in range(500):
        y_vals = []
        for idx in range(4):
            phase = idx * math.pi / 2
            freq = 2 + idx * 0.5
            amp = 30 + idx * 10
            y_vals.append(amp * math.sin(2 * math.pi * freq * x / 500 + phase))
        avg = sum(y_vals) / 4
        super_pts.append("{:.1f},{:.1f}".format(x, cy + 200 + avg))

    # NPR cyclische punten
    npr_pts = []
    random.seed(e["dr"])
    for i in range(24):
        angle = 2 * math.pi * i / 24
        r = 80 + random.uniform(-15, 15)
        npr_pts.append({
            "x": cx + r * math.cos(angle),
            "y": cy + r * math.sin(angle),
            "phase": i % 3,  # 0=noise, 1=pattern, 2=return
        })

    return {
        "cx": cx, "cy": cy, "base_hue": base_hue,
        "waves": waves, "superposition": " ".join(super_pts),
        "npr_pts": npr_pts, "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    bh = g["base_hue"]
    parts = []

    # Achtergrond grid
    for i in range(0, 500, 25):
        parts.append('<line x1="{}" y1="0" x2="{}" y2="500" stroke="hsl({},20%,15%)" stroke-width="0.2" opacity="0.3"/>'.format(i, i, bh))
        parts.append('<line x1="0" y1="{}" x2="500" y2="{}" stroke="hsl({},20%,15%)" stroke-width="0.2" opacity="0.3"/>'.format(i, i, bh))

    # 4 bron-golven
    for wave in g["waves"]:
        parts.append('<polyline points="{}" fill="none" stroke="{}" stroke-width="1" opacity="0.3"/>'.format(
            wave["points"], wave["color"]))

    # Superpositie E(t) — dikke lijn
    parts.append('<polyline points="{}" fill="none" stroke="hsl({},80%,70%)" stroke-width="3" opacity="0.8"/>'.format(
        g["superposition"], bh))

    # NPR cyclische punten
    phase_colors = ["#888", "#4af", "#f4a"]  # noise, pattern, return
    for pt in g["npr_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="{}" opacity="0.6"/>'.format(
            pt["x"], pt["y"], phase_colors[pt["phase"]]))

    # Kern
    parts.append('<circle cx="{}" cy="{}" r="5" fill="hsl({},90%,75%)" opacity="0.9"/>'.format(cx, cy, bh))

    return "\n".join(parts)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #06060a; color: #d4d4e0; font-family: 'Instrument Sans', -apple-system, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }}
.field {{ position: relative; width: 500px; height: 500px; }}
.layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
.layer-rotate {{ animation: rotate 90s linear infinite; }}
@keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
.metadata {{ position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: hsl({bh}, 40%, 50%); opacity: 0.5; }}
.metadata .title {{ font-size: 1.1rem; margin-bottom: 6px; color: hsl({bh}, 60%, 55%); opacity: 0.8; }}
.metadata .params {{ display: flex; gap: 12px; justify-content: center; }}
</style>
</head>
<body>
<div class="field">
  <div class="layer layer-rotate">
    <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
{svg}
    </svg>
  </div>
  <div class="metadata">
    <div class="title">{title}</div>
    <div class="params">
      <span>AUDIO-SUPERPOSITIE</span>
      <span>4 GOLVEN → E(t)</span>
      <span>DR: {dr}</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "Artikel E: Audio-superpositie"
    for l in text.split("\n")[:3]:
        if l.startswith("# "):
            title = l[2:].strip()
            break
    svg = gen_svg(g)
    return HTML_TEMPLATE.format(
        title=title, svg=svg, bh=g["base_hue"],
        dr=g["dr"],
    )

def main():
    text = read_article()
    e = extract(text)
    g = compute_geometry(e)
    print("Artikel 017 — Artikel E: Audio-superpositie")
    for k, v in [("DR", e["dr"]), ("NPR", e["has_npr"]), ("4 Lenzen", e["has_lenses"]), ("nidrā", e["nidra_links"]), ("Woorden", e["word_count"])]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
