#!/usr/bin/env python3
"""
8-Layer Mono Audio Generator — Hexa-Boek
Base64 → geometrie → geluid → geometrie

Mono field: 8 language/frequency layers through one speaker.
BPM-synced structure. No stereo tricks — pure phase interaction.

Layers:
  1. Sanskrit    — phoneme → sanskrit_freq
  2. Arabisch    — Abjad → DR → freq
  3. Grieks      — phoneme → triangle wave
  4. Vogels      — frequency sweeps + trill
  5. Latijn      — Pythagoras ratio → freq
  6. Hebreeuws   — Gematria → DR → freq
  7. Oud-Chinees — Bagua/I Ching → pentatonic
  8. Egyptisch   — Hiërogliefen → DR → freq
"""

import sys
import os
import numpy as np
import wave
import math

# --- Import sanskrit bridge ---
SKILL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "..", "skills", "sanskrit-frequency-bridge", "scripts")
sys.path.insert(0, SKILL_DIR)
try:
    import sanskrit_freq
    HAS_SANSKRIT = True
except ImportError:
    HAS_SANSKRIT = False
    print("WARN: sanskrit_freq not available, skipping Sanskrit layer")

# --- Config ---
SR = 48000
DURATION = 180  # 3 minutes
BPM = 138
BEAT = 60.0 / BPM
BAR = BEAT * 4
N = int(SR * DURATION)

buf = np.zeros(N, dtype=np.float64)

def add(buf, seg, t0, gain=1.0):
    end = min(t0 + len(seg), N)
    src_end = end - t0
    if src_end > 0:
        buf[t0:end] += seg[:src_end] * gain

