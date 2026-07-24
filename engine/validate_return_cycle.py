#!/usr/bin/env python3
"""
validate_return_cycle.py — Onafhankelijke validatie Route 1a + ReturnCycle.
Test multiple invoeren met assertions; draait niet alleen voor hardcoded 432.
"""

import sys

# === hex_to_phoneme: Gaṇa-kaart (16-posities) ===
GANA_MAP = {
    '0': ('a',     'vowel',       432),
    '1': ('ka',    'vr̥ṣṭi',      55),
    '2': ('kha',   'vr̥ṣṭi',      110),
    '3': ('ga',    'vr̥ṣṭi',      165),
    '4': ('gha',   'vr̥ṣṭi',      220),
    '5': ('ṅa',    'vr̥ṣṭi',      275),
    '6': ('ca',    'mūrdhanya',   330),
    '7': ('cha',   'mūrdhanya',   385),
    '8': ('ja',    'mūrdhanya',   440),
    '9': ('jha',   'mūrdhanya',   495),
    'A': ('ṇa',    'mūrdhanya',   550),
    'B': ('ṭa',    'antaḥstha',   605),
    'C': ('ṭha',   'antaḥstha',   660),
    'D': ('ḍa',    'antaḥstha',   715),
    'E': ('ḍha',   'antaḥstha',   770),
    'F': ('ṇa',    'antaḥstha',   825),
}


def dr(n):
    """Digital root — cijfer-som zonder decimaal punt."""
    s = str(n).replace('.', '').replace('-', '')
    while len(s) > 1:
        s = str(sum(int(c) for c in s))
    return int(s)


# === Forward operators ===
def byte_to_freq(B, ref_bytes, base=432.0):
    """Model A: globale referentie.
    
    base = 432.0 (Vedic, default) of 396.0 (Flower of Life).
    """
    return base * B / ref_bytes


def hex_avg_freq(byte_val):
    """Byte → hex → gemiddelde frequentie van beide hex-cijfers."""
    hex_str = format(byte_val, '02X')
    freqs = [GANA_MAP[h][2] for h in hex_str.upper()]
    return sum(freqs) / len(freqs)


# === ReturnCycle operators ===
def R_prime(centroid):
    """R': ℱ → ReturnSeed (centroid-extractie).
    
    Verwacht: centroid is float (spectral_centroid van fractaalveld).
    Retourneert: seed frequentie (dezelfde float; R' = extractie, niet transformatie).
    """
    assert isinstance(centroid, (int, float)), f"R': centroid moet numeriek zijn, got {type(centroid)}"
    assert centroid > 0, f"R': centroid moet positief zijn, got {centroid}"
    return float(centroid)


def E_prime(seed_freq):
    """E': ReturnSeed → Signal (single-tone reconstructie).
    
    Verwacht: seed_freq van R'.
    Retourneert: signaal-frequentie (identiek; E' = reconstructie, geen extra transformatie).
    """
    assert isinstance(seed_freq, (int, float)), f"E': seed_freq moet numeriek zijn"
    assert seed_freq > 0, f"E': seed_freq moet positief zijn"
    return float(seed_freq)


def C_prime(seed_freq, ref_bytes, base=432.0):
    """C': Signal → CInput (byte_to_freq inverse).
    
    Inverse van byte_to_freq(B, ref, base) = base * B / ref
    Dus: B' = seed_freq * ref / base
    
    Verwacht: seed_freq van E', ref_bytes (globale referentie).
    Retourneert: bytes (C'-input).
    """
    assert seed_freq > 0, f"C': seed_freq moet positief zijn"
    assert ref_bytes > 0, f"C': ref_bytes moet positief zijn"
    assert base > 0, f"C': base moet positief zijn"
    return seed_freq * ref_bytes / base


def return_cycle(centroid, ref_bytes, base=432.0):
    """Volledige returnketen: ℱ → R' → E' → C'."""
    r = R_prime(centroid)
    e = E_prime(r)
    c = C_prime(e, ref_bytes, base)
    return r, e, c


