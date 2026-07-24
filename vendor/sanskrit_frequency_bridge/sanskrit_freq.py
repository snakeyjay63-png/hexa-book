#!/usr/bin/env python3
"""
Sanskrit Frequency Bridge — Devanagari → Audio
Pure phoneme mapping via Gaṇa + Śāradā systems.
No LLM, no interpretation — deterministic frequency synthesis.

Modes:
- synth: Generate WAV from Devanagari text
- map:   Return JSON frequency mapping (no audio)
- chain: map → synth in one call

Pure numpy + wave (no scipy needed).
Compatible with npr-modulator-transformer output.
"""

import sys
import json
import struct
import argparse
import random
import wave
import numpy as np
import os

# ──────────────────────────────────────────────
# CONSONANT TABLE — full 35 consonant mapping
# Gaṇa → base register, Śāradā → exact pitch
# ──────────────────────────────────────────────
CONSONANTS = {
    # Velar (Gaṇa 1)
    'क': {'freq': 130.81, 'type': 'sparśa', 'name': 'ka'},
    'ख': {'freq': 146.83, 'type': 'sparśa', 'name': 'kha'},
    'ग': {'freq': 164.81, 'type': 'sparśa', 'name': 'ga'},
    'घ': {'freq': 174.61, 'type': 'sparśa', 'name': 'gha'},
    'ङ': {'freq': 196.00, 'type': 'nāda', 'name': 'ṅa'},
    # Palatal (Gaṇa 2)
    'च': {'freq': 220.00, 'type': 'sparśa', 'name': 'ca'},
    'छ': {'freq': 233.08, 'type': 'sparśa', 'name': 'cha'},
    'ज': {'freq': 261.63, 'type': 'sparśa', 'name': 'ja'},
    'झ': {'freq': 277.18, 'type': 'sparśa', 'name': 'jha'},
    'ञ': {'freq': 311.13, 'type': 'nāda', 'name': 'ña'},
    # Retroflex (Gaṇa 3)
    'ट': {'freq': 329.63, 'type': 'sparśa', 'name': 'ṭa'},
    'ठ': {'freq': 349.23, 'type': 'sparśa', 'name': 'ṭha'},
    'ड': {'freq': 392.00, 'type': 'sparśa', 'name': 'ḍa'},
    'ढ': {'freq': 415.30, 'type': 'sparśa', 'name': 'ḍha'},
    'ण': {'freq': 466.16, 'type': 'nāda', 'name': 'ṇa'},
    # Dental (Gaṇa 4)
    'त': {'freq': 493.88, 'type': 'sparśa', 'name': 'ta'},
    'थ': {'freq': 523.25, 'type': 'sparśa', 'name': 'tha'},
    'द': {'freq': 587.33, 'type': 'sparśa', 'name': 'da'},
    'ध': {'freq': 622.25, 'type': 'sparśa', 'name': 'dha'},
    'न': {'freq': 698.46, 'type': 'nāda', 'name': 'na'},
    # Labial (Gaṇa 5)
    'प': {'freq': 739.99, 'type': 'sparśa', 'name': 'pa'},
    'फ': {'freq': 830.61, 'type': 'sparśa', 'name': 'pha'},
    'ब': {'freq': 932.33, 'type': 'sparśa', 'name': 'ba'},
    'भ': {'freq': 987.77, 'type': 'sparśa', 'name': 'bha'},
    'म': {'freq': 1108.73, 'type': 'nāda', 'name': 'ma'},
    # Semi-vowels (Gaṇa 6)
    'य': {'freq': 220.00, 'type': 'antaḥstha', 'name': 'ya'},
    'र': {'freq': 261.63, 'type': 'antaḥstha', 'name': 'ra'},
    'ल': {'freq': 293.66, 'type': 'antaḥstha', 'name': 'la'},
    'व': {'freq': 196.00, 'type': 'antaḥstha', 'name': 'va'},
    # Sibilants (Gaṇa 7)
    'श': {'freq': 349.23, 'type': 'uṣma', 'name': 'śa'},
    'ष': {'freq': 392.00, 'type': 'uṣma', 'name': 'ṣa'},
    'स': {'freq': 440.00, 'type': 'uṣma', 'name': 'sa'},
    # Hāla + retroflex liquid
    'ह': {'freq': 130.81, 'type': 'uṣma', 'name': 'ha'},
    'ऌ': {'freq': 164.81, 'type': 'antaḥstha', 'name': 'ḷa'},
}

