#!/usr/bin/env python3
"""
Sunya Visuals — bijna-niets

Zwarte canvas. Soms een stip. Soms een lijn.
Stil. Licht. Geen zware geometrie.
"""

import numpy as np
import struct
import subprocess
import os

W, H = 1920, 1080
FPS = 25
DUR = 60
FRAMES = FPS * DUR  # 1500

# Generate raw frames as PPM, then mux with ffmpeg
raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunya_frames")
os.makedirs(raw_dir, exist_ok=True)

def ppm(path, pixels):
    """Write raw frame as PPM."""
    with open(path, "wb") as f:
        f.write(b"P6\n%d %d\n255\n" % (W, H))
        f.write(pixels)

# Pre-seed randomness for sparseness
np.random.seed(42)
# Random moments where something almost appears
events = np.random.random(FRAMES)

for frame in range(FRAMES):
    # Almost always: pure black
    pixels = np.zeros((H, W, 3), dtype=np.uint8)

    # Very subtle — only 2% of frames have anything visible
    if events[frame] < 0.02:
        cx, cy = np.random.randint(200, W - 200), np.random.randint(200, H - 200)
        r = np.random.randint(1, 4)  # tiny dot
        y_idx, x_idx = np.ogrid[:H, :W]
        dist = np.sqrt((x_idx - cx)**2 + (y_idx - cy)**2)
        brightness = np.maximum(0, 8 - dist * 2)  # barely visible glow
        pixels = np.clip(pixels + brightness[:, :, np.newaxis].astype(np.uint8), 0, 255)

    # Occasional faint line (0.3% of frames)
    if events[frame] < 0.003:
        y_line = np.random.randint(H // 4, 3 * H // 4)
        x1, x2 = sorted([np.random.randint(100, W - 100) for _ in range(2)])
        pixels[y_line, x1:x2, :] = np.array([3, 3, 4], dtype=np.uint8)

    ppm(os.path.join(raw_dir, f"{frame:04d}.ppm"), pixels.tobytes())
    if frame % 250 == 0:
        print(f"  frame {frame}/{FRAMES}")

print("  muxing...")

# Mux frames + audio
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunya-birds-60s-visual.mp4")
audio = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunya-birds-60s.wav")

cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(raw_dir, "%04d.ppm"),
    "-i", audio,
    "-c:v", "libx264", "-preset", "slow", "-crf", "28",
    "-pix_fmt", "yuv420p",
    "-c:a", "libmp3lame", "-q:a", "4",
    "-shortest",
    out,
]

subprocess.run(cmd, check=True)

# Cleanup frames
import shutil
shutil.rmtree(raw_dir)

mb = os.path.getsize(out) / 1024 / 1024
print(f"done: {out} ({DUR}s, {mb:.1f}MB)")
