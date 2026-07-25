#!/usr/bin/env python3
"""
Dark Forest Psytrance Generator
Pure synthesis — numpy only. No samples.
Buffer-based: all instruments write to a shared buffer.
Output: WAV file (48kHz mono)
"""

import numpy as np
import wave
import os

# --- Config ---
SR = 48000
DURATION = 180  # 3 minutes
BPM = 138
BEAT = 60.0 / BPM
BAR = BEAT * 4
N = int(SR * DURATION)

buf = np.zeros(N, dtype=np.float64)

def add(buf, seg, t0, gain=1.0):
    """Add segment to buffer at position t0."""
    end = min(t0 + len(seg), N)
    src_end = end - t0
    buf[t0:end] += seg[:src_end] * gain

def mk_kick(t0):
    """Kick drum at sample position t0."""
    dur = int(0.15 * SR)
    t = np.arange(dur) / SR
    freq = 150 * np.exp(-20 * t) + 50
    phase = np.cumsum(freq) / SR
    out = np.sin(2 * np.pi * phase) * np.exp(-t * 30)
    sub = np.sin(2 * np.pi * 40 * t) * np.exp(-t * 20)
    return out * 0.7 + sub * 0.3

def mk_snare(t0):
    t = np.arange(int(0.12 * SR)) / SR
    noise = np.random.randn(len(t)) * np.exp(-t * 40)
    tone = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 50)
    return noise * 0.6 + tone * 0.4

def mk_hat(t0, open_=False):
    dur = int((0.08 if open_ else 0.04) * SR)
    t = np.arange(dur) / SR
    noise = np.diff(np.concatenate([[0], np.random.randn(dur)]))
    return noise * np.exp(-t * (25 if open_ else 80)) * 0.3

def mk_bass(freq, t0, dur_s):
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    phase = (t * freq) % 1.0
    saw = 2 * phase - 1
    sub = np.sin(2 * np.pi * freq * t)
    out = saw * 0.4 + sub * 0.6
    env = np.ones(n)
    att = min(int(0.01 * SR), n)
    rel = min(int(0.1 * SR), n)
    if att > 0: env[:att] = np.linspace(0, 1, att)
    if rel > 0 and n > rel: env[n-rel:] = np.linspace(1, 0, rel)
    return out * env

def mk_arpeggio(freq, t0, dur_s):
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    phase = (t * freq) % 1.0
    tri = 4 * np.abs(phase - 0.5) - 1
    harm = 4 * np.abs((t * freq * 3) % 1.0 - 0.5) - 1
    return (tri * 0.6 + harm * 0.15) * np.exp(-t * 25) * 0.2

def mk_pad(freqs, t0, dur_s):
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        vib = np.sin(2 * np.pi * 0.5 * t) * 2
        out += np.sin(2 * np.pi * (f + vib) * t)
    out /= len(freqs)
    att = min(int(2 * SR), n)
    rel = min(int(3 * SR), n)
    env = np.ones(n)
    if att > 0: env[:att] = np.linspace(0, 1, att) ** 0.5
    if rel > 0 and n > rel: env[n-rel:] = np.linspace(1, 0, rel) ** 0.5
    return out * env * 0.15

def mk_drone(freq, t0, dur_s):
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    mod = np.sin(2 * np.pi * 0.1 * t) * 0.5
    out = np.sin(2 * np.pi * (freq + mod) * t)
    out += 0.3 * np.sin(2 * np.pi * freq * 0.5 * t)
    return out * 0.5 * 0.12

# === Build ===
print(f"Generating {DURATION}s psytrance at {BPM} BPM, {SR}Hz...")

# --- Continuous drones ---
add(buf, mk_drone(396, 0, DURATION), 0)
add(buf, mk_drone(432, 0, DURATION), 0)

# --- Pads ---
add(buf, mk_pad([130.81, 196.0, 261.63], 0, DURATION), 0, 0.8)
add(buf, mk_pad([98.0, 146.83, 196.0], 0, DURATION - 32), 0, 0.6)

# --- Drum section: bars 16-112 ---
for bar in range(16, 112):
    bar_s = bar * BAR
    # Kick on every beat
    for beat in range(4):
        t = int((bar_s + beat * BEAT) * SR)
        if t + 100 < N:
            vol = 0.8 if bar < 80 else 0.6
            add(buf, mk_kick(t), t, vol)
    # Snare on 2 & 4
    for beat in [1, 3]:
        t = int((bar_s + beat * BEAT) * SR)
        if t + 100 < N:
            add(buf, mk_snare(t), t, 0.4 if bar < 80 else 0.3)
    # Hi-hats (8th notes)
    for eighth in range(8):
        t = int((bar_s + eighth * BEAT / 2) * SR)
        if t + 50 < N:
            add(buf, mk_hat(t, eighth % 2 == 1), t, 0.25)
    # Extra 16ths in drop
    if bar < 80:
        for sixt in range(16):
            if sixt % 2 == 1:
                t = int((bar_s + sixt * BEAT / 4) * SR)
                if t + 50 < N:
                    add(buf, mk_hat(t), t, 0.12)

# --- Rolling bass: bars 16-80 ---
bass_r, bass_5 = 65.41, 98.0
for bar in range(16, 80):
    bar_s = bar * BAR
    for offset, freq in [(0, bass_r), (BEAT, bass_r), (2.5*BEAT, bass_5), (3*BEAT, bass_r)]:
        t = int((bar_s + offset) * SR)
        if t + 500 < N:
            add(buf, mk_bass(freq, t, BEAT * 0.9), t, 0.5)

# --- Arpeggio: bars 16-80 ---
arp = [261.63, 329.63, 392.0, 523.25]
for bar in range(16, 80):
    bar_s = bar * BAR
    for i in range(16):
        t = int((bar_s + i * BEAT / 4) * SR)
        if t + 300 < N:
            add(buf, mk_arpeggio(arp[(bar*4+i)%4], t, BEAT/8), t, 0.6)

# --- Arpeggio 2: bars 80-112 ---
arp2 = [329.63, 392.0, 493.88, 587.33]
for bar in range(80, 112):
    bar_s = bar * BAR
    for i in range(16):
        t = int((bar_s + i * BEAT / 4) * SR)
        if t + 300 < N:
            add(buf, mk_arpeggio(arp2[(bar*4+i)%4], t, BEAT/8), t, 0.5)

# --- Normalize & limit ---
peak = np.abs(buf).max()
if peak > 0:
    buf *= 0.85 / peak
buf = np.tanh(buf)

# --- Write WAV ---
samples = (buf * 32767).astype(np.int16)
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "psytrance-3min.wav")

with wave.open(out_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(samples.tobytes())

print(f"Done: {out_path} ({DURATION}s, {BPM} BPM, {SR}Hz)")