# ──────────────────────────────────────────────
# VOWEL TABLE — filter cutoff + resonance
# ──────────────────────────────────────────────
VOWELS = {
    'अ': {'cutoff': 200, 'q': 0.5, 'dur_mult': 0.5},
    'आ': {'cutoff': 250, 'q': 0.6, 'dur_mult': 1.0},
    'इ': {'cutoff': 350, 'q': 0.7, 'dur_mult': 0.5},
    'ई': {'cutoff': 400, 'q': 0.8, 'dur_mult': 1.0},
    'उ': {'cutoff': 300, 'q': 0.6, 'dur_mult': 0.5},
    'ऊ': {'cutoff': 350, 'q': 0.7, 'dur_mult': 1.0},
    'ऋ': {'cutoff': 500, 'q': 0.9, 'dur_mult': 0.5},
    'ए': {'cutoff': 600, 'q': 1.0, 'dur_mult': 0.75},
    'ऐ': {'cutoff': 700, 'q': 1.2, 'dur_mult': 0.75},
    'ओ': {'cutoff': 650, 'q': 1.1, 'dur_mult': 1.0},
    'औ': {'cutoff': 750, 'q': 1.3, 'dur_mult': 1.0},
}

# ──────────────────────────────────────────────
# SPECIAL CHARS — effects
# ──────────────────────────────────────────────
SPECIALS = {
    'ॐ': {'type': 'om'},
    'ः': {'type': 'visarga', 'delay_ms': 300, 'feedback': 0.3, 'count': 3},
    'ं': {'type': 'anusvāra', 'sub_ratio': 0.5, 'gain': 0.4},
    'ँ': {'type': 'chandra', 'res_q': 2.0, 'center': 150},
}

# Inherent अ vowel (hidden in consonant + consonant sequences)
INHERENT_VOWEL = {'cutoff': 200, 'q': 0.5, 'dur_mult': 0.25}

# Matras (vowel signs) — modify the vowel of their base consonant
MATRAS = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ',
          'ृ': 'ऋ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ',
          'ं': 'ं', 'ः': 'ः', 'ँ': 'ँ', '्': None}  # '्' = halant (kills inherent vowel)

# Envelope defaults by consonant type
ENVELOPES = {
    'sparśa':     {'attack': 0.005, 'decay': 0.05, 'sustain': 0.2, 'release': 0.1},
    'nāda':       {'attack': 0.02,  'decay': 0.1,  'sustain': 0.7, 'release': 0.2},
    'antaḥstha':  {'attack': 0.01,  'decay': 0.08, 'sustain': 0.5, 'release': 0.15},
    'uṣma':       {'attack': 0.001, 'decay': 0.02, 'sustain': 0.8, 'release': 0.05},
}


# ──────────────────────────────────────────────
# UTILITY
# ──────────────────────────────────────────────
def write_wav(filepath, fs, signal):
    """Write float32 numpy array as 16-bit mono/stereo WAV."""
    if len(signal.shape) == 1:
        channels = 1
    else:
        channels = signal.shape[0]
    peak = np.max(np.abs(signal))
    if peak > 0:
        signal = signal / peak * 0.85
    s16 = (signal * 32767).astype(np.int16)
    if channels == 2:
        s16 = np.interleave(s16[0], s16[1])
    with wave.open(filepath, "w") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(s16.tobytes())


def lowpass(signal, cutoff, fs):
    """Simple moving-average lowpass."""
    wc = max(1, int(fs / max(cutoff, 30)))
    if wc > 1:
        k = np.ones(wc) / wc
        return np.convolve(signal, k, mode="same")
    return signal


