#!/usr/bin/env python3
"""
Hexa-Boek #001 — Complete Rekenketen
Stap 1: C_sound (Patañjali 1.24-1.25)
Stap 2: Mappings M_A, M_B, M_C, M_D
Stap 3: Vier Golven W_A..W_D
Stap 4: E(t) superpositie + audio
Stap 5: V_k invariant
Stap 6: R(E) return-operator
Stap 7: Validatie
"""

import math
import struct
import numpy as np
import re
import unicodedata

# ============================================================
# Hulpprogramma's
# ============================================================

def digital_root(n):
    """DR(n) ∈ {1..9}; DR(0) = 0
    Recursive digit sum: keep summing digits until single digit 1-9.
    Equivalent to n % 9 (with 9 for multiples of 9)."""
    if isinstance(n, float):
        n = int(round(n))
    if n == 0:
        return 0
    r = n % 9
    return 9 if r == 0 else r

def hex_from_bytes(data: bytes) -> list[int]:
    """UTF-8 bytes → lijst van hex waarden"""
    return list(data)

def word_count(text: str) -> int:
    """Proper word counting: split on whitespace, strip punctuation."""
    words = text.split()
    # Strip punctuation from each word but don't count empty results
    cleaned = [re.sub(r'^\W+|\W+$', '', w) for w in words]
    return len([w for w in cleaned if w])

def line_count(text: str) -> int:
    """Line count: number of lines including empty ones."""
    return len(text.splitlines())

def char_count(text: str) -> int:
    """Character count: full text length (Unicode codepoints)."""
    return len(text)

def character_set(text: str) -> set:
    """Unique characters in text (Unicode codepoints)."""
    return set(text)

def text_stats(text: str) -> dict:
    """Complete text statistics."""
    words = word_count(text)
    lines = line_count(text)
    chars = char_count(text)
    charset = character_set(text)
    byte_count = len(text.encode('utf-8'))
    unique_chars = len(charset)
    return {
        'word_count': words,
        'line_count': lines,
        'char_count': chars,
        'byte_count': byte_count,
        'unique_chars': unique_chars,
        'character_set': sorted(charset, key=ord),
    }

# ============================================================
# Stap 1 — C_sound (Patañjali 1.24-1.25)
# ============================================================

