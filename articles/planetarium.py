#!/usr/bin/env python3
"""
Hexa-Boek Planetarium

Elke .py generator is een gear.
0.0.0.0 = zon in het midden (het veld zelf).
18 ringen draaien als vortex — elk met eigen snelheid en richting.

Geen iframes. Geen static files.
Pure Python → SVG → één frame.
"""

import importlib.util
import math
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# All 18 generators with metadata
GENERATORS = [
    {"mod": "gen_001", "label": "01: Hexa-Boek", "dim": 1, "hue": 200},
    {"mod": "gen_002", "label": "02: Terugkeerpad", "dim": 2, "hue": 30},
    {"mod": "gen_003", "label": "03: Audio-Veld", "dim": 3, "hue": 60},
    {"mod": "gen_004", "label": "04: Returnmedium", "dim": 4, "hue": 90},
    {"mod": "gen_005", "label": "05: Quran-Route", "dim": 5, "hue": 120},
    {"mod": "gen_006", "label": "06: Dimensie 3", "dim": 6, "hue": 150},
    {"mod": "gen_007", "label": "07: Dimensie 4", "dim": 7, "hue": 180},
    {"mod": "gen_008", "label": "08: Dimensie 5", "dim": 8, "hue": 210},
    {"mod": "gen_009", "label": "09: Dimensie 6", "dim": 9, "hue": 240},
    {"mod": "gen_010", "label": "10: Dimensie 7", "dim": 10, "hue": 270},
    {"mod": "gen_011", "label": "11: Synth-Fractaal", "dim": 11, "hue": 300},
    {"mod": "gen_012", "label": "12: 24-Brug", "dim": 12, "hue": 330},
    {"mod": "gen_013", "label": "13: Dimensie 8", "dim": 13, "hue": 15},
    {"mod": "gen_014", "label": "14: Dimensie 11", "dim": 14, "hue": 45},
    {"mod": "gen_015", "label": "15: Dimensie 12", "dim": 15, "hue": 75},
    {"mod": "gen_016", "label": "16: Dimensie 13", "dim": 16, "hue": 105},
    {"mod": "gen_017", "label": "17: Audio-E", "dim": 17, "hue": 280},
    {"mod": "gen_018", "label": "18: Return-F", "dim": 18, "hue": 200},
]

OUTPUT = os.path.join(SCRIPT_DIR, "planetarium.art.html")


def load_gen(mod_name):
    """Load a generator module and return (read_article, extract, compute_geometry, gen_svg)."""
    path = os.path.join(SCRIPT_DIR, mod_name + ".py")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def compute_vortex_layout(count, radius=220):
    """Position 18 gears in a vortex/spiral pattern."""
    positions = []
    golden_angle = math.pi * (3 - math.sqrt(5))  # ~137.5°

    for i in range(count):
        # Spiral distribution
        r = radius * math.sqrt((i + 1) / count)
        theta = i * golden_angle

        x = 400 + r * math.cos(theta)
        y = 300 + r * math.sin(theta)

        # Rotation speed: inner gears faster, outer slower
        # Direction alternates based on digital root
        dr = digital_root(i + 1)
        speed = 40 - (dr * 3)  # seconds per full rotation
        direction = 1 if dr % 2 == 0 else -1

        positions.append({
            "x": x,
            "y": y,
            "speed": abs(speed) * direction,
            "dr": dr,
            "index": i,
        })

    return positions


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
                "dim": gen_meta["dim"],
                "dr": g.get("dr", digital_root(gen_meta["dim"])),
            })
        except Exception as ex:
            print(f"  ⚠ {gen_meta['mod']}: {ex}", file=sys.stderr)
            gears.append({
                "svg": f'<text x="250" y="250" fill="hsl({gen_meta["hue"]},50%,50%)" text-anchor="middle" font-size="14">• {gen_meta["label"]}</text>',
                "label": gen_meta["label"],
                "hue": gen_meta["hue"],
                "dim": gen_meta["dim"],
                "dr": digital_root(gen_meta["dim"]),
            })

    layout = compute_vortex_layout(len(gears))

    return gears, layout


