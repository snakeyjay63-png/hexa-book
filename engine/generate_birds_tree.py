#!/usr/bin/env python3
"""
Vogels in een boom — generatieve scène

Numpy canvas. Generatieve boom (L-system).
Vogels op takken. Af en toe: zingend pulsje.
"""

import numpy as np
import subprocess
import os
import math

W, H = 1920, 1080
FPS = 25
DUR = 60
FRAMES = int(FPS * DUR)

raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bird_tree_frames")
os.makedirs(raw_dir, exist_ok=True)

np.random.seed(47)

# === Boom genereren ===
def gen_tree(x, y, angle, length, depth, max_depth, branches=None):
    """Recursieve boom — takken die naar boven groeien."""
    if branches is None:
        branches = []
    if depth > max_depth or length < 5:
        return branches

    # Tak eindpunt
    x2 = x + length * np.cos(angle)
    y2 = y + length * np.sin(angle)

    # Slaak tak op
    thickness = max(1, (max_depth - depth + 1) * 1.5)
    branches.append((x, y, x2, y2, thickness))

    # Split
    spread = 0.4 + np.random.random() * 0.3
    shrink = 0.68 + np.random.random() * 0.1

    # Links
    gen_tree(x2, y2, angle - spread, length * shrink, depth + 1, max_depth, branches)
    # Rechts
    gen_tree(x2, y2, angle + spread, length * shrink, depth + 1, max_depth, branches)

    # Soms midden-tak
    if depth < max_depth - 2 and np.random.random() < 0.3:
        gen_tree(x2, y2, angle + (np.random.random() - 0.5) * 0.2,
                 length * shrink * 0.85, depth + 1, max_depth, branches)

    return branches