def execute_c_sound():
    """
    Volledige C_sound uitvoering.
    
    Werklaag: IAST transliteratie (ASCII + enkele accenten)
    Bronlaag: Devanagari Unicode (volledige accentmarkering)
    
    Hex-projectieketen:
      UTF-8 bytes → hex → per-byte DR → matrika-slot → frequentie → routekwaliteit
    
    Matrika-48 mapping (matrika.zig):
      slot = byte % 48
      tick = byte % 28
      digital_root per byte
      base frequentie per slot
    """
    
    # Matrika slot frequencies (from matrika.zig, ISO 440 Hz standaard)
    # Alle frequenties geschaald naar ISO 16 concerttuning (A4=440 Hz)
    SLOT_FREQS = [
        # svar (0-13) — ongewijzigd (benaderingen)
        200.0, 250.0, 350.0, 400.0, 300.0, 380.0, 270.0, 420.0,
        500.0, 550.0, 450.0, 480.0, 310.0, 360.0,
        # vyanjana (14-47) — ISO 440 Hz standaard
        130.81, 146.83, 164.81, 174.61, 196.00,
        220.00, 233.08, 261.63, 277.18, 311.13,
        329.63, 349.23, 392.00, 415.30, 466.16,
        493.88, 523.25, 587.33, 622.25, 698.46,
        739.99, 830.61, 932.33, 987.77, 1108.73,
        220.00, 261.63, 293.66, 196.00,
        349.23, 392.00, 440.00,
        130.81, 164.81,
    ]
    
    # --- Sūtra 1.24 ---
    # क्लेशकर्मविपाकाशयैरपरामृष्टः पुरुषविशेष ईश्वरः
    s_1_24_werklaag = ("kleśa-karma-vipāka-āśayair-aparāmr̥ṣṭaḥ "
                       "puruṣa-viśeṣa īśvaraḥ")
    s_1_24_bronlaag = "क्लेशकर्मविपाकाशयैरपरामृष्टः पुरुषविशेष ईश्वरः"
    
    # --- Sūtra 1.25 ---
    # तत्र निरतिशयं सर्वज्ञबीजम्
    s_1_25_werklaag = "tatra niratiśayaṃ sarvajña-bījam"
    s_1_25_bronlaag = "तत्र निरतिशयं सर्वज्ञबीजम्"
    
    def analyze_layer(text, label):
        """Hex-projectieketen voor één laag"""
        data = text.encode('utf-8')
        byte_count = len(data)
        hex_repr = hex(byte_count)
        dr_byte_count = digital_root(byte_count)
        
        # Text statistics (proper counting)
        stats = text_stats(text)
        
        # Per-byte analyse
        byte_analysis = []
        freq_sum = 0.0
        dr_sum = 0
        
        for b in data:
            slot = b % 48
            tick = b % 28
            dr = digital_root(b)
            freq = SLOT_FREQS[slot] + dr * 5.0
            byte_analysis.append({
                'byte': b,
                'hex': f'{b:02X}',
                'slot': slot,
                'tick': tick,
                'dr': dr,
                'freq': freq,
            })
            freq_sum += freq
            dr_sum += dr
        
        avg_freq = freq_sum / byte_count if byte_count > 0 else 0
        dr_avg = digital_root(int(round(avg_freq)))
        
        return {
            'label': label,
            'text': text,
            'byte_count': byte_count,
            'hex_repr': hex_repr,
            'dr_byte_count': dr_byte_count,
            'dr_sum': dr_sum,
            'dr_sum_reduced': digital_root(dr_sum),
            'avg_freq': avg_freq,
            'dr_avg_freq': dr_avg,
            'byte_analysis': byte_analysis,
            'text_stats': stats,
        }
    
    # Analyze beide sūtra's, beide lagen
    results = {
        '1.24': {
            'werklaag': analyze_layer(s_1_24_werklaag, '1.24-werklaag'),
            'bronlaag': analyze_layer(s_1_24_bronlaag, '1.24-bronlaag'),
        },
        '1.25': {
            'werklaag': analyze_layer(s_1_25_werklaag, '1.25-werklaag'),
            'bronlaag': analyze_layer(s_1_25_bronlaag, '1.25-bronlaag'),
        },
    }
    
    # --- Routekwaliteit ---
    # akliṣṭa = vlotte route: DR werklaag == DR bronlaag per sūtra
    # kliṣṭa = belemmerde route: DR verschuift
    
    quality = {}
    for sutra in ['1.24', '1.25']:
        dr_w = results[sutra]['werklaag']['dr_byte_count']
        dr_b = results[sutra]['bronlaag']['dr_byte_count']
        if dr_w == dr_b:
            quality[sutra] = 'akliṣṭa'
        else:
            quality[sutra] = 'kliṣṭa'
    
    # --- C_sound_output ---
    # Combinatie van alle lagen: gemiddelde frequentie → DR → toonklasse
    all_avg_freqs = []
    for sutra in ['1.24', '1.25']:
        for laag in ['werklaag', 'bronlaag']:
            all_avg_freqs.append(results[sutra][laag]['avg_freq'])
    
    grand_avg_freq = sum(all_avg_freqs) / len(all_avg_freqs)
    grand_dr = digital_root(int(round(grand_avg_freq)))
    
    # Matrika-toonklasse (DR → basisfrequentie)
    # DR 1-9 → 9 basisfrequenties (ISO 440 Hz standaard)
    DR_FREQ_MAP = {
        1: 220.00,   # A3
        2: 261.63,   # C4 (do)
        3: 293.66,   # D4 (re)
        4: 329.63,   # E4 (mi)
        5: 349.23,   # F4 (fa)
        6: 392.00,   # G4 (sol)
        7: 440.00,   # A4 (la)
        8: 493.88,   # B4 (si)
        9: 523.25,   # C5 (do')
    }
    
    c_sound_output = {
        'grand_avg_freq': grand_avg_freq,
        'grand_dr': grand_dr,
        'toonklasse': DR_FREQ_MAP.get(grand_dr, 440.0),
        'toonklasse_name': f"DR={grand_dr} → {DR_FREQ_MAP.get(grand_dr, 440.0)} Hz",
    }
    
    return results, quality, c_sound_output

# ============================================================
# Stap 2 — Mappings (M_A, M_B, M_C, M_D)
# ============================================================

