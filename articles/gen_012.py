#!/usr/bin/env python3
"""Artikel 012 — 24-brug en 6-bit Routing. الجسر 24, 6-bit, NPR Bedrock."""
import hashlib, math, os, random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-012.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "12-24-brug.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f: return f.read()
def digital_root(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": h, "dr": digital_root(int(h[:6], 16)), "word_count": len(text.split()),
            "has_24": "24" in text, "has_6bit": "6-bit" in text or "6-bit" in text,
            "has_arabic": "الجسر" in text, "has_sanskrit": "सेतु" in text}
def compute_geometry(e):
    cx, cy = 250, 250; base_hue = 30  # goud = brug/routing
    # 24 brug-punten in cirkel
    bridge_pts = []
    for i in range(24):
        angle = 2 * math.pi * i / 24
        bridge_pts.append({"x": cx + 160 * math.cos(angle), "y": cy + 160 * math.sin(angle)})
    # 6-bit routing (6 lagen van 4)
    routes = []
    for layer in range(6):
        pts = []
        for i in range(4):
            angle = 2 * math.pi * i / 4 + layer * 0.2
            r = 60 + layer * 25
            pts.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
        routes.append({"pts": " ".join(pts), "hue": (base_hue + layer * 40) % 360})
    # Kringlijnen
    circle_r = 160
    return {"cx": cx, "cy": cy, "base_hue": base_hue, "bridge_pts": bridge_pts,
            "routes": routes, "dr": e["dr"]}
def gen_svg(g):
    parts = []; cx, cy = g["cx"], g["cy"]; bh = g["base_hue"]
    # 24 brug-punten
    for p in g["bridge_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="2" fill="hsl({},50%,55%)" opacity="0.5"/>'.format(p["x"], p["y"], bh))
    # Cirkel
    parts.append('<circle cx="{}" cy="{}" r="160" fill="none" stroke="hsl({},40%,40%)" stroke-width="0.5" opacity="0.2"/>'.format(cx, cy, bh))
    # 6-bit routing lagen
    for r in g["routes"]:
        parts.append('<polygon points="{}" fill="none" stroke="hsl({},60%,50%)" stroke-width="1" opacity="0.4"/>'.format(r["pts"], r["hue"]))
    # Lijnen centrum naar brug
    for i, p in enumerate(g["bridge_pts"]):
        if i % 4 == 0:
            parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},30%,35%)" stroke-width="0.5" opacity="0.15"/>'.format(cx, cy, p["x"], p["y"], bh))
    parts.append('<circle cx="{}" cy="{}" r="5" fill="hsl({},80%,65%)" opacity="0.9"/>'.format(cx, cy, bh))
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
<span>24-BRUG</span><span>6-BIT</span><span>DR:{dr}</span></div></div></div></body></html>"""
def gen_html(g, e, text):
    title = "24-brug en 6-bit Routing"
    for l in text.split("\n")[:3]:
        if l.startswith("# "): title = l[2:].strip(); break
    return HTML_TEMPLATE.format(title=title, svg=gen_svg(g), bh=g["base_hue"], dr=g["dr"])
def main():
    text = read_article(); e = extract(text); g = compute_geometry(e)
    print("Artikel 012 — 24-brug en 6-bit Routing")
    for k, v in [("DR", e["dr"]), ("24", e["has_24"]), ("6-bit", e["has_6bit"]), ("Arabic", e["has_arabic"])]:
        print("  {}: {}".format(k, v))
    with open(OUTPUT, "w", encoding="utf-8") as f: f.write(gen_html(g, e, text))
    print("→ {}".format(OUTPUT))
if __name__ == "__main__": main()
