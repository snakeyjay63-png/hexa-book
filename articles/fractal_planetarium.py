#!/usr/bin/env python3
"""
Hexa-Boek Fractaal Planetarium v3

Nieuwe lagen:
1. Jupiter als eigen zon (Galilese maan 1:2:4 Laplace resonantie)
2. Uranus ijsbaan (98° kanteling → maan draait op zijde)
3. E/M veld-laag (Schumann-frequentie per planeet)
4. Referentiepunt schakelen (vanuit elke planeet kijken)

Principes:
- Patronen herhalen op verschillende schalen
- Dezelfde Maxwell, verschillende harmonischen
- c = koppelingsconstante, niet snelheid
"""

import json
import math
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "fractal_planetarium.art.html")

# ── Planetaire data ──
PLANETS = [
    {
        "name": "Maan",
        "synodic": 29.5306,
        "orbital": 27.3217,        # siderisch
        "color": "#c0c0c0",
        "hue": 220,
        "schumann": None,          # geen eigen veld
        "field_strength": "0 μT",
    },
    {
        "name": "Venus",
        "synodic": 583.9209,
        "orbital": 224.7010,
        "color": "#e8c070",
        "hue": 40,
        "schumann": None,          # geen magnetosfeer
        "field_strength": "~0 μT",
    },
    {
        "name": "Aarde",
        "synodic": 365.2422,
        "orbital": 365.2564,
        "color": "#4a90d9",
        "hue": 210,
        "schumann": 7.83,          # Hz
        "field_strength": "25-65 μT",
    },
    {
        "name": "Mars",
        "synodic": 686.9798,
        "orbital": 687.0000,
        "color": "#c1440e",
        "hue": 15,
        "schumann": None,          # zwak veld
        "field_strength": "~0 μT",
    },
    {
        "name": "Jupiter",
        "synodic": 398.8844,
        "orbital": 4332.5900,
        "color": "#c88b3a",
        "hue": 30,
        "schumann": 10.0,          # Hz (ongeveer)
        "field_strength": "422 μT",
        "moons": [                 # Galilese maan!
            {"name": "Io",        "orbital": 1.769,  "resonance": 1, "color": "#d4a843"},
            {"name": "Europa",    "orbital": 3.551,  "resonance": 2, "color": "#a8c4d4"},
            {"name": "Ganymedes", "orbital": 7.155,  "resonance": 4, "color": "#8a8a8a"},
            {"name": "Callisto",  "orbital": 16.689, "resonance": None, "color": "#6a6a6a"},
        ],
    },
    {
        "name": "Saturnus",
        "synodic": 792.5395,
        "orbital": 10759.2200,
        "color": "#a8845a",
        "hue": 35,
        "schumann": None,
        "field_strength": "22.2 μT",
    },
    {
        "name": "Uranus",
        "synodic": 12340.0,
        "orbital": 30685.0,
        "color": "#72b5c4",
        "hue": 185,
        "schumann": None,
        "field_strength": "23.9 μT",
        "axial_tilt": 97.77,       # ° — op zijn ZIJKANT
        "moons": [
            {"name": "Miranda", "orbital": 1.413, "color": "#b0b0b0"},
            {"name": "Ariel",   "orbital": 2.520, "color": "#c0c0c0"},
            {"name": "Umbriel", "orbital": 4.144, "color": "#808080"},
            {"name": "Titania", "orbital": 8.706, "color": "#a0a0a0"},
            {"name": "Oberon",  "orbital": 13.463,"color": "#909090"},
        ],
    },
    {
        "name": "Neptunus",
        "synodic": 14640.0,
        "orbital": 60190.0,
        "color": "#3f54ba",
        "hue": 230,
        "schumann": None,
        "field_strength": "14.2 μT",
    },
]

# ── Nested sub-systems ──
# Jupiter = mini zonnestelsel
# Uranus = ijsbaan (kanteling)
SUBSYSTEMS = {
    "Jupiter": {
        "type": "mini-sun",
        "description": "Eigen resonantiestelsel, 318× Aarde",
        "laplace": True,           # 1:2:4 resonantie
    },
    "Uranus": {
        "type": "ice-track",
        "description": "98° kanteling → maan draait op zijde",
        "tilt": 97.77,
    },
}

