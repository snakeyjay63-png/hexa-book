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
    "dr_signature": (1, 8, 1, 2),  # dr(82)=1, dr(134)=8, dr(37)=1, dr(74)=2
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
    
    Rejects frequencies at or above Nyquist to enforce SynthInput contract:
      SynthInput := {f ∈ ℝ | 0 < f < sample_rate/2}
    
    Returns numpy array of float64 samples.
    """
    nyquist = sample_rate / 2
    if not 0 < freq_hz < nyquist:
        raise ValueError(
            f"Frequency {freq_hz} Hz must be below Nyquist ({nyquist} Hz) "
            f"for sample_rate={sample_rate}"
        )
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


def component_frequency_centroid(freqs, weights):
    """Weighted average of known oscillator frequencies (component-level).
    
    Dit is de centroid van de oscillator-frequenties ZELF, niet van het
    gegenereerde signaal E(t). Voor echte signaalanalyse: signal_spectral_centroid().
    """
    total_weight = np.sum(weights)
    if total_weight == 0:
        return 0.0
    return float(np.sum(freqs * weights) / total_weight)


def signal_spectral_centroid(samples, sample_rate):
    """Spectral centroid from FFT of generated signal E(t).
    
    Dit is de ACTUELE signaal-centroid, gemeten uit de FFT.
    Kan afwijken van component_frequency_centroid door window leakage.
    """
    magnitude = np.abs(np.fft.rfft(samples))
    frequencies = np.fft.rfftfreq(len(samples), 1 / sample_rate)
    total_mag = np.sum(magnitude)
    if total_mag == 0:
        return 0.0
    return float(np.sum(frequencies * magnitude) / total_mag)


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
    
    Model A1:
      E_raw(t) = Σ W_i(t)
      E_audio(t) = E_raw(t) / max(1, peak(E_raw))  ← normalisatie voorkomt clipping
    
    Args:
        wave_specs: {"W_X": {"freq": float, "byte": int}, ...}
        sample_rate: int
        duration_s: float
        amplitude: float per wave
    
    Returns (E_raw, E_audio, individual_waves, metadata)
    """
    n_samples = int(sample_rate * duration_s)
    individual = {}
    E_raw = np.zeros(n_samples, dtype=np.float64)
    
    freqs = []
    weights = []
    
    for name, spec in wave_specs.items():
        f = spec["freq"]
        w = synth_sine(f, amplitude, sample_rate, duration_s)
        individual[name] = w
        E_raw += w
        freqs.append(f)
        weights.append(1.0)  # Equal weight for identical amplitude
    
    # Normalisatie: voorkomt clipping bij WAV-opslag
    raw_peak = float(np.max(np.abs(E_raw)))
    norm_gain = raw_peak if raw_peak > 1.0 else 1.0
    E_audio = E_raw / norm_gain
    
    metadata = {
        "sample_count": n_samples,
        "sample_rate": sample_rate,
        "duration": duration_s,
        "n_waves": len(wave_specs),
        "component_centroid": component_frequency_centroid(np.array(freqs), np.array(weights)),
        "signal_centroid": signal_spectral_centroid(E_audio, sample_rate),
        "raw_peak": raw_peak,
        "normalization_gain": norm_gain,
        "normalized_peak": float(np.max(np.abs(E_audio))),
    }
    
    return E_raw, E_audio, individual, metadata


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
    """Validate Model A synth + analysis pipeline."""
    waves = MODEL_A["waves"]
    sr = MODEL_A["sample_rate"]
    dur = MODEL_A["duration"]
    amp = MODEL_A["amplitude"]
    
    print("=" * 60)
    print("  NPR Sound Engine — Model A Validatie")
    print("=" * 60)
    
    passed, failed = 0, 0
    
    E_raw, E_audio, individual, meta = superposition(waves, sr, dur, amp)
    
    # Test 1: Superposition sample count
    expected_samples = sr * int(dur)
    if len(E_raw) == expected_samples:
        print(f"  ✅ superposition_samples: {len(E_raw)}")
        passed += 1
    else:
        print(f"  ❌ superposition_samples: {len(E_raw)} (expected {expected_samples})")
        failed += 1
    
    # Test 2: Deterministic (SHA256)
    h = sha256_samples(E_raw)
    print(f"  ℹ SHA256 (raw): {h[:16]}...")
    
    # Test 3: RMS (on raw signal)
    r = rms(E_raw)
    print(f"  ℹ RMS (raw): {r:.4f}")
    
    # Test 4: Component centroid
    freqs = [waves[w]["freq"] for w in waves]
    weights = [1.0] * len(freqs)
    c_comp = component_frequency_centroid(np.array(freqs), np.array(weights))
    expected_centroid = sum(waves[w]["freq"] for w in waves) / len(waves)
    
    if abs(c_comp - expected_centroid) < 0.01:
        print(f"  ✅ component_centroid: {c_comp:.2f} Hz (expected {expected_centroid:.2f})")
        passed += 1
    else:
        print(f"  ❌ component_centroid: {c_comp:.2f} Hz (expected {expected_centroid:.2f})")
        failed += 1
    
    # Test 4b: Signal centroid (from FFT of E_audio)
    c_sig = signal_spectral_centroid(E_audio, sr)
    print(f"  ℹ signal_centroid (FFT): {c_sig:.2f} Hz")
    
    # Test 5: Dominant frequency (superposition)
    dom = dominant_frequency(E_audio, sr)
    print(f"  ℹ dominant_freq (superposition): {dom:.2f} Hz")
    
    # Test 6: DR signature — hardcoded expected values (independent check)
    bytes_a = [waves[w]["byte"] for w in waves]
    actual_drs = tuple(dr(b) for b in bytes_a)
    expected_drs = (1, 8, 1, 2)  # dr(82)=1, dr(134)=8, dr(37)=1, dr(74)=2
    
    if actual_drs == expected_drs:
        print(f"  ✅ DR_signature: {actual_drs}")
        passed += 1
    else:
        print(f"  ❌ DR_signature: {actual_drs} (expected {expected_drs})")
        failed += 1
    
    # Test 7: Normalization
    if meta["raw_peak"] > 1.0 and meta["normalized_peak"] <= 1.0 + 1e-6:
        print(f"  ✅ normalization: raw_peak={meta['raw_peak']:.4f}, gain={meta['normalization_gain']:.4f}, norm_peak={meta['normalized_peak']:.4f}")
        passed += 1
    else:
        print(f"  ❌ normalization: raw_peak={meta['raw_peak']:.4f}, norm_peak={meta['normalized_peak']:.4f}")
        failed += 1
    
    # Test 8: Deterministic hash (raw)
    E_raw2, _, _, _ = superposition(waves, sr, dur, amp)
    h2 = sha256_samples(E_raw2)
    if h == h2:
        print(f"  ✅ deterministic: same_input → same_hash ({h[:16]}...)")
        passed += 1
    else:
        print(f"  ❌ deterministic: hash mismatch ({h[:16]} ≠ {h2[:16]})")
        failed += 1
    
    # Test 9: Individual wave RMS ≈ 1/√2
    expected_rms = 1.0 / math.sqrt(2)
    for name in waves:
        w = individual[name]
        r_i = rms(w)
        if abs(r_i - expected_rms) < 0.01:
            print(f"  ✅ rms({name}): {r_i:.4f}")
            passed += 1
        else:
            print(f"  ❌ rms({name}): {r_i:.4f} (expected ~{expected_rms:.4f})")
            failed += 1
    
    # Test 10: Dominant freq per wave
    for name, spec in waves.items():
        w = individual[name]
        dom_f = dominant_frequency(w, sr)
        expected_f = spec["freq"]
        if abs(dom_f - expected_f) < 0.5:
            print(f"  ✅ dominant_freq({name}): {dom_f:.2f} Hz")
            passed += 1
        else:
            print(f"  ❌ dominant_freq({name}): {dom_f:.2f} Hz (expected {expected_f})")
            failed += 1
    
    print(f"\n  Totaal: {passed} ✅ | {failed} ❌")
    return passed, failed, E_raw, E_audio, individual, meta


