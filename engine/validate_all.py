#!/usr/bin/env python3
"""
validate_all.py — Centrale runner voor alle hexa-book engines.

Voert uit (volgorde):
  1. validate_freq_lenses     — frequentielens validatie
  2. validate_patanjali       — Patanjali veld validatie
  3. npr_sound_engine         — NPR Sound Engine (21 tests)
  4. sanskrit_npr_bridge      — Sanskrit→NPR bridge (24 tests)
  5. validate_return_cycle    — ReturnCycle + ρ_ℱ (26 tests)

Exit codes:
  0 — alle engines gepasseerd
  1 — een of meer engines gefaald of ontbreekt
  2 — dependency ontbreekt (sanskrit_freq, numpy, ...)
"""

import sys
import os
import subprocess

# ── Config ──────────────────────────────────────────────

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, ".."))

# Vendored dependencies
_vendor = os.path.join(REPO_ROOT, "vendor", "sanskrit_frequency_bridge")
if os.path.isdir(_vendor):
    sys.path.insert(0, _vendor)

# Engines in uitvoeringsvolgorde
# required=False → mag ontbreken zonder suite te breken (bijv. zig-afhankelijk)
ENGINES = [
    ("validate_freq_lenses",    os.path.join(ENGINE_DIR, "validate_freq_lenses.py"),    True),
    ("validate_patanjali",      os.path.join(ENGINE_DIR, "validate_patanjali.py"),      False),
    ("npr_sound_engine",        os.path.join(ENGINE_DIR, "npr_sound_engine.py"),        True),
    ("sanskrit_npr_bridge",     os.path.join(ENGINE_DIR, "sanskrit_npr_bridge.py"),     True),
    ("validate_return_cycle",   os.path.join(ENGINE_DIR, "validate_return_cycle.py"),   True),
]

# ── Helpers ─────────────────────────────────────────────

def run_engine(name, path, required=True):
    """Run a single engine via subprocess. Return (passed, output).
    
    required=True  → ontbrekend bestand = suite failure (False)
    required=False → ontbrekend bestand = skip (None)
    """
    if not os.path.isfile(path):
        if required:
            return False, f"  ❌ {name}: bestand niet gevonden ({path})"
        else:
            return None, f"  ⏭ {name}: overgeslagen (niet verplicht)"

    # Injecteer PYTHONPATH zodat vendored dependencies beschikbaar zijn
    env = os.environ.copy()
    current_path = env.get("PYTHONPATH", "")
    vendor_paths = []
    if os.path.isdir(_vendor):
        vendor_paths.append(_vendor)
    for vp in vendor_paths:
        if vp not in current_path:
            current_path = os.pathsep.join([vp] + [current_path] if current_path else [vp])
    env["PYTHONPATH"] = current_path

    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=ENGINE_DIR,
            env=env,
        )
        output = result.stdout.strip()
        if result.stderr:
            output += "\n" + result.stderr.strip()

        if result.returncode == 0:
            return True, f"  ✅ {name}: exit 0"
        else:
            return False, f"  ❌ {name}: exit {result.returncode}"
    except subprocess.TimeoutExpired:
        return False, f"  ❌ {name}: timeout (>60s)"
    except Exception as e:
        return False, f"  ❌ {name}: {e}"


def check_dependencies():
    """Check that core dependencies are available."""
    missing = []

    try:
        import numpy  # noqa: F401
    except ImportError:
        missing.append("numpy")

    # Check vendored sanskrit_freq
    sanskrit_ok = False
    if os.path.isdir(_vendor):
        try:
            from sanskrit_freq import tokenize, map_phonemes  # noqa: F401
            sanskrit_ok = True
        except ImportError:
            missing.append("sanskrit_freq (vendored)")
    else:
        # Try workspace fallback
        _ws = os.path.join(REPO_ROOT, "skills", "sanskrit-frequency-bridge", "scripts")
        if os.path.isdir(_ws):
            try:
                sys.path.insert(0, _ws)
                from sanskrit_freq import tokenize, map_phonemes  # noqa: F401
                sanskrit_ok = True
            except ImportError:
                missing.append("sanskrit_freq")
        else:
            missing.append("sanskrit_freq (geen vendored copy, geen workspace skill)")

    return missing


# ── Main ────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  hexa-book engine suite — validate_all")
    print("=" * 60)
    print()

    # 1. Dependencies
    print("├─ Dependencies:")
    missing = check_dependencies()
    if missing:
        for m in missing:
            print(f"  ❌ Missing: {m}")
        print()
        print("FIX: pip install -r requirements.txt")
        print("     of zorg dat vendor/ map aanwezig is")
        print()
        sys.exit(2)
    else:
        print("  ✅ numpy, sanskrit_freq")
    print()

    # 2. Run engines
    print("├─ Engines:")
    results = []
    for name, path, required in ENGINES:
        passed, output = run_engine(name, path, required)
        results.append((name, passed, output))
        print(output)

    # 3. Summary
    print()
    print("└─ Samenvatting:")
    total = len(results)
    passed = sum(1 for _, p, _ in results if p is True)
    failed = sum(1 for _, p, _ in results if p is False)
    skipped = sum(1 for _, p, _ in results if p is None)

    print(f"  Totaal:  {total}")
    print(f"  ✅ Gedaan: {passed}")
    print(f"  ❌ Gefaald: {failed}")
    if skipped:
        print(f"  ⏭ Geskipped: {skipped}")

    print()
    if failed > 0:
        print("STATUS: SUITE GEFAALD ❌")
        sys.exit(1)
    elif skipped > 0 and passed == 0:
        print("STATUS: GEEN ENGINES UITGEVOERD")
        sys.exit(1)
    else:
        if skipped > 0:
            print("STATUS: ALLE VERPLICHTE ENGINES GEPASSEERD ✅")
        else:
            print("STATUS: ALLE ENGINES GEPASSEERD ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()
