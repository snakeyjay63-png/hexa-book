#!/usr/bin/env python3
"""Artikel 009 — Dimensie 6: De Terugkeer Vormt Zich. 3×2=6, verdubbeling."""
import hashlib, math, os, random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-009.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "09-dimensie-6.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f: return f.read()
def digital_root(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": h, "dr": digital_root(int(h[:6], 16)), "word_count": len(text.split()),
            "nidra_links": sum(1 for n in ["012", "017"] if n in text), "has_64": "64" in text}
def compute_geometry(e):
    cx, cy = 250, 250; base_hue = 270  # paars = vorming
    # 6 hoeken — terugkeer die zich vormt door verdubbeling (3×2=6)
    hex_pts = []
    for i in range(6):
        angle = 2 * math.pi * i / 6 - math.pi / 6
        hex_pts.append({"x": cx + 140 * math.cos(angle), "y": cy + 140 * math.sin(angle)})
    # 64 staten (subdivisies)
    states = []
    for i in range(8):
        for j in range(8):
            angle = 2 * math.pi * (i * 8 + j) / 64
            r = 170 + random.uniform(-5, 5)
            states.append({"x": cx + r * math.cos(angle), "y": cy + r * math.sin(angle)})
    # 3 binnenlagen (NPR)
    layers = []
    for k, (n, label) in enumerate([(3, "N"), (6, "P"), (9, "R")]):
        pts = []
        r = 40 + k * 30
        for j in range(n):
            a = 2 * math.pi * j / n + k * 0.1
            pts.append("{:.1f},{:.1f}".format(cx + r * math.cos(a), cy + r * math.sin(a)))
        layers.append({"pts": " ".join(pts), "hue": (base_hue + k * 30) % 360})
    return {"cx": cx, "cy": cy, "base_hue": base_hue, "hex_pts": hex_pts, "states": states, "layers": layers, "dr": e["dr"]}
def gen_svg(g):
    parts = []; cx, cy = g["cx"], g["cy"]; bh = g["base_hue"]
    for lay in g["layers"]:
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},60%,50%)" stroke-width="1.5" opacity="0.5"/>'.format(lay["pts"], lay["hue"]))
    # Hexagon
    h = " ".join("{:.1f},{:.1f}".format(p["x"], p["y"]) for p in g["hex_pts"])
    parts.append('<polygon points="{}" fill="none" stroke="hsl({},70%,55%)" stroke-width="2" opacity="0.7"/>'.format(h, bh))
    # Lijnen van centrum naar hex hoeken
    for p in g["hex_pts"]:
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},30%,40%)" stroke-width="0.5" opacity="0.2"/>'.format(cx, cy, p["x"], p["y"], bh))
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="hsl({},60%,55%)" opacity="0.6"/>'.format(p["x"], p["y"], bh))
    # Staten
    for s in g["states"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="0.8" fill="hsl({},30%,45%)" opacity="0.15"/>'.format(s["x"], s["y"], bh))
    parts.append('<circle cx="{}" cy="{}" r="5" fill="hsl({},80%,65%)" opacity="0.9"/>'.format(cx, cy, bh))
    return "\n".join(parts)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#06060a;color:#d4d4e0;font-family:'Instrument Sans',-apple-system,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}}
.field{{position:relative;width:500px;height:500px}}.layer{{position:absolute;top:0;left:0;width:100%;height:100%}}
.layer-rotate{{animation:rotate 65s linear infinite}}@keyframes rotate{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
.metadata{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:hsl({bh},40%,50%);opacity:0.5}}
.metadata .title{{font-size:1.1rem;margin-bottom:6px;color:hsl({bh},60%,55%);opacity:0.8}}
.metadata .params{{display:flex;gap:12px;justify-content:center}}
</style></head><body><div class="field"><div class="layer layer-rotate">
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">{svg}</svg></div>
<div class="metadata"><div class="title">{title}</div><div class="params">
<span>3×2=6</span><span>STATEN:{states}</span><span>DR:{dr}</span></div></div></div></body></html>"""
def gen_html(g, e, text):
    title = "Dimensie 6: De Terugkeer Vormt Zich"
    for l in text.split("\n")[:3]:
        if l.startswith("# "): title = l[2:].strip(); break
    return HTML_TEMPLATE.format(title=title, svg=gen_svg(g), bh=g["base_hue"], states=len(g["states"]), dr=g["dr"])
def main():
    text = read_article(); e = extract(text); g = compute_geometry(e)
    print("Artikel 009 — Dimensie 6: De Terugkeer Vormt Zich")
    for k, v in [("DR", e["dr"]), ("64", e["has_64"]), ("nidrā", e["nidra_links"])]:
        print("  {}: {}".format(k, v))
    with open(OUTPUT, "w", encoding="utf-8") as f: f.write(gen_html(g, e, text))
    print("→ {}".format(OUTPUT))
if __name__ == "__main__": main()
