#!/usr/bin/env python3
"""
sanskrit_npr_bridge.py — Sanskrit → NPR Bridge Operator

Officiële hexa-book engine operator.
Integreert twee systemen:
  1. sanskrit_freq.py — Devanagari → phoneme → freq
  2. npr_sound_engine.py — byte → wave → E(t) → NPR analysis

Pipeline:
  Devanagari → tokenize → freq → byte → synth → E(t) → R(E)

Routes:
  - C_phoneme → C_freq (route 5: phonem-mapping)
  - C_freq → C_byte → C_wave → E(t) (route 6: synth-keten)
  - E(t) → NPR_analysis → R(E) (route 7: NPR-reductie)

Model:
  REF_BYTES = 81.75
  CENTROID_TARGET = 432.0 Hz
  byte = freq × ref / 432
  freq = byte × 432 / ref

Auteur: hexa-book engine
Datum: 2026-07-24
Status: gevalideerd_lokaal (spike-020)
"""

import sys
import os
import numpy as np
import hashlib
import math

# === Engine imports ===
WORKSPACE = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(WORKSPACE, "skills", "sanskrit-frequency-bridge", "scripts"))
sys.path.insert(0, os.path.dirname(__file__))

from sanskrit_freq import tokenize, map_phonemes
import npr_sound_engine as npr

# === Constants ===
REF_BYTES = 81.75
CENTROID_TARGET = 432.0
SAMPLE_RATE = 44100


# === Core Operators ===

def dr(n):
    """Digital root — cijfer-som zonder decimaal punt."""
    s = str(n).replace('.', '').replace('-', '')
    while len(s) > 1:
        s = str(sum(int(c) for c in s))
    return int(s)


def freq_to_byte(freq_hz: float, ref_bytes: float = REF_BYTES) -> float:
    """Return cycle forward: byte = freq × ref / 432.
    
    Route 6a: C_freq → C_byte
    """
    return freq_hz * ref_bytes / CENTROID_TARGET


def byte_to_freq(byte_val: float, ref_bytes: float = REF_BYTES) -> float:
    """Return cycle inverse: freq = byte × 432 / ref.
    
    Route 6b: C_byte → C_freq
    """
    return byte_val * CENTROID_TARGET / ref_bytes


# === Phoneme Operators ===

def tokenize_text(devanagari: str) -> list:
    """Route 5a: Devanagari → phoneme tokens.
    
    Returns list of token dicts.
    """
    return tokenize(devanagari)


def map_phoneme_frequencies(devanagari: str, base_hz: float = 55.0) -> list:
    """Route 5b: Devanagari → phoneme frequency map.
    
    Returns list of dicts with freq, cutoff, env, etc.
    """
    return map_phonemes(devanagari, base_hz=base_hz)


# === Bridge Operators ===

def phonemes_to_waves(phoneme_map: list, ref_bytes: float = REF_BYTES) -> dict:
    """Route 5→6: phoneme map → wave specs for superposition.
    
    Filters out effect-only phonemes (visarga, anusvāra, chandra).
    Returns wave specs dict compatible with npr.superposition().
    """
    waves = {}
    for idx, p in enumerate(phoneme_map):
        if p.get('type') in ('visarga', 'anusvāra', 'chandra'):
            continue  # effect-only
        
        freq = p.get('freq', 55.0)
        byte_val = freq_to_byte(freq, ref_bytes)
        
        name = f"PH_{idx:02d}"
        waves[name] = {
            "freq": freq,
            "byte": byte_val,
            "char": p.get('char', '?'),
            "name": p.get('name', 'unknown'),
        }
    
    return waves


