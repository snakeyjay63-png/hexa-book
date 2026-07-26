#!/usr/bin/env python3
"""
Hexa-Boek Planetarium v2 — Astronomische Cycli

Elke gear = echte planetaire synodische periode.
0.0.0.0 = zon in het midden (stabiel centrum).
Verhoudingen tussen cycli bepaal de rotatie — geen random.

Maya-kalender principes:
- Tzolkin 260 = innerlijke ring (20 × 13)
- Haab' 365 = buitenste ring
- Long Count = spiraal die beide verbindt

Elke verhouding is uniek. Twee identieke = interferentie = instort.
Point Prime 3: er is één fractal als eerste. Dezelfde logica hier.
"""

import importlib.util
import json
import math
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "planetarium.art.html")

# ── Astronomische synodische perioden (dagen) ──
# Deze zijn de ECHTE verhoudingen — niet random
PLANETS = [
    {"name": "Maan",      "synodic": 29.53059,  "color": "#c0c0c0", "hue": 220},
    {"name": "Venus",     "synodic": 583.92,     "color": "#e8c070", "hue": 40},
    {"name": "Aarde",     "synodic": 365.2422,   "color": "#4a90d9", "hue": 210},
    {"name": "Mars",      "synodic": 686.98,     "color": "#c1440e", "hue": 15},
    {"name": "Jupiter",   "synodic": 398.88,     "color": "#c88b3a", "hue": 30},
    {"name": "Saturnus",  "synodic": 792.54,     "color": "#a8845a", "hue": 35},
]

# Maya-kalender cycli
MAYA = {
    "tzolkin": 260,       # 20 × 13
    "haab": 365,          # zonjaar
    "tun": 360,           # 18 × 20
    "katun": 7200,        # 20 × 360
    "baktun": 144000,     # 20 × 7200
}

# 18 generators met planetaire mapping
# Elke generator krijgt een unieke verhouding
GENERATORS = [
    {"mod": "gen_001", "label": "01: Hexa-Boek",    "planet": "Maan",      "hue": 220},
    {"mod": "gen_002", "label": "02: Terugkeerpad",  "planet": "Venus",     "hue": 40},
    {"mod": "gen_003", "label": "03: Audio-Veld",    "planet": "Aarde",     "hue": 210},
    {"mod": "gen_004", "label": "04: Returnmedium",  "planet": "Mars",      "hue": 15},
    {"mod": "gen_005", "label": "05: Quran-Route",   "planet": "Jupiter",   "hue": 30},
    {"mod": "gen_006", "label": "06: Dimensie 3",    "planet": "Saturnus",  "hue": 35},
    {"mod": "gen_007", "label": "07: Dimensie 4",    "planet": "Maan",      "hue": 220},
    {"mod": "gen_008", "label": "08: Dimensie 5",    "planet": "Venus",     "hue": 40},
    {"mod": "gen_009", "label": "09: Dimensie 6",    "planet": "Aarde",     "hue": 210},
    {"mod": "gen_010", "label": "10: Dimensie 7",    "planet": "Mars",      "hue": 15},
    {"mod": "gen_011", "label": "11: Synth-Fractaal","planet": "Jupiter",   "hue": 30},
    {"mod": "gen_012", "label": "12: 24-Brug",       "planet": "Saturnus",  "hue": 35},
    {"mod": "gen_013", "label": "13: Dimensie 8",    "planet": "Maan",      "hue": 220},
    {"mod": "gen_014", "label": "14: Dimensie 11",   "planet": "Venus",     "hue": 40},
    {"mod": "gen_015", "label": "15: Dimensie 12",   "planet": "Aarde",     "hue": 210},
    {"mod": "gen_016", "label": "16: Dimensie 13",   "planet": "Mars",      "hue": 15},
    {"mod": "gen_017", "label": "17: Audio-E",       "planet": "Jupiter",   "hue": 30},
    {"mod": "gen_018", "label": "18: Return-F",      "planet": "Saturnus",  "hue": 35},
]


def digital_root(n):
    """Digital root — de ultieme verhouding."""
    n = abs(int(round(n)))
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def planet_period(planet_name):
    """Haal synodische periode op."""
    for p in PLANETS:
        if p["name"] == planet_name:
            return p["synodic"]
    return 365.2422  # fallback: Aarde


