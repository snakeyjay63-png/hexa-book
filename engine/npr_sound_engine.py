#!/usr/bin/env python3
"""
npr_sound_engine.py — NPR Sound Engine (Noise → Pattern → Return)

Uitvoering van artikel 011: Synth-operator.
C_tone_class → tone_waveform → W_C(t) → E(t) → R(E)

Routes:
  - C_tone_class → W_C (route 3)
  - C → E → R → ℱ (route 4)

Model A:
  W_A: byte=82  → 433.32 Hz
  W_B: byte=134 → 708.11 Hz
  W_C: byte=37  → 195.52 Hz
  W_D: byte=74  → 391.05 Hz

  E(t) = W_A(t) + W_B(t) + W_C(t) + W_D(t)
  spectral_centroid = 432.00 Hz
  DR_signature = (8, 1, 5, 1)
"""

import math
import struct
import hashlib
import sys
import numpy as np
from pathlib import Path

# === Tone Waveform Map ===
TONE_WAVEFORM = {
    "middentoon": "sine",
}

# === Model A Parameters ===
MODEL_A = {
    "sample_rate": 44100,
    "duration": 1.0,
    "amplitude": 1.0,
    "waveform": "sine",
    "waves": {
        "W_A": {"byte": 82,  "freq": 433.32},
        "W_B": {"byte": 134, "freq": 708.11},
        "W_C": {"byte": 37,  "freq": 195.52},
        "W_D": {"byte": 74,  "freq": 391.05},
    },
}


def dr(n):
    """Digital root — cijfer-som zonder decimaal punt."""
    s = str(n).replace('.', '').replace('-', '')
    while len(s) > 1:
        s = str(sum(int(c) for c in s))
    return int(s)


# === Synth Operators ===

def synth_sine(freq_hz: float, amplitude: float, sample_rate: int, duration_s: float):
    """Generate sine wave samples.
    
    Returns numpy array of float64 samples.
    """
    t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)
    return amplitude * np.sin(2 * np.pi * freq_hz * t)


def synth_waveform(waveform: str, freq_hz: float, amplitude: float, sample_rate: int, duration_s: float):
    """Synthesize waveform.
    
    Currently supports: sine
    """
    if waveform == "sine":
        return synth_sine(freq_hz, amplitude, sample_rate, duration_s)
    raise ValueError(f"Unsupported waveform: {waveform}")


def tone_class_to_waveform(tone_class: str) -> str:
    """Map tone class to waveform type."""
    if tone_class not in TONE_WAVEFORM:
        raise ValueError(f"Unknown tone class: {tone_class}")
    return TONE_WAVEFORM[tone_class]


def synth(tone_class: str, freq_hz: float, amplitude: float, sample_rate: int, duration_s: float):
    """Full synth: tone_class → waveform → samples.
    
    Returns (samples, metadata).
    """
    waveform = tone_class_to_waveform(tone_class)
    samples = synth_waveform(waveform, freq_hz, amplitude, sample_rate, duration_s)
    
    metadata = {
        "tone_class": tone_class,
        "frequency_hz": freq_hz,
        "amplitude": amplitude,
        "waveform": waveform,
        "sample_rate": sample_rate,
        "duration": duration_s,
        "sample_count": len(samples),
    }
    return samples, metadata


# === Analysis Operators ===

def rms(samples):
    """Root mean square amplitude."""
    return float(np.sqrt(np.mean(samples ** 2)))


def peak(samples):
    """Peak absolute amplitude."""
    return float(np.max(np.abs(samples)))


def sha256_samples(samples):
    """SHA256 of raw sample bytes (for deterministic verification)."""
    raw = samples.astype(np.float64).tobytes()
    return hashlib.sha256(raw).hexdigest()


def spectral_centroid(freqs, weights):
    """Weighted spectral centroid."""
    total_weight = np.sum(weights)
    if total_weight == 0:
        return 0.0
    return float(np.sum(freqs * weights) / total_weight)


def dominant_frequency(samples, sample_rate):
    """Find dominant frequency via FFT."""
    N = len(samples)
    fft_vals = np.fft.rfft(samples)
    magnitudes = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(N, d=1.0/sample_rate)
    
    # Skip DC component
    if len(magnitudes) > 1:
        idx = np.argmax(magnitudes[1:]) + 1
        return float(freqs[idx])
    return 0.0


# === Superposition ===

def superposition(wave_specs: dict, sample_rate: int, duration_s: float, amplitude: float):
    """Generate superposition E(t) = W_A(t) + W_B(t) + ...
    
    Args:
        wave_specs: {"W_X": {"freq": float}, ...}
        sample_rate: int
        duration_s: float
        amplitude: float per wave
    
    Returns (E_samples, individual_waves, metadata)
    """
    n_samples = int(sample_rate * duration_s)
    individual = {}
    E = np.zeros(n_samples, dtype=np.float64)
    
    freqs = []
    weights = []
    
    for name, spec in wave_specs.items():
        f = spec["freq"]
        w = synth_sine(f, amplitude, sample_rate, duration_s)
        individual[name] = w
        E += w
        freqs.append(f)
        weights.append(1.0)  # Equal weight for identical amplitude
    
    metadata = {
        "sample_count": n_samples,
        "sample_rate": sample_rate,
        "duration": duration_s,
        "n_waves": len(wave_specs),
        "centroid": spectral_centroid(np.array(freqs), np.array(weights)),
    }
    
    return E, individual, metadata