def synthesize(devanagari: str, sample_rate: int = SAMPLE_RATE,
               duration: float = 1.0, amplitude: float = 1.0,
               ref_bytes: float = REF_BYTES):
    """Full bridge: Devanagari → E(t) superposition.
    
    Routes: 5a → 5b → 6 → E(t)
    
    Returns (E_samples, waves, phoneme_map, metadata).
    """
    # Route 5: phoneme mapping
    phoneme_map = map_phoneme_frequencies(devanagari, base_hz=55.0)
    if not phoneme_map:
        return None, {}, phoneme_map, {"error": "no phonemes"}
    
    # Route 5→6: waves
    waves = phonemes_to_waves(phoneme_map, ref_bytes)
    if not waves:
        return None, waves, phoneme_map, {"error": "no synth-able phonemes"}
    
    # Route 6: superposition
    wave_specs = {k: {"freq": v["freq"]} for k, v in waves.items()}
    E, individual, synth_meta = npr.superposition(wave_specs, sample_rate, duration, amplitude)
    
    # Route 7: metadata
    freqs = [v["freq"] for v in waves.values()]
    bytes_out = [v["byte"] for v in waves.values()]
    drs = [dr(int(round(b))) for b in bytes_out]
    
    metadata = {
        "text": devanagari,
        "phoneme_count": len(phoneme_map),
        "wave_count": len(waves),
        "frequencies": freqs,
        "bytes": bytes_out,
        "digital_roots": drs,
        "centroid": synth_meta["centroid"],
        "peak": npr.peak(E),
        "rms": npr.rms(E),
        "dominant_freq": npr.dominant_frequency(E, sample_rate),
        "sample_count": len(E),
        "hash": npr.sha256_samples(E),
        "individual_waves": individual,
    }
    
    return E, waves, phoneme_map, metadata


def npr_analysis(devanagari: str) -> dict:
    """Route 7: NPR analysis of input text.
    
    Noise → Pattern → Return on token lengths.
    """
    return npr.npr_analysis(devanagari)


# === Validation ===

def validate():
    """Validate bridge with canonical test cases."""
    print("=" * 60)
    print("  Sanskrit-NPR Bridge — Engine Validatie")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    test_cases = [
        ("ॐ", "Om", 1),
        ("ॐ नमः शिवाय", "Panchakshara", 5),
        ("सत्यम्", "Satyam", 2),
        ("अहं ब्रह्मास्मि", "Aham Brahmasmi", 4),
    ]
    
    for text, label, expected_waves in test_cases:
        print(f"\n  --- {label}: \"{text}\" ---")
        
        E, waves, phoneme_map, meta = synthesize(text)
        
        if E is None:
            print(f"  ❌ Bridge failed: {meta.get('error', 'unknown')}")
            failed += 1
            continue
        
        # Test 1: wave count
        if meta["wave_count"] == expected_waves:
            print(f"  ✅ wave_count: {meta['wave_count']}")
            passed += 1
        else:
            print(f"  ❌ wave_count: {meta['wave_count']} ≠ {expected_waves}")
            failed += 1
        
        # Test 2: sample_count
        expected = SAMPLE_RATE * 1.0
        if meta["sample_count"] == expected:
            print(f"  ✅ sample_count: {meta['sample_count']}")
            passed += 1
        else:
            print(f"  ❌ sample_count: {meta['sample_count']} ≠ {expected}")
            failed += 1
        
        # Test 3: byte roundtrip
        roundtrip_ok = True
        for name, w in waves.items():
            rt_freq = byte_to_freq(w["byte"])
            if abs(rt_freq - w["freq"]) > 0.01:
                roundtrip_ok = False
                break
        if roundtrip_ok:
            print(f"  ✅ byte_roundtrip: consistent")
            passed += 1
        else:
            print(f"  ❌ byte_roundtrip: loss > 0.01 Hz")
            failed += 1
        
        # Test 4: deterministic
        E2, _, _, _ = synthesize(text)
        if meta["hash"] == npr.sha256_samples(E2):
            print(f"  ✅ deterministic: stable ({meta['hash'][:16]}...)")
            passed += 1
        else:
            print(f"  ❌ deterministic: hash differs")
            failed += 1
        
        # Test 5: DR in range
        if all(1 <= d <= 9 for d in meta["digital_roots"]):
            print(f"  ✅ DR_signature: {meta['digital_roots']}")
            passed += 1
        else:
            print(f"  ❌ DR out of range: {meta['digital_roots']}")
            failed += 1
        
        # Test 6: peak bounded
        max_possible = meta["wave_count"] * 1.0
        if meta["peak"] <= max_possible + 0.01:
            print(f"  ✅ peak_bounded: {meta['peak']:.4f} ≤ {max_possible}")
            passed += 1
        else:
            print(f"  ❌ peak: {meta['peak']:.4f} > {max_possible}")
            failed += 1
    
    print(f"\n{'=' * 60}")
    print(f"  Totaal: {passed} ✅ | {failed} ❌")
    print(f"{'=' * 60}")
    
    if failed == 0:
        print("  Status: Sanskrit-NPR Bridge = gevalideerd_lokaal ✅")
    else:
        print(f"  Status: {failed} failures ❌")
    
    return passed, failed


def main():
    p, f = validate()
    return 0 if f == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
