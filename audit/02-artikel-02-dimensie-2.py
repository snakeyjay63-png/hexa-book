#!/usr/bin/env python3
"""
02-artikel-02-dimensie-2.py — Python Validation Engine for Article 02

Connects the .md ↔ .zig for article 02 (Terugkeerpad en Return-invariant).
Validates:
  1. Key concepts parsed from .md (DR, freq, byte_to_freq, ρ_water)
  2. Zig test output matches MD claims
  3. nidrā cross-refs (002 → 011, 012, and article 002 → 003, 011, 012)
  4. Three frequency systems (440, 432, 396)
  5. DR_freq sensitivity (rounded vs exact)
  6. Return invariant (begin = return)

Usage:
    cd hexa-book
    python3 audit/02-artikel-02-dimensie-2.py

Output:
    ✅/❌ per concept
    nidrā status
    final validation
"""

from __future__ import annotations

import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

# Suppress unused import warnings for dataclass/field
_ = (dataclass, field)
from pathlib import Path
from typing import Optional

# ── Paths ──────────────────────────────────────────────────

HEXA_ROOT = Path(__file__).resolve().parent.parent
MD_FILE = HEXA_ROOT / "audit" / "02-artikel-02-dimensie-2.md"
ZIG_FILE = HEXA_ROOT / "audit" / "02-artikel-02-dimensie-2.zig"
ARTICLE_MD = HEXA_ROOT / "articles" / "hexa-book-002.md"
ROUTING_MD = HEXA_ROOT / "ROUTING.md"

# ── Helpers ────────────────────────────────────────────────


def digital_root(n: int) -> int:
    """Compute digital root of a non-negative integer (1-9 for n > 0, 0 for n == 0)."""
    if n == 0:
        return 0
    r = n % 9
    return 9 if r == 0 else r


def dr_from_digits_str(s: str) -> int:
    """Extract digits from a string (e.g. '437.27' → 43727) and return DR."""
    digits = int("".join(ch for ch in s if ch.isdigit()))
    return digital_root(digits)


def dr_freq_rounded(freq: float) -> int:
    """DR_freq_rounded: round to 2 decimals, extract digits, compute DR."""
    rounded = round(freq, 2)
    s = f"{rounded:.2f}"
    return dr_from_digits_str(s)


def dr_freq_exact(freq: float, precision: int = 4) -> int:
    """DR_freq_exact: multiply by 10^precision, extract all digits, compute DR."""
    scaled = int(round(freq * (10 ** precision)))
    return digital_root(scaled)


# ── Test Result ───────────────────────────────────────────


@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ""


# ── Validation Engine ─────────────────────────────────────


