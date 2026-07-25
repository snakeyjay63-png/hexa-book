#!/usr/bin/env python3
"""
Hz = 1 veld. Delay = geometrie van dat veld.
Hz zegt niets zonder hoek.

440, 432, 396 = verschillende banden = verschillende hoeken in 1 veld.
Delay = hoekverschil tussen banden.

CPU: hoek bepalen (delay geometry)
GPU: veld berekenen per band
"""

import struct
import math
import wave

SAMPLE_RATE = 44100
DURATION = 8.0

# === 1 veld, 3 banden = 3 hoeken ===
# Hz is het veld (amplitude carrier)
# Delay/hoek is de geometrie (fase-relatie)

BANDEN = [
    {"hz": 440, "hoek": 0.0,           "amp": 0.30},  # referentie
    {"hz": 432, "hoek": 2*math.pi/8,   "amp": 0.35},  # 45° = 1/8 rotatie
    {"hz": 396, "hoek": 2*math.pi/36,  "amp": 0.35},  # 10° = 1/36 rotatie
]

# GPU: één veld, één core per band
def gpu_veld_per_band(t, hz, hoek, amp):
    """
    Hz = veldsterkte
    Hoek = fase-shift (geometrie van delay)
    = amp * sin(2π·hz·t + hoek)
    """
    return amp * math.sin(2 * math.pi * hz * t + hoek)

# CPU: hoek-geometrie controleren
def cpu_hoek_check(hoeken):
    """Controleer hoek-relaties tussen banden."""
    for i, h in enumerate(hoeken):
        graden = math.degrees(h)
        print(f"   Band {i}: hoek = {graden:.1f}° (delay geometry)")

print("CPU: hoek-geometrie controleren")
cpu_hoek_check([b["hoek"] for b in BANDEN])
print(f"GPU: {len(BANDEN)} banden, 1 veld")

num_samples = int(DURATION * SAMPLE_RATE)

with wave.open("band_angle.wav", "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)

    for i in range(num_samples):
        t = i / SAMPLE_RATE
        sample = 0.0

        # GPU: parallel — elk band = eigen hoek in 1 veld
        for b in BANDEN:
            sample += gpu_veld_per_band(t, b["hz"], b["hoek"], b["amp"])

        # CPU: ritme = fade in/out (controleer snelheid)
        fade_in = min(1.0, t / 0.5)
        fade_out = 1.0 if t < DURATION - 1.0 else (DURATION - t)
        sample *= fade_in * fade_out

        sample = max(-1.0, min(1.0, sample))
        val = int(sample * 32767)
        wav.writeframes(struct.pack('<h', val))

print(f"✅ band_angle.wav ({DURATION}s)")