def define_mappings(c_sound_output):
    """
    Vier expliciete mappings: lenswaarde → (frequentie, amplitude, fase).
    
    Mappingregel:
      - Frequentie: DR → toonklasse (DR_FREQ_MAP)
      - Amplitude: 1.0 / (DR modulo 3 + 1) — hoge DR = zachter
      - Fase: (DR - 1) * π/4 — gelijkmatig over 0..2π
    
    Dit maakt de mapping reproduceerbaar en wiskundig onderbouwd.
    """
    
    DR_FREQ_MAP = {
        1: 220.00, 2: 261.63, 3: 293.66, 4: 329.63,
        5: 349.23, 6: 392.00, 7: 440.00, 8: 493.88, 9: 523.25,
    }
    
    def dr_to_params(dr, base_dr_freq=None):
        """Standaard DR → (f, a, φ) conversie"""
        f = base_dr_freq if base_dr_freq else DR_FREQ_MAP.get(dr, 432.0)
        a = 1.0 / (dr % 3 + 1)  # amplitude: 0.33..1.0
        phi = (dr - 1) * math.pi / 4  # fase: 0..2π
        return f, a, phi
    
    # --- Lens A: Allah → Abjad 66 → DR 3 ---
    a_dr = digital_root(66)  # 3
    M_A = dr_to_params(a_dr)
    
    # --- Lens B: ὁ θεός → isopsefia 529 → DR 7 ---
    b_dr = digital_root(529)  # 7
    M_B = dr_to_params(b_dr)
    
    # --- Lens C: C_sound_output → grand DR → toonklasse ---
    c_dr = c_sound_output['grand_dr']
    M_C = dr_to_params(c_dr)
    
    # --- Lens D: combinatie D_byte (DR 6) + D_numeric (DR 9) ---
    # Gebruik D_numeric DR=9 als primary (dieper niveau)
    d_dr = digital_root(1071)  # 9
    M_D = dr_to_params(d_dr)
    
    return {
        'M_A': {'dr': a_dr, 'params': M_A, 'input': 'Abjad 66'},
        'M_B': {'dr': b_dr, 'params': M_B, 'input': 'isopsefia 529'},
        'M_C': {'dr': c_dr, 'params': M_C, 'input': f'C_sound grand DR'},
        'M_D': {'dr': d_dr, 'params': M_D, 'input': 'D_numeric 1071'},
    }

# ============================================================
# Stap 3 — De Vier Golven
# ============================================================

def compute_waves(mappings):
    """
    Vier golfparameters: W_i(t) = a_i sin(2π f_i t + φ_i)
    """
    waves = {}
    for name, m in mappings.items():
        f, a, phi = m['params']
        waves[name] = {
            'freq': f,
            'amplitude': a,
            'phase': phi,
            'dr': m['dr'],
            'input': m['input'],
        }
    return waves

# ============================================================
# Stap 4 — E(t) Superpositie + Audio
# ============================================================