# === Return Projection Operator ===
def return_projection(component_centroid, dr_signature):
    """ρ_ℱ: ReturnProjectionInput → ℱ (fractal field projection).
    
    Projects a subset of R_raw(E_raw) into a 2D fractal field ℱ.
    Uses only component_centroid and DR_signature, not the full AudioFeatureSpace.
    
    Args:
        component_centroid: float > 0 (ComponentCentroid from R_raw)
        dr_signature: tuple of ints, each in [1,9] (DRSignature from R_raw)
    
    Returns:
        tuple[int, int]: ℱ = (DR(round(centroid)), DR(sum(dr_signature)))
    
    Raises:
        TypeError: if centroid is not numeric or signature is not tuple of ints
        ValueError: if centroid ≤ 0, signature empty, or any DR not in [1,9]
    """
    # Type checks
    if not isinstance(component_centroid, (int, float)):
        raise TypeError(
            f"component_centroid must be numeric, got {type(component_centroid).__name__}"
        )
    if not isinstance(dr_signature, (tuple, list)):
        raise TypeError(
            f"dr_signature must be tuple/list of ints, got {type(dr_signature).__name__}"
        )
    if not all(isinstance(x, int) for x in dr_signature):
        raise TypeError(
            f"dr_signature elements must be ints, got {[type(x).__name__ for x in dr_signature]}"
        )
    
    # Value checks
    if component_centroid <= 0:
        raise ValueError(
            f"component_centroid must be positive, got {component_centroid}"
        )
    if len(dr_signature) == 0:
        raise ValueError("dr_signature must not be empty")
    if not all(1 <= x <= 9 for x in dr_signature):
        raise ValueError(
            f"all DR values must be in [1,9], got {tuple(dr_signature)}"
        )
    
    # Projection
    dr_centroid = dr(round(component_centroid))
    dr_sig_sum = dr(sum(dr_signature))
    
    return (dr_centroid, dr_sig_sum)


def test_return_projection():
    """Test ρ_ℱ with Model A and diverse inputs."""
    passed, failed = 0, 0
    
    # Model A: the canonical case
    tests = [
        # (centroid, dr_sig, expected_ℱ, label)
        (432.00, (1, 8, 1, 2), (9, 3), "Model A canonical"),
        # 396 base (Flower of Life) — same DR pattern if sig unchanged
        (396.00, (1, 8, 1, 2), (9, 3), "396 Hz, same sig"),
        # 440 Hz (ISO standard)
        (440.00, (1, 8, 1, 2), (8, 3), "440 Hz, same sig"),
        # Different DR signature
        (432.00, (3, 6, 9), (9, 9), "alt sig (3,6,9)"),
        # Single-element signature
        (220.00, (5,), (4, 5), "single sig, 220 Hz"),
        # High centroid
        (880.00, (1, 8, 1, 2), (7, 3), "880 Hz"),
        # Decimal centroid
        (433.32, (1, 8, 1, 2), (1, 3), "433.32 Hz"),
    ]
    
    print("\n--- Return Projection (ρ_ℱ) Tests ---")
    for centroid, sig, expected, label in tests:
        try:
            result = return_projection(centroid, sig)
            if result == expected:
                print(f"  ✅ {label}: ρ_ℱ({centroid}, {sig}) = {result}")
                passed += 1
            else:
                print(f"  ❌ {label}: ρ_ℱ({centroid}, {sig}) = {result}, expected {expected}")
                failed += 1
        except Exception as e:
            print(f"  ❌ {label}: unexpected error: {e}")
            failed += 1
    
    return passed, failed


def test_return_projection_edge_cases():
    """Test ρ_ℱ error handling."""
    print("\n--- Return Projection Edge Cases ---")
    passed, failed = 0, 0
    
    # Zero centroid
    try:
        return_projection(0, (1, 8, 1, 2))
        print("  ❌ ρ_ℱ(0, ...) should raise ValueError")
        failed += 1
    except ValueError:
        print("  ✅ ρ_ℱ(0, ...) raises ValueError")
        passed += 1
    
    # Negative centroid
    try:
        return_projection(-432, (1, 8, 1, 2))
        print("  ❌ ρ_ℱ(-432, ...) should raise ValueError")
        failed += 1
    except ValueError:
        print("  ✅ ρ_ℱ(-432, ...) raises ValueError")
        passed += 1
    
    # String centroid
    try:
        return_projection("432", (1, 8, 1, 2))
        print("  ❌ ρ_ℱ('432', ...) should raise TypeError")
        failed += 1
    except TypeError:
        print("  ✅ ρ_ℱ('432', ...) raises TypeError")
        passed += 1
    
    # Empty signature
    try:
        return_projection(432, ())
        print("  ❌ ρ_ℱ(432, ()) should raise ValueError")
        failed += 1
    except ValueError:
        print("  ✅ ρ_ℱ(432, ()) raises ValueError")
        passed += 1
    
    # Invalid DR value (0)
    try:
        return_projection(432, (0, 8, 1, 2))
        print("  ❌ ρ_ℱ(432, (0,...)) should raise ValueError")
        failed += 1
    except ValueError:
        print("  ✅ ρ_ℱ(432, (0,...)) raises ValueError")
        passed += 1
    
    # Invalid DR value (10)
    try:
        return_projection(432, (10,))
        print("  ❌ ρ_ℱ(432, (10,)) should raise ValueError")
        failed += 1
    except ValueError:
        print("  ✅ ρ_ℱ(432, (10,)) raises ValueError")
        passed += 1
    
    # Non-int in signature
    try:
        return_projection(432, (1.5, 8, 1, 2))
        print("  ❌ ρ_ℱ(432, (1.5,...)) should raise TypeError")
        failed += 1
    except TypeError:
        print("  ✅ ρ_ℱ(432, (1.5,...)) raises TypeError")
        passed += 1
    
    # String signature
    try:
        return_projection(432, "1812")
        print("  ❌ ρ_ℱ(432, '1812') should raise TypeError")
        failed += 1
    except TypeError:
        print("  ✅ ρ_ℱ(432, '1812') raises TypeError")
        passed += 1
    
    return passed, failed


