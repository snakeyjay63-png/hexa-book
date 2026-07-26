#!/usr/bin/env python3
"""
Artikel 004 — F: Het ReturnMedium

Geometrie afgeleid uit de tekst:
- Water/medium → vloeibare patronen (geen harde randen)
- 2 niveaus feature-extractie: R_raw (buiten) ↔ R_audio (binnen)
- 432 Hz ↔ 1354.75 Hz (verschil tussen oscillator en FFT)
- nidrā → 3 bruggen (002, 012, 017)
- Medium = geen lens, maar dragend vlak
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-004.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "04-returnmedium.art.html")

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
    lines = text.split("\n")

    has_water = "water" in text or "ماء" in text
    has_nidra = "nidrā" in text or "nidra" in text
    has_432 = "432" in text
    has_1354 = "1354" in text

    # Tel features
    raw_features = text.count("component_centroid") + text.count("rms_raw") + text.count("raw_peak") + text.count("DR_signature")
    audio_features = text.count("signal_centroid") + text.count("rms_normalized") + text.count("normalized_peak") + text.count("dominant_frequency")

    # nidrā verwijzingen
    nidra_links = sum(1 for n in ["002", "012", "017"] if n in text)

    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "line_count": len(lines),
        "has_water": has_water, "has_nidra": has_nidra,
        "has_432": has_432, "has_1354": has_1354,
        "raw_features": raw_features, "audio_features": audio_features,
        "nidra_links": nidra_links,
    }

def compute_geometry(e):
    cx, cy = 250, 250
    base_hue = 200 if e["has_water"] else int(e["hash"][:6], 16) % 360

    # Medium: water-lagen (vloeibaar, geen harde randen)
    water_layers = []
    for i in range(5):
        pts = []
        n_pts = 24
        r = 100 + i * 20
        for j in range(n_pts):
            angle = (2 * math.pi * j / n_pts)
            # Vloeibare variatie
            r_var = r + random.uniform(-5, 5)
            pts.append("{:.1f},{:.1f}".format(cx + r_var * math.cos(angle), cy + r_var * math.sin(angle)))
        water_layers.append({"points": " ".join(pts), "hue": (base_hue + i * 8) % 360, "opacity": 0.2 - i * 0.03})

    # R_raw ring (buiten)
    raw_pts = []
    for i in range(e["raw_features"]):
        angle = (2 * math.pi * i / e["raw_features"]) - math.pi / 2
        raw_pts.append({
            "x": cx + 160 * math.cos(angle),
            "y": cy + 160 * math.sin(angle),
            "hue": (base_hue + 30) % 360,
        })

    # R_audio ring (binnen)
    audio_pts = []
    for i in range(e["audio_features"]):
        angle = (2 * math.pi * i / e["audio_features"]) - math.pi / 2
        audio_pts.append({
            "x": cx + 100 * math.cos(angle),
            "y": cy + 100 * math.sin(angle),
            "hue": (base_hue + 180) % 360,
        })

    # Dual-freq kern (432 vs 1354)
    freq_core = {
        "outer": 432 if e["has_432"] else 0,
        "inner": 1354 if e["has_1354"] else 0,
    }

    # nidrā bruggen
    bridge_pts = []
    for i in range(e["nidra_links"]):
        angle = (2 * math.pi * i / 3) + math.pi / 6
        bridge_pts.append({
            "x": cx + 200 * math.cos(angle),
            "y": cy + 200 * math.sin(angle),
        })

    return {
        "cx": cx, "cy": cy, "base_hue": base_hue,
        "water_layers": water_layers,
        "raw_pts": raw_pts, "audio_pts": audio_pts,
        "freq_core": freq_core, "bridge_pts": bridge_pts,
        "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    bh = g["base_hue"]
    parts = []

    # Water-lagen
    for lay in g["water_layers"]:
        parts.append('<polygon points="{}" fill="hsl({},{},{}%)" stroke="hsl({},{},{}%)" stroke-width="0.5" opacity="{}"/>'.format(
            lay["points"], lay["hue"], 40, 15, lay["hue"], 50, 30, lay["opacity"]))

    # nidrā bruggen
    for pt in g["bridge_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="hsl({},40%,50%)" opacity="0.4"/>'.format(
            pt["x"], pt["y"], (bh + 60) % 360))
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},30%,40%)" stroke-width="0.5" opacity="0.2" stroke-dasharray="3,3"/>'.format(
            cx, cy, pt["x"], pt["y"], bh))

    # R_raw punten
    for pt in g["raw_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3.5" fill="hsl({},55%,50%)" opacity="0.6"/>'.format(
            pt["x"], pt["y"], pt["hue"]))
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},35%,45%)" stroke-width="0.5" opacity="0.15"/>'.format(
            cx, cy, pt["x"], pt["y"], bh))

    # R_audio punten
    for pt in g["audio_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="hsl({},60%,55%)" opacity="0.7"/>'.format(
            pt["x"], pt["y"], pt["hue"]))

    # Dual-freq kern
    parts.append('<circle cx="{}" cy="{}" r="18" fill="none" stroke="hsl({},50%,50%)" stroke-width="1.5" opacity="0.5"/>'.format(
        cx, cy, bh))
    parts.append('<circle cx="{}" cy="{}" r="10" fill="hsl({},65%,55%)" opacity="0.8"/>'.format(
        cx, cy, bh))
    parts.append('<circle cx="{}" cy="{}" r="4" fill="hsl({},75%,60%)" opacity="0.9"/>'.format(
        cx, cy, (bh + 180) % 360))

    # Vonken
    random.seed(g["dr"])
    for _ in range(10):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(20, 80)
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
body {{
  background: #06060a; color: #d4d4e0;
  font-family: 'Instrument Sans', -apple-system, sans-serif;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-height: 100vh; overflow: hidden;
}}
.field {{ position: relative; width: 500px; height: 500px; }}
.layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
.layer-rotate {{ animation: rotate 65s linear infinite; }}
@keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
.metadata {{
  position: absolute; bottom: 30px; left: 50%;
  transform: translateX(-50%); text-align: center;
  font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
  color: hsl({bh}, 40%, 50%); opacity: 0.5;
}}
.metadata .title {{
  font-size: 1.1rem; margin-bottom: 6px;
  color: hsl({bh}, 55%, 55%); opacity: 0.8;
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
      <span>MEDIUM: water</span>
      <span>R_raw: {raw}</span>
      <span>R_audio: {audio}</span>
      <span>DR: {dr}</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "F: Het ReturnMedium"
    for l in text.split("\n")[:3]:
        if l.startswith("# "):
            title = l[2:].strip()
            break
    svg = gen_svg(g)
    return HTML_TEMPLATE.format(
        title=title, svg=svg,
        bh=g["base_hue"],
        raw=len(g["raw_pts"]), audio=len(g["audio_pts"]),
        dr=g["dr"],
    )

def main():
    text = read_article()
    e = extract(text)
    g = compute_geometry(e)
    print("Artikel 004 — ReturnMedium")
    for k, v in [
        ("DR", e["dr"]), ("Water", e["has_water"]),
        ("R_raw", e["raw_features"]), ("R_audio", e["audio_features"]),
        ("nidrā", e["nidra_links"]), ("Woorden", e["word_count"]),
    ]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