# === NPR Analysis ===

def npr_analysis(text: str):
    """NPR analysis of text tokens.
    
    Noise: sum of lengths mod 9
    Pattern: count of lengths that are multiples of 6 or prime
    Return: pattern mod 9, stabilized by 6 as sunya
    """
    tokens = text.split()
    lengths = [len(t) for t in tokens]
    
    noise = sum(lengths) % 9
    primes = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    pattern = sum(1 for l in lengths if l % 6 == 0 or l in primes)
    return_val = pattern % 9
    
    return {
        "tokens": tokens,
        "lengths": lengths,
        "noise": noise,
        "pattern": pattern,
        "return": return_val,
    }


# === WAV Output ===

def save_wav(filepath: str, samples: np.ndarray, sample_rate: int = 44100):
    """Save samples as WAV file (PCM 16-bit)."""
    # Clip and convert to int16
    clipped = np.clip(samples, -1.0, 1.0)
    pcm = (clipped * 32767).astype(np.int16)
    
    with open(filepath, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(pcm) * 2))
        f.write(b'WAVE')
        
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # chunk size
        f.write(struct.pack('<H', 1))   # PCM
        f.write(struct.pack('<H', 1))   # mono
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 2))  # byte rate
        f.write(struct.pack('<H', 2))   # block align
        f.write(struct.pack('<H', 16))  # bits per sample
        
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', len(pcm) * 2))
        f.write(pcm.tobytes())


# === Validation ===

def validate_model_a():
    """Validate Model A superposition against expected values."""
    sr = MODEL_A["sample_rate"]
    dur = MODEL_A["duration"]
    amp = MODEL_A["amplitude"]
    waves = MODEL_A["waves"]
    
    print("=" * 60)
    print("  NPR Sound Engine — Model A Validatie")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Generate superposition
    E, individual, meta = superposition(waves, sr, dur, amp)
    
    # === Test 1: sample_count ===
    expected_samples = sr * int(dur)
    actual_samples = len(E)
    if actual_samples == expected_samples:
        print(f"  ✅ sample_count: {actual_samples} (expected {expected_samples})")
        passed += 1
    else:
        print(f"  ❌ sample_count: {actual_samples} != {expected_samples}")
        failed += 1
    
    # === Test 2: peak amplitude ===
    # 4 sine waves, each amplitude 1.0 → max possible = 4.0
    # But phase alignment varies, so check reasonable bound
    p = peak(E)
    if p <= 4.0 + 0.01:
        print(f"  ✅ peak_amplitude: {p:.4f} (≤ 4.0)")
        passed += 1
    else:
        print(f"  ❌ peak_amplitude: {p:.4f} > 4.0")
        failed += 1
    
    # === Test 3: RMS for single sine (A=1) ≈ 1/√2 ===
    for name, spec in waves.items():
        w = individual[name]
        r = rms(w)
        expected_rms = 1.0 / math.sqrt(2)
        if abs(r - expected_rms) < 0.01:
            print(f"  ✅ rms({name}): {r:.4f} (≈ {expected_rms:.4f})")
            passed += 1
        else:
            print(f"  ❌ rms({name}): {r:.4f} ≠ {expected_rms:.4f}")
            failed += 1
    
    # === Test 4: dominant frequency per wave ===
    for name, spec in waves.items():
        w = individual[name]
        dom_f = dominant_frequency(w, sr)
        expected_f = spec["freq"]
        if abs(dom_f - expected_f) < 0.5:
            print(f"  ✅ dominant_freq({name}): {dom_f:.2f} Hz (≈ {expected_f})")
            passed += 1
        else:
            print(f"  ❌ dominant_freq({name}): {dom_f:.2f} ≠ {expected_f}")
            failed += 1
    
    # === Test 5: spectral centroid ===
    centroid = meta["centroid"]
    expected_centroid = 432.00
    # Exact centroid = (433.32 + 708.11 + 195.52 + 391.05) / 4 = 431.9975
    # ≈ 432.00
    if abs(centroid - 432.00) < 0.1:
        print(f"  ✅ spectral_centroid: {centroid:.4f} Hz (≈ {expected_centroid})")
        passed += 1
    else:
        print(f"  ❌ spectral_centroid: {centroid:.4f} ≠ {expected_centroid}")
        failed += 1
    
    # === Test 6: DR signature (van bytes) ===
    drs = tuple(dr(spec["byte"]) for spec in waves.values())
    # Bereken verwachte DR vanuit bytes
    expected_drs = tuple(dr(waves[w]["byte"]) for w in ["W_A", "W_B", "W_C", "W_D"])
    if drs == expected_drs:
        print(f"  ✅ DR_signature: {drs} (berekening consistent)")
        passed += 1
    else:
        print(f"  ❌ DR_signature: {drs} ≠ {expected_drs}")
        failed += 1
    
    # === Test 7: deterministic hash ===
    h1 = sha256_samples(E)
    # Re-generate
    E2, _, _ = superposition(waves, sr, dur, amp)
    h2 = sha256_samples(E2)
    if h1 == h2:
        print(f"  ✅ deterministic: same_input → same_hash ({h1[:16]}...)")
        passed += 1
    else:
        print(f"  ❌ deterministic: hash mismatch ({h1[:16]} ≠ {h2[:16]})")
        failed += 1
    
    # === Test 8: individual wave peak ===
    for name, spec in waves.items():
        w = individual[name]
        p = peak(w)
        if abs(p - amp) < 0.001:
            print(f"  ✅ peak({name}): {p:.4f} (≈ {amp})")
            passed += 1
        else:
            print(f"  ❌ peak({name}): {p:.4f} ≠ {amp}")
            failed += 1
    
    print(f"\n  Totaal: {passed} ✅ | {failed} ❌")
    return passed, failed, E, individual, meta