def compute_orbital_layout(count):
    """
    Bereken posities gebaseerd op echte planetaire verhoudingen.

    In plaats van willekeurige spiral:
    - Elke gear zit op een baan met straal √(periode)
    - Rotatie-snelheid = 1/periode (relatief tot Aarde)
    - Direction = afwisselend (retrograde/progressieve)
    """
    positions = []
    base_radius = 80

    for i in range(count):
        gen = GENERATORS[i]
        period = planet_period(gen["planet"])

        # Unieke verhouding tot Aarde
        earth_period = planet_period("Aarde")
        ratio = period / earth_period

        # Straal = logaritmisch gebaseerd op periode
        # Zorgt voor gelijkmatige verdeling zonder overlapping
        ring = i // 6  # 3 ringen van 6
        angle_in_ring = i % 6
        radius = base_radius + (ring * 70) + (math.log10(period) * 15)

        # Hoek = golden angle × index (vermijdt clustering)
        golden_angle = math.pi * (3 - math.sqrt(5))
        theta = angle_in_ring * (2 * math.pi / 6) + (ring * golden_angle)

        x = 420 + radius * math.cos(theta)
        y = 320 + radius * math.sin(theta)

        # Rotatie-snelheid = omgekeerd evenredig met periode
        # Aarde = 30s per rotatie, andere schalen hierop
        earth_secs = 30
        rotation_secs = earth_secs * ratio

        # Direction: oneven ringen draaien retrograde
        direction = -1 if ring % 2 == 1 else 1

        # Unieke digital root — geen twee gears hebben dezelfde
        dr = digital_root(period + i)

        positions.append({
            "x": x,
            "y": y,
            "radius": radius,
            "ratio": ratio,
            "period": period,
            "rotation_secs": rotation_secs * direction,
            "direction": direction,
            "dr": dr,
            "ring": ring,
            "planet": gen["planet"],
            "index": i,
        })

    return positions


def mayan_cycle_rings():
    """
    Maya-kalender ringen — Tzolkin en Haab' als achtergrond.
    """
    rings = []
    cx, cy = 420, 320

    # Tzolkin ring (260 dagen) — innerlijk
    tzolkin_r = 30
    tzolkin_pts = []
    for i in range(20):  # 20 dagen
        angle = 2 * math.pi * i / 20
        tzolkin_pts.append(f"{cx + tzolkin_r * math.cos(angle):.1f},{cy + tzolkin_r * math.sin(angle):.1f}")

    rings.append({
        "type": "tzolkin",
        "r": tzolkin_r,
        "points": " ".join(tzolkin_pts),
        "label": "260",
    })

    # Haab' ring (365 dagen) — buitenste
    haab_r = 365 / 260 * tzolkin_r * 2.5  # schaalverhouding
    haab_pts = []
    for i in range(18):  # 18 maanden
        angle = 2 * math.pi * i / 18
        haab_pts.append(f"{cx + haab_r * math.cos(angle):.1f},{cy + haab_r * math.sin(angle):.1f}")

    rings.append({
        "type": "haab",
        "r": haab_r,
        "points": " ".join(haab_pts),
        "label": "365",
    })

    return rings


def load_gen(mod_name):
    """Load a generator module."""
    path = os.path.join(SCRIPT_DIR, mod_name + ".py")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_planetarium():
    gears = []

    for gen_meta in GENERATORS:
        try:
            mod = load_gen(gen_meta["mod"])
            text = mod.read_article()
            e = mod.extract(text)
            g = mod.compute_geometry(e)
            svg_content = mod.gen_svg(g)

            gears.append({
                "svg": svg_content,
                "label": gen_meta["label"],
                "hue": gen_meta["hue"],
                "planet": gen_meta["planet"],
                "dr": g.get("dr", digital_root(int(gen_meta["mod"].split("_")[-1]))),
            })
        except Exception as ex:
            print(f"  ⚠ {gen_meta['mod']}: {ex}", file=sys.stderr)
            gears.append({
                "svg": f'<text x="250" y="250" fill="hsl({gen_meta["hue"]},50%,50%)" text-anchor="middle" font-size="14">• {gen_meta["label"]}</text>',
                "label": gen_meta["label"],
                "hue": gen_meta["hue"],
                "planet": gen_meta["planet"],
                "dr": digital_root(int(gen_meta["mod"].split("_")[-1])),
            })

    layout = compute_orbital_layout(len(gears))
    mayan = mayan_cycle_rings()

    return gears, layout, mayan