def envelope(n, attack_s=0.05, release_s=0.3):
    """Smooth attack-release envelope."""
    env = np.ones(n)
    att = min(int(attack_s * SR), n // 2)
    rel = min(int(release_s * SR), n // 2)
    if att > 0:
        env[:att] = np.linspace(0, 1, att) ** 0.5
    if rel > 0 and n > rel:
        env[n-rel:] = np.linspace(1, 0, rel) ** 0.5
    return env

def digital_root(n):
    n = abs(int(n))
    if n == 0:
        return 1
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

# ============================================================
# FREQUENCY MAPPINGS
# ============================================================

# Equal-tempered scale from DR
DR_FREQ = {
    1: 261.63,  # C4
    2: 293.66,  # D4
    3: 329.63,  # E4
    4: 349.23,  # F4
    5: 392.00,  # G4
    6: 440.00,  # A4
    7: 493.88,  # B4
    8: 523.25,  # C5
    9: 587.33,  # D5
}

# Pentatonic (Chinese) — C D F G A
PENTATONIC = [261.63, 293.66, 349.23, 392.00, 440.00]

# Pythagorean ratios (Latin)
PYTH_RATIOS = {
    'unison':      1/1,
    'octave':      2/1,
    'fifth':       3/2,
    'fourth':      4/3,
    'major_third': 81/64,
    'minor_third': 32/27,
    'major_sixth': 27/16,
    'minor_sixth': 128/81,
}

# ============================================================
# LAYER 1: Sanskrit mantras → melody
# ============================================================

SANSKRIT_PHRASES = [
    "\u0950",                        # Om
    "\u0936\u093e\u0928\u094d\u0924\u093f",       # Shanti
    "\u0924\u0924\u094d\u0938\u0924\u094d",     # Tattva
    "\u0938\u0942\u0924\u094d\u0930",      # Sutra
]

def synth_sanskrit(phrase, start_s, dur_s, base_hz=110):
    if not HAS_SANSKRIT:
        return np.zeros(0)
    params = sanskrit_freq.map_phonemes(phrase)
    seg = sanskrit_freq.synthesize(
        params, duration_per_char=dur_s / max(1, len(phrase)),
        base_hz=base_hz, waveform='sine', fs=SR
    )
    n = len(seg)
    seg *= envelope(n, attack_s=0.1, release_s=0.5)
    return seg

# ============================================================
# LAYER 2: Arabic Abjad → frequency field
# ============================================================

ABJAD = {
    '\u0628': 2, '\u062c': 3, '\u062d': 8, '\u062e': 60, '\u062f': 4,
    '\u0630': 700, '\u0631': 200, '\u0633': 60, '\u0634': 300, '\u0637': 500,
    '\u0636': 90, '\u0639': 70, '\u0641': 80, '\u0642': 100, '\u0643': 20,
    '\u0644': 30, '\u0645': 40, '\u0646': 50, '\u0647': 5, '\u0648': 6,
    '\u0623': 1, '\u0625': 1, '\u0627': 1, '\u0622': 1,
    '\u062b': 30, '\u0632': 7, '\u064a': 10, '\u0626': 1, '\u0624': 1,
}

ARABIC_PHRASES = [
    "\u0644\u0627 \u0625\u0644\u0627\u0647 \u0625\u0644\u0627 \u0644\u0644",
    "\u062d\u0643\u0645\u0629",
    "\u0639\u0644\u0645",
    "\u062d\u0642\u064a\u0642\u0629",
]

def synth_arabic(text, start_s, dur_s):
    n_total = int(dur_s * SR)
    seg = np.zeros(n_total, dtype=np.float64)
    valid_chars = [c for c in text if c in ABJAD]
    if not valid_chars:
        return seg
    char_dur = dur_s / len(valid_chars)
    n_char = int(char_dur * SR)
    for i, char in enumerate(valid_chars):
        freq = DR_FREQ.get(digital_root(ABJAD[char]), 396.0)
        t = np.arange(n_char) / SR
        vib = np.sin(2 * np.pi * 0.3 * t) * 3
        tone = np.sin(2 * np.pi * (freq + vib) * t)
        tone *= envelope(n_char, attack_s=0.05, release_s=0.15)
        offset = i * n_char
        end = min(offset + n_char, n_total)
        seg[offset:end] = tone[:end - offset] * 0.06
    return seg

# ============================================================
# LAYER 3: Greek phonemes → triangle wave
# ============================================================

GREEK_MAP = {
    '\u03B1': 261.63, '\u03B5': 293.66, '\u03B7': 311.13,
    '\u03B9': 329.63, '\u03BF': 349.23, '\u03C5': 392.00,
    '\u03C9': 440.00, '\u03B3': 196.00, '\u03B4': 220.00,
    '\u03BA': 174.61, '\u03BC': 164.81, '\u03BD': 130.81,
    '\u03C0': 146.83, '\u03C1': 155.56, '\u03C3': 185.00,
    '\u03C2': 185.00, '\u03C4': 196.00, '\u03C6': 246.94,
    '\u03C7': 207.65, '\u03C8': 200.00, ' ': 0,
}

GREEK_PHRASES = [
    "\u03B3\u03BD\u03CE\u03B8\u03B7\u03C4\u03B1\u03B9 \u03B5\u03B1\u03C5\u03C4\u03CC\u03C2",  # Gnothi seauton
    "\u03B1\u03C1\u03C7\u03AE",  # Arke
    "\u03C3\u03CD\u03BD\u03BA\u03BF\u03B9\u03BD\u03BF\u03BD",  # Synekheion
]

def synth_greek(text, start_s, dur_s):
    n_total = int(dur_s * SR)
    seg = np.zeros(n_total, dtype=np.float64)
    valid_chars = [(i, c) for i, c in enumerate(text) if c in GREEK_MAP and GREEK_MAP[c] > 0]
    if not valid_chars:
        return seg
    char_dur = dur_s / len(valid_chars)
    n_char = int(char_dur * SR)
    for idx, (orig_i, char) in enumerate(valid_chars):
        freq = GREEK_MAP[char]
        t = np.arange(n_char) / SR
        phase = (t * freq) % 1.0
        tri = 4 * np.abs(phase - 0.5) - 1
        harm = 4 * np.abs((t * freq * 1.5) % 1.0 - 0.5) - 1
        tone = (tri * 0.7 + harm * 0.15) * envelope(n_char, attack_s=0.05, release_s=0.1)
        offset = idx * n_char
        end = min(offset + n_char, n_total)
        seg[offset:end] = tone[:end - offset] * 0.05
    return seg

# ============================================================
# LAYER 4: Bird-like frequency sweeps
# ============================================================

def synth_bird(start_s, dur_s, seed=0):
    n_total = int(dur_s * SR)
    seg = np.zeros(n_total, dtype=np.float64)
    counter = 0
    t = 0.0
    while t < dur_s:
        interval = 0.2 + ((counter * 7 + 13 + seed) % 50) / 50 * 0.6
        if t + interval < dur_s:
            chirp_dur = 0.1 + ((counter * 3) % 4) / 10
            freq = 1500 + int(((t * 13 + 7 + seed) % 50)) * 40
            chirp = synth_single_chirp(chirp_dur, freq)
            offset = int(t * SR)
            chirp_len = min(len(chirp), n_total - offset)
            if chirp_len > 0:
                seg[offset:offset+chirp_len] += chirp[:chirp_len]
        t += interval
        counter += 1
    return seg

def synth_single_chirp(dur_s, base_freq):
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    mid = n // 2
    sweep = 600
    freq_up = np.linspace(base_freq, base_freq + sweep, mid)
    freq_down = np.linspace(base_freq + sweep, base_freq, n - mid)
    freq = np.concatenate([freq_up, freq_down])
    phase = np.cumsum(freq) / SR
    tone = np.sin(2 * np.pi * phase)
    env = np.exp(-t * 12) * (1 - np.exp(-t * 200))
    trill = 1 + 0.3 * np.sin(2 * np.pi * 30 * t)
    return tone * env * trill * 0.02

# ============================================================
# LAYER 5: Latin — Pythagoras ratios
# ============================================================

LATIN_PHRASES = [
    "OMNIA NUMERUS",         # Everything is number (Pythagoras)
    "AS ABOVE SO BELOW",     # Hermetic
    "IGNORANTIA IN TENEbris", # Ignorance in darkness
    "LUX VERITAS",           # Light truth
]

def synth_latin(text, start_s, dur_s, base_hz=130.81):
    n_total = int(dur_s * SR)
    seg = np.zeros(n_total, dtype=np.float64)
    chars = [c for c in text.upper() if c.isalpha()]
    if not chars:
        return seg
    char_dur = dur_s / len(chars)
    n_char = int(char_dur * SR)
    ratio_keys = list(PYTH_RATIOS.keys())
    for i, char in enumerate(chars):
        ratio_name = ratio_keys[ord(char) % len(ratio_keys)]
        freq = base_hz * PYTH_RATIOS[ratio_name]
        t = np.arange(n_char) / SR
        # Sine + soft square for Latin — pure and ancient
        sine = np.sin(2 * np.pi * freq * t)
        square = 2 * ((freq * t) % 1.0 < 0.5).astype(float) - 1
        tone = sine * 0.7 + square * 0.1
        tone *= envelope(n_char, attack_s=0.03, release_s=0.2)
        offset = i * n_char
        end = min(offset + n_char, n_total)
        seg[offset:end] = tone[:end - offset] * 0.05
    return seg

# ============================================================
# LAYER 6: Hebrew — Gematria → DR → freq
# ============================================================

HEBREW_VALUES = {
    '\u05D0': 1,  '\u05D1': 2,  '\u05D2': 3,  '\u05D3': 4,  '\u05D4': 5,
    '\u05D5': 6,  '\u05D6': 7,  '\u05D7': 8,  '\u05D8': 9,  '\u05D9': 10,
    '\u05DB': 20, '\u05DC': 30, '\u05DD': 40, '\u05DE': 50, '\u05DF': 60,
    '\u05E0': 70, '\u05E1': 80, '\u05E2': 90, '\u05E4': 200, '\u05E6': 60,
    '\u05E8': 200, '\u05E9': 300, '\u05EA': 400, ' ': 0,
}

HEBREW_PHRASES = [
    "\u05D4\u05D9\u05D4 \u05DE\u05E9\u05D9\u05DA",  # H' m'shiach (Who is like God)
    "\u05E9\u05DC\u05D5\u05DD",                       # Shalom (peace)
    "\u05D0\u05D5\u05E8",                             # Ohr (light)
    "\u05E6\u05D3\u05D9\u05EA",                       # Tzedek (justice)
]

def synth_hebrew(text, start_s, dur_s):
    n_total = int(dur_s * SR)
    seg = np.zeros(n_total, dtype=np.float64)
    valid_chars = [c for c in text if c in HEBREW_VALUES and HEBREW_VALUES[c] > 0]
    if not valid_chars:
        return seg
    char_dur = dur_s / len(valid_chars)
    n_char = int(char_dur * SR)
    for i, char in enumerate(valid_chars):
        val = HEBREW_VALUES[char]
        freq = DR_FREQ.get(digital_root(val), 396.0)
        t = np.arange(n_char) / SR
        # Sine with subtle vibrato — ancient and resonant
        vib = np.sin(2 * np.pi * 0.4 * t) * 4
        tone = np.sin(2 * np.pi * (freq + vib) * t)
        # Add 5th harmonic for richness
        harm5 = np.sin(2 * np.pi * (freq * 1.5 + vib) * t) * 0.15
        tone = tone * 0.8 + harm5
        tone *= envelope(n_char, attack_s=0.04, release_s=0.25)
        offset = i * n_char
        end = min(offset + n_char, n_total)
        seg[offset:end] = tone[:end - offset] * 0.05
    return seg

# ============================================================
# LAYER 7: Old Chinese — Bagua/I Ching → pentatonic
# ============================================================

# Simplified Chinese character → Bagua number mapping
BAGUA_MAP = {
    '\u5929': 1,   # Heaven
    '\u5730': 2,   # Earth
    '\u706b': 3,   # Fire
    '\u6C34': 4,   # Water
    '\u98CE': 5,   # Wind
    '\u5C71': 6,   # Mountain
    '\u6C99': 7,   # Lake
    '\u96F7': 8,   # Thunder
    '\u9053': 1,   # Dao
    '\u548C': 2,   # Harmony
    '\u5E73': 3,   # Peace
    '\u5149': 4,   # Light
    '\u660E': 5,   # Bright
    '\u5FC3': 6,   # Heart/Mind
    '\u7075': 7,   # Spirit
    '\u592A': 8,   # Supreme
}

CHINESE_PHRASES = [
    "\u9053\u548C",    # Dao Harmony
    "\u5E73\u5149",    # Peace Light
    "\u660E\u5FC3",    # Bright Heart
    "\u7075\u592A",    # Spirit Supreme
]

def synth_chinese(text, start_s, dur_s):
    n_total = int(dur_s * SR)
    seg = np.zeros(n_total, dtype=np.float64)
    valid_chars = [c for c in text if c in BAGUA_MAP]
    if not valid_chars:
        return seg
    char_dur = dur_s / len(valid_chars)
    n_char = int(char_dur * SR)
    for i, char in enumerate(valid_chars):
        bagua = BAGUA_MAP[char]
        freq = PENTATONIC[(bagua - 1) % len(PENTATONIC)]
        t = np.arange(n_char) / SR
        # Pentatonic sine — pure Chinese timbre
        tone = np.sin(2 * np.pi * freq * t)
        # Soft breath-like amplitude modulation
        breath = 0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * t)
        tone *= breath
        tone *= envelope(n_char, attack_s=0.08, release_s=0.4)
        offset = i * n_char
        end = min(offset + n_char, n_total)
        seg[offset:end] = tone[:end - offset] * 0.04
    return seg

# ============================================================
# LAYER 8: Old Egyptian — Hieroglyphs → DR → freq
# ============================================================

# Unicode Egyptian hieroglyphs (African Unicode block)
EGYPTIAN_MAP = {
    '\u1300': 1,   # Aa (eye)
    '\u1301': 2,
    '\u1302': 3,
    '\u1303': 4,
    '\u1304': 5,
    '\u1305': 6,
    '\u1306': 7,
    '\u1307': 8,
    '\u1308': 9,
    '\u1309': 10,
    '\u130A': 20,
    '\u130B': 30,
    '\u130C': 40,
    '\u130D': 50,
    '\u130E': 60,
    '\u130F': 70,
    '\u1310': 80,
    '\u1311': 90,
    '\u1312': 100,
    '\u1313': 200,
    '\u1314': 300,
    '\u1315': 400,
    '\u1316': 500,
    '\u1317': 600,
    '\u1318': 700,
    '\u1319': 800,
    '\u131A': 900,
    # Fallback: use common symbols
    '\u2625': 1,   # Ankh
    '\u2622': 2,   # Ouroboros
    '\u260F': 3,   # Alchemy sun
    '\u262B': 4,   # Alchemy air
    '\u262D': 5,   # Alchemy water
}

EGYPTIAN_GLYPHS = [
    "\u1300\u1310\u1305",  # Eye + power
    "\u1303\u1308\u1302",  # Cycle
    "\u1306\u130B\u1309",  # Light
    "\u1301\u1304\u1307",  # Eternal
]

def synth_egyptian(text, start_s, dur_s):
    n_total = int(dur_s * SR)
    seg = np.zeros(n_total, dtype=np.float64)
    valid_chars = [c for c in text if c in EGYPTIAN_MAP]
    if not valid_chars:
        return seg
    char_dur = dur_s / len(valid_chars)
    n_char = int(char_dur * SR)
    for i, char in enumerate(valid_chars):
        val = EGYPTIAN_MAP[char]
        freq = DR_FREQ.get(digital_root(val), 396.0)
        t = np.arange(n_char) / SR
        # Sawtooth + sine — Egyptian drone-like quality
        phase = (t * freq) % 1.0
        saw = 2 * phase - 1
        sine = np.sin(2 * np.pi * freq * t)
        tone = saw * 0.2 + sine * 0.6
        tone *= envelope(n_char, attack_s=0.1, release_s=0.5)
        offset = i * n_char
        end = min(offset + n_char, n_total)
        seg[offset:end] = tone[:end - offset] * 0.03
    return seg

# ============================================================
# BPM-SYNCED COMPOSITION
# ============================================================

# Structure (BPM-aware):
# Intro:      bars 0-8    (0-17.4s)  — drones only
# Build:      bars 8-32   (17.4-70s) — drums enter, layers appear
# Peak 1:     bars 32-48  (70-104s)  — all layers active
# Transition: bars 48-56  (104-121s) — density shift
# Peak 2:     bars 56-80  (121-174s) — maximum layering
# Outro:      bars 80-88  (174-180s) — fade

def build_composition():
    global buf
    buf = np.zeros(N, dtype=np.float64)
    print(f"Generating {DURATION}s 8-layer mono audio at {BPM} BPM...")

    bar_8  = int(8 * BAR * SR)
    bar_32 = int(32 * BAR * SR)
    bar_48 = int(48 * BAR * SR)
    bar_56 = int(56 * BAR * SR)
    bar_80 = int(80 * BAR * SR)

    # --- LAYER 1: Sanskrit (build → peak 1, aligned to 8-bar blocks) ---
    if HAS_SANSKRIT:
        print("  Layer 1/8: Sanskrit...")
        for i, phrase in enumerate(SANSKRIT_PHRASES):
            # Start on bar boundaries
            bar_start = 12 + i * 8
            start_s = bar_start * BAR
            dur_s = 4 * BAR  # 4 bars
            melody = synth_sanskrit(phrase, start_s, dur_s, base_hz=110)
            if len(melody) > 0:
                add(buf, melody, int(start_s * SR), 0.4)

    # --- LAYER 2: Arabic Abjad (build → peak 2) ---
    print("  Layer 2/8: Arabic Abjad...")
    for i, phrase in enumerate(ARABIC_PHRASES):
        bar_start = 16 + i * 10
        start_s = bar_start * BAR
        dur_s = 3 * BAR
        field = synth_arabic(phrase, start_s, dur_s)
        add(buf, field, int(start_s * SR), 0.5)

    # --- LAYER 3: Greek (peak 1 → peak 2) ---
    print("  Layer 3/8: Greek...")
    for i, phrase in enumerate(GREEK_PHRASES):
        bar_start = 36 + i * 8
        start_s = bar_start * BAR
        dur_s = 3 * BAR
        melody = synth_greek(phrase, start_s, dur_s)
        add(buf, melody, int(start_s * SR), 0.4)

    # --- LAYER 4: Birds (throughout, sparse) ---
    print("  Layer 4/8: Birds...")
    for block in range(6):
        bar_start = 2 + block * 14
        start_s = bar_start * BAR
        dur_s = 10 * BAR
        song = synth_bird(start_s, dur_s, seed=block * 17)
        add(buf, song, int(start_s * SR), 0.25)

    # --- LAYER 5: Latin (build → peak 1) ---
    print("  Layer 5/8: Latin (Pythagoras)...")
    for i, phrase in enumerate(LATIN_PHRASES):
        bar_start = 20 + i * 10
        start_s = bar_start * BAR
        dur_s = 4 * BAR
        melody = synth_latin(phrase, start_s, dur_s, base_hz=130.81)
        add(buf, melody, int(start_s * SR), 0.35)

    # --- LAYER 6: Hebrew (peak 1 → peak 2) ---
    print("  Layer 6/8: Hebrew (Gematria)...")
    for i, phrase in enumerate(HEBREW_PHRASES):
        bar_start = 34 + i * 8
        start_s = bar_start * BAR
        dur_s = 3 * BAR
        melody = synth_hebrew(phrase, start_s, dur_s)
        add(buf, melody, int(start_s * SR), 0.35)

    # --- LAYER 7: Chinese (transition → peak 2) ---
    print("  Layer 7/8: Chinese (Bagua)...")
    for i, phrase in enumerate(CHINESE_PHRASES):
        bar_start = 50 + i * 6
        start_s = bar_start * BAR
        dur_s = 2 * BAR
        melody = synth_chinese(phrase, start_s, dur_s)
        add(buf, melody, int(start_s * SR), 0.3)

    # --- LAYER 8: Egyptian (peak 2, finale) ---
    print("  Layer 8/8: Egyptian (Hieroglyphs)...")
    for i, phrase in enumerate(EGYPTIAN_GLYPHS):
        bar_start = 60 + i * 5
        start_s = bar_start * BAR
        dur_s = 3 * BAR
        melody = synth_egyptian(phrase, start_s, dur_s)
        add(buf, melody, int(start_s * SR), 0.25)

    # --- Global fade-out (last bar) ---
    fade_start = int(87 * BAR * SR)
    fade_len = N - fade_start
    if fade_len > 0:
        fade = np.linspace(1, 0, fade_len)
        buf[fade_start:] *= fade

    # --- Normalize ---
    peak = np.abs(buf).max()
    if peak > 0:
        buf *= 0.80 / peak
    buf = np.tanh(buf)

    return buf

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    buf = build_composition()

    samples = (buf * 32767).astype(np.int16)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multilayer-3min.wav")

    with wave.open(out_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(samples.tobytes())

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"Done: {out_path} ({DURATION}s, 8 layers, mono, {size_mb:.1f}MB)")