# ── E/M resonantie ──
EM_LAYERS = {
    "Aarde": {
        "schumann": 7.83,
        "harmonics": [7.83, 15.66, 22.96, 30.85, 38.57],  # Hz
        "brain_resonance": "theta (4-8 Hz)",
    },
    "Jupiter": {
        "schumann": 10.0,
        "harmonics": [10.0, 20.0, 30.0],
        "brain_resonance": "alfa (8-12 Hz)",
    },
}


def digital_root(n):
    n = abs(int(round(n)))
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def compute_main_layout():
    """Hoofdslagen — 8 planeten in 3 ringen."""
    positions = []
    cx, cy = 500, 400
    base_r = 90

    for i, p in enumerate(PLANETS):
        orbital = p["orbital"]
        earth_orbital = planet_lookup("Aarde")["orbital"]
        ratio = orbital / earth_orbital

        ring = i // 3
        angle_in_ring = i % 3
        radius = base_r + (ring * 75)

        theta = angle_in_ring * (2 * math.pi / 3) + (ring * math.pi / 5)
        x = cx + radius * math.cos(theta)
        y = cy + radius * math.sin(theta)

        rotation_secs = 30 * ratio
        direction = -1 if ring % 2 == 1 else 1

        positions.append({
            **p,
            "x": x, "y": y,
            "radius": radius,
            "ratio": ratio,
            "rotation_secs": rotation_secs * direction,
            "direction": direction,
            "dr": digital_root(orbital + i),
            "ring": ring,
        })

    return positions


def compute_subsystem_jupiter():
    """Jupiter als mini-zon met Galilese maan (1:2:4 Laplace).
    Retourneert posities relatief (0,0) = Jupiter-center."""
    moons = planet_lookup("Jupiter")["moons"]
    positions = []

    for i, m in enumerate(moons):
        base_period = moons[0]["orbital"]  # Io
        if m["resonance"]:
            ratio_to_io = m["resonance"] / moons[0]["resonance"]
        else:
            ratio_to_io = m["orbital"] / base_period

        sub_radius = 18 + (i * 12)
        theta = i * (2 * math.pi / 4)
        x = sub_radius * math.cos(theta)
        y = sub_radius * math.sin(theta)

        rotation_secs = 8 * ratio_to_io

        positions.append({
            **m,
            "rx": x, "ry": y,   # relatieve coördinaten
            "sub_radius": sub_radius,
            "ratio_to_io": ratio_to_io,
            "rotation_secs": rotation_secs,
            "dr": digital_root(m["orbital"] * 100 + i),
        })

    return positions


def compute_subsystem_uranus():
    """Uranus ijsbaan — maan-systeem op 98° kanteling.
    Retourneert posities relatief (0,0) = Uranus-center."""
    moons = planet_lookup("Uranus")["moons"]
    positions = []
    tilt = math.radians(97.77)

    for i, m in enumerate(moons):
        sub_radius = 15 + (i * 9)
        theta = i * (2 * math.pi / 5)

        x_raw = sub_radius * math.cos(theta)
        y_raw = sub_radius * math.sin(theta)

        # Kanteling: Y wordt geschaald met cos(tilt)
        x_tilted = x_raw
        y_tilted = y_raw * math.cos(tilt)

        rotation_secs = 6 * (m["orbital"] / moons[0]["orbital"])

        positions.append({
            **m,
            "rx": x_tilted, "ry": y_tilted,
            "sub_radius": sub_radius,
            "tilt_deg": 97.77,
            "rotation_secs": rotation_secs,
            "dr": digital_root(m["orbital"] * 100 + i),
        })

    return positions


def planet_lookup(name):
    for p in PLANETS:
        if p["name"] == name:
            return p
    return PLANETS[2]  # fallback: Aarde


def build_fractal_planetarium():
    """Bouw het complete fractale planetarium."""
    main = compute_main_layout()

    # Sub-systemen zijn relatief (0,0 = planeet-center)
    # Worden later gepositioneerd via transform
    jupiter_moons = compute_subsystem_jupiter()
    uranus_moons = compute_subsystem_uranus()

    return {
        "main": main,
        "jupiter_moons": jupiter_moons,
        "uranus_moons": uranus_moons,
        "em_layers": EM_LAYERS,
    }


