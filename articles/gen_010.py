#!/usr/bin/env python3
"""Artikel 010 — Dimensie 7: Reflectie. 7=2³-1, spiegel, lens."""
import hashlib, math, os, random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(SCRIPT_DIR, "hexa-book-010.md")
OUTPUT  = os.path.join(SCRIPT_DIR, "10-dimensie-7.art.html")

def read_article():
    with open(ARTICLE, encoding="utf-8") as f: return f.read()
def digital_root(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def extract(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": h, "dr": digital_root(int(h[:6], 16)), "word_count": len(text.split()),
            "nidra_links": sum(1 for n in ["001", "002", "017"] if n in text), "has_7": "7" in text}
def compute_geometry(e):
    cx, cy = 250, 250; base_hue = 180  # cyaan = reflectie/spiegel
    # 7 reflectie-punten in heptagoon
    hept_pts = []
    for i in range(7):
        angle = 2 * math.pi * i / 7 - math.pi / 2
        hept_pts.append({"x": cx + 150 * math.cos(angle), "y": cy + 150 * math.sin(angle)})
    # Spiegel-laag (gedupliceerd, gespiegeld)
    mirror_pts = []
    for p in hept_pts:
        mirror_pts.append({"x": p["x"], "y": 2 * cy - p["y"]})  # spiegelen over y-as
    # 2³-1 = 7 states
    binary_pts = []
    for i in range(7):
        angle = 2 * math.pi * i / 7 + 0.3
        r = 100
        binary_pts.append({"x": cx + r * math.cos(angle), "y": cy + r * math.sin(angle)})
    return {"cx": cx, "cy": cy, "base_hue": base_hue, "hept_pts": hept_pts, "mirror_pts": mirror_pts,
            "binary_pts": binary_pts, "dr": e["dr"]}
def gen_svg(g):
    parts = []; cx, cy = g["cx"], g["cy"]; bh = g["base_hue"]
    # Heptagoon
    h = " ".join("{:.1f},{:.1f}".format(p["x"], p["y"]) for p in g["hept_pts"])
    parts.append('<polygon points="{}" fill="none" stroke="hsl({},60%,50%)" stroke-width="2" opacity="0.6"/>'.format(h, bh))
    # Spiegel-laag
    m = " ".join("{:.1f},{:.1f}".format(p["x"], p["y"]) for p in g["mirror_pts"])
    parts.append('<polygon points="{}" fill="none" stroke="hsl({},40%,40%)" stroke-width="1" opacity="0.25" stroke-dasharray="5,5"/>'.format(m, bh))
    # Lijnen tussen origine en spiegel
    for i, p in enumerate(g["hept_pts"]):
        mp = g["mirror_pts"][i]
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},30%,35%)" stroke-width="0.5" opacity="0.15"/>'.format(p["x"], p["y"], mp["x"], mp["y"], bh))
    # 2³-1 punten
    for p in g["binary_pts"]:
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="2.5" fill="hsl({},50%,55%)" opacity="0.5"/>'.format(p["x"], p["y"], bh))
        parts.append('<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="hsl({},20%,35%)" stroke-width="0.3" opacity="0.1"/>'.format(cx, cy, p["x"], p["y"], bh))
    parts.append('<circle cx="{}" cy="{}" r="5" fill="hsl({},80%,65%)" opacity="0.9"/>'.format(cx, cy, bh))
    return "\n".join(parts)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hexa-Boek</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#06060a;color:#d4d4e0;font-family:'Instrument Sans',-apple-system,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}}
.field{{position:relative;width:500px;height:500px}}.layer{{position:absolute;top:0;left:0;width:100%;height:100%}}
.layer-rotate{{animation:rotate 75s linear infinite}}@keyframes rotate{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
.metadata{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:hsl({bh},40%,50%);opacity:0.5}}
.metadata .title{{font-size:1.1rem;margin-bottom:6px;color:hsl({bh},60%,55%);opacity:0.8}}
.metadata .params{{display:flex;gap:12px;justify-content:center}}
</style></head><body><div class="field"><div class="layer layer-rotate">
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">{svg}</svg></div>
<div class="metadata"><div class="title">{title}</div><div class="params">
<span>2³-1=7</span><span>SPIEGEL</span><span>DR:{dr}</span></div></div></div></body></html>"""
def gen_html(g, e, text):
    title = "Dimensie 7: Reflectie"
    for l in text.split("\n")[:3]:
        if l.startswith("# "): title = l[2:].strip(); break
    return HTML_TEMPLATE.format(title=title, svg=gen_svg(g), bh=g["base_hue"], dr=g["dr"])
def main():
    text = read_article(); e = extract(text); g = compute_geometry(e)
    print("Artikel 010 — Dimensie 7: Reflectie")
    for k, v in [("DR", e["dr"]), ("nidrā", e["nidra_links"])]:
        print("  {}: {}".format(k, v))
    with open(OUTPUT, "w", encoding="utf-8") as f: f.write(gen_html(g, e, text))
    print("→ {}".format(OUTPUT))
if __name__ == "__main__": main()
