#!/usr/bin/env python3
"""
Artikel 006 — Dimensie 3: 3-6-9 Veld

Geometrie afgeleid uit de tekst:
- 3-6-9 als basisstructuur (niet cyclus, maar container)
- 3 lagen: driehoek → hexagon → 9-voud
- nidrā → 3 bruggen (012, 012, 017)
- 64 staten → hexa-subdivisies
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-006.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "06-dimensie-3.art.html")

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
    has_369 = "3-6-9" in text
    has_nidra = "nidrā" in text
    nidra_links = sum(1 for n in ["012", "017"] if n in text)
    has_64 = "64" in text
    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "has_369": has_369,
        "has_nidra": has_nidra, "nidra_links": nidra_links,
        "has_64": has_64,
    }

def compute_geometry(e):
    cx, cy = 250, 250
    base_hue = 30  # goud

    # 3-6-9 structurele lagen
    layers = []
    for i, (n, label) in enumerate([(3, "N"), (6, "P"), (9, "R")]):
        pts = []
        r = 80 + i * 35
        for j in range(n * 2):
            angle = (2 * math.pi * j / (n * 2)) + (i * 0.12)
            pts.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
        layers.append({"points": " ".join(pts), "hue": (base_hue + i * 30) % 360, "n": n, "label": label})

    # 64 staten (subdivisies)
    state_pts = []
    for i in range(8):
        for j in range(8):
            angle = (2 * math.pi * (i * 8 + j) / 64)
            r = 170 + random.uniform(-3, 3)
            state_pts.append({
                "x": cx + r * math.cos(angle),
                "y": cy + r * math.sin(angle),
                "opacity": 0.15 + (i / 8) * 0.2,
            })

    # nidrā bruggen
    bridge_pts = []
    for i in range(e["nidra_links"]):
        angle = (2 * math.pi * i / 3) + math.pi / 6
        bridge_pts.append({"x": cx + 200 * math.cos(angle), "y": cy + 200 * math.sin(angle)})

    return {
        "cx": cx, "cy": cy, "base_hue": base_hue,
        "layers": layers, "state_pts": state_pts,
        "bridge_pts": bridge_pts, "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    bh = g["base_hue"]
    parts = []

    # 3-6-9 lagen
    for lay in g["layers"]:
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},{},{}%)" stroke-width="1.5" opacity="0.6"/>'.format(
            lay["points"], lay["hue"], 60, 50))

    # 64 staten
    for pt in g["state_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="1" fill="hsl({},40%,50%)" opacity="{}"/>'.format(
            pt["x"], pt["y"], bh, pt["opacity"]))

    # nidrā bruggen
    for pt in g["bridge_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="hsl({},50%,55%)" opacity="0.5"/>'.format(
            pt["x"], pt["y"], (bh + 120) % 360))
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},30%,40%)" stroke-width="0.5" opacity="0.2" stroke-dasharray="3,3"/>'.format(
            cx, cy, pt["x"], pt["y"], bh))

    # Kern
    parts.append('<circle cx="{}" cy="{}" r="6" fill="hsl({},70%,55%)" opacity="0.8"/>'.format(cx, cy, bh))

    # Vonken
    random.seed(g["dr"])
    for _ in range(10):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(20, 100)
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="0.6" fill="hsl({},50%,60%)" opacity="0.3"/>'.format(
            cx + r * math.cos(angle), cy + r * math.sin(angle), bh))

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
.layer-rotate {{ animation: rotate 70s linear infinite; }}
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
      <span>3-6-9</span>
      <span>STATEN: {states}</span>
      <span>DR: {dr}</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "Dimensie 3: 3-6-9 Veld"
    for l in text.split("\n")[:3]:
        if l.startswith("# "):
            title = l[2:].strip()
            break
    svg = gen_svg(g)
    return HTML_TEMPLATE.format(
        title=title, svg=svg, bh=g["base_hue"],
        states=len(g["state_pts"]), dr=g["dr"],
    )

def main():
    text = read_article()
    e = extract(text)
    g = compute_geometry(e)
    print("Artikel 006 — Dimensie 3: 3-6-9 Veld")
    for k, v in [("DR", e["dr"]), ("3-6-9", e["has_369"]), ("64 staten", e["has_64"]), ("nidrā", e["nidra_links"]), ("Woorden", e["word_count"])]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
