#!/usr/bin/env python3
"""
Artikel 005 — Quran-bronroute en lokale Basmala-Abjadroute

Geometrie afgeleid uit de tekst:
- Basmala → 786 → DR 3
- Pipeline-stappen → lineaire route
- Abjad-letterwaardes → karakter-mapping
- Git-commit hash → deterministisch anker
- 3-6-9 validatie → trio-lagen
"""

import hashlib
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-005-quran-basmala-abjad.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "05-quran-route.art.html")

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

    has_basmala = "basmala" in text.lower() or "بسم" in text
    has_786 = "786" in text
    has_369 = "3-6-9" in text or "3–6–9" in text
    has_abjad = "abjad" in text.lower() or "أبجد" in text

    # Pipeline stappen
    pipeline_steps = text.count("→") + text.count("→")

    # Git commit
    import re
    commit_match = re.search(r'[0-9a-f]{40}', text)
    has_commit = commit_match is not None

    return {
        "hash": h, "dr": digital_root(int(h[:6], 16)),
        "word_count": len(words), "line_count": len(lines),
        "has_basmala": has_basmala, "has_786": has_786,
        "has_369": has_369, "has_abjad": has_abjad,
        "pipeline_steps": pipeline_steps, "has_commit": has_commit,
    }

def compute_geometry(e):
    cx, cy = 250, 250
    basmala_val = 786 if e["has_786"] else int(e["hash"][:6], 16) % 1000
    basmala_dr = digital_root(basmala_val)
    base_hue = basmala_dr * 40  # DR 3 → 120 (groen/goud)

    # Pipeline route (lineaire stappen)
    pipeline_pts = []
    steps = min(e["pipeline_steps"], 9)
    for i in range(steps):
        t = i / max(steps - 1, 1)
        angle = math.pi * (1 - t)  # Bogen van boven naar onder
        r = 150 + 30 * math.sin(t * math.pi)
        pipeline_pts.append({
            "x": cx + r * math.cos(angle - math.pi / 2),
            "y": cy + r * math.sin(angle - math.pi / 2),
            "hue": (base_hue + t * 60) % 360,
        })

    # Basmala kern (786 → 3)
    core = {"x": cx, "y": cy, "r": 14, "val": basmala_val, "dr": basmala_dr}

    # 3-6-9 lagen
    layers = []
    if e["has_369"]:
        for i, n in enumerate([3, 6, 9]):
            pts = []
            r = 100 + i * 30
            for j in range(n * 2):
                angle = (2 * math.pi * j / (n * 2)) + (i * 0.1)
                pts.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
            layers.append({"points": " ".join(pts), "hue": (base_hue + n * 15) % 360, "n": n})

    # Abjad letters (28 → tonen 6 prominent)
    abjad_pts = []
    for i in range(6):
        angle = (2 * math.pi * i / 6) - math.pi / 6
        abjad_pts.append({
            "x": cx + 190 * math.cos(angle),
            "y": cy + 190 * math.sin(angle),
            "hue": (base_hue + i * 25) % 360,
        })

    return {
        "cx": cx, "cy": cy, "base_hue": base_hue,
        "pipeline_pts": pipeline_pts, "core": core,
        "layers": layers, "abjad_pts": abjad_pts,
        "dr": e["dr"],
    }

def gen_svg(g):
    cx, cy = g["cx"], g["cy"]
    bh = g["base_hue"]
    parts = []

    # 3-6-9 lagen
    for lay in g["layers"]:
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},{},{}%)" stroke-width="1" opacity="0.4"/>'.format(
            lay["points"], lay["hue"], 50, 45))

    # Pipeline route
    for i, pt in enumerate(g["pipeline_pts"]):
        h = pt["hue"]
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="hsl({},{},{})" opacity="0.7"/>'.format(
            pt["x"], pt["y"], h, 60, 55))
        if i > 0:
            prev = g["pipeline_pts"][i - 1]
            parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},40%,45%)" stroke-width="0.8" opacity="0.3"/>'.format(
                prev["x"], prev["y"], pt["x"], pt["y"], bh))

    # Abjad punten
    for pt in g["abjad_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="2.5" fill="hsl({},45%,50%)" opacity="0.5"/>'.format(
            pt["x"], pt["y"], pt["hue"]))

    # Basmala kern
    c = g["core"]
    parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="hsl({},70%,55%)" opacity="0.85"/>'.format(
        c["x"], c["y"], c["r"], bh))
    parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="none" stroke="hsl({},50%,50%)" stroke-width="1" opacity="0.4"/>'.format(
        c["x"], c["y"], c["r"] + 8, bh))
    # DR marker
    parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="4" fill="hsl({},80%,60%)" opacity="0.9"/>'.format(
        c["x"], c["y"], (bh + 60) % 360))

    # Vonken
    random.seed(g["dr"])
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(20, 120)
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="0.7" fill="hsl({},55%,60%)" opacity="0.3"/>'.format(
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
@keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
.metadata {{
  position: absolute; bottom: 30px; left: 50%;
  transform: translateX(-50%); text-align: center;
  font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
  color: hsl({bh}, 40%, 50%); opacity: 0.5;
}}
.metadata .title {{
  font-size: 1.1rem; margin-bottom: 6px;
  color: hsl({bh}, 60%, 55%); opacity: 0.8;
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
      <span>BASMALA: {basmala}</span>
      <span>DR: {dr}</span>
      <span>STAPPEN: {steps}</span>
      <span>3-6-9: {has369}</span>
    </div>
  </div>
</div>
</body>
</html>"""

def gen_html(g, e, text):
    title = "Quran-bronroute en Basmala-Abjad"
    for l in text.split("\n")[:3]:
        if l.startswith("# "):
            title = l[2:].strip()
            break
    svg = gen_svg(g)
    return HTML_TEMPLATE.format(
        title=title, svg=svg,
        bh=g["base_hue"],
        basmala=g["core"]["val"], dr=g["dr"],
        steps=len(g["pipeline_pts"]), has369="ja" if e["has_369"] else "nee",
    )

def main():
    text = read_article()
    e = extract(text)
    g = compute_geometry(e)
    print("Artikel 005 — Quran-bronroute")
    for k, v in [
        ("DR", e["dr"]), ("Basmala", g["core"]["val"]),
        ("786→DR", g["core"]["dr"]), ("3-6-9", e["has_369"]),
        ("Pipeline", e["pipeline_steps"]), ("Woorden", e["word_count"]),
    ]:
        print("  {}: {}".format(k, v))
    html = gen_html(g, e, text)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("→ {}".format(OUTPUT))

if __name__ == "__main__":
    main()
