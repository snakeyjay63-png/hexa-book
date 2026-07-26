#!/usr/bin/env python3
"""
Artikel 007 — Dimensie 4: Expansie

Geometrie afgeleid uit de tekst:
- Mandelbrot → expansie die zichzelf herhaalt
- 0.0.0.0 → het eiland van nul
- Expansie = groeiende ringen met fractale subdivisies
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-007.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "07-dimensie-4.art.html")

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
    has_mandelbrot = "Mandelbrot" in text
    has_ip = "0.0.0.0" in text or "IP" in text
    nidra_links = sum(1 for n in ["011", "012", "001"] if n in text)
    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "has_mandelbrot": has_mandelbrot,
        "has_ip": has_ip, "nidra_links": nidra_links,
    }

def compute_geometry(e):
    cx, cy = 250, 250
    base_hue = 200  # blauw = expansie

    # Expansie-ringgen — groeiende cirkels met fractale subdivisions
    rings = []
    num_rings = 8
    for i in range(num_rings):
        r = 30 + i * 22
        # Fractale subdivisies per ring
        subdivisions = 6 + i * 4
        pts = []
        for j in range(subdivisions):
            angle = (2 * math.pi * j / subdivisions) + (i * 0.05)
            pts.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
        rings.append({
            "points": " ".join(pts),
            "r": r,
            "hue": (base_hue + i * 15) % 360,
            "opacity": 0.7 - (i * 0.06),
        })

    # 0.0.0.0 → nul-eiland (centrale leegte)
    center_pts = []
    for j in range(12):
        angle = 2 * math.pi * j / 12
        center_pts.append("{:.1f},{:.1f}".format(cx + 15 * math.cos(angle), cy + 15 * math.sin(angle)))

    # Expansie-vonken (uitgaande punten)
    spark_pts = []
    random.seed(e["dr"])
    for _ in range(60):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(25, 220)
        spark_pts.append({
            "x": cx + r * math.cos(angle),
            "y": cy + r * math.sin(angle),
            "size": random.uniform(0.5, 2),
        })

    return {
        "cx": cx, "cy": cy, "base_hue": base_hue,
        "rings": rings, "center_pts": " ".join(center_pts),
        "spark_pts": spark_pts, "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    bh = g["base_hue"]
    parts = []

    # Expansie-ringgen
    for ring in g["rings"]:
        parts.append('<polygon points="{}" fill="hsl({},{},{}%)" stroke="hsl({},{},{}%)" stroke-width="1" opacity="{}"/>'.format(
            ring["points"], ring["hue"], 50, 15, ring["hue"], 60, 45, ring["opacity"]))

    # Nul-eiland (centrum)
    parts.append('<polygon points="{}" fill="#06060a" stroke="hsl({},70%,60%)" stroke-width="2" opacity="0.9"/>'.format(
        g["center_pts"], bh))

    # Uitgaande lijnen
    for spark in g["spark_pts"]:
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},30%,40%)" stroke-width="0.3" opacity="0.15"/>'.format(
            cx, cy, spark["x"], spark["y"], bh))

    # Vonken
    for spark in g["spark_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{}" fill="hsl({},50%,60%)" opacity="0.4"/>'.format(
            spark["x"], spark["y"], spark["size"], bh))

    # Kern
    parts.append('<circle cx="{}" cy="{}" r="4" fill="hsl({},80%,70%)" opacity="0.9"/>'.format(cx, cy, bh))

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
.layer-rotate {{ animation: rotate 80s linear infinite; }}
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
      <span>EXPANSIE</span>
      <span>RINGEN: {rings}</span>
      <span>DR: {dr}</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "Dimensie 4: Expansie"
    for l in text.split("\n")[:3]:
        if l.startswith("# "):
            title = l[2:].strip()
            break
    svg = gen_svg(g)
    return HTML_TEMPLATE.format(
        title=title, svg=svg, bh=g["base_hue"],
        rings=len(g["rings"]), dr=g["dr"],
    )

def main():
    text = read_article()
    e = extract(text)
    g = compute_geometry(e)
    print("Artikel 007 — Dimensie 4: Expansie")
    for k, v in [("DR", e["dr"]), ("Mandelbrot", e["has_mandelbrot"]), ("IP", e["has_ip"]), ("nidrā", e["nidra_links"]), ("Woorden", e["word_count"])]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