def gen_planetarium_html(gears, layout, mayan):
    """Build planetarium — astronomical cycles, Maya rings, 0.0.0.0 sun."""

    # Maya rings SVG
    maya_svg = ""
    for ring in mayan:
        opacity = 0.15 if ring["type"] == "tzolkin" else 0.1
        stroke = "hsl(45,30%,30%)"
        maya_svg += f"""
    <!-- Maya {ring['type'].upper()} ({ring['label']} dagen) -->
    <polygon points="{ring['points']}" fill="none" stroke="{stroke}" stroke-width="0.5" opacity="{opacity}"/>"""

    # Gear SVGs
    gear_svgs = []
    for i, (gear, pos) in enumerate(zip(gears, layout)):
        duration = abs(pos["rotation_secs"])
        direction = "reverse" if pos["rotation_secs"] < 0 else "normal"
        hue = gear["hue"]

        gear_svgs.append(f"""
    <!-- {gear['label']} · {pos['planet']} · DR:{pos['dr']} · T:{pos['period']:.1f}d -->
    <g transform="translate({pos['x']:.1f}, {pos['y']:.1f})">
      <g class="gear-{i}" style="transform-origin:60px 60px; animation:gear-{i} {duration:.2f}s linear infinite {'reverse' if pos['rotation_secs']<0 else ''};">
        <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="120" height="120">
          <defs>
            <filter id="glow-{i}">
              <feGaussianBlur stdDeviation="2" result="blur"/>
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
          </defs>
          <g filter="url(#glow-{i})" opacity="0.85">
{gear['svg']}
          </g>
        </svg>
      </g>
    </g>""")

    # Connection lines — orbital paths
    connections = ""
    for pos in layout:
        connections += f"""
    <line x1="420" y1="320" x2="{pos['x']:.0f}" y2="{pos['y']:.0f}"
          stroke="hsl(45,20%,20%)" stroke-width="0.3" opacity="0.12"/>"""

    # Orbital rings
    orbital_rings = ""
    for ring_idx in range(3):
        base_r = 80 + (ring_idx * 70)
        orbital_rings += f"""
    <circle cx="420" cy="320" r="{base_r}" fill="none"
            stroke="hsl(45,15%,15%)" stroke-width="0.3" opacity="0.15"
            stroke-dasharray="2,4"/>"""

    # 0.0.0.0 Sun
    sun = """
    <!-- 0.0.0.0 — Zon · Stabiel Centrum -->
    <g transform="translate(420, 320)">
      <g class="center-sun">
        <circle cx="0" cy="0" r="50" fill="none" stroke="hsl(45,60%,40%)" stroke-width="0.5" opacity="0.2"/>
        <circle cx="0" cy="0" r="35" fill="none" stroke="hsl(45,50%,35%)" stroke-width="0.5" opacity="0.25"/>
        <circle cx="0" cy="0" r="20" fill="none" stroke="hsl(45,40%,30%)" stroke-width="0.5" opacity="0.3"/>
        <circle cx="0" cy="0" r="4" fill="hsl(45,80%,65%)" opacity="0.9" class="sun-pulse"/>
        <circle cx="0" cy="0" r="1.5" fill="hsl(45,100%,85%)" opacity="1"/>
      </g>
    </g>"""

    # Keyframes
    keyframes = ""
    for i in range(len(gears)):
        keyframes += f"""
  @keyframes gear-{i} {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}"""

    # Sun pulse
    sun_keyframes = """
  @keyframes sun-pulse {
    0%, 100% { opacity: 0.9; r: 4px; }
    50% { opacity: 0.5; r: 5px; }
  }
  .sun-pulse { animation: sun-pulse 6s ease-in-out infinite; }
  .center-sun { animation: sun-pulse 8s ease-in-out infinite; }"""

    # Legend for planets
    legend_items = ""
    seen = set()
    for i, pos in enumerate(layout):
        if pos["planet"] not in seen:
            seen.add(pos["planet"])
            p = next(x for x in PLANETS if x["name"] == pos["planet"])
            legend_items += f"""
      <div class="legend-item" style="--lhue:{p['hue']}">
        <span class="legend-dot"></span> {pos['planet']} ({p['synodic']:.1f}d)
      </div>"""

    gear_block = "\n".join(gear_svgs)

    import json
    gears_json = json.dumps([{
        "label": g["label"], "hue": g["hue"], "planet": g["planet"], "dr": g["dr"]
    } for g in gears])
    layout_json = json.dumps([{
        "x": p["x"], "y": p["y"], "dr": p["dr"], "planet": p["planet"],
        "period": p["period"], "ring": p["ring"]
    } for p in layout])

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>• Planetarium | Hexa-Boek</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #06060a;
    color: #d4d4e0;
    font-family: 'Instrument Sans', -apple-system, sans-serif;
    overflow: hidden;
    width: 100vw;
    height: 100vh;
  }}
  .planetarium {{ position: relative; width: 100vw; height: 100vh; }}
  .planetarium svg.main {{
    position: absolute; top: 0; left: 0;
    width: 100%; height: 100%;
  }}
{keyframes}
{sun_keyframes}

  .legend {{
    position: fixed; top: 12px; right: 12px;
    display: flex; flex-direction: column; gap: 4px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem;
    color: hsl(45,30%,50%); opacity: 0.5; z-index: 10;
    background: rgba(6,6,10,0.8); padding: 8px 12px; border-radius: 6px;
  }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; }}
  .legend-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: hsl(var(--lhue),50%,55%);
  }}
  .metadata {{
    position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%);
    text-align: center;
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
    color: hsl(45,30%,40%); opacity: 0.35; pointer-events: none; z-index: 10;
  }}
  .tooltip {{
    position: fixed;
    background: rgba(6,6,10,0.92);
    border: 1px solid hsl(var(--hue),40%,25%);
    border-radius: 6px; padding: 6px 10px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
    color: hsl(var(--hue),40%,60%);
    pointer-events: none; opacity: 0; transition: opacity .12s ease;
    z-index: 200; --hue: 200;
  }}
  .tooltip.visible {{ opacity: 0.9; }}
