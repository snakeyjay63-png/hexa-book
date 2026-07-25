#!/usr/bin/env python3
"""
Hexa-Boek Geometric Visuals — BPM-Synced Edition
Pure geometry. No external assets.
Reacts to audio sections: intro/build/peak/transition/outro.
Frequencies drive geometry: layer count → ring count → pulse speed.
Output: PNG frames → ffmpeg MP4
"""

import numpy as np
from PIL import Image, ImageDraw
import math
import os
import sys

# --- Config ---
WIDTH = 1920
HEIGHT = 1080
FPS = 25
DURATION_SEC = 180
BPM = 138
BEAT = 60.0 / BPM
BAR = BEAT * 4
TOTAL_FRAMES = FPS * DURATION_SEC
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "psy_frames")

# --- Palette ---
BG = (5, 10, 8)
PALETTE = {
    "teal":      (0, 220, 180),
    "green":     (0, 255, 80),
    "acid":      (180, 255, 0),
    "cyan":      (0, 200, 255),
    "magenta":   (255, 0, 180),
    "violet":    (120, 0, 255),
    "amber":     (255, 180, 0),
    "deep_green":(0, 100, 60),
    "forest":    (0, 60, 40),
    "white":     (240, 240, 240),
}

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def pulse(t, freq=1.0, phase=0.0):
    return 0.5 + 0.5 * math.sin(2 * math.pi * (freq * t + phase))

def beat_pulse(time_s, intensity=1.0):
    """Pulse synced to BPM beat."""
    beat_pos = (time_s / BEAT) % 1.0
    return (1.0 - beat_pos) ** 3 * intensity

def bar_pulse(time_s, intensity=1.0):
    """Pulse synced to bar boundary (stronger at bar start)."""
    bar_pos = (time_s / BAR) % 1.0
    return (1.0 - bar_pos) ** 2 * intensity

# --- Drawing helpers ---
def draw_circle(draw, cx, cy, r, fill=None, outline=None, width=1):
    if r < 0.5:
        return
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)

def draw_line(draw, x1, y1, x2, y2, fill, width=1):
    draw.line([(x1, y1), (x2, y2)], fill=fill, width=width)

def draw_polygon(draw, points, fill=None, outline=None, width=1):
    draw.polygon(points, fill=fill, outline=outline, width=width)

# --- Section detection ---
def section_at(time_s):
    """Return section name based on time."""
    bar = time_s / BAR
    if bar < 8:
        return "intro", bar / 8
    elif bar < 32:
        return "build", (bar - 8) / 24
    elif bar < 48:
        return "peak1", (bar - 32) / 16
    elif bar < 56:
        return "transition", (bar - 48) / 8
    elif bar < 80:
        return "peak2", (bar - 56) / 24
    else:
        return "outro", min((bar - 80) / 8, 1.0)

