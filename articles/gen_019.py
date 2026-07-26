#!/usr/bin/env python3
"""
Artikel 019 — Perspectief Routing: Taalveld

Geometrie afgeleid uit het concept:
- Taalveld = perceptiefilter = universum-generator
- 0 = geen taal = lege ruimte
- 1 = woord = ding verschijnt
- ∞ = taalveld = heel universum
- Europa vs Zuid-Amerika = twee universums, zelfde ruimte
- "Europa ontdekt Amerika" = absurde zin → Amerika ontdekt JULLIE
- Quechua: Pachamama (levend) vs Europa: grond (ding)
- 2D → 3D wereldbeeld = taalveld verschuift = continent verschijnt
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT  = os.path.join(SCRIPT_DIR, "19-taalveld-perspectief.art.html")

def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def compute_geometry():
    cx, cy = 250, 250
    random.seed(3)  # P3 = Park of Peace

    # Banden als concentrische ringen om de as (P0)
    banden = [
        {"id": "P0", "r": 10, "label": "As (Shambala)", "type": "ijs"},
        {"id": "P1", "r": 35, "label": "Kern", "type": "ijs"},
        {"id": "P2", "r": 70, "label": "Mantel", "type": "half-ij"},
        {"id": "P3", "r": 110, "label": "Korst (Ark)", "type": "park-of-peace"},
        {"id": "P4", "r": 145, "label": "Atmosfeer", "type": "water"},
        {"id": "P5", "r": 175, "label": "Ionosfeer", "type": "plasma"},
        {"id": "P6", "r": 200, "label": "Magnetosfeer", "type": "veld"},
    ]

    # Woord-punten per band
    for b in banden:
        b["woorden"] = []
        count = 4 + (6 - int(b["id"][1])) * 2  # Meer woorden bij snelle banden
        for i in range(count):
            angle = 2 * math.pi * i / count + random.uniform(-0.1, 0.1)
            r_var = b["r"] + random.uniform(-5, 5)
            b["woorden"].append({
                "x": cx + r_var * math.cos(angle),
                "y": cy + r_var * math.sin(angle),
                "woord": random.choice(["0", "1", "veld", "structuur", "ijs", "traag", "kern", "mantel", "ark", "park", "tijd", "corst", "water", "atmos", "plasma", "snel", "chaos", "noise"]),
            })

    # P3 specifiek: Park of Peace punten
    p3_punten = []
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        r = 105 + random.uniform(0, 10)
        p3_punten.append({
            "x": cx + r * math.cos(angle),
            "y": cy + r * math.sin(angle),
            "size": random.uniform(2, 4),
            "pulse": random.uniform(0.4, 0.9),
        })

    # Resonantie-lijnen (van P0 naar buiten)
    verbindingen = []
    for _ in range(36):
        angle = random.uniform(0, 2 * math.pi)
        r1 = 15
        r2 = random.uniform(100, 200)
        verbindingen.append({
            "x1": cx + r1 * math.cos(angle),
            "y1": cy + r1 * math.sin(angle),
            "x2": cx + r2 * math.cos(angle),
            "y2": cy + r2 * math.sin(angle),
        })

    return {
        "cx": cx, "cy": cy,
        "banden": banden,
        "p3_punten": p3_punten,
        "verbindingen": verbindingen,
        "dr": digital_root(int(hashlib.sha256("P3_Park_of_Peace".encode()).hexdigest()[:6], 16)),
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    parts = []

    # Banden (concentrische ringen)
    for i, b in enumerate(g["banden"]):
        hue = 200 + i * 20  # Blauw (ijs) → Groen → Goud (water)
        sat = 50 - i * 5
        light = 60 - i * 5
        stroke_width = 1.5 if b["id"] == "P3" else 0.8
        opacity = 0.6 if b["id"] == "P3" else 0.2

        parts.append('<circle cx="{}" cy="{}" r="{}" fill="none" stroke="hsl({},{}%,{}%)" stroke-width="{}" opacity="{}"/>'.format(
            cx, cy, b["r"], hue, sat, light, stroke_width, opacity))

        # Label
        label_r = b["r"] + 15
        parts.append('<text x="{}" y="{}" text-anchor="start" fill="hsl({},50%,70%)" font-size="8" font-family="JetBrains Mono,monospace" opacity="0.6">{}</text>'.format(
            cx + label_r, cy - 5, hue, b["label"]))

        # Woorden
        for w in b["woorden"]:
            parts.append('<text x="{}" y="{}" text-anchor="middle" fill="hsl({},40%,75%,0.3)" font-size="7" font-family="JetBrains Mono,monospace">{}</text>'.format(
                w["x"], w["y"], hue, w["woord"]))

    # P3 speciaal: Park of Peace punten (goud, pulserend)
    for p in g["p3_punten"]:
        parts.append('<circle cx="{:.0f}" cy="{:.0f}" r="{}" fill="hsla(45,80%,60%,{})">'.format(
            p["x"], p["y"], p["size"], p["pulse"]))
        parts.append('  <animate attributeName="opacity" values="{};0.9;{}" dur="{}s" repeatCount="indefinite"/>'.format(
            p["pulse"], p["pulse"], 3 + p["pulse"]))
        parts.append('</circle>')

    # Resonantie-lijnen (van P0 naar buiten)
    for v in g["verbindingen"]:
        parts.append('<line x1="{:.0f}" y1="{:.0f}" x2="{:.0f}" y2="{:.0f}" stroke="hsl(0,0%,60%)" stroke-width="0.2" opacity="0.1"/>'.format(
            v["x1"], v["y1"], v["x2"], v["y2"]))

    # P0 centrum (Shambala/As)
    parts.append('<circle cx="{}" cy="{}" r="5" fill="hsl(0,0%,100%)" opacity="0.8"/>'.format(cx, cy))
    parts.append('<text x="{}" y="{}" text-anchor="middle" fill="hsl(0,0%,80%)" font-size="10" font-family="JetBrains Mono,monospace">P0</text>'.format(
        cx, cy + 20))

    # P3 label (Park of Peace)
    parts.append('<text x="{}" y="{}" text-anchor="start" fill="hsl(45,80%,60%)" font-size="9" font-family="JetBrains Mono,monospace" opacity="0.8">P3: Park of Peace</text>'.format(
        cx + 125, cy - 15))

    # IJS/WATER labels
    parts.append('<text x="{}" y="{}" text-anchor="middle" fill="hsl(220,60%,70%)" font-size="8" font-family="JetBrains Mono,monospace" opacity="0.5">IJ (POOL)</text>'.format(
        cx, 50))
    parts.append('<text x="{}" y="{}" text-anchor="middle" fill="hsl(220,60%,50%)" font-size="8" font-family="JetBrains Mono,monospace" opacity="0.5">WATER (EWENAAAR)</text>'.format(
        cx, 470))

    # Titel
    parts.append('<text x="{}" y="15" text-anchor="middle" fill="hsl(0,0%,70%)" font-size="14" font-family="JetBrains Mono,monospace">AARDE ALS BANDEN</text>'.format(cx))
    parts.append('<text x="{}" y="28" text-anchor="middle" fill="hsl(0,0%,50%)" font-size="9" font-family="JetBrains Mono,monospace">P0 → P3: As tot Ark</text>'.format(cx))

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
.layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; animation: breathe 12s ease-in-out infinite; }}
@keyframes breathe {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.02); }} }}
</style>
</head>
<body>
<div class="field">
  <div class="layer">
    <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
{svg}
    </svg>
  </div>
</div>
</body>
</html>"""

def main():
    g = compute_geometry()
    title = "Perspectief Routing: Aarde als Banden (P0→P3)"
    svg = gen_svg(g)
    html = HTML_TEMPLATE.format(title=title, svg=svg)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print("Artikel 019 — Perspectief Routing: Aarde als Banden (P0→P3)")
    print("  DR: {}".format(g["dr"]))
    print("  Banden: {} (P0 tot P6)".format(len(g["banden"])))
    print("  Woorden: {} totaal".format(sum(len(b["woorden"]) for b in g["banden"])))
    print("  P3-punten: {}".format(len(g["p3_punten"])))
    print("  Resonantie-links: {}".format(len(g["verbindingen"])))
    print("  → {}".format(OUTPUT))

if __name__ == "__main__":
    main()