def gen_planetarium_html(gears, layout):
    """Build the full planetarium HTML — one frame, all gears."""

    # Build gear SVGs with CSS animations
    gear_svgs = []
    for i, (gear, pos) in enumerate(zip(gears, layout)):
        speed = pos["speed"]
        duration = abs(speed)
        direction = "reverse" if speed < 0 else "normal"
        anim_name = f"gear-{i}"

        gear_svgs.append(f"""
    <!-- Gear {gear['label']} -->
    <g transform="translate({pos['x']}, {pos['y']})">
      <g class="gear-{i}">
        <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="120" height="120">
          <defs>
            <filter id="glow-{i}">
              <feGaussianBlur stdDeviation="2" result="blur"/>
              <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          <g filter="url(#glow-{i})" opacity="0.8">
{gear['svg']}
          </g>
        </svg>
      </g>
    </g>""")

    # Build center — 0.0.0.0 sun
    center = """
    <!-- 0.0.0.0 — Het Zon-Veld -->
    <g transform="translate(400, 300)">
      <g class="center-sun">
        <circle cx="0" cy="0" r="60" fill="none" stroke="hsl(45,80%,60%)" stroke-width="1" opacity="0.3"/>
        <circle cx="0" cy="0" r="40" fill="none" stroke="hsl(45,60%,50%)" stroke-width="0.5" opacity="0.4"/>
        <circle cx="0" cy="0" r="20" fill="none" stroke="hsl(45,40%,40%)" stroke-width="0.3" opacity="0.5"/>
        <circle cx="0" cy="0" r="3" fill="hsl(45,80%,70%)" opacity="0.9"/>
        <text x="0" y="80" fill="hsl(45,40%,50%)" text-anchor="middle" font-family="monospace" font-size="10" opacity="0.4">0.0.0.0</text>
      </g>
    </g>"""

    # Connection lines from center to each gear
    connections = []
    for pos in layout:
        dx = pos["x"] - 400
        dy = pos["y"] - 300
        dist = math.sqrt(dx * dx + dy * dy)
        opacity = max(0.05, 0.2 - (dist / 1500))
        connections.append(
            f'<line x1="400" y1="300" x2="{pos["x"]:.0f}" y2="{pos["y"]:.0f}" '
            f'stroke="hsl(45,30%,30%)" stroke-width="0.3" opacity="{opacity}"/>'
        )

    gear_block = "\n".join(gear_svgs)
    conn_block = "\n".join(connections)

    # CSS keyframes for each gear — embedded in SVG <style>
    gear_styles = ""
    for i, pos in enumerate(layout):
        direction = "reverse" if pos["speed"] < 0 else ""
        duration = abs(pos["speed"])
        gear_styles += f"""
  @keyframes gear-{i} {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}
  .gear-{i} {{
    transform-origin: 60px 60px;
    animation: gear-{i} {duration}s linear infinite {direction};
  }}"""

    sun_css = """
  @keyframes sun-pulse {
    0%, 100% { opacity: 0.9; }
    50% { opacity: 0.5; }
  }
  .center-sun {
    animation: sun-pulse 6s ease-in-out infinite;
  }"""

    # Full standalone HTML (for direct viewing)
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
  .planetarium {{
    position: relative;
    width: 100vw;
    height: 100vh;
  }}
  .planetarium svg.main {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }}
{gear_styles}
{sun_css}

  .metadata {{
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: hsl(45, 40%, 50%);
    opacity: 0.4;
    pointer-events: none;
    z-index: 10;
  }}
  .metadata .title {{
    font-size: 1rem;
    margin-bottom: 4px;
    color: hsl(45, 60%, 55%);
  }}
  .tooltip {{
    position: absolute;
    background: rgba(6, 6, 10, 0.9);
    border: 1px solid hsl(var(--hue), 50%, 30%);
    border-radius: 8px;
    padding: 8px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: hsl(var(--hue), 50%, 65%);
    pointer-events: none;
    opacity: 0;
    transition: opacity .15s ease;
    z-index: 20;
    --hue: 200;
  }}
  .tooltip.visible {{ opacity: 0.9; }}
</style>
</head>
<body>
<div class="planetarium">
  <svg class="main" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <style>{gear_styles}
{sun_css}
    </style>
    <defs>
      <radialGradient id="bg-grad" cx="50%" cy="50%">
        <stop offset="0%" stop-color="hsl(45,20%,8%)" />
        <stop offset="100%" stop-color="#06060a" />
      </radialGradient>
    </defs>

    <!-- Background -->
    <rect width="100%" height="100%" fill="url(#bg-grad)" />

    <!-- Connection lines -->
{conn_block}

    <!-- Center sun -->
    {center}

    <!-- Gears -->
{gear_block}
  </svg>

  <div class="metadata">
    <div class="title">• Planetarium</div>
    <div>18 gears · 1 field · 0.0.0.0</div>
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

<script>
  const gears = {gears};
  const layout = {layout};
  const tooltip = document.getElementById('tooltip');

  // Hover detection
  document.addEventListener('mousemove', function(e) {{
    const svg = document.querySelector('svg.main');
    const pt = svg.createSVGPoint();
    pt.x = e.clientX;
    pt.y = e.clientY;
    const ctm = svg.getScreenCTM();
    if (!ctm) return;
    const svgP = pt.matrixTransform(ctm.inverse());

    let found = false;
    for (let i = 0; i < layout.length; i++) {{
      const p = layout[i];
      const dx = svgP.x - p.x;
      const dy = svgP.y - p.y;
      if (Math.sqrt(dx*dx + dy*dy) < 60) {{
        tooltip.style.setProperty('--hue', gears[i].hue);
        tooltip.innerHTML = gears[i].label + ' · DR: ' + gears[i].dr + ' · ' + gears[i].dim;
        tooltip.style.left = (e.clientX + 12) + 'px';
        tooltip.style.top = (e.clientY - 30) + 'px';
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
    print("• Hexa-Boek Planetarium")
    print(f"  Loading {len(GENERATORS)} generators...")

    gears, layout = build_planetarium()

    # Serialize gear data for JS
    import json
    gears_json = json.dumps([
        {"label": g["label"], "hue": g["hue"], "dim": g["dim"], "dr": g["dr"]}
        for g in gears
    ])
    layout_json = json.dumps([
        {"x": p["x"], "y": p["y"], "dr": p["dr"]}
        for p in layout
    ])

    html = gen_planetarium_html(gears, layout)

    # Inject JSON data
    html = html.replace("{gears}", gears_json)
    html = html.replace("{layout}", layout_json)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  → {OUTPUT}")
    print(f"  Gears: {len(gears)}")
    print(f"  Layout: {len(layout)} positions")
    print("  • 0.0.0.0 = sun, all bardos are this moment")


if __name__ == "__main__":
    main()