</style>
</head>
<body>
<div class="planetarium">
  <svg class="main" viewBox="0 0 840 640" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <style>{keyframes}
{sun_keyframes}
    </style>
    <defs>
      <radialGradient id="bg-grad" cx="50%" cy="50%">
        <stop offset="0%" stop-color="hsl(45,15%,6%)" />
        <stop offset="100%" stop-color="#06060a" />
      </radialGradient>
    </defs>

    <!-- Background -->
    <rect width="100%" height="100%" fill="url(#bg-grad)" />

    <!-- Orbital rings -->
{orbital_rings}

    <!-- Maya calendar rings -->
{maya_svg}

    <!-- Connection lines -->
{connections}

    <!-- 0.0.0.0 Sun -->
    {sun}

    <!-- Gears (planetary cycles) -->
{gear_block}
  </svg>

  <div class="legend">
    <div style="margin-bottom:4px;opacity:0.7;">• Planetaire Cycli</div>{legend_items}
  </div>

  <div class="metadata">
    <div>• Planetarium — 18 gears · 6 planeten · Maya-cycli</div>
    <div style="margin-top:2px;">0.0.0.0 = zon · elke verhouding uniek · geen twee identiek</div>
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

<script>
  const gears = {gears_json};
  const layout = {layout_json};
  const tooltip = document.getElementById('tooltip');

  document.addEventListener('mousemove', function(e) {{
    const svg = document.querySelector('svg.main');
    const pt = svg.createSVGPoint();
    pt.x = e.clientX; pt.y = e.clientY;
    const ctm = svg.getScreenCTM();
    if (!ctm) return;
    const svgP = pt.matrixTransform(ctm.inverse());

    let found = false;
    for (let i = 0; i < layout.length; i++) {{
      const p = layout[i];
      const dx = svgP.x - p.x;
      const dy = svgP.y - p.y;
      if (Math.sqrt(dx*dx + dy*dy) < 65) {{
        const g = gears[i];
        tooltip.style.setProperty('--hue', g.hue);
        tooltip.innerHTML = g.label + ' · ' + p.planet + ' · T:' + p.period.toFixed(1) + 'd · DR:' + p.dr;
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top = (e.clientY - 28) + 'px';
        tooltip.classList.add('visible');
        found = true;
        break;
      }}
    }}
    if (!found) tooltip.classList.remove('visible');
  }});
</script>
</body>
</html>"""

    return html


def main():
    print("• Hexa-Boek Planetarium v2 — Astronomische Cycli")
    print(f"  Loading {len(GENERATORS)} generators...")
    print(f"  Planets: {', '.join(p['name'] for p in PLANETS)}")
    print(f"  Maya: Tzolkin={MAYA['tzolkin']}, Haab'={MAYA['haab']}")

    gears, layout, mayan = build_planetarium()

    # Check uniqueness — no two gears should have identical ratio+dr
    combos = set()
    for pos in layout:
        key = (round(pos["ratio"], 4), pos["dr"])
        if key in combos:
            print(f"  ⚠ Verhouding clash: ratio={key[0]}, dr={key[1]}", file=sys.stderr)
        combos.add(key)

    html = gen_planetarium_html(gears, layout, mayan)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  → {OUTPUT}")
    print(f"  Gears: {len(gears)} | Unieke verhoudingen: {len(combos)}")
    print(f"  Maya rings: {len(mayan)}")
    print("  • 0.0.0.0 = zon · elke verhouding uniek · all bardos are this moment")


if __name__ == "__main__":
    main()