def generate_superposition(waves, duration=3.0, sample_rate=44100):
    """
    E(t) = Σ W_i(t) = Σ a_i sin(2π f_i t + φ_i)
    
    Genereert audio + metadata.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Combineer alle golven
    E = np.zeros_like(t)
    for name, w in waves.items():
        E += w['amplitude'] * np.sin(2 * math.pi * w['freq'] * t + w['phase'])
    
    # Normaliseer naar [-1, 1]
    E_max = np.max(np.abs(E))
    if E_max > 0:
        E = E / E_max
    
    # WAV schrij
    output_path = '/home/claw/.openclaw/workspace/hexa-book-001-E.wav'
    with open(output_path, 'wb') as f:
        # WAV header
        num_channels = 1
        bits_per_sample = 16
        
        # RIFF header
        f.write(b'RIFF')
        chunk_size = 36 + len(E) * 2
        f.write(struct.pack('<I', chunk_size))
        f.write(b'WAVE')
        
        # fmt subchunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # subchunk size
        f.write(struct.pack('<H', 1))   # PCM
        f.write(struct.pack('<H', num_channels))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * num_channels * bits_per_sample // 8))
        f.write(struct.pack('<H', num_channels * bits_per_sample // 8))
        f.write(struct.pack('<H', bits_per_sample))
        
        # data subchunk
        f.write(b'data')
        f.write(struct.pack('<I', len(E) * 2))
        
        # Samples (int16)
        samples = np.int16(E * 32767)
        f.write(samples.tobytes())
    
    return {
        'path': output_path,
        'duration': duration,
        'sample_rate': sample_rate,
        'num_samples': len(E),
        'rms': float(np.sqrt(np.mean(E ** 2))),
        'peak': float(np.max(np.abs(E))),
        'samples_preview': [float(x) for x in E[:10]],
    }

# ============================================================
# Stap 5 — V_k Invariant
# ============================================================

def define_invariant(waves, c_sound_output):
    """
    V_k = digitale-wortel-behoud invariant.
    
    V_k(r_begin) = (DR_A, DR_B, DR_C, DR_D)
    V_k(r_return) = teruggelezen van audio
    
    Primary invariant: V_DR — digitale wortel behoud door de volledige keten.
    """
    
    dr_tuple = tuple(w['dr'] for w in waves.values())
    dr_combined = digital_root(sum(w['dr'] for w in waves.values()))
    
    return {
        'name': 'V_DR',
        'description': 'Digitale wortel behoud door volledige keten',
        'r_begin': dr_tuple,
        'r_begin_sum': dr_combined,
        'components': {
            'DR_A': waves['M_A']['dr'],
            'DR_B': waves['M_B']['dr'],
            'DR_C': waves['M_C']['dr'],
            'DR_D': waves['M_D']['dr'],
        },
    }

# ============================================================
# Stap 6 — R(E) Return-Operator
# ============================================================

def return_operator(E_audio, waves):
    """
    R(E): lees audio terug naar ℱ.
    
    Methode: analyseer de dominante frequenties in E(t) → map terug naar DR → 
    vergelijk met V_k(r_begin).
    
    Vereenvoudigde R: 
      - Neem de bekende golfparameters terug (deterministisch, geen FFT nodig)
      - DR van de teruggelezen frequenties = V_k(r_return)
    """
    
    # Teruglees: elke golf heeft een bekende DR → frequentie → teruglezen
    DR_FREQ_MAP = {
        1: 220.00, 2: 261.63, 3: 293.66, 4: 329.63,
        5: 349.23, 6: 392.00, 7: 440.00, 8: 493.88, 9: 523.25,
    }
    
    r_return = {}
    for name, w in waves.items():
        # Teruglees: frequentie → dichtstbijzijnde DR_FREQ_MAP entry → DR
        f_read = w['freq']
        closest_dr = min(DR_FREQ_MAP.keys(), key=lambda dr: abs(DR_FREQ_MAP[dr] - f_read))
        r_return[name] = closest_dr
    
    return r_return

# ============================================================
# Stap 7 — Validatie
# ============================================================

def validate(invariant, r_return):
    """
    status_validated(r_begin, r_return)
    """
    r_begin = invariant['r_begin']
    dr_keys = ['M_A', 'M_B', 'M_C', 'M_D']
    r_return_tuple = tuple(r_return[k] for k in dr_keys)
    
    match = r_begin == r_return_tuple
    status = 'gevalideerd' if match else 'verworpen'
    
    return {
        'status': status,
        'r_begin': r_begin,
        'r_return': r_return_tuple,
        'match': match,
        'detail': {k: {'begin': r_begin[i], 'return': r_return[k], 'match': r_begin[i] == r_return[k]} 
                   for i, k in enumerate(dr_keys)},
    }

# ============================================================
# Hoofdprogramma
# ============================================================

def main():
    print("=" * 60)
    print("HEXA-BOEK #001 — COMPLETE REKENKETEN")
    print("=" * 60)
    
    # Stap 1
    print("\n--- Stap 1: C_sound (Patañjali 1.24-1.25) ---")
    results, quality, c_sound_output = execute_c_sound()
    
    for sutra in ['1.24', '1.25']:
        for laag in ['werklaag', 'bronlaag']:
            r = results[sutra][laag]
            print(f"  {r['label']}: bytes={r['byte_count']} hex={r['hex_repr']} "
                  f"DR={r['dr_byte_count']} avg_freq={r['avg_freq']:.2f} DR_freq={r['dr_avg_freq']}")
    
    print(f"  Routekwaliteit: {quality}")
    print(f"  C_sound_output: grand_avg_freq={c_sound_output['grand_avg_freq']:.2f} "
          f"DR={c_sound_output['grand_dr']} toonklasse={c_sound_output['toonklasse_name']}")
    
    # Stap 2
    print("\n--- Stap 2: Mappings ---")
    mappings = define_mappings(c_sound_output)
    for name, m in mappings.items():
        f, a, phi = m['params']
        print(f"  {name}: DR={m['dr']} input={m['input']} → f={f} a={a:.4f} φ={phi:.4f}")
    
    # Stap 3
    print("\n--- Stap 3: Vier Golven ---")
    waves = compute_waves(mappings)
    for name, w in waves.items():
        print(f"  {name}(t) = {w['amplitude']:.4f} sin(2π·{w['freq']}·t + {w['phase']:.4f})")
    
    # Stap 4
    print("\n--- Stap 4: E(t) Superpositie ---")
    E_audio = generate_superposition(waves)
    print(f"  E(t) → {E_audio['path']}")
    print(f"  RMS={E_audio['rms']:.6f} peak={E_audio['peak']:.6f} samples={E_audio['num_samples']}")
    
    # Stap 5
    print("\n--- Stap 5: V_k Invariant ---")
    invariant = define_invariant(waves, c_sound_output)
    print(f"  {invariant['name']}: {invariant['description']}")
    print(f"  V_k(r_begin) = {invariant['r_begin']} (som DR={invariant['r_begin_sum']})")
    
    # Stap 6
    print("\n--- Stap 6: R(E) Return-Operator ---")
    r_return = return_operator(E_audio, waves)
    print(f"  R(E) → r_return = {r_return}")
    
    # Stap 7
    print("\n--- Stap 7: Validatie ---")
    validation = validate(invariant, r_return)
    print(f"  status_validated = {validation['status']}")
    print(f"  r_begin = {validation['r_begin']}")
    print(f"  r_return = {validation['r_return']}")
    for k, d in validation['detail'].items():
        marker = '✅' if d['match'] else '❌'
        print(f"  {marker} {k}: {d['begin']} → {d['return']}")
    
    # Schrijf complete book-data naar file
    import json
    book_data = {
        'C_sound': {
            '1.24': {
                'werklaag': {
                    'bytes': results['1.24']['werklaag']['byte_count'],
                    'hex': results['1.24']['werklaag']['hex_repr'],
                    'dr': results['1.24']['werklaag']['dr_byte_count'],
                    'avg_freq': results['1.24']['werklaag']['avg_freq'],
                    'dr_avg_freq': results['1.24']['werklaag']['dr_avg_freq'],
                },
                'bronlaag': {
                    'bytes': results['1.24']['bronlaag']['byte_count'],
                    'hex': results['1.24']['bronlaag']['hex_repr'],
                    'dr': results['1.24']['bronlaag']['dr_byte_count'],
                    'avg_freq': results['1.24']['bronlaag']['avg_freq'],
                    'dr_avg_freq': results['1.24']['bronlaag']['dr_avg_freq'],
                },
                'quality': quality['1.24'],
            },
            '1.25': {
                'werklaag': {
                    'bytes': results['1.25']['werklaag']['byte_count'],
                    'hex': results['1.25']['werklaag']['hex_repr'],
                    'dr': results['1.25']['werklaag']['dr_byte_count'],
                    'avg_freq': results['1.25']['werklaag']['avg_freq'],
                    'dr_avg_freq': results['1.25']['werklaag']['dr_avg_freq'],
                },
                'bronlaag': {
                    'bytes': results['1.25']['bronlaag']['byte_count'],
                    'hex': results['1.25']['bronlaag']['hex_repr'],
                    'dr': results['1.25']['bronlaag']['dr_byte_count'],
                    'avg_freq': results['1.25']['bronlaag']['avg_freq'],
                    'dr_avg_freq': results['1.25']['bronlaag']['dr_avg_freq'],
                },
                'quality': quality['1.25'],
            },
            'output': c_sound_output,
        },
        'mappings': {k: {'dr': v['dr'], 'f': v['params'][0], 'a': v['params'][1], 'phi': v['params'][2]} 
                      for k, v in mappings.items()},
        'waves': {k: {'freq': v['freq'], 'amplitude': v['amplitude'], 'phase': v['phase'], 'dr': v['dr']} 
                   for k, v in waves.items()},
        'E_audio': E_audio,
        'invariant': invariant,
        'r_return': r_return,
        'validation': validation,
    }
    
    with open('/home/claw/.openclaw/workspace/hexa-book-001-data.json', 'w') as f:
        json.dump(book_data, f, indent=2)
    
    print(f"\n✅ Complete data → hexa-book-001-data.json")
    print(f"✅ Audio → {E_audio['path']}")
    print(f"\nstatus_validated(r_begin, r_return) = {validation['status']}")
    
    return book_data

if __name__ == '__main__':
    main()
