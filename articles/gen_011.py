#!/usr/bin/env python3
"""Artikel 011 — Synth en Fractaalveld. Synth-operator, fractaal projecties, Sanskrit."""
import hashlib, math, os, random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-011.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "11-synth-fractaal.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f: return f.read()
def digital_root(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": h, "dr": digital_root(int(h[:6], 16)), "word_count": len(text.split()),
            "has_sanskrit": "संस्कृतं" in text or "सिंथेसिर्" in text,
            "has_fractal": "fractal" in text.lower() or "fractaal" in text.lower(),
            "has_water": "water" in text.lower() or "ρ_water" in text}
def compute_geometry(e):
    cx, cy = 250, 250; base_hue = 190  # blauw-groen = synth + water
    # Fractaal boom-structuur
    branches = []
    def branch(x, y, angle, depth, length):
        if depth <= 0: return
        x2 = x + length * math.cos(angle)
        y2 = y + length * math.sin(angle)
        branches.append({"x1": x, "y1": y, "x2": x2, "y2": y2, "depth": depth, "hue": (base_hue + (3 - depth) * 30) % 360})
        branch(x2, y2, angle - 0.5, depth - 1, length * 0.7)
        branch(x2, y2, angle + 0.5, depth - 1, length * 0.7)
    branch(cx, cy + 150, -math.pi / 2, 6, 60)
    # Synth waveform (sine wave)
    wave_pts = []
    for i in range(200):
        x = 50 + i * 2
        y = cy + 40 * math.sin(2 * math.pi * i / 40) * math.exp(-i / 200)
        wave_pts.append("{:.1f},{:.1f}".format(x, y))
    # C-keten punten (frequentie basis)
    chain_pts = []
    for i in range(11):
        angle = 2 * math.pi * i / 11
        r = 180
        chain_pts.append({"x": cx + r * math.cos(angle), "y": cy + r * math.sin(angle)})
    return {"cx": cx, "cy": cy, "base_hue": base_hue, "branches": branches,
            "wave_path": " ".join(wave_pts), "chain_pts": chain_pts, "dr": e["dr"]}
def gen_svg(g):
    parts = []; cx, cy = g["cx"], g["cy"]; bh = g["base_hue"]
    # Fractaal boom
    for b in g["branches"]:
        w = b["depth"] * 0.8
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},60%,55%)" stroke-width="{}" opacity="0.5"/>'.format(b["x1"], b["y1"], b["x2"], b["y2"], b["hue"], w))
    # Waveform
    parts.append('<path d="M {}" fill="none" stroke="hsl({},50%,50%)" stroke-width="1" opacity="0.3"/>'.format(g["wave_path"], bh))
    # C-keten
    for p in g["chain_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="hsl({},60%,55%)" opacity="0.5"/>'.format(p["x"], p["y"], bh))
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},20%,35%)" stroke-width="0.3" opacity="0.1"/>'.format(cx, cy, p["x"], p["y"], bh))
    parts.append('<circle cx="{}" cy="{}" r="5" fill="hsl({},80%,65%)" opacity="0.9"/>'.format(cx, cy, bh))
    return "\n".join(parts)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#06060a;color:#d4d4e0;font-family:'Instrument Sans',-apple-system,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}}
.field{{position:relative;width:500px;height:500px}}.layer{{position:absolute;top:0;left:0;width:100%;height:100%}}
.layer-rotate{{animation:rotate 90s linear infinite}}@keyframes rotate{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
.metadata{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:hsl({bh},40%,50%);opacity:0.5}}
.metadata .title{{font-size:1.1rem;margin-bottom:6px;color:hsl({bh},60%,55%);opacity:0.8}}
.metadata .params{{display:flex;gap:12px;justify-content:center}}
</style></head><body><div class="field"><div class="layer layer-rotate">
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">{svg}</svg></div>
<div class="metadata"><div class="title">{title}</div><div class="params">
<span>SYNTH</span><span>TAKKEN:{branches}</span><span>DR:{dr}</span></div></div></div></body></html>"""
def gen_html(g, e, text):
    title = "Synth en Fractaalveld"
    for l in text.split("\n")[:3]:
        if l.startswith("# "): title = l[2:].strip(); break
    return HTML_TEMPLATE.format(title=title, svg=gen_svg(g), bh=g["base_hue"], branches=len(g["branches"]), dr=g["dr"])
def main():
    text = read_article(); e = extract(text); g = compute_geometry(e)
    print("Artikel 011 — Synth en Fractaalveld")
    for k, v in [("DR", e["dr"]), ("Sanskrit", e["has_sanskrit"]), ("fractal", e["has_fractal"])]:
        print("  {}: {}".format(k, v))
    with open(OUTPUT, "w", encoding="utf-8") as f: f.write(gen_html(g, e, text))
    print("→ {}".format(OUTPUT))
if __name__ == "__main__": main()
