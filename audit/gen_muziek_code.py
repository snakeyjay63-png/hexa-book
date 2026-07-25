#!/usr/bin/env python3
"""
Muziek = Code + Frequentie

CPU:  Ritme controleren (sequentieel, timing)
GPU:  Frequentie veld (parallel, amplitude)

CPU bepaalt WANNEER, GPU berekent WAT.
"""

import struct
import math
import wave

# === CPU: Ritme controleren ===
# Ritme: noten-duur in beats (1 = hele maat, 0.5 = kwart, etc.)
RITME = [1.0, 0.5, 0.5, 1.0, 1.0, 0.25, 0.25, 0.5, 0.5, 2.0]
TEMPO = 100.0  # BPM

# === GPU: Frequentie veld ===
# Frequenties die tegelijk klinken (polyfonie)
# 3 banden, elk >440Hz
# Band 1: bas (440-660)  | Band 2: mid (660-880)  | Band 3: hoge (880-1320+)
FREQUENTIES = [
    523.25,   # C5 - bas band
    659.25,   # E5 - mid band  
    783.99,   # G5 - hoge band
    1046.50,  # C6 - overtoon 1
    1174.66,  # D6 - overtoon 2
    1318.51,  # E6 - overtoon 3
    1567.98,  # G6 - overtoon 4
    2093.00,  # C7 - shimmer
]
AMPLITUDES  = [0.35, 0.30, 0.25, 0.15, 0.12, 0.10, 0.08, 0.05]

# Sample rate
SAMPLE_RATE = 44100
BIT_RATE = 16

def cpu_ritme_tijden(ritme, tempo):
    """CPU: bepaalt wanneer elke noot begint en eindigt."""
    beat_dur = 60.0 / tempo
    tijden = []
    t = 0.0
    for duur in ritme:
        tijden.append((t, t + duur * beat_dur))
        t += duur * beat_dur
    return tijden

CUDA_CORES = 8

def gpu_core(core_id, t, start, count, frequenties, amplitudes):
    """Één CUDA core: berekent zijn subset van frequenties."""
    totaal = 0.0
    for i in range(start, start + count):
        totaal += amplitudes[i] * math.sin(2 * math.pi * frequenties[i] * t)
    return totaal

def gpu_frequentie_veld(t, frequenties, amplitudes):
    """GPU: 8 cores berekenen parallel, daarna reduce (sum)."""
    n = len(frequenties)
    per_core = n // CUDA_CORES
    remainder = n % CUDA_CORES

    # Launch cores
    resultaten = []
    idx = 0
    for core_id in range(CUDA_CORES):
        count = per_core + (1 if core_id < remainder else 0)
        res = gpu_core(core_id, t, idx, count, frequenties, amplitudes)
        resultaten.append(res)
        idx += count

    # Reduce: som alle cores
    return sum(resultaten)

def envelope(t, start, end, attack=0.01, release=0.05):
    """Simple attack-release envelope."""
    duration = end - start
    elapsed = t - start
    if elapsed < attack:
        return elapsed / attack
    elif elapsed > duration - release:
        return (duration - elapsed) / release
    return 1.0

# Generate
tijden = cpu_ritme_tijden(RITME, TEMPO)
total_time = tijden[-1][1]
num_samples = int(total_time * SAMPLE_RATE)

with wave.open("muziek_code.wav", "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)

    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # Vind welke noot nu klinkt
        noot_factor = 0.0
        for start, end in tijden:
            if start <= t < end:
                noot_factor = envelope(t, start, end)
                break

        if noot_factor > 0:
            # GPU: veld berekenen
            sample = gpu_frequentie_veld(t, FREQUENTIES, AMPLITUDES) * noot_factor
        else:
            sample = 0.0

        # Clip en convert
        sample = max(-1.0, min(1.0, sample))
        val = int(sample * 32767)
        wav.writeframes(struct.pack('<h', val))

print(f"✅ muziek_code.wav gegenereerd ({total_time:.1f}s, {num_samples} samples)")
print(f"   Ritme: {len(RITME)} noten @ {TEMPO} BPM")
print(f"   GPU: {len(FREQUENTIES)} frequenties >440Hz, {CUDA_CORES} CUDA cores")