# === Test cases ===
def test_return_cycle():
    """Test ReturnCycle met diverse centroids."""
    ref = 81.75
    passed, failed = 0, 0

    # Test data: (centroid, expected_R, expected_E, expected_C)
    tests = [
        # Triviaal: Vedic basis
        (432.0,  432.0,   432.0,   ref),
        # ISO standaard
        (440.0,  440.0,   440.0,   ref * 440 / 432),
        # 432 + offset
        (433.32, 433.32,  433.32,  ref * 433.32 / 432),
        # Laag frequentie
        (220.0,  220.0,   220.0,   ref * 220 / 432),
        # Hoog frequentie
        (880.0,  880.0,   880.0,   ref * 880 / 432),
        # Willekeurig
        (517.5,  517.5,   517.5,   ref * 517.5 / 432),
    ]

    print("--- ReturnCycle Tests ---")
    for centroid, exp_r, exp_e, exp_c in tests:
        r, e, c = return_cycle(centroid, ref)
        ok = True
        try:
            assert abs(r - exp_r) < 1e-9, f"R' mismatch: {r} != {exp_r}"
            assert abs(e - exp_e) < 1e-9, f"E' mismatch: {e} != {exp_e}"
            assert abs(c - exp_c) < 1e-6, f"C' mismatch: {c} != {exp_c}"
        except AssertionError as ex:
            print(f"  ❌ centroid={centroid}: {ex}")
            failed += 1
            ok = False

        # R' identiteit-check: DR(centroid) == DR(R'(centroid))
        # (tautologisch onder Model A — R' = extractie zonder transformatie)
        # Echte V_k-invariant zit in roundtrip-test: DR(fwd) == DR(ret)
        v_fwd = dr(centroid)
        v_ret = dr(r)
        if v_fwd != v_ret:
            print(f"  ❌ R' identiteit gebroken: DR({centroid})={v_fwd} != DR({r})={v_ret}")
            failed += 1
            ok = False

        if ok:
            print(f"  ✅ centroid={centroid} → R'={r}, E'={e}, C'={c:.4f} | R' ident: DR={v_fwd}")
            passed += 1

    return passed, failed


def test_forward_return_roundtrip(base=432.0, ref=81.75, label="432"):
    """Test forward → return roundtrip: byte → freq → R' → E' → C' → byte.

    Echte roundtrip: byte_to_freq(B, ref, base) → R' → E' → C' → B'
    Onder Model A: C'(E'(R'(byte_to_freq(B)))) = B (algebraïsch exact)

    V_k-invariant: DR(fwd_freq) == DR(return_seed) == DR(returned_byte)
    """
    passed, failed = 0, 0

    # Bytes to test
    bytes_to_test = [82, 66, 72, 81, 128, 255, 1, 43]

    print(f"\n--- Forward↔Return Roundtrip (base={label}) ---")
    for B in bytes_to_test:
        # Forward: B → freq
        fwd_freq = byte_to_freq(B, ref, base)

        # Return: fwd_freq → R' → E' → C' → B'
        r, e, c = return_cycle(fwd_freq, ref, base)

        # V_k invariant: DR(fwd_freq) == DR(return_seed) == DR(returned_byte)
        # Splitsen: byte-roundtrip is harde claim, V_k DR is soft claim
        v_fwd = dr(fwd_freq)
        v_ret = dr(r)
        v_c = dr(int(round(c)))

        ok = True
        try:
            assert abs(c - B) < 1e-6, f"roundtrip: B={B} → C'={c:.6f}"
        except AssertionError as ex:
            print(f"  ❌ B={B} ({hex(B)}): {ex}")
            failed += 1
            ok = False

        if ok:
            v_k_status = ""
            if v_fwd == v_ret == v_c:
                v_k_status = f" | V_k={v_fwd}"
            else:
                v_k_status = f" | V_k: DR(fwd={v_fwd},ret={v_ret},C'={v_c})"
            print(f"  ✅ B={B:3d} ({hex(B):>4s}): fwd={fwd_freq:.2f}Hz → R'={r:.2f} → C'={c:.1f}{v_k_status}")
            passed += 1

    return passed, failed