def gen_fractal_html(data):
    """Genereer HTML met fractale lagen."""
    main = data["main"]
    j_moons = data["jupiter_moons"]
    u_moons = data["uranus_moons"]
    em = data["em_layers"]

    cx, cy = 500, 400

    # ── Keyframes ──
    keyframes = ""
    for i, p in enumerate(main):
        dur = abs(p["rotation_secs"])
        rev = "reverse" if p["direction"] < 0 else ""
        keyframes += f"""
  @keyframes orbit-{i} {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}"""

    # ── Hoofdingen ──
    main_gears = ""
    for i, p in enumerate(main):
        dur = abs(p["rotation_secs"])
        rev = "reverse" if p["direction"] < 0 else ""
        hue = p["hue"]

        has_sub = p["name"] in ("Jupiter", "Uranus")
        marker = " ◈" if has_sub else ""

        main_gears += f"""
    <!-- {p['name']} · T:{p['orbital']:.0f}d{marker} -->
    <g transform="translate({p['x']:.1f}, {p['y']:.1f})">
      <g class="orbit-{i}" style="transform-origin:8px 8px; animation:orbit-{i} {dur:.2f}s linear infinite {rev};">
        <circle cx="0" cy="0" r="8" fill="hsl({hue},40%,45%)" opacity="0.8"/>
        <circle cx="0" cy="0" r="3" fill="hsl({hue},60%,70%)" opacity="0.9"/>
        <text x="12" y="4" fill="hsl({hue},30%,65%)" font-size="8" font-family="monospace" opacity="0.7">{p['name']}</text>
      </g>
      {f'<circle cx="0" cy="0" r="14" fill="none" stroke="hsl({hue},30%,30%)" stroke-width="0.3" stroke-dasharray="1,2" opacity="0.2"/>' if has_sub else ''}
    </g>"""

    # ── Jupiter Galilese maan ──
    j_base = next(p for p in main if p["name"] == "Jupiter")
    jupiter_section = f"""
    <!-- ═══ Jupiter Sub-System: Galilese Maan (1:2:4 Laplace) ═══ -->
    <g transform="translate({j_base['x']:.1f}, {j_base['y']:.1f})" opacity="0.75">
      <g transform="scale(2.5)" style="transform-origin:0px 0px;">
        <!-- Jupiter center -->
        <circle cx="0" cy="0" r="3" fill="hsl(30,50%,35%)" stroke="hsl(30,60%,55%)" stroke-width="0.5" opacity="0.9"/>
        <!-- Baanringen -->
        <circle cx="0" cy="0" r="18" fill="none" stroke="hsl(30,20%,25%)" stroke-width="0.15" opacity="0.2"/>
        <circle cx="0" cy="0" r="30" fill="none" stroke="hsl(30,20%,25%)" stroke-width="0.15" opacity="0.15"/>
        <circle cx="0" cy="0" r="42" fill="none" stroke="hsl(30,20%,25%)" stroke-width="0.15" opacity="0.12"/>
        <circle cx="0" cy="0" r="54" fill="none" stroke="hsl(30,20%,25%)" stroke-width="0.15" opacity="0.1"/>"""

    for i, m in enumerate(j_moons):
        dur = m["rotation_secs"]
        color = m.get("color", "#888")
        label = m["name"]
        res = m.get("resonance", "?")
        res_str = f" ({res}:1)" if res else ""

        # Relatieve coördinaten (reeds berekend)
        rx = m["rx"]
        ry = m["ry"]

        jupiter_section += f"""
        <g class="j-moon-{i}" style="transform-origin:0px 0px; animation:orbit-jm{i} {dur:.2f}s linear infinite;">
          <circle cx="{rx:.1f}" cy="{ry:.1f}" r="1.5" fill="{color}" opacity="0.8"/>
          <text x="{rx:.1f}" y="{ry:.1f}-3" fill="{color}" font-size="2.5" font-family="monospace" opacity="0.6" text-anchor="middle">{label}{res_str}</text>
        </g>
        <line x1="0" y1="0" x2="{rx:.1f}" y2="{ry:.1f}" stroke="hsl(30,20%,30%)" stroke-width="0.2" opacity="0.15"/>"""

        keyframes += f"""
  @keyframes orbit-jm{i} {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}"""

    jupiter_section += """
      </g>
    </g>"""

    # ── Uranus ijsbaan ──
    u_base = next(p for p in main if p["name"] == "Uranus")
    uranus_section = f"""
    <!-- ═══ Uranus Sub-System: IJsbane (98° kanteling) ═══ -->
    <g transform="translate({u_base['x']:.1f}, {u_base['y']:.1f})" opacity="0.75">
      <g transform="scale(2.5)" style="transform-origin:0px 0px;">
        <!-- Uranus center -->
        <circle cx="0" cy="0" r="3" fill="hsl(185,40%,35%)" stroke="hsl(185,50%,55%)" stroke-width="0.5" opacity="0.9"/>
        <!-- IJsbane (gekantelde baan) -->
        <ellipse cx="0" cy="0" rx="25" ry="4" fill="none" stroke="hsl(185,20%,30%)" stroke-width="0.2" opacity="0.2"/>
        <ellipse cx="0" cy="0" rx="35" ry="6" fill="none" stroke="hsl(185,20%,30%)" stroke-width="0.2" opacity="0.15"/>"""

    for i, m in enumerate(u_moons):
        color = m.get("color", "#888")
        dur = m["rotation_secs"]

        # Relatieve gekantelde coördinaten
        rx = m["rx"]
        ry = m["ry"]

        uranus_section += f"""
        <g class="u-moon-{i}" style="transform-origin:0px 0px; animation:orbit-um{i} {dur:.2f}s linear infinite;">
          <circle cx="{rx:.1f}" cy="{ry:.1f}" r="1.2" fill="{color}" opacity="0.7"/>
          <text x="{rx:.1f}" y="{ry:.1f}-3" fill="{color}" font-size="2" font-family="monospace" opacity="0.5" text-anchor="middle">{m['name']}</text>
        </g>
        <line x1="0" y1="0" x2="{rx:.1f}" y2="{ry:.1f}" stroke="hsl(185,20%,30%)" stroke-width="0.2" opacity="0.12"/>"""

        keyframes += f"""
  @keyframes orbit-um{i} {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}"""

    uranus_section += """
      </g>
    </g>"""

    # ── E/M Veld Lagen ──
    em_layer = ""
    for pname, edata in em.items():
        p = next((x for x in main if x["name"] == pname), None)
        if not p:
            continue
        hue = p["hue"]
        freq = edata["schumann"]
        brain = edata["brain_resonance"]

        # Pulserende ring = E/M veld
        pulse_dur = 1.0 / freq * 5  # schaal naar zichtbaar
        em_layer += f"""
    <!-- E/M veld: {pname} · Schumann {freq} Hz -->
    <g transform="translate({p['x']:.1f}, {p['y']:.1f})" opacity="0.4">
      <circle cx="0" cy="0" r="20" fill="none" stroke="hsl({hue},50%,40%)" stroke-width="0.5" class="em-pulse-{pname}" style="animation:em-pulse {pulse_dur:.2f}s ease-in-out infinite;"/>
      <circle cx="0" cy="0" r="28" fill="none" stroke="hsl({hue},40%,30%)" stroke-width="0.3" class="em-pulse-{pname}-2" style="animation:em-pulse-2 {pulse_dur*1.5:.2f}s ease-in-out infinite;"/>
    </g>"""

        keyframes += f"""
  @keyframes em-pulse {{
    0%, 100% {{ r: 20px; opacity: 0.4; }}
    50% {{ r: 24px; opacity: 0.2; }}
  }}
  @keyframes em-pulse-2 {{
    0%, 100% {{ r: 28px; opacity: 0.3; }}
    50% {{ r: 32px; opacity: 0.15; }}
  }}"""

    # ── Zon ──
    sun = f"""
    <!-- 0.0.0.0 — Zon -->
    <g transform="translate({cx}, {cy})">
      <circle cx="0" cy="0" r="12" fill="hsl(45,80%,55%)" opacity="0.8"/>
      <circle cx="0" cy="0" r="4" fill="hsl(45,100%,85%)" opacity="1"/>
      <circle cx="0" cy="0" r="25" fill="none" stroke="hsl(45,40%,40%)" stroke-width="0.3" opacity="0.2"/>
      <circle cx="0" cy="0" r="40" fill="none" stroke="hsl(45,30%,30%)" stroke-width="0.3" opacity="0.15"/>
    </g>"""

    # ── Baanlijnen ──
    orbits = ""
    for i, p in enumerate(main):
        r = p["radius"]
        orbits += f"""
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none"
            stroke="hsl(45,15%,18%)" stroke-width="0.3" opacity="0.12"
            stroke-dasharray="2,3"/>"""

    # ── Legenda ──
    legend_items = ""
    for p in main:
        hue = p["hue"]
        has_sub = p["name"] in SUBSYSTEMS
        marker = " ◈" if has_sub else ""
        field = p.get("field_strength", "—")
        legend_items += f"""
      <div class="legend-item" style="--lhue:{hue}">
        <span class="legend-dot"></span> {p['name']}{marker} <span class="legend-field">({field})</span>
      </div>"""

    sub_legend = ""
    for jm in j_moons:
        res = jm.get("resonance", "?")
        res_str = f"{res}: " if res else ""
        sub_legend += f"""
      <div class="legend-sub">
        <span class="legend-sub-dot" style="background:{jm.get('color','#888')}"></span>
        {jm['name']} ({res_str}{jm['orbital']:.2f}d)
      </div>"""

    # ── Data voor JS ──
    main_json = json.dumps([{
        "name": p["name"], "x": p["x"], "y": p["y"], "hue": p["hue"],
        "orbital": p["orbital"], "synodic": p["synodic"],
        "field": p.get("field_strength", "—"),
        "schumann": p.get("schumann"),
        "has_subsystem": p["name"] in SUBSYSTEMS,
        "sub_type": SUBSYSTEMS.get(p["name"], {}).get("type", ""),
    } for p in main])

    j_moons_json = json.dumps([{
        "name": m["name"], "resonance": m.get("resonance"),
        "orbital": m["orbital"], "color": m.get("color"),
    } for m in j_moons])

    u_moons_json = json.dumps([{
        "name": m["name"], "orbital": m["orbital"], "color": m.get("color"),
    } for m in u_moons])

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>• Fractaal Planetarium v3 | Hexa-Boek</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #06060a;
    color: #d4d4e0;
    font-family: 'Instrument Sans', -apple-system, sans-serif;
    overflow: hidden;
    width: 100vw; height: 100vh;
  }}
  .planetarium {{ position: relative; width: 100vw; height: 100vh; }}
  .planetarium svg.main {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
{keyframes}

  .legend {{
    position: fixed; top: 12px; right: 12px;
    display: flex; flex-direction: column; gap: 4px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem;
    color: hsl(45,30%,50%); opacity: 0.5; z-index: 10;
    background: rgba(6,6,10,0.85); padding: 8px 12px; border-radius: 6px;
  }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; }}
  .legend-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: hsl(var(--lhue),50%,55%);
  }}
  .legend-field {{ opacity: 0.6; }}
  .legend-sub {{ display: flex; align-items: center; gap: 4px; padding-left: 12px; font-size: 0.55rem; opacity: 0.7; }}
  .legend-sub-dot {{ width: 4px; height: 4px; border-radius: 50%; }}
  .legend-sub-title {{ opacity: 0.5; margin-top: 4px; font-size: 0.55rem; }}

  .metadata {{
    position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%);
    text-align: center;
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem;
    color: hsl(45,30%,40%); opacity: 0.35; z-index: 10;
  }}
  .metadata div {{ margin: 2px 0; }}

  .tooltip {{
    position: fixed;
    background: rgba(6,6,10,0.92);
    border: 1px solid hsl(var(--hue),40%,25%);
    border-radius: 6px; padding: 6px 10px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem;
    color: hsl(var(--hue),40%,60%);
    pointer-events: none; opacity: 0; transition: opacity .12s ease;
    z-index: 200; --hue: 200;
  }}
  .tooltip.visible {{ opacity: 0.9; }}

  .layer-toggle {{
    position: fixed; bottom: 16px; right: 16px;
    display: flex; gap: 6px; z-index: 10;
  }}
  .layer-btn {{
    background: rgba(6,6,10,0.85);
    border: 1px solid hsl(45,20%,25%);
    color: hsl(45,30%,55%);
    padding: 4px 8px; border-radius: 4px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.55rem;
    cursor: pointer; opacity: 0.6; transition: opacity .15s;
  }}
  .layer-btn:hover {{ opacity: 1; }}
  .layer-btn.active {{ opacity: 1; border-color: hsl(45,40%,45%); }}