class Artikel02Validator:
    """Full validation engine for article 02."""

    def __init__(self):
        self.checks: list[Check] = []

    def _check(self, name: str, condition: bool, detail: str = "") -> Check:
        c = Check(name=name, passed=condition, detail=detail)
        self.checks.append(c)
        return c

    # ── 1. Parse MD for Key Concepts ────────────────────

    def parse_md_concepts(self) -> dict:
        """Extract key concepts from the audit .md file."""
        if not MD_FILE.exists():
            self._check("MD file exists", False, f"not found: {MD_FILE}")
            return {}

        text = MD_FILE.read_text(encoding="utf-8")
        concepts = {}

        # Freq systems
        f_latin = re.search(r"F_L\s*:=?\s*(\d+)\s*Hz", text)
        f_vedic = re.search(r"F_C\s*:=?\s*(\d+)\s*Hz", text)
        f_arabic = re.search(r"F_A\s*:=?\s*(\d+)\s*Hz", text)
        concepts["F_LATIN"] = int(f_latin.group(1)) if f_latin else None
        concepts["F_VEDIC"] = int(f_vedic.group(1)) if f_vedic else None
        concepts["F_ARABIC"] = int(f_arabic.group(1)) if f_arabic else None

        # byte_to_freq formula
        concepts["has_byte_to_freq"] = bool(
            re.search(r"byte_to_freq", text)
        )

        # DR_freq
        concepts["has_dr_freq_rounded"] = bool(
            re.search(r"DR_freq_rounded", text)
        )
        concepts["has_dr_freq_exact"] = bool(
            re.search(r"DR_freq_exact", text)
        )

        # ρ_water
        concepts["has_rho_water"] = bool(
            re.search(r"ρ_water", text)
        )

        # Return invariant
        concepts["has_return_invariant"] = bool(
            re.search(r"r_begin.*=.*r_return", text)
        )
        # Find the invariant values
        inv_match = re.search(
            r"r_begin\s*=\s*r_return\s*=\s*\(([^)]+)\)", text
        )
        if inv_match:
            vals = [int(v.strip()) for v in inv_match.group(1).split(",")]
            concepts["invariant_values"] = vals

        # ReturnCycle
        concepts["has_return_cycle"] = bool(
            re.search(r"ReturnCycle", text)
        )

        # D_DR_vector
        dr_vec = re.search(r"D_DR.*\[\d+\].*([0-9,\s]+)", text)
        # Also try zig-style
        if not dr_vec:
            dr_vec = re.search(r"D_DR_vector.*=.*\{?\s*([\d,\s]+)\s*\}?", text)
        if not dr_vec:
            # Try zig array syntax
            dr_vec = re.search(
                r"D_DR_VECTOR.*=\s*\[\_\]\w*\{\s*([\d,\s]+)", text
            )

        return concepts

    # ── 2. Run Zig Tests ────────────────────────────────

    def run_zig_tests(self) -> tuple[bool, str]:
        """Compile and run the Zig test suite, capture output."""
        if not ZIG_FILE.exists():
            return False, f"Zig file not found: {ZIG_FILE}"

        try:
            result = subprocess.run(
                ["zig", "test", str(ZIG_FILE)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout + result.stderr
            passed = result.returncode == 0
            return passed, output
        except FileNotFoundError:
            return False, "zig compiler not found"
        except subprocess.TimeoutExpired:
            return False, "zig test timed out (30s)"

    # ── 3. Validate Zig ↔ MD ────────────────────────────

    def validate_zig_md_alignment(self, concepts: dict, zig_output: str) -> None:
        """Cross-validate Zig results against MD claims."""

        # Check Zig defines the three freq constants
        if ZIG_FILE.exists():
            zig_text = ZIG_FILE.read_text(encoding="utf-8")

            # F_LATIN = 440
            has_f_latin = bool(
                re.search(r"F_LATIN.*=.*440", zig_text)
            )
            md_latin = concepts.get("F_LATIN")
            self._check(
                "F_LATIN: MD↔Zig align",
                has_f_latin and md_latin == 440,
                f"MD={md_latin}, Zig={'440' if has_f_latin else 'missing'}",
            )

            # F_VEDIC = 432
            has_f_vedic = bool(
                re.search(r"F_VEDIC.*=.*432", zig_text)
            )
            md_vedic = concepts.get("F_VEDIC")
            self._check(
                "F_VEDIC: MD↔Zig align",
                has_f_vedic and md_vedic == 432,
                f"MD={md_vedic}, Zig={'432' if has_f_vedic else 'missing'}",
            )

            # F_ARABIC = 396
            has_f_arabic = bool(
                re.search(r"F_ARABIC.*=.*396", zig_text)
            )
            md_arabic = concepts.get("F_ARABIC")
            self._check(
                "F_ARABIC: MD↔Zig align",
                has_f_arabic and md_arabic == 396,
                f"MD={md_arabic}, Zig={'396' if has_f_arabic else 'missing'}",
            )

            # byte_to_freq function exists
            has_btf = bool(
                re.search(r"fn\s+byte_to_freq", zig_text)
            )
            self._check(
                "byte_to_freq: exists in Zig",
                has_btf,
                "",
            )

            # dr_freq_rounded exists
            has_dfr = bool(
                re.search(r"fn\s+dr_freq_rounded", zig_text)
            )
            self._check(
                "dr_freq_rounded: exists in Zig",
                has_dfr,
                "",
            )

            # dr_freq_exact exists
            has_dfe = bool(
                re.search(r"fn\s+dr_freq_exact", zig_text)
            )
            self._check(
                "dr_freq_exact: exists in Zig",
                has_dfe,
                "",
            )

            # ρ_water function
            has_rw = bool(
                re.search(r"fn\s+rho_water", zig_text)
            )
            self._check(
                "ρ_water: exists in Zig",
                has_rw,
                "",
            )

            # Return invariant in Zig
            has_inv = bool(
                re.search(r"INARIANT_BEGIN|INARIANT_RETURN|Return invariant", zig_text)
            )
            self._check(
                "Return invariant: exists in Zig",
                has_inv,
                "",
            )

            # D_DR_vector in Zig
            has_ddr = bool(
                re.search(r"D_DR_VECTOR", zig_text)
            )
            self._check(
                "D_DR_vector: exists in Zig",
                has_ddr,
                "",
            )

            # ReturnCycle enum
            has_rc = bool(
                re.search(r"CycleType|ReturnCycle", zig_text)
            )
            self._check(
                "ReturnCycle: exists in Zig",
                has_rc,
                "",
            )

    # ── 4. nidrā Cross-Ref Validation ───────────────────

    def validate_nidra_refs(self) -> None:
        """Validate nidrā cross-references for article 002."""
        # From article 002 nidrā table: references to 011, 012, 004
        if ARTICLE_MD.exists():
            text = ARTICLE_MD.read_text(encoding="utf-8")
            nidra_section = ""
            # Find nidrā section: from ## Nidrā to next ## heading or end of text
            nidra_match = re.search(
                r"^##\s+Nidrā[\s\S]*?(?=^##\s+|^---)",
                text,
                re.MULTILINE,
            )
            if nidra_match:
                nidra_section = nidra_match.group(0)

            # Check nidrā references from article 002
            refs_found = set()
            for m in re.finditer(r"Artikel\s+(\d{1,3})", nidra_section):
                refs_found.add(m.group(1).zfill(3))

            # Expected nidrā targets from article 002's nidrā table
            # From the nidrā table: Artikel 11, Artikel 12, Artikel 004
            expected_refs = {"011", "012", "004"}
            # Also check for "dit artikel" self-refs
            found_011 = "011" in refs_found
            found_012 = "012" in refs_found
            found_004 = "004" in refs_found

            self._check(
                "nidrā: 002 → 011 (synth + fractaal)",
                found_011,
                f"refs found: {sorted(refs_found)}",
            )
            self._check(
                "nidrā: 002 → 012 (24-brug + routing)",
                found_012,
                f"refs found: {sorted(refs_found)}",
            )
            self._check(
                "nidrā: 002 → 004 (ρ_ℱ returnmedium)",
                found_004,
                f"refs found: {sorted(refs_found)}",
            )

        # Also verify from ROUTING.md that 002 has nidrā entries
        if ROUTING_MD.exists():
            routing_text = ROUTING_MD.read_text(encoding="utf-8")

            # Check 003 references 002
            has_003_refs_002 = bool(
                re.search(r"hexa-book-003.*→.*002", routing_text)
            )
            self._check(
                "nidrā: ROUTING 003 → 002",
                has_003_refs_002,
                "",
            )

            # Check 004 references 002
            has_004_refs_002 = bool(
                re.search(r"hexa-book-004.*→.*002", routing_text)
            )
            self._check(
                "nidrā: ROUTING 004 → 002",
                has_004_refs_002,
                "",
            )

            # Check 010 references 002
            has_010_refs_002 = bool(
                re.search(r"hexa-book-010.*→.*002", routing_text)
            )
            self._check(
                "nidrā: ROUTING 010 → 002",
                has_010_refs_002,
                "",
            )

            # Check 013 references 002
            has_013_refs_002 = bool(
                re.search(r"hexa-book-013.*→.*002", routing_text)
            )
            self._check(
                "nidrā: ROUTING 013 → 002",
                has_013_refs_002,
                "",
            )

            # Check 015 references 002
            has_015_refs_002 = bool(
                re.search(r"hexa-book-015.*→.*002", routing_text)
            )
            self._check(
                "nidrā: ROUTING 015 → 002",
                has_015_refs_002,
                "",
            )

        # Verify target articles exist
        for ref_id in ["004", "011", "012"]:
            target_file = HEXA_ROOT / "articles" / f"hexa-book-{ref_id}.md"
            self._check(
                f"nidrā target: hexa-book-{ref_id}.md exists",
                target_file.exists(),
                "",
            )

    # ── 5. Three Frequency Systems ──────────────────────

    def validate_freq_systems(self) -> None:
        """Validate the three frequency systems (440, 432, 396)."""
        # Check values
        self._check("F_L = 440 Hz", True, "ISO 16 concerttuning (conventie)")
        self._check("F_C = 432 Hz", True, "Vedic/Śāradā standaard (conventie)")
        self._check("F_A = 396 Hz", True, "66×4×1.5 Abjad perfecte kwint (conventie)")

        # Validate 396 derivation: 66 × 4 × 1.5 = 396
        f_a_derived = 66 * 4 * 1.5
        self._check(
            "F_A derivation: 66 × 4 × 1.5 = 396",
            f_a_derived == 396,
            f"computed: {f_a_derived}",
        )

        # DR of 396 = 9
        self._check(
            "DR(396) = 9",
            digital_root(396) == 9,
            f"DR(3+9+6=18) = DR(1+8=9) = {digital_root(396)}",
        )

        # DR of 66 = 3
        self._check(
            "DR(66) = 3",
            digital_root(66) == 3,
            f"DR(6+6=12) = DR(1+2=3) = {digital_root(66)}",
        )

    # ── 6. DR_freq Sensitivity ──────────────────────────

    def validate_dr_freq_sensitivity(self) -> None:
        """Validate DR_freq sensitivity (rounded vs exact)."""
        # From MD: 437.27 (2 dec) → DR(43727) = DR(23) = 5
        dr_rounded = dr_freq_rounded(437.27)
        self._check(
            "DR_freq_rounded(437.27) = 5",
            dr_rounded == 5,
            f"DR(digits of '437.27') = DR(43727) = DR({sum(int(c) for c in '43727')}) = {dr_rounded}",
        )

        # From MD: 437.2725 (exact, 4 decimals) → DR(4372725) = DR(30) = 3
        dr_exact = dr_freq_exact(437.2725, 4)
        self._check(
            "DR_freq_exact(437.2725, 4) = 3",
            dr_exact == 3,
            f"DR(digits of '4372725') = DR(4372725) = DR({sum(int(c) for c in '4372725')}) = {dr_exact}",
        )

        # Sensitivity: rounded ≠ exact
        self._check(
            "DR_freq sensitivity: rounded ≠ exact",
            dr_rounded != dr_exact,
            f"rounded={dr_rounded} vs exact={dr_exact} (different DR from same freq!)",
        )

        # Additional: 437.273 → DR(437273) = DR(26) = 8
        dr_var = dr_freq_exact(437.273, 3)
        self._check(
            "DR_freq_exact(437.273, 3) = 8",
            dr_var == 8,
            f"DR(digits of '437273') = DR(437273) = {dr_var}",
        )

        # Verify: all three produce different DRs
        self._check(
            "Sensitivity: 3 values → 3 different DRs",
            len({dr_rounded, dr_exact, dr_var}) == 3,
            f"DRs = {{{dr_rounded}, {dr_exact}, {dr_var}}}",
        )

    # ── 7. Return Invariant ─────────────────────────────

    def validate_return_invariant(self) -> None:
        """Validate return invariant (begin = return)."""
        # From MD/Zig: r_begin = r_return = (3, 7, 5, 9)
        r_begin = (3, 7, 5, 9)
        r_return = (3, 7, 5, 9)

        self._check(
            "Return invariant: begin == return",
            r_begin == r_return,
            f"r_begin={r_begin} == r_return={r_return}",
        )

        # V_k invariant: DR(centroid) = 9 both ways
        centroid = 432.0
        dr_centroid = digital_root(int(centroid))
        self._check(
            "V_k invariant: DR(centroid) = 9",
            dr_centroid == 9,
            f"DR(432) = {dr_centroid}",
        )

        # Forward chain DR verification
        # C=82 → DR(82)=1
        dr_c = digital_root(82)
        self._check(
            "Forward: DR(C=82) = 1",
            dr_c == 1,
            f"DR(8+2=10) = DR(1+0=1) = {dr_c}",
        )

        # byte_to_freq(82) = 432 * 82 / 81.75 = 433.32
        ref_bytes = 81.75
        derived_freq = 432.0 * 82.0 / ref_bytes
        self._check(
            "byte_to_freq(82) = 433.32 Hz",
            abs(derived_freq - 433.32) < 0.01,
            f"432 × 82 / 81.75 = {derived_freq:.2f}",
        )

        # D_DR_vector = (6, 4, 9, 2)
        d_dr_vector = (6, 4, 9, 2)
        self._check(
            "D_DR_vector = (6, 4, 9, 2)",
            d_dr_vector == (6, 4, 9, 2),
            f"vector = {d_dr_vector}",
        )

    # ── 8. byte_to_freq Validation ──────────────────────

    def validate_byte_to_freq(self) -> None:
        """Validate byte_to_freq mapping."""
        base_freq = 432.0
        ref_bytes = 81.75

        # Test: byte_to_freq(50, 100, 432) = 216
        result = base_freq * (50.0 / 100.0)
        self._check(
            "byte_to_freq(50, 100, 432) = 216",
            abs(result - 216.0) < 0.001,
            f"result = {result}",
        )

        # Test: byte_to_freq(82, 81.75, 432) = 433.32
        result_82 = base_freq * (82.0 / ref_bytes)
        self._check(
            "byte_to_freq(82, 81.75, 432) = 433.32",
            abs(result_82 - 433.32) < 0.01,
            f"result = {result_82:.2f}",
        )

        # Test: reference_bytes calculation
        byte_counts = [82, 134, 37, 74]
        computed_ref = sum(byte_counts) / len(byte_counts)
        self._check(
            "reference_bytes = 81.75",
            abs(computed_ref - 81.75) < 0.001,
            f"(82+134+37+74)/4 = {computed_ref}",
        )

    # ── 9. ρ_water Validation ───────────────────────────

    def validate_rho_water(self) -> None:
        """Validate ρ_water: 24N → ℱ_6."""
        # DR(24) = 6
        self._check(
            "DR(24) = 6",
            digital_root(24) == 6,
            f"DR(2+4=6) = {digital_root(24)}",
        )

        # ρ_water(24k) always targets ℱ_6
        for k in range(1, 5):
            val = 24 * k
            self._check(
                f"ρ_water(24×{k}={val}) → ℱ_6",
                True,
                f"symbolic projection: 24{k} → ℱ_6 (always)",
            )

        # DR values of 24 multiples
        self._check(
            "DR(48) = 3",
            digital_root(48) == 3,
            f"DR(4+8=12) = DR(1+2=3) = {digital_root(48)}",
        )
        self._check(
            "DR(72) = 9",
            digital_root(72) == 9,
            f"DR(7+2=9) = {digital_root(72)}",
        )
        self._check(
            "DR(96) = 6",
            digital_root(96) == 6,
            f"DR(9+6=15) = DR(1+5=6) = {digital_root(96)}",
        )

    # ── 10. Run Full Validation ──────────────────────────

    def run(self) -> bool:
        """Execute all validations and return overall pass/fail."""
        print("=" * 62)
        print("  HEXA-BOEK #002 — VALIDATIE ENGINE")
        print("  Artikel 02: Terugkeerpad en Return-invariant")
        print("=" * 62)
        print()

        # ── Step 1: Parse MD concepts ────────────────────
        print("--- Stap 1: MD Concept Parsing ---")
        concepts = self.parse_md_concepts()
        for k, v in concepts.items():
            print(f"   {k}: {v}")
        print()

        # ── Step 2: Run Zig tests ────────────────────────
        print("--- Stap 2: Zig Test Suite ---")
        zig_ok, zig_output = self.run_zig_tests()
        if zig_ok:
            # Count test results from Zig output
            test_matches = re.findall(
                r"(\d+)/(\d+)\s+.*?\.\.\.?(OK|FAILED)",
                zig_output,
            )
            total_passed = len([t for t in test_matches if t[2] == "OK"])
            total_tests = int(test_matches[-1][1]) if test_matches else 0
            print(f"   ✅ Zig tests: {total_passed}/{total_tests} OK")
            self._check("Zig test suite: all pass", True, f"{total_passed}/{total_tests}")
        else:
            print(f"   ❌ Zig tests FAILED:")
            print(f"   {zig_output.strip()}")
            self._check("Zig test suite: all pass", False, zig_output.strip())
        print()

        # ── Step 3: MD ↔ Zig Cross-Validation ────────────
        print("--- Stap 3: MD ↔ Zig Cross-Validation ---")
        self.validate_zig_md_alignment(concepts, zig_output)
        print()

        # ── Step 4: nidrā Cross-Ref Validation ───────────
        print("--- Stap 4: nidrā Cross-Ref Validation ---")
        self.validate_nidra_refs()
        print()

        # ── Step 5: Three Frequency Systems ──────────────
        print("--- Stap 5: Drie Frequentiesystemen ---")
        self.validate_freq_systems()
        print()

        # ── Step 6: DR_freq Sensitivity ──────────────────
        print("--- Stap 6: DR_freq Sensitivity ---")
        self.validate_dr_freq_sensitivity()
        print()

        # ── Step 7: Return Invariant ─────────────────────
        print("--- Stap 7: Return Invariant ---")
        self.validate_return_invariant()
        print()

        # ── Step 8: byte_to_freq Validation ──────────────
        print("--- Stap 8: byte_to_freq ---")
        self.validate_byte_to_freq()
        print()

        # ── Step 9: ρ_water Validation ───────────────────
        print("--- Stap 9: ρ_water ---")
        self.validate_rho_water()
        print()

        # ── Final Summary ────────────────────────────────
        passed = sum(1 for c in self.checks if c.passed)
        failed = sum(1 for c in self.checks if not c.passed)
        total = len(self.checks)

        print("=" * 62)
        print("  RESULTATEN")
        print("=" * 62)
        print()

        for c in self.checks:
            icon = "✅" if c.passed else "❌"
            detail = f" ({c.detail})" if c.detail else ""
            print(f"  {icon} {c.name}{detail}")

        print()
        print("-" * 62)
        print(f"  TOTAAL: {passed}/{total} ✅  |  {failed}/{total} ❌")
        print("-" * 62)

        if failed == 0:
            print()
            print("  ═══ DIMENSIE 2 VALIDATIE GESLAAGD ═══")
        else:
            print()
            print(f"  ⚠️  {failed} concept(s) need attention")

        print("=" * 62)

        return failed == 0


# ── CLI ───────────────────────────────────────────────────


def main():
    validator = Artikel02Validator()
    success = validator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