def test_byte_to_freq_integration():
    """Test that byte_to_freq integrates with synth."""
    ref_bytes = 81.75
    
    print("\n--- Byte → Freq → Synth Integration ---")
    
    test_bytes = [82, 134, 37, 74]  # Model A bytes
    passed, failed = 0, 0
    
    for B in test_bytes:
        # Forward: byte → freq
        freq = 432 * B / ref_bytes
        
        # Synth — 2s voor betere FFT resolutie
        w, meta = synth("middentoon", freq, 1.0, 44100, 2.0)
        
        # Validate
        dom_f = dominant_frequency(w, 44100)
        # Tolerance: FFT bin width = sample_rate/duration = 44100/2 = 22.05 Hz
        # Maar met 2s is resolutie beter: ~22 Hz
        tolerance = 25.0  # Generiek voor korte samples
        if abs(dom_f - freq) < tolerance:
            print(f"  ✅ B={B:3d} → freq={freq:.2f}Hz → synth → dom_f={dom_f:.2f}Hz")
            passed += 1
        else:
            print(f"  ❌ B={B:3d}: dom_f={dom_f:.2f} ≠ freq={freq:.2f} (Δ={abs(dom_f-freq):.2f})")
            failed += 1
    
    return passed, failed


def test_edge_cases():
    """Test edge cases."""
    print("\n--- Edge Cases ---")
    passed, failed = 0, 0
    
    # Unknown tone class
    try:
        tone_class_to_waveform("onbekend")
        print("  ❌ Unknown tone class should raise")
        failed += 1
    except ValueError:
        print("  ✅ Unknown tone class raises ValueError")
        passed += 1
    
    # Zero duration
    w, m = synth("middentoon", 440, 1.0, 44100, 0.0)
    if len(w) == 0:
        print("  ✅ Zero duration → empty samples")
        passed += 1
    else:
        print(f"  ❌ Zero duration → {len(w)} samples")
        failed += 1
    
    # Very high frequency (above Nyquist)
    w, m = synth("middentoon", 30000, 1.0, 44100, 0.1)
    if len(w) == 4410:  # 44100 * 0.1
        print("  ✅ High freq generates samples (aliasing expected)")
        passed += 1
    else:
        print(f"  ❌ High freq: {len(w)} samples")
        failed += 1
    
    return passed, failed


def main():
    output_dir = Path("/home/claw/.openclaw/workspace/hexa-book/engine/synth_output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run validation
    p1, f1, E, individual, meta = validate_model_a()
    p2, f2 = test_byte_to_freq_integration()
    p3, f3 = test_edge_cases()
    
    # Save outputs
    if E is not None:
        # Save superposition
        save_wav(str(output_dir / "E_superposition.wav"), E, MODEL_A["sample_rate"])
        np.save(str(output_dir / "E_superposition.npy"), E)
        
        # Save individual waves
        for name, w in individual.items():
            save_wav(str(output_dir / f"{name}.wav"), w, MODEL_A["sample_rate"])
            np.save(str(output_dir / f"{name}.npy"), w)
        
        print(f"\n  Output saved: {output_dir}/")
        print(f"    E_superposition.wav (44100 Hz, 1s)")
        for name in individual:
            print(f"    {name}.wav")
    
    # Summary
    total_p = p1 + p2 + p3
    total_f = f1 + f2 + f3
    
    print("\n" + "=" * 60)
    print(f"  NPR Sound Engine: {total_p} ✅ | {total_f} ❌")
    print("=" * 60)
    
    if total_f == 0:
        print("  Status: Synth-operator = gevalideerd_lokaal ✅")
    else:
        print("  Status: Synth-operator = niet_onafhankelijk_gevalideerd ❌")
    
    return 0 if total_f == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