</style>
</head>
<body>
<div class="planetarium">
  <svg class="main" viewBox="0 0 1000 800" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <style>{keyframes}</style>
    <defs>
      <radialGradient id="bg-grad" cx="50%" cy="50%">
        <stop offset="0%" stop-color="hsl(45,15%,5%)" />
        <stop offset="100%" stop-color="#06060a" />
      </radialGradient>
    </defs>

    <rect width="100%" height="100%" fill="url(#bg-grad)" />

    <!-- Baanringen -->
{orbits}

    <!-- Zon -->
    {sun}

    <!-- Hoofdingen -->
    {main_gears}

    <!-- Jupiter sub-systeem (Galilese maan) -->
    {jupiter_section}

    <!-- Uranus sub-systeem (ijsbaan) -->
    {uranus_section}

    <!-- E/M veld lagen -->
    {em_layer}

    <!-- Fractaal label -->
    <text x="20" y="30" fill="hsl(45,30%,35%)" font-size="8" font-family="monospace" opacity="0.3">
      fractaal v3 · Maxwell constant · harmonischen variëren · c²=1/(ε₀μ₀)
    </text>
  </svg>

  <div class="legend">
    <div style="margin-bottom:4px;opacity:0.7;">• Planetaire Cycli ◈=sub-systeem</div>
    {legend_items}
    <div class="legend-sub-title">══ Jupiter: Galilese Maan (1:2:4 Laplace) ══</div>
    {sub_legend}
    <div class="legend-sub-title">══ Uranus: IJsbane (98° kanteling) ══</div>
    {" ".join(f'<div class="legend-sub"><span class="legend-sub-dot" style="background:{m.get("color","#888")}"></span>{m["name"]} ({m["orbital"]:.2f}d)</div>' for m in u_moons)}
  </div>

  <div class="metadata">
    <div>• Fractaal Planetarium — 8 planeten · 2 sub-systemen · E/M resonantie</div>
    <div>Maxwell constant overal · harmonischen variëren per planeet · c²=1/(ε₀μ₀)</div>
    <div>0.0.0.0 = zon · patronen herhalen · elke planeet = eigen resonantiestelsel</div>
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

