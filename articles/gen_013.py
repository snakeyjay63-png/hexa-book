#!/usr/bin/env python3
"""Artikel 013 — Dimensie 8: Onzichtbaar. 8=2³, onzichtbaar door simpelheid."""
import hashlib, math, os, random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-013.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "13-dimensie-8.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f: return f.read()
def digital_root(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": h, "dr": digital_root(int(h[:6], 16)), "word_count": len(text.split()),
            "nidra_links": sum(1 for n in ["001", "017", "002"] if n in text)}
def compute_geometry(e):
    cx, cy = 250, 250; base_hue = 220  # donkerblauw = onzichtbaar
    # 2³ = 8 onzichtbare knopen — zichtbaar alleen door hun afwezigheid
    cube_pts = []
    # Cube projectie (8 hoekpunten)
    for i in range(8):
        x = ((i >> 0) & 1) * 2 - 1
        y = ((i >> 1) & 1) * 2 - 1
        z = ((i >> 2) & 1) * 2 - 1
        # Projecteer 3D→2D
        px = cx + (x * 80 - z * 40)
        py = cy + (y * 80 - z * 20)
        cube_pts.append({"x": px, "y": py, "z": z, "i": i})
    # 8 onzichtbare zones (cirkels met lage opacity)
    invisible_zones = []
    for p in cube_pts:
        invisible_zones.append({"x": p["x"], "y": p["y"], "r": 20 + abs(p["z"]) * 10})
    # Verborgen verbindingen
    edges = []
    for i, p1 in enumerate(cube_pts):
        for j, p2 in enumerate(cube_pts):
            if bin(i ^ j).count("1") == 1:  # cube edge
                edges.append((p1, p2))
    return {"cx": cx, "cy": cy, "base_hue": base_hue, "cube_pts": cube_pts,
            "zones": invisible_zones, "edges": edges, "dr": e["dr"]}
def gen_svg(g):
    parts = []; cx, cy = g["cx"], g["cy"]; bh = g["base_hue"]
    # Onzichtbare zones
    for z in g["zones"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="hsl({},20%,8%)" stroke="hsl({},30%,30%)" stroke-width="0.5" opacity="0.2"/>'.format(z["x"], z["y"], z["r"], bh, bh))
    # Cube edges (bijna onzichtbaar)
    for p1, p2 in g["edges"]:
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},20%,25%)" stroke-width="0.5" opacity="0.15"/>'.format(p1["x"], p1["y"], p2["x"], p2["y"], bh))
    # 2³ punten
    for p in g["cube_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="2" fill="hsl({},30%,40%)" opacity="0.3"/>'.format(p["x"], p["y"], bh))
    # Centrum (de enige zichtbare punt)
    parts.append('<circle cx="{}" cy="{}" r="3" fill="hsl({},40%,50%)" opacity="0.6"/>'.format(cx, cy, bh))
    return "\n".join(parts)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#06060a;color:#d4d4e0;font-family:'Instrument Sans',-apple-system,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}}
.field{{position:relative;width:500px;height:500px}}.layer{{position:absolute;top:0;left:0;width:100%;height:100%}}
.layer-rotate{{animation:rotate 85s linear infinite}}@keyframes rotate{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
.metadata{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:hsl({bh},40%,50%);opacity:0.5}}
.metadata .title{{font-size:1.1rem;margin-bottom:6px;color:hsl({bh},60%,55%);opacity:0.8}}
.metadata .params{{display:flex;gap:12px;justify-content:center}}
</style></head><body><div class="field"><div class="layer layer-rotate">
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">{svg}</svg></div>
<div class="metadata"><div class="title">{title}</div><div class="params">
<span>2³=8</span><span>ONZICHTBAAR</span><span>DR:{dr}</span></div></div></div></body></html>"""
def gen_html(g, e, text):
    title = "Dimensie 8: Onzichtbaar"
    for l in text.split("\n")[:3]:
        if l.startswith("# "): title = l[2:].strip(); break
    return HTML_TEMPLATE.format(title=title, svg=gen_svg(g), bh=g["base_hue"], dr=g["dr"])
def main():
    text = read_article(); e = extract(text); g = compute_geometry(e)
    print("Artikel 013 — Dimensie 8: Onzichtbaar")
    for k, v in [("DR", e["dr"]), ("nidrā", e["nidra_links"])]:
        print("  {}: {}".format(k, v))
    with open(OUTPUT, "w", encoding="utf-8") as f: f.write(gen_html(g, e, text))
    print("→ {}".format(OUTPUT))
if __name__ == "__main__": main()