def adsr_envelope(fs, duration, attack, decay, sustain_level, release):
    """Generate ADSR envelope as numpy array."""
    n = max(1, int(fs * duration))
    na = min(max(1, int(fs * attack)), n // 4)
    nd = min(max(1, int(fs * decay)), (n - na) // 3)
    nr = min(max(1, int(fs * release)), (n - na - nd) // 2)
    ns = max(1, n - na - nd - nr)
    env = np.zeros(n)
    env[:na] = np.linspace(0, 1, na)
    if nd > 0 and ns > 0:
        end_d = min(na + nd, n)
        env[na:end_d] = np.linspace(1, sustain_level, end_d - na)
        env[end_d:end_d + ns] = sustain_level
    start_r = n - nr
    if start_r >= na + nd and nr > 0:
        release_len = min(nr, n - start_r)
        if release_len > 0:
            env[start_r:start_r + release_len] = np.linspace(
                sustain_level if start_r >= na + nd else 1, 0, release_len
            )
    return env[:n]


def sine_burst(fs, freq, duration, waveform='sine'):
    """Generate a single-frequency burst."""
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    if waveform == 'sine':
        return np.sin(2 * np.pi * freq * t)
    elif waveform == 'triangle':
        return 2 * np.abs(2 * (freq * t - np.floor(freq * t + 0.5))) - 1
    elif waveform == 'square':
        return np.sign(np.sin(2 * np.pi * freq * t))
    return np.sin(2 * np.pi * freq * t)


# ──────────────────────────────────────────────
# PHONEME TOKENIZER
# ──────────────────────────────────────────────
def tokenize(text):
    """
    Tokenize Devanagari into phoneme units.
    Handles matras (vowel signs), conjuncts (halant), and special chars.
    Returns list of dicts with phoneme info.
    """
    phonemes = []
    i = 0
    chars = list(text)

    while i < len(chars):
        ch = chars[i]

        # Special: Om
        if ch in SPECIALS:
            phonemes.append({
                'char': ch,
                'kind': 'special',
                'data': SPECIALS[ch],
            })
            i += 1
            continue

        # Vowel (standalone)
        if ch in VOWELS:
            phonemes.append({
                'char': ch,
                'kind': 'vowel',
                'data': VOWELS[ch],
            })
            i += 1
            continue

        # Consonant (possibly with matra)
        if ch in CONSONANTS:
            cons = CONSONANTS[ch]
            vowel = INHERENT_VOWEL  # default inherent अ
            halant = False

            # Look ahead for matra or halant
            if i + 1 < len(chars):
                next_ch = chars[i + 1]
                if next_ch == '्':
                    halant = True  # kill inherent vowel
                    i += 1
                    # Look further for matra after halant
                    if i + 1 < len(chars) and chars[i + 1] in MATRAS:
                        mv = MATRAS[chars[i + 1]]
                        if mv is not None and mv in VOWELS:
                            vowel = VOWELS[mv]
                            i += 1
                        elif mv is None:
                            pass  # matra without vowel
                        else:
                            i += 1
                        continue
                    # Halant at end or before consonant = conjunct
                    continue
                elif next_ch in MATRAS:
                    mv = MATRAS[next_ch]
                    if mv is not None and mv in VOWELS:
                        vowel = VOWELS[mv]
                        i += 2
                        phonemes.append({
                            'char': ch + next_ch,
                            'kind': 'consonant_vowel',
                            'consonant': cons,
                            'vowel': vowel,
                        })
                        continue
                    elif mv is None:
                        i += 2
                        continue  # conjunct, skip
                    else:
                        i += 1
                        continue

            phonemes.append({
                'char': ch,
                'kind': 'consonant_vowel',
                'consonant': cons,
                'vowel': vowel if not halant else None,
            })
            i += 1
            continue

        # Skip whitespace / unknown
        i += 1

    return phonemes


# ──────────────────────────────────────────────
# MAP — phoneme → JSON params
# ──────────────────────────────────────────────
def map_phonemes(text, base_hz=55):
    """Map Devanagari text to frequency parameter JSON."""
    tokens = tokenize(text)
    result = []
    for tok in tokens:
        entry = {'char': tok['char']}
        if tok['kind'] == 'special':
            entry['type'] = tok['data'].get('type', 'special')
            if tok['data'].get('type') == 'om':
                entry['freq'] = base_hz
                entry['sub_freq'] = base_hz * 0.5
                entry['cutoff'] = {'sweep': [200, 800]}
                entry['q'] = 1.0
                entry['env'] = {'attack': 2.0, 'sustain': 1.0, 'release': 3.0}
            elif tok['data'].get('type') == 'visarga':
                entry['effect'] = 'delay'
                entry['effect_params'] = {k: v for k, v in tok['data'].items() if k != 'type'}
            elif tok['data'].get('type') == 'anusvāra':
                entry['effect'] = 'sub_bass'
                entry['effect_params'] = {k: v for k, v in tok['data'].items() if k != 'type'}
            elif tok['data'].get('type') == 'chandra':
                entry['effect'] = 'resonance_peak'
                entry['effect_params'] = {k: v for k, v in tok['data'].items() if k != 'type'}
        elif tok['kind'] == 'consonant_vowel':
            cons = tok['consonant']
            entry['freq'] = cons['freq']
            entry['consonant_type'] = cons['type']
            entry['name'] = cons['name']
            env = ENVELOPES.get(cons['type'], ENVELOPES['sparśa'])
            entry['env'] = env
            if tok.get('vowel'):
                v = tok['vowel']
                entry['cutoff'] = v['cutoff']
                entry['q'] = v['q']
                entry['dur_mult'] = v['dur_mult']
            else:
                entry['cutoff'] = 400
                entry['q'] = 0.5
                entry['dur_mult'] = 0.25
        elif tok['kind'] == 'vowel':
            v = tok['data']
            entry['cutoff'] = v['cutoff']
            entry['q'] = v['q']
            entry['dur_mult'] = v['dur_mult']
            entry['freq'] = base_hz  # vowels alone use base freq drone
        result.append(entry)
    return result


# ──────────────────────────────────────────────
# SYNTH — phoneme params → audio
# ──────────────────────────────────────────────
def synthesize(params, duration_per_char=0.5, base_hz=55,
               waveform='sine', fs=44100, stereo=False):
    """
    Synthesize audio from phoneme parameter list.
    Returns numpy array of audio signal.
    """
    total_duration = sum(
        p.get('dur_mult', 0.5) * duration_per_char
        if p.get('type') != 'om' and 'env' in p
        else (5.0 if p.get('type') == 'om' else 0.5)
        for p in params
    )
    if total_duration < 0.5:
        total_duration = 0.5
    total_duration = round(total_duration, 1)

    t_full = np.linspace(0, total_duration, int(fs * total_duration), endpoint=False)
    signal = np.zeros_like(t_full)
    pos = 0

    for p in params:
        pt = 0
        if p.get('type') == 'om':
            # Om: full spectrum treatment
            om_dur = duration_per_char * 3
            om_env = adsr_envelope(fs, om_dur,
                                   attack=min(2.0, om_dur * 0.3),
                                   decay=om_dur * 0.2,
                                   sustain_level=0.9,
                                   release=min(1.5, om_dur * 0.3))
            n = int(fs * om_dur)

            # Main oscillator at 55 Hz
            osc = sine_burst(fs, base_hz, om_dur, waveform) * om_env

            # Sub-bass at 27.5 Hz
            sub = sine_burst(fs, base_hz * 0.5, om_dur, waveform) * om_env * 0.4

            # Filter sweep oscillator
            sweep_freq = base_hz * 2
            osc2 = sine_burst(fs, sweep_freq, om_dur, waveform) * om_env * 0.3

            om_signal = (osc + sub + osc2)
            end = min(pos + n, len(signal))
            if end > pos:
                signal[pos:end] += om_signal[:end - pos]
            pos += n
            continue

        if p.get('type') in ('visarga', 'anusvāra', 'chandra'):
            continue  # effects applied post-synthesis

        # Regular phoneme
        freq = p.get('freq', base_hz)
        dur = p.get('dur_mult', 0.5) * duration_per_char
        env_p = p.get('env', ENVELOPES['sparśa'])
        env = adsr_envelope(fs, dur,
                            attack=env_p.get('attack', 0.01),
                            decay=env_p.get('decay', 0.05),
                            sustain_level=env_p.get('sustain', 0.5),
                            release=env_p.get('release', 0.1))
        n = int(fs * dur)

        osc = sine_burst(fs, freq, dur, waveform) * env

        # Apply filter
        cutoff = p.get('cutoff', 400)
        osc = lowpass(osc, cutoff, fs)

        end = min(pos + n, len(signal))
        if end > pos:
            signal[pos:end] += osc[:end - pos]
        pos += n

    # Post-synthesis effects
    for p in params:
        if p.get('type') == 'visarga':
            ep = p.get('effect_params', {})
            dt = int(ep.get('delay_ms', 300) / 1000 * fs)
            fb = ep.get('feedback', 0.3)
            count = ep.get('count', 3)
            for i in range(1, count + 1):
                if i * dt < len(signal):
                    delay_sig = signal[:len(signal) - i * dt] * fb ** i
                    signal[i * dt:] += delay_sig[:len(signal) - i * dt]
        elif p.get('type') == 'anusvāra':
            ep = p.get('effect_params', {})
            sub_ratio = ep.get('sub_ratio', 0.5)
            gain = ep.get('gain', 0.4)
            t_sub = np.linspace(0, total_duration, len(signal), endpoint=False)
            sub = np.sin(2 * np.pi * base_hz * sub_ratio * t_sub) * gain * 0.3
            signal += sub

    return signal


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Sanskrit Frequency Bridge")
    subparsers = parser.add_subparsers(dest="action")

    # synth
    sp_synth = subparsers.add_parser("synth")
    sp_synth.add_argument("--text", required=True, help="Devanagari text")
    sp_synth.add_argument("--duration", type=float, default=0.5, help="Seconds per character")
    sp_synth.add_argument("--output", default=None, help="Output WAV path")
    sp_synth.add_argument("--base-hz", type=float, default=55, help="Base frequency (Om)")
    sp_synth.add_argument("--waveform", default="sine", choices=["sine", "triangle", "square"])
    sp_synth.add_argument("--stereo", action="store_true")

    # map
    sp_map = subparsers.add_parser("map")
    sp_map.add_argument("--text", required=True, help="Devanagari text")
    sp_map.add_argument("--base-hz", type=float, default=55)

    # chain
    sp_chain = subparsers.add_parser("chain")
    sp_chain.add_argument("--text", required=True, help="Devanagari text")
    sp_chain.add_argument("--duration", type=float, default=0.5)
    sp_chain.add_argument("--output", default=None)
    sp_chain.add_argument("--base-hz", type=float, default=55)
    sp_chain.add_argument("--waveform", default="sine", choices=["sine", "triangle", "square"])

    args = parser.parse_args()

    if args.action == "map":
        params = map_phonemes(args.text, base_hz=args.base_hz)
        print(json.dumps(params, indent=2, ensure_ascii=False))

    elif args.action == "synth":
        params = map_phonemes(args.text, base_hz=args.base_hz)
        signal = synthesize(params,
                            duration_per_char=args.duration,
                            base_hz=args.base_hz,
                            waveform=args.waveform)
        output_dir = "/home/claw/.openclaw/workspace/MEDIA"
        os.makedirs(output_dir, exist_ok=True)
        if not args.output:
            rid = f"{random.randint(0x10000, 0xFFFFF):05x}"
            args.output = os.path.join(output_dir, f"sanskrit-bridge-{rid}.wav")
        write_wav(args.output, 44100, signal)
        print(json.dumps({
            "success": True,
            "output_path": args.output,
            "duration_sec": round(len(signal) / 44100, 1),
            "sample_rate": 44100,
            "phonemes": len(params),
            "text": args.text,
        }, ensure_ascii=False))

    elif args.action == "chain":
        params = map_phonemes(args.text, base_hz=args.base_hz)
        print(json.dumps({"mapping": params}, indent=2, ensure_ascii=False))
        signal = synthesize(params,
                            duration_per_char=args.duration,
                            base_hz=args.base_hz,
                            waveform=args.waveform)
        output_dir = "/home/claw/.openclaw/workspace/MEDIA"
        os.makedirs(output_dir, exist_ok=True)
        outp = args.output or os.path.join(output_dir, f"sanskrit-bridge-chain-{random.randint(0x10000, 0xFFFFF):05x}.wav")
        write_wav(outp, 44100, signal)
        print(json.dumps({
            "success": True,
            "output_path": outp,
            "duration_sec": round(len(signal) / 44100, 1),
            "phonemes": len(params),
        }, ensure_ascii=False))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