def analyze_hex_phoneme_complementarity():
    """Analyse hex_to_phoneme: DR(hex_avg) vs DR(byte_to_freq).

    Observatiemodus — meet statistiek, valideert geen claim.
    Retourneert analyse-resultaten (telt niet mee als passed/failed).
    """
    ref = 81.75
    matching, complementary = 0, 0

    print("\n--- hex_phoneme Analyse (observatie) ---")

    for B in range(1, 256):
        avg = hex_avg_freq(B)
        fwd = byte_to_freq(B, ref)
        dr_avg = dr(avg)
        dr_fwd = dr(fwd)

        if dr_avg == dr_fwd:
            matching += 1
        else:
            complementary += 1

    # Validatie: de tellers moeten optellen tot 255
    assert matching + complementary == 255, "matching + complementary != 255"
    assert complementary > 0, "geen complementaire bytes gevonden"
    assert matching > 0, "geen matchende bytes gevonden"

    print(f"  ℹ {matching}/255 bytes: DR match (bonus-alignment)")
    print(f"  ℹ {complementary}/255 bytes: complementair (verwacht)")

    # Voorbeelden van matches
    matches = []
    for B in range(1, 256):
        avg = hex_avg_freq(B)
        fwd = byte_to_freq(B, ref)
        if dr(avg) == dr(fwd):
            matches.append((B, hex(B), avg, fwd, dr(avg)))

    if matches:
        print(f"  Match-voorbeelden:")
        for B, hx, avg, fwd, d in matches[:5]:
            print(f"    B={B} ({hx:>4s}): DR(avg={avg:.1f}) = DR(fwd={fwd:.2f}) = {d}")

    # Retourneert (None, None) — telt niet mee als test
    return None, None


def test_edge_cases():
    """Test edge cases: zero, negative, non-numeric."""
    print("\n--- Edge Cases ---")
    passed, failed = 0, 0

    # R' moet falen op 0
    try:
        R_prime(0)
        print("  ❌ R'(0) should raise assertion")
        failed += 1
    except AssertionError:
        print("  ✅ R'(0) correctly raises")
        passed += 1

    # R' moet falen op negatief
    try:
        R_prime(-432)
        print("  ❌ R'(-432) should raise assertion")
        failed += 1
    except AssertionError:
        print("  ✅ R'(-432) correctly raises")
        passed += 1

    # R' moet falen op non-numeric
    try:
        R_prime("432")
        print("  ❌ R'('432') should raise assertion")
        failed += 1
    except AssertionError:
        print("  ✅ R'('432') correctly raises")
        passed += 1

    # C' moet falen op nul ref
    try:
        C_prime(432, 0)
        print("  ❌ C'(432, 0) should raise assertion")
        failed += 1
    except AssertionError:
        print("  ✅ C'(432, 0) correctly raises")
        passed += 1

    return passed, failed


def main():
    print("=" * 60)
    print("  HEXA-BOEK: Onafhankelijke ReturnCycle Validatie")
    print("=" * 60)

    results = []

    p, f = test_return_cycle()
    results.append(("ReturnCycle", p, f))

    p, f = test_forward_return_roundtrip(base=432.0, ref=81.75, label="432")
    results.append(("Roundtrip-432", p, f))

    p, f = test_forward_return_roundtrip(base=396.0, ref=81.75, label="396")
    results.append(("Roundtrip-396", p, f))

    p, f = test_forward_return_roundtrip(base=440.0, ref=81.75, label="440")
    results.append(("Roundtrip-440", p, f))

    # Return Projection (ρ_ℱ)
    p, f = test_return_projection()
    results.append(("ReturnProjection", p, f))

    p, f = test_return_projection_edge_cases()
    results.append(("ProjectionEdge", p, f))

    # hex_phoneme is observatie — telt niet mee als test
    p, f = analyze_hex_phoneme_complementarity()
    results.append(("hex_phoneme", "obs", 0))

    p, f = test_edge_cases()
    results.append(("Edge cases", p, f))

    # Samenvatting
    total_pass = sum(1 if r[1] == "obs" else r[1] for r in results)
    total_fail = sum(r[2] for r in results)

    print("\n--- SAMENVATTING ---")
    for name, p, f in results:
        if p == "obs":
            print(f"  {name:15s}: observatie (niet geteld)")
        else:
            status = "✅" if f == 0 else f"⚠ ({f} failures)"
            print(f"  {name:15s}: {p} passed, {f} failed {status}")

    # Tel hex_phoneme niet mee
    test_pass = sum(0 if r[1] == "obs" else r[1] for r in results)
    test_fail = sum(r[2] for r in results)

    print(f"\n  Totaal (tests): {test_pass} ✅ | {test_fail} ❌")

    if test_fail == 0:
        print("\n  Status: ReturnCycle = gevalideerd_lokaal")
    else:
        print("\n  Status: ReturnCycle = gedeeltelijk_gevalideerd")

    print("=" * 60)
    return 0 if test_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