<script>
  const main = {main_json};
  const jMoons = {j_moons_json};
  const uMoons = {u_moons_json};
  const tooltip = document.getElementById('tooltip');

  document.addEventListener('mousemove', function(e) {{
    const svg = document.querySelector('svg.main');
    const pt = svg.createSVGPoint();
    pt.x = e.clientX; pt.y = e.clientY;
    const ctm = svg.getScreenCTM();
    if (!ctm) return;
    const svgP = pt.matrixTransform(ctm.inverse());

    let found = false;
    for (const p of main) {{
      const dx = svgP.x - p.x;
      const dy = svgP.y - p.y;
      if (Math.sqrt(dx*dx + dy*dy) < 18) {{
        tooltip.style.setProperty('--hue', p.hue);
        let html = p.name + ' · ' + p.orbital.toFixed(0) + 'd · veld: ' + p.field;
        if (p.schumann) html += ' · Schumann: ' + p.schumann + 'Hz';
        if (p.has_subsystem) html += '<br>◈ ' + p.sub_type + (p.name==='Jupiter' ? ' (1:2:4 Laplace)' : ' (98° ijsbaan)');
        tooltip.innerHTML = html;
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top = (e.clientY - 8) + 'px';
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
    print("• Hexa-Boek Fractaal Planetarium v3 — Geneste Systeem")
    print(f"  Planeten: {len(PLANETS)}")
    print(f"  Jupiter-maan: {len(planet_lookup('Jupiter')['moons'])} (1:2:4 Laplace)")
    print(f"  Uranus-maan: {len(planet_lookup('Uranus')['moons'])} (98° ijsbaan)")
    print(f"  E/M lagen: {', '.join(EM_LAYERS.keys())}")
    print()

    data = build_fractal_planetarium()
    html = gen_fractal_html(data)

    with open(OUTPUT, "w") as f:
        f.write(html)

    print(f"  → {OUTPUT}")

    # Verhoudingen
    j_moons = planet_lookup("Jupiter")["moons"]
    print(f"  Laplace resonantie: {j_moons[0]['name']}={j_moons[0]['orbital']:.3f}d")
    print(f"    1:2:4 → {j_moons[0]['name']}:{j_moons[1]['name']}:{j_moons[2]['name']}")
    print(f"    {j_moons[0]['orbital']:.3f} : {j_moons[1]['orbital']:.3f} : {j_moons[2]['orbital']:.3f}")
    print(f"    ≈ 1 : {j_moons[1]['orbital']/j_moons[0]['orbital']:.2f} : {j_moons[2]['orbital']/j_moons[0]['orbital']:.2f}")

    print(f"  Uranus tilt: {planet_lookup('Uranus')['axial_tilt']}°")
    print(f"  E/M: {', '.join(f'{k}={v['schumann']}Hz' for k,v in EM_LAYERS.items())}")
    print(f"  • patronen herhalen · Maxwell constant · c²=1/(ε₀μ₀)")


if __name__ == "__main__":
    main()
