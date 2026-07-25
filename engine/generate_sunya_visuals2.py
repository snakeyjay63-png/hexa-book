#!/usr/bin/env python3
"""
Sunya Visuals — een ademend punt

Zwarte ruimte. In het midden: één stip die ademt.
Heel zacht. Niet meer dan 5% helderheid.
"""

import numpy as np
import subprocess
import os

W, H = 1920, 1080
FPS = 25
DUR = 60
FRAMES = int(FPS * DUR)

raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunya_v2")
os.makedirs(raw_dir, exist_ok=True)

# Ademcyclus: 6 seconden per cyclus (150 frames)
BREATH_PERIOD = 150
# Subtiele kleurverschuiving
COLOR_CYCLE = 300

for frame in range(FRAMES):
    pixels = np.zeros((H, W, 3), dtype=np.float64)

    # Ademend punt — radius varieert met sin
    breath = 0.5 + 0.5 * np.sin(2 * np.pi * frame / BREATH_PERIOD)
    # Radius: 30 → 50 pixels
    r = 30 + 20 * breath

    # Center
    cx, cy = W // 2, H // 2

    # Zacht gloeiend punt
    y_idx, x_idx = np.ogrid[:H, :W]
    dist = np.sqrt((x_idx - cx) ** 2 + (y_idx - cy) ** 2)

    # Gaussian glow
    glow = np.exp(-dist ** 2 / (2 * (r ** 2)))

    # Kleur: heel zacht, wisselt tussen wit en lichtblauw
    color_shift = 0.5 + 0.5 * np.sin(2 * np.pi * frame / COLOR_CYCLE)
    r_ch = glow * (8 + 4 * color_shift)
    g_ch = glow * (8 + 2 * color_shift)
    b_ch = glow * (10 + 3 * (1 - color_shift))

    pixels[:, :, 0] = r_ch
    pixels[:, :, 1] = g_ch
    pixels[:, :, 2] = b_ch

    # Af en toe: heel zachte stip ergens anders — zoals een vogel die ver weg vliegt
    if frame % 73 == 0:
        sx = int(W * (0.3 + 0.4 * (frame / FRAMES)))
        sy = int(H * (0.2 + 0.6 * np.sin(frame / 20)))
        sr = 2
        glow2 = np.exp(-((dist - np.sqrt((sx - cx) ** 2 + (sy - cy) ** 2)) ** 2) / (2 * (sr ** 2)))
        pixels = np.clip(pixels + glow2[:, :, np.newaxis] * 3, 0, 255)

    # Schrijf PPM
    pixels = pixels.astype(np.uint8)
    ppm_path = os.path.join(raw_dir, f"{frame:04d}.ppm")
    with open(ppm_path, "wb") as f:
        f.write(f"P6\n{W} {H}\n255\n".encode())
        f.write(pixels.tobytes())

    if frame % 250 == 0:
        print(f"  frame {frame}/{FRAMES}")

print("  muxing...")

# Mux met audio
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunya-birds.mp4")
audio = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunya-birds-60s.wav")

cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(raw_dir, "%04d.ppm"),
    "-i", audio,
    "-c:v", "libx264", "-preset", "slow", "-crf", "23",
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