def test_byte_to_freq_integration():
    """Test byte → freq → synth → dominant_freq."""
    passed, failed = 0, 0
    sr = MODEL_A["sample_rate"]
    dur = 2.0  # Longer for FFT resolution
    amp = MODEL_A["amplitude"]
    
    print("\n--- Byte → Freq → Synth Integration ---")
    
    for name, wave in MODEL_A["waves"].items():
        f = wave["freq"]
        B = wave["byte"]
        
        # Generate
        w = synth_sine(f, amp, sr, dur)
        
        # Measure
        dom = dominant_frequency(w, sr)
        
        # Tolerance: bin width = sr / (sr * dur) = 1/dur = 0.5 Hz
        bin_width = sr / len(w)
        tolerance = max(bin_width, 0.6)
        
        diff = abs(dom - f)
        if diff <= tolerance:
            print(f"  ✅ {name}: {f:.2f} Hz → measured {dom:.2f} Hz (diff={diff:.3f}, tol={tolerance:.2f})")
            passed += 1
        else:
            print(f"  ❌ {name}: {f:.2f} Hz → measured {dom:.2f} Hz (diff={diff:.3f}, tol={tolerance:.2f})")
            failed += 1
    
    return passed, failed


def test_edge_cases():
    """Test edge cases."""
    print("\n--- Edge Cases ---")
    passed, failed = 0, 0
    sr = 44100
    
    # Nyquist rejection: freq >= sample_rate/2 must raise
    try:
        synth_sine(22050, 1.0, sr, 0.1)  # exactly at Nyquist
        print("  ❌ Nyquist boundary should raise")
        failed += 1
    except ValueError:
        print("  ✅ Nyquist boundary (22050 Hz) raises ValueError")
        passed += 1
    
    # Above Nyquist must also raise
    try:
        synth_sine(30000, 1.0, sr, 0.1)
        print("  ❌ Above-Nyquist should raise")
        failed += 1
    except ValueError:
        print("  ✅ Above-Nyquist (30000 Hz) raises ValueError")
        passed += 1
    
    # Zero duration → empty samples
    w = synth_sine(440, 1.0, sr, 0.0)
    if len(w) == 0:
        print("  ✅ Zero duration → empty samples")
        passed += 1
    else:
        print(f"  ❌ Zero duration → {len(w)} samples")
        failed += 1
    
    # Unknown waveform
    try:
        synth_waveform("square", 440, 1.0, sr, 0.1)
        print("  ❌ Unknown waveform should raise")
        failed += 1
    except ValueError:
        print("  ✅ Unknown waveform raises ValueError")
        passed += 1
    
    return passed, failed


def main():
    # Relative output path for portability
    output_dir = Path(__file__).parent / "synth_output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run validation
    p1, f1, E_raw, E_audio, individual, meta = validate_model_a()
    p2, f2 = test_byte_to_freq_integration()
    p3, f3 = test_edge_cases()
    
    # Save normalized audio (E_audio), not raw (E_raw)
    if E_audio is not None:
        # Save normalized superposition
        save_wav(str(output_dir / "E_superposition.wav"), E_audio, MODEL_A["sample_rate"])
        np.save(str(output_dir / "E_superposition.npy"), E_audio)
        
        # Save individual waves
        for name, w in individual.items():
            save_wav(str(output_dir / f"{name}.wav"), w, MODEL_A["sample_rate"])
            np.save(str(output_dir / f"{name}.npy"), w)
        
        print(f"\n  Output saved: {output_dir}/")
        print(f"    E_superposition.wav (normalized, {MODEL_A['sample_rate']} Hz, 1s)")
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
