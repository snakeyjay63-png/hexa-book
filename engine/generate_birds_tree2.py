#!/usr/bin/env python3
"""
Vogels in een boom — efficiënte versie

Generatieve boom met vectorized lijnen.
Vogels op takken. Zingend glow.
"""

import numpy as np
import subprocess
import os
import math

W, H = 1920, 1080
FPS = 25
DUR = 60
FRAMES = int(FPS * DUR)

raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bird_tree_v2")
os.makedirs(raw_dir, exist_ok=True)

np.random.seed(47)

# === Boom genereren ===
def gen_tree(x, y, angle, length, depth, max_depth, branches=None):
    if branches is None:
        branches = []
    if depth > max_depth or length < 5:
        return branches
    x2 = x + length * np.cos(angle)
    y2 = y + length * np.sin(angle)
    thickness = max(1, (max_depth - depth + 1) * 1.5)
    branches.append((x, y, x2, y2, thickness))
    spread = 0.4 + np.random.random() * 0.3
    shrink = 0.68 + np.random.random() * 0.1
    gen_tree(x2, y2, angle - spread, length * shrink, depth + 1, max_depth, branches)
    gen_tree(x2, y2, angle + spread, length * shrink, depth + 1, max_depth, branches)
    if depth < max_depth - 2 and np.random.random() < 0.3:
        gen_tree(x2, y2, angle + (np.random.random() - 0.5) * 0.2,
                 length * shrink * 0.85, depth + 1, max_depth, branches)
    return branches

print("  boom genereren...")
branches = gen_tree(W // 2, H - 60, -np.pi / 2, 180, 0, 10)
print(f"  {len(branches)} takken")

# Vogels op takken
bird_indices = np.random.choice(len(branches), size=min(7, len(branches)), replace=False)
birds = []
for idx in bird_indices:
    bx, by, bx2, by2, _ = branches[idx]
    t = 0.4 + np.random.random() * 0.3
    px = bx + t * (bx2 - bx)
    py = by + t * (by2 - by)
    birds.append({
        "x": px, "y": py,
        "phase": np.random.random() * 2 * np.pi,
        "period": 3 + np.random.random() * 5,
        "dur": 0.5 + np.random.random() * 0.5,
    })
print(f"  {len(birds)} vogels")

# Sterren
np.random.seed(123)
stars = np.column_stack([
    np.random.randint(0, W, 200),
    np.random.randint(0, H // 2, 200),
    np.random.randint(80, 180, 200),
])

# === Snel lijnteken ===
def draw_line(canvas, x1, y1, x2, y2, r, g, b):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    xs = np.linspace(x1, x2, steps).astype(int)
    ys = np.linspace(y1, y2, steps).astype(int)
    for px, py in zip(xs, ys):
        if 0 <= py < H and 0 <= px < W:
            canvas[py, max(0, px - 1):min(W, px + 2), 0] = r
            canvas[py, max(0, px - 1):min(W, px + 2), 1] = g
            canvas[py, max(0, px - 1):min(W, px + 2), 2] = b

# === Render ===
for frame in range(FRAMES):
    # Achtergrond — nachtelijke hemel
    t = frame / FPS
    shift = 0.5 + 0.5 * math.sin(2 * np.pi * frame / (DUR * FPS))
    y_grad = np.linspace(0, 1, H).reshape(H, 1)
    canvas = np.zeros((H, W, 3), dtype=np.float64)
    canvas[:, :, 0] = 5 + 3 * (1 - y_grad) * shift
    canvas[:, :, 1] = 5 + 5 * (1 - y_grad) * shift
    canvas[:, :, 2] = 8 + 12 * (1 - y_grad) * (0.5 + 0.5 * shift)

    # Sterren
    twinkle = 0.7 + 0.3 * math.sin(2 * np.pi * frame / 50)
    for sx, sy, sb in stars:
        canvas[sy, sx, :] = int(sb * twinkle)

    # Boom — wind
    wind = math.sin(2 * np.pi * frame / 200) * 2
    for bx, by, bx2, by2, thick in branches:
        # Wind offset voor hogere takken
        mid_y = (by + by2) / 2
        wo = wind * (H - mid_y) / H
        draw_line(canvas, bx + wo * 0.5, by, bx2 + wo, by2, 25, 20, 15)

    # Vogels + glow
    for bird in birds:
        bx, by = bird["x"], bird["y"]
        cycle = ((t / bird["period"]) + bird["phase"] / (2 * np.pi)) % 1.0
        is_singing = cycle < (bird["dur"] / bird["period"])
        glow_val = cycle / bird["period"] * 0.6 if is_singing else 0

        # Vogel — klein donker silhouet
        for dy in range(-4, 5):
            for dx in range(-6, 7):
                shape = math.exp(-(dx ** 2) / 15 - (dy ** 2) / 6)
                if shape > 0.2:
                    px = int(bx + dx)
                    py = int(by + dy)
                    if 0 <= py < H and 0 <= px < W:
                        b = int(shape * 25)
                        canvas[py, px, 0] = max(canvas[py, px, 0], b + 5)
                        canvas[py, px, 1] = max(canvas[py, px, 1], b + 3)
                        canvas[py, px, 2] = max(canvas[py, px, 2], b + 8)

        # Glow — warm licht rond zingende vogel (lokaal)
        if is_singing and glow_val > 0:
            r = 60
            x0 = max(0, int(bx) - r)
            x1 = min(W, int(bx) + r)
            y0 = max(0, int(by) - r)
            y1 = min(H, int(by) + r)
            y_idx, x_idx = np.ogrid[y0:y1, x0:x1]
            dist = np.sqrt((x_idx - bx) ** 2 + (y_idx - by) ** 2)
            glow = np.exp(-dist ** 2 / (2 * 35 ** 2)) * glow_val
            canvas[y0:y1, x0:x1, 0] = np.clip(canvas[y0:y1, x0:x1, 0].astype(float) + glow * 18, 0, 255)
            canvas[y0:y1, x0:x1, 1] = np.clip(canvas[y0:y1, x0:x1, 1].astype(float) + glow * 12, 0, 255)
            canvas[y0:y1, x0:x1, 2] = np.clip(canvas[y0:y1, x0:x1, 2].astype(float) + glow * 4, 0, 255)

    # PPM
    canvas = np.clip(canvas, 0, 255).astype(np.uint8)
    ppm_path = os.path.join(raw_dir, f"{frame:04d}.ppm")
    with open(ppm_path, "wb") as f:
        f.write(f"P6\n{W} {H}\n255\n".encode())
        f.write(canvas.tobytes())

    if frame % 250 == 0:
        print(f"  frame {frame}/{FRAMES}")

print("  muxing...")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vogels-boom.mp4")
audio = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunya-birds-60s.wav")

cmd = [
    "ffmpeg", "-y", "-framerate", str(FPS),
    "-i", os.path.join(raw_dir, "%04d.ppm"),
    "-i", audio,
    "-c:v", "libx264", "-preset", "medium", "-crf", "22",
    "-pix_fmt", "yuv420p",
    "-c:a", "libmp3lame", "-q:a", "4",
    "-shortest", out,
]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("error:", result.stderr[:500])
else:
    mb = os.path.getsize(out) / 1024 / 1024
    print(f"done: {out} ({DUR}s, {mb:.1f}MB)")

import shutil
shutil.rmtree(raw_dir)
