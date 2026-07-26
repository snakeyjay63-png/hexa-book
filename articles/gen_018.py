#!/usr/bin/env python3
"""
Artikel 018 — Artikel F: Het Returnmedium

Geometrie afgeleid uit de tekst:
- Water = symbolisch medium = continuïteit
- HEXA routing (H) vs returnmedium (F)
- Alles vloeit terug → concentrische stromingsvelden
- ρ_routing(H)=6, ρ_nul(F)=0
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-004.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "18-f-returnmedium.art.html")

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
    has_hexa = "HEXA" in text or "ρ_routing" in text
    has_water = "water" in text.lower() or "medium" in text.lower() or "जलम्" in text
    nidra_links = sum(1 for n in ["001", "002", "012"] if n in text)
    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "has_hexa": has_hexa,
        "has_water": has_water, "nidra_links": nidra_links,
    }

def compute_geometry(e):
    cx, cy = 250, 250
    base_hue = 200  # blauw = water

    # Concentrische stromingsringen (return-velden)
    flow_rings = []
    num_rings = 12
    for i in range(num_rings):
        r = 20 + i * 18
        subdivisions = 8 + i * 6
        pts = []
        for j in range(subdivisions):
            angle = (2 * math.pi * j / subdivisions) + (i * 0.03)
            # Stromings-afwijking
            r_var = r + random.uniform(-5, 5)
            pts.append("{:.1f},{:.1f}".format(cx + r_var * math.cos(angle), cy + r_var * math.sin(angle)))
        flow_rings.append({
            "points": " ".join(pts),
            "r": r,
            "hue": (base_hue + i * 8) % 360,
            "opacity": 0.8 - (i * 0.05),
        })

    # 6 HEXA routing-punten (hexagonaal)
    hexa_pts = []
    for i in range(6):
        angle = 2 * math.pi * i / 6 - math.pi / 6
        hexa_pts.append({
            "x": cx + 100 * math.cos(angle),
            "y": cy + 100 * math.sin(angle),
        })

    # Return-stromingen (van HEXA punten naar centrum)
    return_flows = []
    for pt in hexa_pts:
        flow_pts = []
        steps = 20
        for s in range(steps):
            t = s / (steps - 1)
            x = pt["x"] * (1 - t) + cx * t
            y = pt["y"] * (1 - t) + cy * t
            # Spiro-afwijking
            spiral_angle = 2 * math.pi * t * 2
            r_spiral = 10 * (1 - t)
            x += r_spiral * math.cos(spiral_angle)
            y += r_spiral * math.sin(spiral_angle)
            flow_pts.append("{:.1f},{:.1f}".format(x, y))
        return_flows.append(" ".join(flow_pts))

    # Water-druppels
    droplets = []
    random.seed(e["dr"])
    for _ in range(40):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(30, 220)
        droplets.append({
            "x": cx + r * math.cos(angle),
            "y": cy + r * math.sin(angle),
            "size": random.uniform(1, 3),
        })

    return {
        "cx": cx, "cy": cy, "base_hue": base_hue,
        "flow_rings": flow_rings, "hexa_pts": hexa_pts,
        "return_flows": return_flows, "droplets": droplets, "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    bh = g["base_hue"]
    parts = []

    # Stromingsringen
    for ring in g["flow_rings"]:
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},{},{}%)" stroke-width="0.8" opacity="{}"/>'.format(
            ring["points"], ring["hue"], 50, 20, ring["opacity"]))

    # HEXA routing-punten
    for pt in g["hexa_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="4" fill="hsl({},70%,60%)" opacity="0.7"/>'.format(
            pt["x"], pt["y"], bh))
        # Verbinding met centrum
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{}" y2="{}" stroke="hsl({},30%,25%)" stroke-width="0.3" opacity="0.2"/>'.format(
            pt["x"], pt["y"], cx, cy, bh))

    # Return-stromingen (spiro)
    for flow in g["return_flows"]:
        parts.append('<polyline points="{}" fill="none" stroke="hsl({},60%,50%)" stroke-width="0.8" opacity="0.3"/>'.format(
            flow, bh))

    # Water-druppels
    for d in g["droplets"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{}" fill="hsl({},40%,55%)" opacity="0.4"/>'.format(
            d["x"], d["y"], d["size"], bh))

    # Nul-centrum (ρ_nul = 0)
    parts.append('<circle cx="{}" cy="{}" r="8" fill="none" stroke="hsl({},80%,70%)" stroke-width="2" opacity="0.9"/>'.format(cx, cy, bh))
    parts.append('<circle cx="{}" cy="{}" r="2" fill="hsl({},90%,80%)" opacity="0.9"/>'.format(cx, cy, bh))

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
.layer-rotate {{ animation: rotate 100s linear infinite; }}
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
      <span>RETURNMEDIUM</span>
      <span>ρ_nul(F)=0</span>
      <span>DR: {dr}</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "Artikel F: Het Returnmedium"
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
    print("Artikel 018 — Artikel F: Het Returnmedium")
    for k, v in [("DR", e["dr"]), ("HEXA", e["has_hexa"]), ("Water", e["has_water"]), ("nidrā", e["nidra_links"]), ("Woorden", e["word_count"])]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
