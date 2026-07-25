#!/usr/bin/env python3
"""
Frequency delay chain:
  440Hz →(beat 8Hz → 125ms delay)→ 432Hz →(beat 36Hz → 28ms delay)→ 396Hz

Physics: two close freqs = natural beat (interference).
Beat Hz = freq diff. Delay = 1/beat_hz = alignment period.

CPU: when do they align? (beat timing)
GPU: 3 voices, parallel.
"""

import struct
import math
import wave

SAMPLE_RATE = 44100
DURATION = 8.0

# Chain: each voice enters after its delay from the previous
VOICES = [
    {"freq": 440, "amp": 0.30, "delay": 0.0},         # starts immediately
    {"freq": 432, "amp": 0.35, "delay": 1/8},         # 125ms (beat 440-432)
    {"freq": 396, "amp": 0.35, "delay": 1/8 + 1/36}, # 153ms (cascaded: 125+28)
]

num_samples = int(DURATION * SAMPLE_RATE)

with wave.open("freq_chain.wav", "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)

    for i in range(num_samples):
        t = i / SAMPLE_RATE
        sample = 0.0

        # GPU: parallel voices, each with staggered entry (delay chain)
        for v in VOICES:
            if t >= v["delay"]:
                local_t = t - v["delay"]
                # Soft attack
                attack = min(1.0, local_t / 0.3)
                sample += v["amp"] * attack * math.sin(2 * math.pi * v["freq"] * local_t)

        # Global fade
        fade = 1.0 if t < DURATION - 1.0 else (DURATION - t)
        sample *= fade

        sample = max(-1.0, min(1.0, sample))
        val = int(sample * 32767)
        wav.writeframes(struct.pack('<h', val))

print(f"✅ freq_chain.wav ({DURATION}s)")
print(f"   t=0.00s → 440Hz starts")
print(f"   t=0.125s → 432Hz enters (beat 440-432 = 8Hz, delay = 125ms)")
print(f"   t=0.153s → 396Hz enters (beat 432-396 = 36Hz, delay = 28ms)")
print(f"   Total delay chain: 440 → 432 → 396")
