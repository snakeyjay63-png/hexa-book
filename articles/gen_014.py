#!/usr/bin/env python3
"""Artikel 014 — Dimensie 11: Eka Routing. Eka=één, 3 lagen, 4 routes."""
import hashlib, math, os, random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-014.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "14-dimensie-11.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f: return f.read()
def digital_root(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": h, "dr": digital_root(int(h[:6], 16)), "word_count": len(text.split()),
            "nidra_links": sum(1 for n in ["001", "012", "017"] if n in text), "has_eka": "eka" in text.lower()}
def compute_geometry(e):
    cx, cy = 250, 250; base_hue = 45  # goud-oranje = eka/één
    # 3 lagen (concentrische ruitjes)
    layers = []
    for k in range(3):
        pts = []
        n = 4 + k * 2
        for j in range(n):
            angle = 2 * math.pi * j / n + k * 0.15
            r = 50 + k * 50
            pts.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
        layers.append({"pts": " ".join(pts), "hue": (base_hue + k * 40) % 360})
    # 4 routes (cardinale lijnen)
    routes = []
    for j in range(4):
        angle = math.pi / 2 * j
        routes.append({"x2": cx + 200 * math.cos(angle), "y2": cy + 200 * math.sin(angle), "hue": (base_hue + j * 60) % 360})
    # 11 rode draad punten
    thread_pts = []
    for i in range(11):
        angle = 2 * math.pi * i / 11
        r = 170
        thread_pts.append({"x": cx + r * math.cos(angle), "y": cy + r * math.sin(angle)})
    return {"cx": cx, "cy": cy, "base_hue": base_hue, "layers": layers, "routes": routes,
            "thread_pts": thread_pts, "dr": e["dr"]}
def gen_svg(g):
    parts = []; cx, cy = g["cx"], g["cy"]; bh = g["base_hue"]
    # 3 lagen
    for lay in g["layers"]:
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},60%,50%)" stroke-width="1.5" opacity="0.5"/>'.format(lay["pts"], lay["hue"]))
    # 4 routes
    for r in g["routes"]:
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},50%,50%)" stroke-width="1" opacity="0.4"/>'.format(cx, cy, r["x2"], r["y2"], r["hue"]))
    # 11 rode draad
    for p in g["thread_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="2.5" fill="hsl({},70%,60%)" opacity="0.6"/>'.format(p["x"], p["y"], bh))
    # Eka (één) centrum
    parts.append('<circle cx="{}" cy="{}" r="6" fill="hsl({},80%,65%)" opacity="0.9"/>'.format(cx, cy, bh))
    return "\n".join(parts)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#06060a;color:#d4d4e0;font-family:'Instrument Sans',-apple-system,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}}
.field{{position:relative;width:500px;height:500px}}.layer{{position:absolute;top:0;left:0;width:100%;height:100%}}
.layer-rotate{{animation:rotate 60s linear infinite}}@keyframes rotate{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
.metadata{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:hsl({bh},40%,50%);opacity:0.5}}
.metadata .title{{font-size:1.1rem;margin-bottom:6px;color:hsl({bh},60%,55%);opacity:0.8}}
.metadata .params{{display:flex;gap:12px;justify-content:center}}
</style></head><body><div class="field"><div class="layer layer-rotate">
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">{svg}</svg></div>
<div class="metadata"><div class="title">{title}</div><div class="params">
<span>EKA=1</span><span>3×4</span><span>DR:{dr}</span></div></div></div></body></html>"""
def gen_html(g, e, text):
    title = "Dimensie 11: Eka Routing"
    for l in text.split("\n")[:3]:
        if l.startswith("# "): title = l[2:].strip(); break
    return HTML_TEMPLATE.format(title=title, svg=gen_svg(g), bh=g["base_hue"], dr=g["dr"])
def main():
    text = read_article(); e = extract(text); g = compute_geometry(e)
    print("Artikel 014 — Dimensie 11: Eka Routing")
    for k, v in [("DR", e["dr"]), ("eka", e["has_eka"]), ("nidrā", e["nidra_links"])]:
        print("  {}: {}".format(k, v))
    with open(OUTPUT, "w", encoding="utf-8") as f: f.write(gen_html(g, e, text))
    print("→ {}".format(OUTPUT))
if __name__ == "__main__": main()
