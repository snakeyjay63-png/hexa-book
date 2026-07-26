#!/usr/bin/env python3
"""
Artikel 002 — Terugkeerpad en Frequentie

Geometrie afgeleid uit de tekst:
- 432 Hz → centrale cirkel (spectral centroid)
- Forward cycle: 4 golven → 4 buitenpunten
- Return cycle: 1 golf → 1 binnenpunt (compressie 4→1)
- DR-invariant: 9 → nega-lagen
- ℱ fractaalveld → hexa-structuur
- nidrā → kruisverwijzingen als bruggen
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-002.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "02-terugkeerpad.art.html")

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

    has_432 = "432" in text
    has_fractaal = "fractaal" in text or "ℱ" in text
    has_nidra = "nidrā" in text or "nidra" in text

    # Tel verwijzingen naar cycli/stappen
    cycle_refs = text.count("R'") + text.count("E'") + text.count("C'")
    forward_refs = text.count("C(") + text.count("E(") + text.count("R(")

    # 4 artikelen gelinkt
    linked = sum(1 for n in ["002", "011", "012", "018"] if n in text)

    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "line_count": len(lines),
        "has_432": has_432, "has_fractaal": has_fractaal,
        "has_nidra": has_nidra,
        "cycle_refs": cycle_refs, "forward_refs": forward_refs,
        "linked_articles": linked,
    }

def compute_geometry(e):
    cx, cy = 250, 250
    freq = 432 if e["has_432"] else int(e["hash"][:6], 16) % 1000 + 200
    base_hue = (freq % 360)  # 432 → 72 (goud/groen)
    return_hue = (base_hue + 180) % 360

    # Forward cyclus: 4 golven als buitenring
    forward_pts = []
    for i in range(4):
        angle = (math.pi / 2) * i - math.pi / 2
        forward_pts.append({
            "x": cx + 180 * math.cos(angle),
            "y": cy + 180 * math.sin(angle),
            "hue": (base_hue + i * 30) % 360,
        })

    # Return cyclus: 1 golf als kern
    return_core = {"x": cx, "y": cy, "r": 12, "hue": return_hue}

    # Hexa-lagen (fractaalveld)
    layer_count = 3 if e["has_fractaal"] else 2
    layers = []
    for i in range(layer_count):
        n_sides = 6
        radius = 120 - i * 25
        hue = (base_hue + i * 40) % 360
        pts = []
        for j in range(n_sides):
            angle = (2 * math.pi * j / n_sides) + (i * 0.2)
            pts.append("{:.1f},{:.1f}".format(cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        layers.append({"points": " ".join(pts), "hue": hue, "opacity": 0.5 - i * 0.12})

    # DR invariant marker (9)
    dr_ring_pts = []
    for i in range(9):
        angle = (2 * math.pi * i / 9) - math.pi / 2
        dr_ring_pts.append({
            "x": cx + 210 * math.cos(angle),
            "y": cy + 210 * math.sin(angle),
        })

    # nidrā bruggen (kruisverwijzingen)
    bridge_pts = []
    for i in range(e["linked_articles"]):
        angle = (math.pi / 3) * i + math.pi / 6
        bridge_pts.append({
            "x": cx + 150 * math.cos(angle),
            "y": cy + 150 * math.sin(angle),
            "hue": (return_hue + i * 50) % 360,
        })

    return {
        "cx": cx, "cy": cy,
        "freq": freq, "base_hue": base_hue, "return_hue": return_hue,
        "forward_pts": forward_pts, "return_core": return_core,
        "layers": layers, "dr_ring_pts": dr_ring_pts,
        "bridge_pts": bridge_pts,
        "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    bh, rh = g["base_hue"], g["return_hue"]
    parts = []

    # DR-invariant ring (9 punten)
    for pt in g["dr_ring_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="2" fill="hsl({},40%,50%)" opacity="0.3"/>'.format(
            pt["x"], pt["y"], bh))

    # Hexa-lagen (fractaalveld)
    for lay in g["layers"]:
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},{},{}%)" stroke-width="1" opacity="{}"/>'.format(
            lay["points"], lay["hue"], 55, 50, lay["opacity"]))

    # Forward cyclus (4 buitenpunten + lijnen)
    for pt in g["forward_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="4" fill="hsl({},70%,55%)" opacity="0.8"/>'.format(
            pt["x"], pt["y"], pt["hue"]))
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},50%,50%)" stroke-width="0.5" opacity="0.2"/>'.format(
            cx, cy, pt["x"], pt["y"], bh))

    # Return cyclus (kern)
    rc = g["return_core"]
    parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="hsl({},80%,55%)" opacity="0.9"/>'.format(
        rc["x"], rc["y"], rc["r"], rc["hue"]))
    # Pulse ring
    parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="none" stroke="hsl({},60%,50%)" stroke-width="1" opacity="0.4"/>'.format(
        rc["x"], rc["y"], rc["r"] + 6, rc["hue"]))

    # nidrā bruggen
    for pt in g["bridge_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="2.5" fill="hsl({},50%,50%)" opacity="0.6"/>'.format(
            pt["x"], pt["y"], pt["hue"]))
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},40%,45%)" stroke-width="0.8" opacity="0.25"/>'.format(
            cx, cy, pt["x"], pt["y"], bh))

    # Compressie-lijn: 4→1
    for pt in g["forward_pts"]:
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},50%,50%)" stroke-width="0.3" opacity="0.15"/>'.format(
            pt["x"], pt["y"], rc["x"], rc["y"], rh))

    # Frequentie vonken
    random.seed(g["dr"])
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(30, 100)
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="0.8" fill="hsl({},70%,60%)" opacity="0.4"/>'.format(
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
body {{
  background: #06060a; color: #d4d4e0;
  font-family: 'Instrument Sans', -apple-system, sans-serif;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-height: 100vh; overflow: hidden;
}}
.field {{ position: relative; width: 500px; height: 500px; }}
.layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
.layer-rotate {{ animation: rotate 50s linear infinite; }}
.layer-reverse {{ animation: rotate-rev 40s linear infinite; }}
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
  color: hsl({rh}, 60%, 55%); opacity: 0.8;
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
      <span>FREQ: {freq}Hz</span>
      <span>FORWARD: 4</span>
      <span>RETURN: 1</span>
      <span>DR: {dr}</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "Terugkeerpad en Frequentie"
    for l in text.split("\n")[:3]:
        if l.startswith("# "):
            title = l[2:].strip()
            break
    svg = gen_svg(g)
    return HTML_TEMPLATE.format(
        title=title, svg=svg,
        bh=g["base_hue"], rh=g["return_hue"],
        freq=g["freq"], dr=g["dr"],
    )

def main():
    text = read_article()
    e = extract(text)
    g = compute_geometry(e)
    print("Artikel 002 — Terugkeerpad en Frequentie")
    for k, v in [
        ("Freq", g["freq"]), ("DR", e["dr"]),
        ("Forward", e["forward_refs"]), ("Return", e["cycle_refs"]),
        ("Fractaal", e["has_fractaal"]), ("nidrā", e["has_nidra"]),
        ("Gelinkt", e["linked_articles"]), ("Woorden", e["word_count"]),
    ]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
