#!/usr/bin/env python3
"""
Sunya Birds — vogels uit leegte

Geen mantra. Geen taal. Geen structuur.
Alleen frequenties die als vogels klinken.
Zacht. Kort. Stil.

Puur numpy. Geen samples. Geen externe audio.
"""

import numpy as np
import wave
import os

SR = 48000
DUR = 60  # 1 minuut
N = int(SR * DUR)

buf = np.zeros(N, dtype=np.float64)


def chirp(dur_s, base_freq, peak_freq, trill_hz=0, attack=0.01, decay=0.15):
    """Enkele vogeltonetjes — zuiver en kort."""
    n = int(dur_s * SR)
    t = np.arange(n) / SR

    # Frequentie boog: op naar piek, terug
    mid = n // 2
    f_up = np.linspace(base_freq, peak_freq, mid)
    f_down = np.linspace(peak_freq, base_freq, n - mid)
    freq = np.concatenate([f_up, f_down])

    # Trill — vogels vibrato
    if trill_hz > 0:
        vib = np.sin(2 * np.pi * trill_hz * t) * (peak_freq - base_freq) * 0.15
        freq = freq + vib

    # Phase continuous
    phase = np.cumsum(freq) / SR
    tone = np.sin(2 * np.pi * phase)

    # Envelope — snel op, zacht af
    env = np.ones(n)
    att = min(int(attack * SR), n // 2)
    dec = min(int(decay * SR), n // 2)
    if att > 0:
        env[:att] = np.linspace(0, 1, att) ** 0.3
    if dec > 0 and dec < n:
        tail = n - dec
        env[tail:] = np.linspace(1, 0, dec) ** 1.5

    return tone * env


def flutter(dur_s, base_freq, trill_hz=30, depth=100):
    """Zacht trillerend geluid — kleine vogel."""
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    vib = np.sin(2 * np.pi * trill_hz * t) * depth
    freq = base_freq + vib
    phase = np.cumsum(freq) / SR
    tone = np.sin(2 * np.pi * phase)
    env = np.exp(-t * 8) * (1 - np.exp(-t * 300))
    env = np.clip(env, 0, 1)
    return tone * env


def ambient_pad(dur_s, freqs, vol=0.008):
    """Zachter grondgeluid — wind/ruimte."""
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    seg = np.zeros(n)
    for f in freqs:
        # Zeer langzame mod
        slow = np.sin(2 * np.pi * 0.05 * t) * 2
        seg += np.sin(2 * np.pi * (f + slow) * t)
    # Fade in/out
    fade = int(3 * SR)
    env = np.ones(n)
    env[:fade] = np.linspace(0, 1, fade) ** 0.5
    env[n - fade:] = np.linspace(1, 0, fade) ** 0.5
    return seg * env * vol


# === Compositie ===

# Grond — bijna hoorbaar
pad = ambient_pad(DUR, freqs=[396, 432, 528], vol=0.006)
buf[:len(pad)] += pad

# Vogel-achtigheden — verspreid door de tijd
np.random.seed(7)  # herhaalbaar

# "Vogelsoorten" — frequentiegebieden
birds = {
    "klein":  {"base": 2800, "peak": 4200, "dur": (0.04, 0.08), "trill": (20, 50)},
    "middel": {"base": 1800, "peak": 2800, "dur": (0.08, 0.15), "trill": (10, 30)},
    "groot":  {"base": 1200, "peak": 1800, "dur": (0.12, 0.25), "trill": (5, 20)},
}

vol_map = {"klein": 0.018, "middel": 0.015, "groot": 0.012}

for second in np.arange(0.5, DUR, 0.3):
    # Niet elke stap — ruimtelijk
    if np.random.random() > 0.4:
        continue

    soort = np.random.choice(list(birds.keys()), p=[0.4, 0.4, 0.2])
    b = birds[soort]
    d = np.random.uniform(*b["dur"])
    tr = np.random.randint(*b["trill"]) if b["trill"][1] > b["trill"][0] else 0
    bf = b["base"] + np.random.randint(-200, 400)
    pf = b["peak"] + np.random.randint(-300, 500)

    seg = chirp(d, bf, pf, trill_hz=tr)
    offset = int(second * SR)
    end = offset + len(seg)
    if end < N:
        buf[offset:end] += seg * vol_map[soort]

    # Soms een tweede tonetje — vogels zelden alleen
    if np.random.random() > 0.6 and soort == "klein":
        pause = np.random.uniform(0.05, 0.15)
        seg2 = flutter(0.06, bf + 200, trill_hz=tr + 10, depth=80)
        off2 = offset + int(pause * SR)
        end2 = off2 + len(seg2)
        if end2 < N:
            buf[off2:end2] += seg2 * 0.012

# Normaliseer — zacht
peak = np.abs(buf).max()
if peak > 0:
    buf *= 0.55 / peak

# Schrijven
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunya-birds-60s.wav")
samples = (buf * 32767).astype(np.int16)
with wave.open(out, "w") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(samples.tobytes())

mb = os.path.getsize(out) / 1024 / 1024
print(f"done: {out} ({DUR}s, mono, {mb:.1f}MB)")
print("sunya → vogels → stilte")