print("  boom genereren...")
branches = gen_tree(W // 2, H - 60, -np.pi / 2, 180, 0, 10)
print(f"  {len(branches)} takken")

# === Vogels plaatsen op willekeurige takken ===
def dist_pt_to_seg(px, py, x1, y1, x2, y2):
    """Afstand van punt tot lijnstuk."""
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


# Kies 6-8 takken voor vogels (voorkeurig hogere takken)
bird_branches = np.random.choice(len(branches), size=min(7, len(branches)), replace=False)
birds = []
for idx in bird_branches:
    bx, by, bx2, by2, _ = branches[idx]
    # Punt op tak — 60% vanaf begin
    t = 0.4 + np.random.random() * 0.3
    px = bx + t * (bx2 - bx)
    py = by + t * (by2 - by)
    # Zingmomenten — elk vogel heeft eigen timing
    sing_phase = np.random.random() * 2 * np.pi
    sing_period = 3 + np.random.random() * 5  # seconden
    sing_dur = 0.5 + np.random.random() * 0.5
    birds.append({"x": px, "y": py, "phase": sing_phase, "period": sing_period, "dur": sing_dur})

print(f"  {len(birds)} vogels geplaatst")

# === Achtergrond gradient ===
def bg_gradient(frame):
    """Nachtelijke hemel — donkerblauw/zwart gradient."""
    grad = np.zeros((H, W, 3), dtype=np.float64)
    for y in range(H):
        t = y / H
        # Subtiele kleurshift over tijd
        shift = 0.5 + 0.5 * math.sin(2 * np.pi * frame / (DUR * FPS))
        grad[y, :, 0] = 5 + 3 * (1 - t) * shift       # R: bijna zwart, licht boven
        grad[y, :, 1] = 5 + 5 * (1 - t) * shift        # G: heel licht groen/blauw boven
        grad[y, :, 2] = 8 + 12 * (1 - t) * (0.5 + 0.5 * shift)  # B: meer blauw
    return grad


# === Sterren ===
np.random.seed(123)
stars_x = np.random.randint(0, W, 200)
stars_y = np.random.randint(0, H // 2, 200)
stars_bright = np.random.randint(80, 180, 200)


def draw_tree(canvas, branches, frame):
    """Teken boom op canvas."""
    # Zachte wind — heel subtiele schuiving
    wind = 0.5 + 0.5 * math.sin(2 * np.pi * frame / 200)

    for bx, by, bx2, by2, thickness in branches:
        # Wind effect — hogere takken bewegen meer
        mid_y = (by + by2) / 2
        wind_offset = wind * (H - mid_y) / H * 2

        # Boomkleur — donkerbruin
        r, g, b = 25, 20, 15

        # Teken lijn
        steps = max(1, int(math.hypot(bx2 - bx, by2 - by)))
        for s in range(steps):
            t = s / max(1, steps - 1)
            px = int(bx + t * (bx2 - bx) + wind_offset * t)
            py = int(by + t * (by2 - by))
            if 0 <= py < H and 0 <= px < W:
                # Breedte
                for dx in range(-int(thickness), int(thickness) + 1):
                    for dy in range(-int(thickness), int(thickness) + 1):
                        nx, ny = px + dx, py + dy
                        if 0 <= ny < H and 0 <= nx < W:
                            if dx * dx + dy * dy <= thickness * thickness:
                                canvas[ny, nx, 0] = max(canvas[ny, nx, 0], r)
                                canvas[ny, nx, 1] = max(canvas[ny, nx, 1], g)
                                canvas[ny, nx, 2] = max(canvas[ny, nx, 2], b)


def draw_bird(canvas, bx, by, singing, glow_strength):
    """Teken vogeltje op canvas."""
    # Klein silhouet — paar pixels
    bird_w, bird_h = 12, 8
    for dy in range(-bird_h, bird_h):
        for dx in range(-bird_w, bird_w):
            # Vogelvorm — lichaam + kop
            body = math.exp(-(dx ** 2) / 20 - (dy ** 2) / 8)
            head = math.exp(-((dx + 5) ** 2) / 5 - ((dy + 3) ** 2) / 5)
            wing = math.exp(-(dx ** 2) / 30 - ((dy - 2) ** 2) / 3)
            shape = max(body * 0.6, head * 0.8, wing * 0.3)

            if shape > 0.1:
                px = int(bx + dx)
                py_idx = int(by + dy)
                if 0 <= py_idx < H and 0 <= px < W:
                    # Donkere vogelkleur
                    bright = int(shape * 30)
                    canvas[py_idx, px, 0] = max(canvas[py_idx, px, 0], bright + 5)
                    canvas[py_idx, px, 1] = max(canvas[py_idx, px, 1], bright + 3)
                    canvas[py_idx, px, 2] = max(canvas[py_idx, px, 2], bright + 8)

    # Sing-glow — zachte cirkel om vogel als die zingt
    if singing and glow_strength > 0:
        y_idx, x_idx = np.ogrid[:H, :W]
        dist = np.sqrt((x_idx - bx) ** 2 + (y_idx - by) ** 2)
        glow = np.exp(-dist ** 2 / (2 * 40 ** 2)) * glow_strength
        # Warm geel/oranje glow
        canvas[:, :, 0] = np.clip(canvas[:, :, 0] + glow * 15, 0, 255).astype(np.float64)
        canvas[:, :, 1] = np.clip(canvas[:, :, 1] + glow * 10, 0, 255).astype(np.float64)
        canvas[:, :, 2] = np.clip(canvas[:, :, 2] + glow * 5, 0, 255).astype(np.float64)


# === Render alle frames ===
for frame in range(FRAMES):
    canvas = bg_gradient(frame).astype(np.float64)

    # Sterren — knipperen
    twinkle = 0.5 + 0.5 * np.sin(2 * np.pi * frame / 50)
    for sx, sy, sb in zip(stars_x, stars_y, stars_bright):
        b = int(sb * (0.7 + 0.3 * twinkle))
        if 0 <= sy < H and 0 <= sx < W:
            canvas[sy, sx, :] = b

    # Boom
    draw_tree(canvas, branches, frame)

    # Vogels
    t = frame / FPS  # tijd in seconden
    for bird in birds:
        # Bepaal of vogel nu zingt
        cycle_pos = ((t / bird["period"]) + bird["phase"] / (2 * np.pi)) % 1.0
        is_singing = cycle_pos < (bird["dur"] / bird["period"])
        glow = cycle_pos / (bird["period"]) * 0.5 if is_singing else 0
        draw_bird(canvas, bird["x"], bird["y"], is_singing, glow)

    # Schrijf PPM
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
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(raw_dir, "%04d.ppm"),
    "-i", audio,
    "-c:v", "libx264", "-preset", "medium", "-crf", "22",
    "-pix_fmt", "yuv420p",
    "-c:a", "libmp3lame", "-q:a", "4",
    "-shortest",
    out,
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("ffmpeg error:", result.stderr[:500])
else:
    mb = os.path.getsize(out) / 1024 / 1024
    print(f"done: {out} ({DUR}s, {mb:.1f}MB)")

# Cleanup
import shutil
shutil.rmtree(raw_dir)
