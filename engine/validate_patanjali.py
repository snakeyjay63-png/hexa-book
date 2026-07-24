#!/usr/bin/env python3
"""
validate_patanjali.py — Patanjali-veld validatie via Zig
Draait de Zig-implementatie en parseert de output.
Ondersteunt zowel Unicode (²↔→×) als ASCII (^2<->->x) notatie.
"""

import subprocess
import sys
import os
import re

VELD_DIR = os.path.dirname(os.path.abspath(__file__))

def build():
    result = subprocess.run(
        ["zig", "build-exe", "-O", "ReleaseSmall", "src/main.zig"],
        cwd=VELD_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Bouw fout:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

def run():
    """Run the Zig binary. std.debug.print writes to stderr."""
    result = subprocess.run(
        ["./main"],
        cwd=VELD_DIR,
        capture_output=True,
        text=True,
    )
    # std.debug.print → stderr in Zig
    return result.stderr or result.stdout

def parse(output: str) -> dict:
    """Parse veld output — supports Unicode and ASCII formats."""
    data = {}
    for line in output.splitlines():
        # Entry: 11 (DR=2)
        m = re.search(r"Entry:.*\(DR=(\d)\)", line)
        if m:
            data["entry_dr"] = int(m.group(1))

        # Trilling: 11²↔13² (4↔7)  OR  11^2<->13^2 (4<->7)
        m = re.search(r"Trilling:.*\((\d)(?:↔|<->|<\->)(\d)\)", line)
        if m:
            data["trilling"] = (int(m.group(1)), int(m.group(2)))

        # Stilte: 17²=19² (1=1)
        m = re.search(r"Stilte:.*\((\d)=(\d)\)", line)
        if m:
            data["stilte"] = (int(m.group(1)), int(m.group(2)))

        # Beide naar entry
        if "Beide naar entry" in line:
            data["beide_naar_entry"] = "true" in line.lower()

        # ×2 / x2 richting (vooruit)
        m = re.search(r"[×x]2.*DR\((\d)\)", line)
        if m and "Richting" not in line.split("×2")[0].split("x2")[0]:
            data["richting_vooruit"] = int(m.group(1))

        # /2 richting (achteruit)
        m = re.search(r"/2.*DR\((\d)\)", line)
        if m:
            data["richting_achteruit"] = int(m.group(1))

        # Cirkels: 19 (DR=1)
        m = re.search(r"Cirkels:\s*(\d+).*\(DR=(\d)\)", line)
        if m:
            data["cirkels"] = int(m.group(1))
            data["cirkels_dr"] = int(m.group(2))

        # Oogjes: 90 (DR=9)
        m = re.search(r"Oogjes:\s*(\d+).*\(DR=(\d)\)", line)
        if m:
            data["oogjes"] = int(m.group(1))
            data["oogjes_dr"] = int(m.group(2))

        # DR cyclus: 2 → 8 → 3 → 3 → 9  OR  2 -> 8 -> ...
        m = re.search(r"DR cyclus:\s*(.+)", line)
        if m:
            nums = re.findall(r"\d+", m.group(1))
            data["dr_cyclus"] = [int(n) for n in nums]

    return data

def main():
    build()
    output = run()
    print(output)

    data = parse(output)

    checks = [
        ("Entry DR=2", data.get("entry_dr") == 2),
        ("Trilling 4↔7", data.get("trilling") == (4, 7)),
        ("Stilte 1=1", data.get("stilte") == (1, 1)),
        ("Beide naar entry", data.get("beide_naar_entry") is True),
        ("Richting ×2=2", data.get("richting_vooruit") == 2),
        ("Richting /2=5", data.get("richting_achteruit") == 5),
        ("Cirkels=19 (DR=1)", data.get("cirkels") == 19 and data.get("cirkels_dr") == 1),
        ("Oogjes=90 (DR=9)", data.get("oogjes") == 90 and data.get("oogjes_dr") == 9),
        ("DR cyclus 2→8→3→3→9", data.get("dr_cyclus") == [2, 8, 3, 3, 9]),
    ]

    alle_ok = True
    for naam, ok in checks:
        status = "✅" if ok else "❌"
        if not ok:
            alle_ok = False
        print(f"  {status} {naam}")

    if alle_ok:
        print("\n✅ Veld validatie geslaagd")
        return 0
    else:
        print("\n❌ Veld validatie mislukt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
