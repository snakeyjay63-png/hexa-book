#!/usr/bin/env python3
"""Artikel 015 — Dimensie 12: Logos. ∞→0, onbegrensde differentiatie."""
import hashlib, math, os, random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-015.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "15-dimensie-12.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f: return f.read()
def digital_root(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": h, "dr": digital_root(int(h[:6], 16)), "word_count": len(text.split()),
            "nidra_links": sum(1 for n in ["002", "001", "017"] if n in text),
            "has_infinity": "∞" in text}
def compute_geometry(e):
    cx, cy = 250, 250; base_hue = 0  # rood = logos/woord
    # ∞→0 spiral — oneindige differentiatie die terugkeert naar nul
    spiral_pts = []
    for i in range(300):
        angle = math.pi * 2 * i / 20
        r = 200 * math.exp(-i / 200)
        spiral_pts.append({"x": cx + r * math.cos(angle), "y": cy + r * math.sin(angle)})
    # 12 = 2⁶ × ¾ → 12 differentiatie-punten
    diff_pts = []
    for j in range(12):
        angle = 2 * math.pi * j / 12
        diff_pts.append({"x": cx + 180 * math.cos(angle), "y": cy + 180 * math.sin(angle)})
    return {"cx": cx, "cy": cy, "base_hue": base_hue, "spiral_pts": spiral_pts,
            "diff_pts": diff_pts, "dr": e["dr"]}
def gen_svg(g):
    parts = []; cx, cy = g["cx"], g["cy"]; bh = g["base_hue"]
    # ∞→0 spiral
    path = "M {:.1f},{:.1f}".format(g["spiral_pts"][0]["x"], g["spiral_pts"][0]["y"])
    for pt in g["spiral_pts"][1:]:
        path += " L {:.1f},{:.1f}".format(pt["x"], pt["y"])
    parts.append('<path d="{}" fill="none" stroke="hsl({},60%,50%)" stroke-width="1" opacity="0.4"/>'.format(path, bh))
    # 12 differentiatie-punten
    for p in g["diff_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="hsl({},60%,55%)" opacity="0.5"/>'.format(p["x"], p["y"], bh))
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},20%,30%)" stroke-width="0.3" opacity="0.1"/>'.format(cx, cy, p["x"], p["y"], bh))
    # Nul centrum
    parts.append('<circle cx="{}" cy="{}" r="6" fill="hsl({},80%,65%)" opacity="0.9"/>'.format(cx, cy, bh))
    return "\n".join(parts)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#06060a;color:#d4d4e0;font-family:'Instrument Sans',-apple-system,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}}
.field{{position:relative;width:500px;height:500px}}.layer{{position:absolute;top:0;left:0;width:100%;height:100%}}
.layer-rotate{{animation:rotate 50s linear infinite}}@keyframes rotate{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
.metadata{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:hsl({bh},40%,50%);opacity:0.5}}
.metadata .title{{font-size:1.1rem;margin-bottom:6px;color:hsl({bh},60%,55%);opacity:0.8}}
.metadata .params{{display:flex;gap:12px;justify-content:center}}
</style></head><body><div class="field"><div class="layer layer-rotate">
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">{svg}</svg></div>
<div class="metadata"><div class="title">{title}</div><div class="params">
<span>∞→0</span><span>12=2⁶×¾</span><span>DR:{dr}</span></div></div></div></body></html>"""
def gen_html(g, e, text):
    title = "Dimensie 12: Logos"
    for l in text.split("\n")[:3]:
        if l.startswith("# "): title = l[2:].strip(); break
    return HTML_TEMPLATE.format(title=title, svg=gen_svg(g), bh=g["base_hue"], dr=g["dr"])
def main():
    text = read_article(); e = extract(text); g = compute_geometry(e)
    print("Artikel 015 — Dimensie 12: Logos")
    for k, v in [("DR", e["dr"]), ("∞", e["has_infinity"]), ("nidrā", e["nidra_links"])]:
        print("  {}: {}".format(k, v))
    with open(OUTPUT, "w", encoding="utf-8") as f: f.write(gen_html(g, e, text))
    print("→ {}".format(OUTPUT))
if __name__ == "__main__": main()
