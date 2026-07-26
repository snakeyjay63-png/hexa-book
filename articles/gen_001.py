#!/usr/bin/env python3
"""
Artikel 001 — 0 ≐ 1

Geometrie afgeleid uit de tekst:
- 4 lenzen (Arabisch, Sanskriet, Grieks, Latijn) → 4 kardinale punten
- 3-6-9 cirkel → concentrische lagen
- 0 ≐ 1 → cirkel + punt (niet-gelijk maar bron-equivalent)
- Agni/vuur → oranje-rode kern
- 6 vṛttis → hexa-ring
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-001.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "00-intro.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f:
        return f.read()

def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    lines = text.split("\n")
    words = text.split()

    has_agni = any(kw in text for kw in ["Agni", "अग्नि", "النار"])
    has_369 = "3-6-9" in text

    vrddi_defs = ["V₀", "V₁", "V₂", "V₃", "V₄", "V₅"]
    vrddis = sum(1 for v in vrddi_defs if v in text)

    lens_count = 0
    for kw in ["أجني", "النار", "अग्निः", "Πῦρ", "πῦρ", "fractaal"]:
        if kw in text:
            lens_count += 1
            if lens_count == 4:
                break

    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "line_count": len(lines),
        "lenses": lens_count, "has_369": has_369,
        "has_agni": has_agni, "vrttis": min(vrddis, 6),
    }

def compute_geometry(e):
    cx, cy = 250, 250
    base_hue = 15 if e["has_agni"] else int(e["hash"][:6], 16) % 360
    core_hue = 0 if e["has_agni"] else (base_hue + 60) % 360

    # 3-6-9 lagen
    layer_nums = [3, 6, 9] if e["has_369"] else [max(2, e["dr"])]
    layers = []
    for i, n in enumerate(layer_nums):
        layers.append({
            "n": n, "radius": 180 - (n // 3) * 18,
            "hue": (base_hue + n * 10) % 360,
            "sat": 60, "light": 45 + n * 2,
        })

    # 4 lens-punten (kardinaal)
    lens_colors = [(30,70,50), (120,60,45), (200,65,50), (280,60,55)]
    lens_pts = []
    for i in range(4):
        angle = (math.pi / 2) * i - math.pi / 2
        lens_pts.append({
            "x": cx + 195 * math.cos(angle),
            "y": cy + 195 * math.sin(angle),
            "c": lens_colors[i],
        })

    # 6 vṛtti punten
    vrddi_pts = []
    for i in range(e["vrttis"]):
        angle = (2 * math.pi * i / 6) - math.pi / 6
        vrddi_pts.append({
            "x": cx + 210 * math.cos(angle),
            "y": cy + 210 * math.sin(angle),
        })

    return {
        "cx": cx, "cy": cy, "layers": layers,
        "lens_pts": lens_pts, "vrddi_pts": vrddi_pts,
        "zero_r": 8, "one_r": 3,
        "base_hue": base_hue, "core_hue": core_hue,
        "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    parts = []
    bh, ch = g["base_hue"], g["core_hue"]

    # 0: cirkel
    parts.append('<circle cx="{}" cy="{}" r="{}" fill="none" stroke="hsl({},40%,60%)" stroke-width="1.5" opacity="0.4"/>'.format(
        cx, cy, g["zero_r"], bh))

    # 1: punt
    parts.append('<circle cx="{}" cy="{}" r="{}" fill="hsl({},80%,55%)"/>'.format(
        cx, cy, g["one_r"], ch))

    # Lagen
    for i, lay in enumerate(g["layers"]):
        pts = []
        n = lay["n"] * 2
        r = lay["radius"]
        for j in range(n):
            angle = (2 * math.pi * j / n) + (i * 0.15)
            pts.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},{},{}%)" stroke-width="1" opacity="{:.2f}"/>'.format(
            " ".join(pts), lay["hue"], lay["sat"], lay["light"], 0.6 - i * 0.12))

    # Lens punten
    for pt in g["lens_pts"]:
        h, s, l = pt["c"]
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="hsl({},{},{})" opacity="0.8"/>'.format(
            pt["x"], pt["y"], h, s, l))
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},{},{})" stroke-width="0.5" opacity="0.15"/>'.format(
            cx, cy, pt["x"], pt["y"], h, s, l))

    # Vṛtti punten
    for pt in g["vrddi_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="1.5" fill="hsl({},30%,50%)" opacity="0.4"/>'.format(
            pt["x"], pt["y"], bh))

    # Agni vonken
    random.seed(g["dr"])
    for _ in range(8):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(20, 60)
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="1" fill="hsl({},90%,60%)" opacity="0.5"/>'.format(
            cx + r * math.cos(angle), cy + r * math.sin(angle), ch))

    return "\n".join(parts)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: #06060a; color: #d4d4e0;
  font-family: 'Instrument Sans', -apple-system, sans-serif;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-height: 100vh; overflow: hidden;
}}
.field {{ position: relative; width: 500px; height: 500px; }}
.layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
.layer-rotate {{ animation: rotate 60s linear infinite; }}
.layer-reverse {{ animation: rotate-rev 45s linear infinite; }}
@keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
@keyframes rotate-rev {{ from {{ transform: rotate(360deg); }} to {{ transform: rotate(0deg); }} }}
.metadata {{
  position: absolute; bottom: 30px; left: 50%;
  transform: translateX(-50%); text-align: center;
  font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
  color: hsl({bh}, 40%, 50%); opacity: 0.5;
}}
.metadata .title {{
  font-size: 1.1rem; margin-bottom: 6px;
  color: hsl({ch}, 60%, 55%); opacity: 0.8;
}}
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
      <span>LENSES: {lenses}</span>
      <span>VṚTTIS: {vrttis}</span>
      <span>DR: {dr}</span>
      <span>0 ≐ 1</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "0 ≐ 1"
    for l in text.split("\n")[:3]:
        if l.startswith("# "):
            title = l[2:].strip()
            break
    svg = gen_svg(g)
    return HTML_TEMPLATE.format(
        title=title, svg=svg,
        bh=g["base_hue"], ch=g["core_hue"],
        lenses=e["lenses"], vrttis=e["vrttis"], dr=g["dr"],
    )

def main():
    text = read_article()
    e = extract(text)
    g = compute_geometry(e)
    print("Artikel 001 — 0 ≐ 1")
    for k, v in [
        ("Lensen", e["lenses"]), ("Vṛttis", e["vrttis"]),
        ("Digital Root", e["dr"]), ("3-6-9", e["has_369"]),
        ("Agni", e["has_agni"]), ("Woorden", e["word_count"]),
        ("Lagen", len(g["layers"])),
    ]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
