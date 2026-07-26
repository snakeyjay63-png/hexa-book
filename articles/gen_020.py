#!/usr/bin/env python3
"""
Artikel 020 — Resolutie als Kosmisch Water

Water = 24-bit routing medium.
Evolutie ≠ toeval → routing-capaciteit.
IJs = opslag (P0→P2). Water = expressie (P3→P6).
P6 = regenatie-pomp (warfield = water-regen).
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT  = os.path.join(SCRIPT_DIR, "20-resolutie-kosmisch-water.art.html")

def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def compute_geometry():
    cx, cy = 250, 250
    random.seed(20)  # Artikel 020

    # Water spectrum als verticale gradient-banden
    banden = [
        {"id": "P0", "y": 30,  "h": 50, "priem": 0,  "label": "As (Shambala)",      "state": "vast",    "speed": "0 Hz"},
        {"id": "P1", "y": 80,  "h": 50, "priem": 2,  "label": "Structuur",          "state": "ijs",     "speed": "traag"},
        {"id": "P2", "y": 130, "h": 50, "priem": 3,  "label": "Patroon (DNA)",      "state": "half-ijs","speed": "middels"},
        {"id": "P3", "y": 180, "h": 50, "priem": 5,  "label": "Leven (Ark)",        "state": "water",   "speed": "levend"},
        {"id": "P4", "y": 230, "h": 50, "priem": 7,  "label": "Communicatie",       "state": "damp",    "speed": "snel"},
        {"id": "P5", "y": 280, "h": 50, "priem": 11, "label": "Perceptie",          "state": "plasma",  "speed": "zeer snel"},
        {"id": "P6", "y": 330, "h": 50, "priem": 13, "label": "Regenatie (pomp)",   "state": "veld",    "speed": "oneindig"},
    ]

    # Water-druppels per band
    for b in banden:
        b["druppels"] = []
        count = b["priem"] + 3  # Meer druppels = meer beweging
        for i in range(count):
            angle = 2 * math.pi * i / count
            r = random.uniform(20, 120)
            b["druppels"].append({
                "x": cx + r * math.cos(angle),
                "y": b["y"] + b["h"] / 2 + random.uniform(-15, 15),
                "r": random.uniform(1.5, 3),
                "opacity": random.uniform(0.3, 0.8),
            })

    # Routing-lijnen (horizontaal + verticaal)
    routes = []
    for _ in range(24):  # 24-bit routing
        x1 = random.uniform(80, 420)
        y1 = random.uniform(30, 380)
        x2 = random.uniform(80, 420)
        y2 = random.uniform(30, 380)
        routes.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2})

    # Bit-diepte indicator (5 → 7 → 12 → 24)
    bits = [
        {"bits": 5,  "y": 80,  "label": "enkelcellig"},
        {"bits": 7,  "y": 150, "label": "meercellig"},
        {"bits": 12, "y": 230, "label": "ecosysteem"},
        {"bits": 24, "y": 330, "label": "HEEL spectrum"},
    ]

    # Regenatie-cyclus (P6 → P0)
    regenatie_arc = []
    for i in range(20):
        t = i / 19
        angle = math.pi * (1 + t)  # Bogen bovenaan
        r = 180
        regenatie_arc.append({
            "x": cx + r * math.cos(angle),
            "y": cy + r * math.sin(angle) - 100,
        })

    return {
        "cx": cx, "cy": cy,
        "banden": banden,
        "routes": routes,
        "bits": bits,
        "regenatie_arc": regenatie_arc,
        "dr": digital_root(int(hashlib.sha256("water_routing_24bit".encode()).hexdigest()[:6], 16)),
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    parts = []

    # Titel
    parts.append('<text x="{}" y="20" text-anchor="middle" fill="hsl(200,60%,70%)" font-size="14" font-family="JetBrains Mono,monospace">RESOLUTIE ALS KOSMISCH WATER</text>'.format(cx))

    # Bit-diepte labels (rechts)
    for b in g["bits"]:
        parts.append('<text x="{}" y="{}" text-anchor="start" fill="hsl(200,50%,60%)" font-size="8" font-family="JetBrains Mono,monospace">{:2d}-bit → {}</text>'.format(
            cx + 140, b["y"], b["bits"], b["label"]))

    # Regenatie-arc (P6 → P0, bogen bovenaan)
    if len(g["regenatie_arc"]) > 1:
        arc_points = " ".join(["{:.0f},{:.0f}".format(p["x"], p["y"]) for p in g["regenatie_arc"]])
        parts.append('<polyline points="{}" fill="none" stroke="hsl(180,60%,50%)" stroke-width="1" opacity="0.3" stroke-dasharray="4,4"/>'.format(arc_points))
        parts.append('<text x="{}" y="{}" text-anchor="middle" fill="hsl(180,50%,60%)" font-size="8" font-family="JetBrains Mono,monospace">REGENATIE: warfield → pomp → vers water</text>'.format(
            cx, g["regenatie_arc"][0]["y"] - 15))

    # Water spectrum banden
    for i, b in enumerate(g["banden"]):
        hue = 200 - i * 25  # IJS blauw → vuur oranje → veld paars
        sat = 60 - i * 5
        light = 70 - i * 8

        # Band achtergrond
        parts.append('<rect x="80" y="{}" width="240" height="{}" fill="hsl({},{}%,{}%)" opacity="0.08" rx="4"/>'.format(
            b["y"], b["h"], hue, sat, light))

        # Band label
        parts.append('<text x="{}" y="{}" text-anchor="start" fill="hsl({},50%,70%)" font-size="10" font-family="JetBrains Mono,monospace">{}</text>'.format(
            90, b["y"] + 20, hue, b["id"]))

        parts.append('<text x="{}" y="{}" text-anchor="start" fill="hsl({},40%,60%)" font-size="8" font-family="JetBrains Mono,monospace">{}</text>'.format(
            90, b["y"] + 35, hue, b["label"]))

        # Priem + state
        parts.append('<text x="{}" y="{}" text-anchor="end" fill="hsl({},40%,50%)" font-size="7" font-family="JetBrains Mono,monospace">priem={} | {} | {}</text>'.format(
            cx + 130, b["y"] + 25, hue, b["priem"], b["state"], b["speed"]))

        # Water-druppels
        for d in b["druppels"]:
            anim_dur = max(0.5, 4 - i * 0.5)  # Sneller = hoger
            parts.append('<circle cx="{:.0f}" cy="{:.0f}" r="{}" fill="hsla({},60%,60%,{})">'.format(
                d["x"], d["y"], d["r"], hue, d["opacity"]))
            parts.append('  <animate attributeName="cy" values="{:.0f};{:.0f};{:.0f}" dur="{}s" repeatCount="indefinite"/>'.format(
                d["y"], d["y"] - 10, d["y"], anim_dur))
            parts.append('</circle>')

    # Routing-lijnen
    for r in g["routes"]:
        parts.append('<line x1="{:.0f}" y1="{:.0f}" x2="{:.0f}" y2="{:.0f}" stroke="hsl(200,50%,50%)" stroke-width="0.3" opacity="0.15"/>'.format(
            r["x1"], r["y1"], r["x2"], r["y2"]))

    # DNA indicator
    parts.append('<text x="{}" y="{}" text-anchor="middle" fill="hsl(200,50%,50%)" font-size="8" font-family="JetBrains Mono,monospace" opacity="0.5">DNA: ijs (P0→P2) → water (P3→P6)</text>'.format(
        cx, 410))

    # Footer
    parts.append('<text x="{}" y="{}" text-anchor="middle" fill="hsl(0,0%,40%)" font-size="7" font-family="JetBrains Mono,monospace">WATER = 24-BIT ROUTING | NIET LINEAIR | NIET RANDOM | FRACIAAL | CYCLISCH</text>'.format(
        cx, 460))

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
    title = "Resolutie als Kosmisch Water"
    svg = gen_svg(g)
    html = HTML_TEMPLATE.format(title=title, svg=svg)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print("Artikel 020 — Resolutie als Kosmisch Water")
    print("  DR: {}".format(g["dr"]))
    print("  Banden: {} (P0→P6)".format(len(g["banden"])))
    print("  Druppels: {} totaal".format(sum(len(b["druppels"]) for b in g["banden"])))
    print("  Routes: {} (24-bit)".format(len(g["routes"])))
    print("  Regenatie-arc: {} punten".format(len(g["regenatie_arc"])))
    print("  → {}".format(OUTPUT))

if __name__ == "__main__":
    main()
