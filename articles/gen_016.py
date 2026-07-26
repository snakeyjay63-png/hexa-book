#!/usr/bin/env python3
"""Artikel 016 — Dimensie 13: Taal, Veld, Soevereiniteit. Elke taal kan het veld dragen."""
import hashlib, math, os, random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-016.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "16-dimensie-13.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f: return f.read()
def digital_root(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": h, "dr": digital_root(int(h[:6], 16)), "word_count": len(text.split()),
            "nidra_links": sum(1 for n in ["001", "017", "012"] if n in text)}
def compute_geometry(e):
    cx, cy = 250, 250; base_hue = 150  # groen = soevereiniteit
    # 4 taal-lensen (A,B,C,D) als kardinaal punten
    lenses = []
    labels = ["A", "B", "C", "D"]
    for i, label in enumerate(labels):
        angle = math.pi / 2 * i - math.pi / 2
        lenses.append({"x": cx + 150 * math.cos(angle), "y": cy + 150 * math.sin(angle), "label": label})
    # 13 = 11 + 2 → 11 rode draad + 2 extra
    field_pts = []
    for j in range(13):
        angle = 2 * math.pi * j / 13
        r = 100 + random.uniform(-20, 20)
        field_pts.append({"x": cx + r * math.cos(angle), "y": cy + r * math.sin(angle)})
    # Veld-lijnen
    veld_lines = []
    for i, p in enumerate(field_pts):
        for j, q in enumerate(field_pts):
            if j > i and random.random() < 0.15:
                veld_lines.append((p, q))
    return {"cx": cx, "cy": cy, "base_hue": base_hue, "lenses": lenses,
            "field_pts": field_pts, "veld_lines": veld_lines, "dr": e["dr"]}
def gen_svg(g):
    parts = []; cx, cy = g["cx"], g["cy"]; bh = g["base_hue"]
    # Veld-lijnen
    for p, q in g["veld_lines"]:
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},20%,30%)" stroke-width="0.3" opacity="0.1"/>'.format(p["x"], p["y"], q["x"], q["y"], bh))
    # 4 lens punten
    for l in g["lenses"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="5" fill="hsl({},60%,55%)" opacity="0.6"/>'.format(l["x"], l["y"], bh))
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},30%,35%)" stroke-width="0.5" opacity="0.2"/>'.format(cx, cy, l["x"], l["y"], bh))
    # 13 veld-punten
    for p in g["field_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="2" fill="hsl({},40%,45%)" opacity="0.3"/>'.format(p["x"], p["y"], bh))
    # Soeverein centrum
    parts.append('<circle cx="{}" cy="{}" r="6" fill="hsl({},80%,65%)" opacity="0.9"/>'.format(cx, cy, bh))
    return "\n".join(parts)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#06060a;color:#d4d4e0;font-family:'Instrument Sans',-apple-system,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}}
.field{{position:relative;width:500px;height:500px}}.layer{{position:absolute;top:0;left:0;width:100%;height:100%}}
.layer-rotate{{animation:rotate 70s linear infinite}}@keyframes rotate{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
.metadata{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:hsl({bh},40%,50%);opacity:0.5}}
.metadata .title{{font-size:1.1rem;margin-bottom:6px;color:hsl({bh},60%,55%);opacity:0.8}}
.metadata .params{{display:flex;gap:12px;justify-content:center}}
</style></head><body><div class="field"><div class="layer layer-rotate">
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">{svg}</svg></div>
<div class="metadata"><div class="title">{title}</div><div class="params">
<span>11+2=13</span><span>4 LENZEN</span><span>DR:{dr}</span></div></div></div></body></html>"""
def gen_html(g, e, text):
    title = "Dimensie 13: Taal, Veld, Soevereiniteit"
    for l in text.split("\n")[:3]:
        if l.startswith("# "): title = l[2:].strip(); break
    return HTML_TEMPLATE.format(title=title, svg=gen_svg(g), bh=g["base_hue"], dr=g["dr"])
def main():
    text = read_article(); e = extract(text); g = compute_geometry(e)
    print("Artikel 016 — Dimensie 13: Taal, Veld, Soevereiniteit")
    for k, v in [("DR", e["dr"]), ("nidrā", e["nidra_links"])]:
        print("  {}: {}".format(k, v))
    with open(OUTPUT, "w", encoding="utf-8") as f: f.write(gen_html(g, e, text))
    print("→ {}".format(OUTPUT))
if __name__ == "__main__": main()
