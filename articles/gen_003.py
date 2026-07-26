#!/usr/bin/env python3
"""
Artikel 003 — E: Het Audio-Veld (Canoniek Contract)

Geometrie afgeleid uit de tekst:
- 4 lenzen convergerend → 1 audio-veld (5de stap = geen 5de lens)
- Signaal-golven → sinusoidale patronen
- Normalisatie → grenscirkel (peak ≤ 1)
- NPR-fasen → 3 sub-ringen (Noise, Pattern, Return)
- Type-contract → producer↔consumer structuur
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-003.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "03-audio-veld.art.html")

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

    has_wave = "Wave" in text or "sin" in text
    has_normalize = "Normalize" in text or "normalize" in text
    has_npr = "NPR" in text or "ρ_NPR" in text

    # Tel type-definities en operators
    types = text.count(":=") + text.count(":")
    operators = sum(1 for kw in ["E_raw", "E_audio", "R_raw", "R_audio", "Normalize"] if kw in text)

    # 4 lens verwijzingen
    lens_refs = sum(1 for kw in ["lens", "lenzen", "عدسة", "लेन्स"] if kw in text.lower())

    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "line_count": len(lines),
        "has_wave": has_wave, "has_normalize": has_normalize,
        "has_npr": has_npr,
        "type_defs": types, "operators": operators,
        "lens_refs": lens_refs,
    }

def compute_geometry(e):
    cx, cy = 250, 250
    base_hue = int(e["hash"][:6], 16) % 360

    # 4 convergerende lenzen
    lens_pts = []
    lens_hues = [(30,65,55), (120,55,50), (200,60,50), (280,50,55)]
    for i in range(4):
        angle = (math.pi / 2) * i - math.pi / 2
        lens_pts.append({
            "x": cx + 170 * math.cos(angle),
            "y": cy + 170 * math.sin(angle),
            "hue": lens_hues[i],
        })

    # Audio-veld kern (5de stap, geen 5de lens — maar convergentie-punt)
    audio_core = {"x": cx, "y": cy, "r": 15, "hue": (base_hue + 30) % 360}

    # Normalisatie-grens (peak ≤ 1)
    norm_radius = 130

    # NPR-fasen (3 sub-ringen)
    npr_layers = []
    if e["has_npr"]:
        for i, (label, offset) in enumerate([("N", 0), ("P", 120), ("R", 240)]):
            r = 90 + i * 15
            pts = []
            n_pts = 12
            for j in range(n_pts):
                angle = (2 * math.pi * j / n_pts) + (offset * math.pi / 180)
                pts.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
            npr_layers.append({"points": " ".join(pts), "hue": (base_hue + offset) % 360, "label": label})

    # Sinusoidale golven
    waves = []
    wave_count = 4
    for w in range(wave_count):
        pts = []
        amplitude = 15 + w * 5
        freq = 3 + w
        for t in range(60):
            t_norm = t / 60.0
            x = cx - 100 + t_norm * 200
            y = cy + 50 * (w - 1.5) + amplitude * math.sin(2 * math.pi * freq * t_norm)
            pts.append("{:.1f},{:.1f}".format(x, y))
        waves.append({"points": " ".join(pts), "hue": (base_hue + w * 45) % 360})

    return {
        "cx": cx, "cy": cy,
        "base_hue": base_hue,
        "lens_pts": lens_pts, "audio_core": audio_core,
        "norm_radius": norm_radius, "npr_layers": npr_layers,
        "waves": waves, "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    bh = g["base_hue"]
    parts = []

    # Normalisatie-grens
    parts.append('<circle cx="{}" cy="{}" r="{}" fill="none" stroke="hsl({},30%,40%)" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>'.format(
        cx, cy, g["norm_radius"], bh))

    # NPR-fasen
    for lay in g["npr_layers"]:
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},{},{}%)" stroke-width="1" opacity="0.35"/>'.format(
            lay["points"], lay["hue"], 50, 45))

    # Golven
    for w in g["waves"]:
        parts.append('<polyline points="{}" fill="none" stroke="hsl({},{},{}%)" stroke-width="1.2" opacity="0.5"/>'.format(
            w["points"], w["hue"], 60, 55))

    # 4 lenzen
    for pt in g["lens_pts"]:
        h, s, l = pt["hue"]
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="5" fill="hsl({},{},{})" opacity="0.7"/>'.format(
            pt["x"], pt["y"], h, s, l))
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},{},{})" stroke-width="0.5" opacity="0.2"/>'.format(
            pt["x"], pt["y"], cx, cy, h, s, l))

    # Audio-veld kern
    ac = g["audio_core"]
    parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="hsl({},70%,55%)" opacity="0.85"/>'.format(
        ac["x"], ac["y"], ac["r"], ac["hue"]))
    # Pulse
    parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="none" stroke="hsl({},50%,50%)" stroke-width="1" opacity="0.3"/>'.format(
        ac["x"], ac["y"], ac["r"] + 8, ac["hue"]))

    # Vonken
    random.seed(g["dr"])
    for _ in range(15):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(20, 100)
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="0.7" fill="hsl({},60%,60%)" opacity="0.3"/>'.format(
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
.layer-rotate {{ animation: rotate 55s linear infinite; }}
@keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
.metadata {{
  position: absolute; bottom: 30px; left: 50%;
  transform: translateX(-50%); text-align: center;
  font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
  color: hsl({bh}, 40%, 50%); opacity: 0.5;
}}
.metadata .title {{
  font-size: 1.1rem; margin-bottom: 6px;
  color: hsl({ah}, 60%, 55%); opacity: 0.8;
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
      <span>LENZEN: 4</span>
      <span>VELD: 5</span>
      <span>WAVES: {waves}</span>
      <span>DR: {dr}</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "E: Het Audio-Veld"
    for l in text.split("\n")[:3]:
        if l.startswith("# "):
            title = l[2:].strip()
            break
    svg = gen_svg(g)
    return HTML_TEMPLATE.format(
        title=title, svg=svg,
        bh=g["base_hue"], ah=g["audio_core"]["hue"],
        waves=len(g["waves"]), dr=g["dr"],
    )

def main():
    text = read_article()
    e = extract(text)
    g = compute_geometry(e)
    print("Artikel 003 — Audio-Veld")
    for k, v in [
        ("DR", e["dr"]), ("Types", e["type_defs"]),
        ("Operators", e["operators"]), ("NPR", e["has_npr"]),
        ("Golven", len(g["waves"])), ("Woorden", e["word_count"]),
    ]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