# --- Scene: Flower of Life (intro) ---
def scene_flower_of_life(draw, time_s, progress):
    cx, cy = WIDTH // 2, HEIGHT // 2
    bp = beat_pulse(time_s, 0.3)
    bar_p = bar_pulse(time_s, 0.2)
    base_r = 100 + 40 * bp

    rotation = time_s * 0.1 * math.pi
    color_t = pulse(time_s / DURATION_SEC, 0.2)

    main = lerp_color(PALETTE["teal"], PALETTE["green"], color_t)
    glow = lerp_color(PALETTE["cyan"], PALETTE["teal"], 1 - color_t)

    # Central circle
    draw_circle(draw, cx, cy, base_r, outline=main, width=2 + int(bp * 2))

    # Ring 1: 6 circles
    for i in range(6):
        angle = rotation + i * math.pi / 3
        px = cx + base_r * math.cos(angle)
        py = cy + base_r * math.sin(angle)
        r = base_r * (0.7 + 0.3 * pulse(time_s, 0.5, i * 0.3))
        draw_circle(draw, px, py, r, outline=main, width=2)

    # Ring 2: 12 circles
    for i in range(12):
        angle = rotation * 0.5 + i * math.pi / 6
        px = cx + 2 * base_r * math.cos(angle)
        py = cy + 2 * base_r * math.sin(angle)
        r = base_r * (0.5 + 0.2 * pulse(time_s, 0.7, i * 0.2))
        alpha = int(80 + 120 * pulse(time_s, 0.3, i * 0.4))
        c = tuple(min(255, x + alpha // 3) for x in glow)
        draw_circle(draw, px, py, r, outline=c, width=1)

    # Inner triangles (3-6-9)
    for tri in range(2):
        tri_angle = rotation * 0.7 * (1 if tri == 0 else -1)
        pts = []
        for j in range(3):
            a = tri_angle + j * 2 * math.pi / 3 + (math.pi / 3 if tri == 1 else 0)
            r_tri = base_r * 1.5 * (1 + 0.1 * bp)
            pts.append((cx + r_tri * math.cos(a), cy + r_tri * math.sin(a)))
        tri_c = lerp_color(PALETTE["acid"], PALETTE["magenta"], pulse(time_s, 0.4, tri))
        draw_polygon(draw, pts, outline=tri_c, width=2)

    # Glyph overlay
    draw_glyph(draw, cx, cy + base_r * 2.8, "\u0950", time_s, scale=0.3 + 0.1 * bp)

# --- Scene: Hex Grid (build) ---
def scene_hex_grid(draw, time_s, progress):
    cx, cy = WIDTH // 2, HEIGHT // 2
    bp = beat_pulse(time_s, 0.5)
    bar_p = bar_pulse(time_s, 0.3)

    hex_size = 35 + 8 * bp
    cols = int(WIDTH / (hex_size * 1.8)) + 2
    rows = int(HEIGHT / (hex_size * 1.6)) + 2

    for row in range(-rows, rows):
        for col in range(-cols, cols):
            x = cx + col * hex_size * 1.8
            y = cy + row * hex_size * 1.6
            if col % 2 != 0:
                y += hex_size * 0.8

            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            max_dist = math.sqrt(cx ** 2 + cy ** 2)
            wave = math.sin(dist / 50 - time_s * 2)
            wave_norm = (wave + 1) / 2

            if wave_norm > 0.35:
                intensity = int(40 + 210 * (wave_norm - 0.35) / 0.65)
                if wave_norm < 0.6:
                    c = lerp_color(PALETTE["teal"], PALETTE["acid"], (wave_norm - 0.35) / 0.25)
                else:
                    c = lerp_color(PALETTE["acid"], PALETTE["magenta"], (wave_norm - 0.6) / 0.4)
                c = tuple(min(255, x + intensity // 4) for x in c)

                pts = []
                for i in range(6):
                    a = math.pi / 6 + i * math.pi / 3
                    pts.append((x + hex_size * 0.9 * math.cos(a),
                                y + hex_size * 0.9 * math.sin(a)))
                draw_polygon(draw, pts, outline=c, width=max(1, int(2 * wave_norm + bp)))

    # Layer indicators
    layer_count = int(2 + 6 * progress)  # 2-8 layers
    draw_layer_rings(draw, cx, cy, layer_count, time_s)

# --- Scene: Digital Root Mandala (peak 1) ---
def scene_dr_mandala(draw, time_s, progress):
    cx, cy = WIDTH // 2, HEIGHT // 2
    bp = beat_pulse(time_s, 0.6)
    max_r = min(WIDTH, HEIGHT) * 0.42

    # 9 concentric rings = 9 digital roots
    for ring in range(1, 10):
        r = max_r * ring / 9
        ring_pulse = pulse(time_s / 10, 0.5, ring * 0.15)
        ring_color = list(PALETTE.values())[ring % len(PALETTE)]

        bright = int(80 + 175 * ring_pulse)
        rc = tuple(min(255, x + bright // 2) for x in ring_color)

        n_segments = ring * 3  # 3, 6, 9...
        for seg in range(n_segments):
            a1 = time_s * 0.5 + seg * 2 * math.pi / n_segments
            a2 = a1 + 2 * math.pi / n_segments * (0.5 + 0.5 * ring_pulse)

            n_pts = max(6, int(12 * ring_pulse))
            pts = []
            for p in range(n_pts + 1):
                a = a1 + (a2 - a1) * p / n_pts
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            if len(pts) >= 2:
                draw_line(draw, pts[0][0], pts[0][1], pts[-1][0], pts[-1][1], rc, width=max(1, ring))

        # Radial connectors
        if ring > 1:
            for seg in range(ring * 3):
                a = time_s * 0.5 + seg * 2 * math.pi / (ring * 3)
                r_inner = max_r * (ring - 1) / 9
                draw_line(draw,
                    cx + r_inner * math.cos(a), cy + r_inner * math.sin(a),
                    cx + r * math.cos(a), cy + r * math.sin(a),
                    PALETTE["deep_green"], width=1)

    # Center glow with beat
    glow_r = 25 + 30 * (0.5 + 0.5 * bp)
    draw_circle(draw, cx, cy, glow_r, fill=PALETTE["teal"])

# --- Scene: Tunnel (transition) ---
def scene_tunnel(draw, time_s, progress):
    cx, cy = WIDTH // 2, HEIGHT // 2
    bp = beat_pulse(time_s, 0.7)

    n_rings = 12 + int(4 * bp)
    for ring in range(n_rings, 0, -1):
        phase = (time_s * 2 + ring) % n_rings
        r = (ring / n_rings) * min(WIDTH, HEIGHT) * 0.45
        rotation = phase * math.pi * 2 / n_rings

        n_sides = 6
        pts = []
        for i in range(n_sides):
            a = rotation + i * 2 * math.pi / n_sides
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

        rc = lerp_color(PALETTE["teal"], PALETTE["magenta"], ring / n_rings)
        intensity = int(40 + 210 * (1 - ring / n_rings))
        c = tuple(min(255, x + intensity) for x in rc)

        draw_polygon(draw, pts, outline=c, width=max(1, 3 - ring // 4))

        # Inner connections
        if ring > 1:
            inner_r = ((ring - 1) / n_rings) * min(WIDTH, HEIGHT) * 0.45
            inner_rot = (phase - 0.5) * math.pi * 2 / n_rings
            for i in range(n_sides):
                a_out = rotation + i * 2 * math.pi / n_sides
                a_in = inner_rot + i * 2 * math.pi / n_sides
                draw_line(draw,
                    cx + r * math.cos(a_out), cy + r * math.sin(a_out),
                    cx + inner_r * math.cos(a_in), cy + inner_r * math.sin(a_in),
                    PALETTE["deep_green"], width=1)

# --- Scene: Sacred Geometry (peak 2) ---
def scene_sacred_geometry(draw, time_s, progress):
    cx, cy = WIDTH // 2, HEIGHT // 2
    bp = beat_pulse(time_s, 0.8)
    rotation = time_s * 0.3 * math.pi

    base_r = min(WIDTH, HEIGHT) * 0.32 * (1 + 0.1 * bp)

    # Metatron's cube
    n_points = 13
    pts = [(cx, cy)]
    for i in range(6):
        a = rotation + i * math.pi / 3
        pts.append((cx + base_r * math.cos(a), cy + base_r * math.sin(a)))
    for i in range(6):
        a = rotation * 0.7 + i * math.pi / 3 + math.pi / 6
        pts.append((cx + base_r * 1.6 * math.cos(a), cy + base_r * 1.6 * math.sin(a)))

    # Connections
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = math.sqrt((pts[i][0] - pts[j][0])**2 + (pts[i][1] - pts[j][1])**2)
            if d < base_r * 2.2:
                pv = pulse(time_s / 5, 0.3, (i + j) * 0.1)
                alpha = int(25 + 130 * pv)
                c = lerp_color(PALETTE["teal"], PALETTE["violet"], pv)
                c = tuple(min(255, x + alpha) for x in c)
                draw_line(draw, pts[i][0], pts[i][1], pts[j][0], pts[j][1], c, width=max(1, int(2 * pv + bp)))

    # Points
    for i, (px, py) in enumerate(pts):
        r = 12 + 18 * pulse(time_s, 0.5, i * 0.2) + 8 * bp
        draw_circle(draw, px, py, r, outline=PALETTE["teal"], width=2)

    # Outer mandala
    for i in range(72):
        a1 = time_s * 0.5 + i * 2 * math.pi / 72
        a2 = a1 + 2 * math.pi / 72
        r1 = base_r * 2.0
        r2 = base_r * 2.2 * (0.5 + 0.5 * pulse(time_s, 1.0, i * 0.1))
        x1 = r1 * math.cos(a1) + cx
        y1 = r1 * math.sin(a1) + cy
        x2 = r2 * math.cos(a2) + cx
        y2 = r2 * math.sin(a2) + cy
        draw_line(draw, x1, y1, x2, y2, PALETTE["green"], width=2)

# --- Scene: Void (outro) ---
def scene_void(draw, time_s, progress):
    cx, cy = WIDTH // 2, HEIGHT // 2
    bp = beat_pulse(time_s, 0.2 * (1 - progress))

    n_voids = 5
    for i in range(n_voids):
        r = 40 + 350 * pulse(time_s / 15, 0.2, i * 0.4) * (1 - progress * 0.7)
        alpha = int(15 + 70 * pulse(time_s / 10, 0.3, i * 0.5) * (1 - progress))
        c = lerp_color(PALETTE["teal"], PALETTE["violet"], pulse(time_s / 20, 0.15, i * 0.3))
        c = tuple(min(255, x + alpha) for x in c)
        draw_circle(draw, cx, cy, r, outline=c, width=max(1, 3 - i // 2))

    # Particles
    np.random.seed(42)
    for _ in range(60):
        px = int(cx + np.random.randn() * 400 * (1 - progress * 0.5))
        py = int(cy + np.random.randn() * 400 * (1 - progress * 0.5))
        size = int(1 + 2 * pulse(time_s, 0.5, np.random.random()) * (1 - progress * 0.8))
        if size > 0:
            draw_circle(draw, px, py, size, fill=PALETTE["teal"])

# --- Layer indicator rings ---
def draw_layer_rings(draw, cx, cy, layer_count, time_s):
    """Draw small rings showing active layer count."""
    r_base = 60
    for i in range(layer_count):
        r = r_base + i * 8
        alpha = int(40 + 60 * pulse(time_s / 3, 1.0, i * 0.5))
        c = tuple(min(255, x + alpha) for x in PALETTE["teal"])
        draw_circle(draw, WIDTH - 50, 50, r, outline=c, width=1)

# --- Glyph overlay ---
def draw_glyph(draw, x, y, text, time_s, scale=0.5):
    """Draw text as simple glyph approximation."""
    # PIL doesn't handle all Unicode well, so draw as colored dots
    # representing the glyph's energy
    if not text:
        return
    np.random.seed(hash(text) % (2**31))
    for i, ch in enumerate(text):
        val = ord(ch) % 9 + 1
        freq_x = x + (i - len(text)/2) * 20 * scale
        freq_y = y + (val - 5) * 15 * scale
        r = 5 + 8 * pulse(time_s, 0.5, i * 0.3) * scale
        c = list(PALETTE.values())[val % len(PALETTE)]
        draw_circle(draw, freq_x, freq_y, r, fill=c)

# --- Main render ---
def render_frame(frame_idx):
    time_s = frame_idx / FPS
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    section, progress = section_at(time_s)

    if section == "intro":
        scene_flower_of_life(draw, time_s, progress)
    elif section == "build":
        scene_hex_grid(draw, time_s, progress)
    elif section == "peak1":
        scene_dr_mandala(draw, time_s, progress)
    elif section == "transition":
        scene_tunnel(draw, time_s, progress)
    elif section == "peak2":
        scene_sacred_geometry(draw, time_s, progress)
    elif section == "outro":
        scene_void(draw, time_s, progress)

    return img

if __name__ == "__main__":
    out_dir = OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    print(f"Rendering {TOTAL_FRAMES} frames ({DURATION_SEC}s @ {FPS}fps, {BPM} BPM)...")
    for i in range(TOTAL_FRAMES):
        img = render_frame(i)
        path = os.path.join(out_dir, f"{i:04d}.png")
        img.save(path, "PNG")
        if i % 50 == 0:
            sec = i / FPS
            sec_name, _ = section_at(sec)
            print(f"  Frame {i}/{TOTAL_FRAMES} ({sec:.0f}s — {sec_name})...")

    print(f"Done. Frames in: {out_dir}")
    print(f"Next: ffmpeg -r {FPS} -i {out_dir}/%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4")
