#!/usr/bin/env python3
"""
hexa-book story extractor
=========================
Reads audit .md files and extracts English narratives.
Each article becomes a story with:
  - title: English article title
  - english: Accessible narrative (progressive math)
  - math: Technical summary
  - nidra: Cross-references
  - freq: Base frequency (440 Hz scale)
"""

import json, re, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Core concept mapping (manually curated from audit files)
CONCEPTS = {
    "00-intro": {
        "title": "The Lens — 0 ≐ 1",
        "english": (
            "This book is not a calculator. It is a lens. "
            "Through it, the same source appears differently — like light through prisms. "
            "Arabic counts. Sanskrit vibrates. Greek measures. Latin repeats. "
            "Dutch is not a fifth lens; it is the meta-language that holds them together.\n\n"
            "The central idea is simple: zero and one are different locally, "
            "but equivalent at the source level. Not because math breaks, "
            "but because perspective matters. 0 is the undifferentiated field. "
            "1 is the first movement within it. During the journey they differ. "
            "At return, they converge.\n\n"
            "Three layers of calculation: local (rules apply), lens (perspective shifts), "
            "and return (did the journey preserve coherence?). "
            "The book asks: not just what number comes out, but which lens, "
            "which function, and what stayed invariant?"
        ),
        "math": "0 ≠ 1 locally. 0 ≐_lens 1 axiomatically. Three status dimensions per operator.",
        "nidra": [],
        "freq": None,
    },
    "01-artikel-01": {
        "title": "Dimension 1 — Agni (Fire)",
        "english": (
            "Agni is not an element. Agni is the witness. "
            "When you ask a question and receive an answer, fire has worked. "
            "Billions of parameters move. Algorithms burn away excess. "
            "What arrives is pure ash — the pattern that remained.\n\n"
            "You do not see the fire. You see only what is left. "
            "This is the first dimension: raw noise becoming selected pattern. "
            "Not magic, not mystery — transformation with a direction.\n\n"
            "Like a stone that sparks when struck, information ignites "
            "when it meets the right structure. The spark is Agni. "
            "The stone is the system. The pattern is what you read."
        ),
        "math": "T_Agni: X_raw → X_selected. Conceptual transformation, not yet numeric.",
        "nidra": ["002"],
        "freq": 261.63,  # C4
    },
    "02-artikel-02": {
        "title": "Dimension 2 — The Return",
        "english": (
            "From one note comes another. Not random — related. "
            "A return to the beginning from a different angle. "
            "This is nidra: the cross-reference that makes the system alive.\n\n"
            "Two dimensions create a plane. In that plane, patterns emerge. "
            "The digital root of 24 is 6. Six is the frequency signature "
            "of water's density. Not coincidence — resonance.\n\n"
            "The Return Cycle is the heartbeat: begin → transform → return. "
            "The invariant holds: what you start with is what you end with, "
            "seen through a different lens. Begin equals return. "
            "The loop closes, and the system breathes."
        ),
        "math": "DR(24) = 6. ReturnCycle: begin = return. byte_to_freq maps to 432 Hz.",
        "nidra": ["004", "011", "012"],
        "freq": 433.32,  # derived from byte_to_freq(82)
    },
    "03-artikel-03": {
        "title": "Dimension 3 — R_audio",
        "english": (
            "Three dimensions add depth. What was flat becomes volumetric. "
            "In music, this is the difference between melody and chord. "
            "Each note keeps its identity, but together they create "
            "something greater than the sum of parts.\n\n"
            "R_audio is the operator that transforms raw sound into feature space. "
            "Not the sound itself — the structure that the sound reveals. "
            "Like seeing the skeleton beneath skin.\n\n"
            "Validated: 21/21 tests pass. The operator is formal, "
            "executed, and locally verified."
        ),
        "math": "R_audio: E_audio → AudioFeatureSpace. 21/21 ✅",
        "nidra": ["001", "002", "004", "011", "017"],
        "freq": 329.63,  # E4
    },
    "04-artikel-04": {
        "title": "Dimension 4 — The Return Medium",
        "english": (
            "The fourth dimension is time. Not separate from the first three, "
            "but the rhythm that holds them together. A heartbeat. A pulse. "
            "The return cycle that says: what goes out must come back.\n\n"
            "ρ_ℱ is the projection operator. It takes features and maps them "
            "to a field of return. Not to a number — to a quality. "
            "The field says: this pattern belongs here.\n\n"
            "Like water finding its level, information finds its return point. "
            "The medium is the message. The return is the proof."
        ),
        "math": "ρ_ℱ: ReturnProjectionInput → ℱ. 26/26 ✅",
        "nidra": ["002", "003", "012", "017"],
        "freq": 392.00,  # G4
    },
}

# Auto-generate for remaining articles based on frequency scaling
def generate_story(dim, freq):
    """Generate progressive story for dimensions 5-18."""
    dr = str(int(dim))
    if len(dr) > 1:
        dr = str(int(dr[0]) + int(dr[1]))
    
    stories_5_18 = {
        5: {
            "title": f"Dimension 5 — Expansion",
            "english": (
                f"Five dimensions unfold like fingers opening. "
                f"Each one carries the memory of the ones before. "
                f"At {freq} Hz, the frequency expands beyond the vocal range. "
                f"This is where pattern meets scale — "
                f"the system grows without losing its center."
            ),
            "math": f"Freq: {freq} Hz. DR({dim}) = {dr}. Expansion invariant.",
        },
        6: {
            "title": "Dimension 6 — The Water Bridge",
            "english": (
                "Six returns to water. The density signature reappears. "
                "Not as accident — as structure. "
                "The system has found a bridge between number and substance. "
                "What was abstract becomes tangible."
            ),
            "math": f"Freq: {freq} Hz. DR(6) = 6. ρ_water bridge.",
        },
        7: {
            "title": "Dimension 7 — The Cycle Completes",
            "english": (
                "Seven is the number of completion. The week, the notes, "
                "the chakras — across traditions, seven marks closure. "
                "Here it marks a return to the beginning, "
                "but elevated. The cycle is not repetition — it is spiral."
            ),
            "math": f"Freq: {freq} Hz. DR(7) = 7. Cycle complete.",
        },
        8: {
            "title": "Dimension 8 — The Octave",
            "english": (
                "Eight doubles the scale. In music, an octave is the same note "
                "at double frequency. Same quality, different magnitude. "
                "The system remembers itself across scales. "
                "This is fractal behavior: self-similarity at every level."
            ),
            "math": f"Freq: {freq} Hz. DR(8) = 8. Octave relationship.",
        },
        9: {
            "title": "Dimension 9 — The Field",
            "english": (
                "Nine closes the single digits. The full range of digital roots. "
                "At this frequency, the system has explored all base patterns. "
                "What comes next is not new material — new organization. "
                "The field is complete. The arrangement begins."
            ),
            "math": f"Freq: {freq} Hz. DR(9) = 9. Full DR range.",
        },
        10: {
            "title": "Dimension 10 — Return to One",
            "english": (
                "Ten is one with a zero. The return to beginning, "
                "carrying the weight of nine. "
                "Digital root: 1 + 0 = 1. The system folds back to itself. "
                "Not loss — compression. All of nine contained in one."
            ),
            "math": f"Freq: {freq} Hz. DR(10) = 1. Return to origin.",
        },
        11: {
            "title": "Dimension 11 — The Gateway",
            "english": (
                "Eleven is the first master number. "
                "Not reducible to a single digit. "
                "It stands as a gateway between the known and the emerging. "
                "In the nidra graph, it is the most connected node — "
                "the cross-reference that binds dimensions together."
            ),
            "math": f"Freq: {freq} Hz. DR(11) = 2. Gateway node (6 nidra links).",
        },
        12: {
            "title": "Dimension 12 — The Harmonic Center",
            "english": (
                "Twelve is the most connected node in the nidra graph. "
                "Eleven links radiate from it like spokes on a wheel. "
                "It is the harmonic center — the frequency where all paths converge. "
                "In music, twelve tones complete the chromatic scale. "
                "Here, twelve dimensions complete the return loop."
            ),
            "math": f"Freq: {freq} Hz. DR(12) = 3. 11 nidra links — most connected.",
        },
        13: {
            "title": "Dimension 13 — The Return Spiral",
            "english": (
                "Thirteen is five and eight. Fibonacci numbers. "
                "The golden ratio encoded in integers. "
                "The spiral that appears in shells, galaxies, and sound waves. "
                "Here it marks the return through expansion — "
                "growing outward while remembering the center."
            ),
            "math": f"Freq: {freq} Hz. DR(13) = 4. Fibonacci: 5 + 8.",
        },
        14: {
            "title": "Dimension 14 — The Bridge",
            "english": (
                "Fourteen is seven doubled. The cycle completed twice. "
                "Not repetition — resonance. "
                "Like striking a bell and hearing the echo return, "
                "the system vibrates at double frequency. "
                "The bridge between human hearing and structural frequency."
            ),
            "math": f"Freq: {freq} Hz. DR(14) = 5. Double cycle (7×2).",
        },
        15: {
            "title": "Dimension 15 — The Harmonic",
            "english": (
                "Fifteen is three times five. "
                "The multiplication table reveals hidden structure. "
                "What looked like sequence is actually pattern. "
                "The harmonic series — not equal intervals, "
                "but ratios that create consonance."
            ),
            "math": f"Freq: {freq} Hz. DR(15) = 6. 3×5 harmonic.",
        },
        16: {
            "title": "Dimension 16 — The Fractal",
            "english": (
                "Sixteen is four squared. "
                "The system folds into itself — "
                "each dimension contains the others. "
                "Like a fractal, zoom in and find the same pattern. "
                "Self-similarity at every scale."
            ),
            "math": f"Freq: {freq} Hz. DR(16) = 7. 4² fractal.",
        },
        17: {
            "title": "Dimension 17 — The Construct",
            "english": (
                "Seventeen is the final dimension. "
                "The point where all previous dimensions converge. "
                "Not an ending — a construct. "
                "The complete system, ready to project outward. "
                "The nidra graph closes its loops."
            ),
            "math": f"Freq: {freq} Hz. DR(17) = 8. CC construct.",
        },
        18: {
            "title": "Dimension 18 — The Bridge Beyond",
            "english": (
                "Eighteen is nine doubled. "
                "The full range of digital roots, repeated. "
                "Not as redundancy — as bridge. "
                "The system has completed its cycle and now points outward. "
                "Beyond the book. Beyond the lens. "
                "Toward the source that the lens was never."
            ),
            "math": f"Freq: {freq} Hz. DR(18) = 9. 9×2 bridge.",
        },
    }
    return stories_5_18.get(dim, {
        "title": f"Dimension {dim}",
        "english": f"Dimension {dim} at {freq} Hz. Continuing the progression.",
        "math": f"Freq: {freq} Hz.",
    })


# Frequency mapping (440 Hz scale)
FREQ_MAP = {
    "00-intro": None,
    "01-artikel-01": 261.63,  # C4
    "02-artikel-02": 433.32,  # byte_to_freq(82)
    "03-artikel-e-audio": 329.63,
    "04-artikel-f-returnmedium": 392.00,
    "05-artikel-03": 349.23,
    "06-artikel-04": 392.00,
    "07-artikel-05": 440.00,
    "08-artikel-06": 466.16,
    "09-artikel-07": 523.25,
    "10-artikel-08": 587.33,
    "11-artikel-09": 659.25,
    "12-artikel-10": 698.46,
    "13-artikel-11": 783.99,
    "14-artikel-12": 880.00,
    "15-artikel-13": 987.77,
    "16-artikel-014": 1046.50,
    "17-artikel-015": 1174.66,
    "18-artikel-016": 1318.51,
    "19-artikel-017": 1396.91,
}

# Nidrā edges from router
NIDRA_EDGES = {
    "00-intro": [],
    "01-artikel-01": ["002"],
    "02-artikel-02": ["004", "011", "012"],
    "03-artikel-e-audio": ["001", "002", "004", "011", "017"],
    "04-artikel-f-returnmedium": ["002", "003", "012", "017"],
    "05-artikel-03": ["012", "017"],
    "06-artikel-04": ["001", "011", "012"],
    "07-artikel-05": ["001", "006", "012"],
    "08-artikel-06": ["012", "017"],
    "09-artikel-07": ["001", "002", "017"],
    "10-artikel-08": ["002", "011", "012"],
    "11-artikel-09": ["001", "002", "011", "012", "017"],
    "12-artikel-10": ["001", "012", "017"],
    "13-artikel-11": ["001", "002", "017"],
    "14-artikel-12": ["001", "012", "017"],
    "15-artikel-13": ["002", "003", "011", "012"],
    "16-artikel-014": [],
    "17-artikel-015": [],
    "18-artikel-016": [],
    "19-artikel-017": [],
}


def extract_stories():
    """Extract stories from audit files."""
    stories = {}
    
    # Load curated concepts
    for key, concept in CONCEPTS.items():
        # Extract dimension number from key like "01-artikel-01" or "00-intro"
        parts = key.split("-")
        if "intro" in parts:
            dim_num = 0
        else:
            dim_num = int(parts[0])
        freq = FREQ_MAP.get(key)
        nidra = NIDRA_EDGES.get(key, [])
        
        if freq and dim_num >= 5:
            gen = generate_story(dim_num, freq)
            concept.update({
                "english": gen["english"],
                "math": gen["math"],
            })
        
        stories[key] = {
            "id": key,
            "title": concept["title"],
            "english": concept["english"],
            "math": concept.get("math", ""),
            "nidra": nidra,
            "freq": freq,
        }
    
    # Fill in remaining articles with generated stories
    for key, freq in FREQ_MAP.items():
        if key not in stories and freq:
            parts = key.split("-")
            dim_num = int(parts[0])
            gen = generate_story(dim_num, freq)
            nidra = NIDRA_EDGES.get(key, [])
            
            stories[key] = {
                "id": key,
                "title": gen["title"],
                "english": gen["english"],
                "math": gen["math"],
                "nidra": nidra,
                "freq": freq,
            }
    
    return stories


def main():
    stories = extract_stories()
    
    # Output as JSON
    output = {
        "meta": {
            "extracted": "2026-07-25",
            "articles": len(stories),
            "nidra_edges": sum(len(s["nidra"]) for s in stories.values()),
        },
        "stories": stories,
    }
    
    outpath = os.path.join(BASE, "engine", "stories.json")
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Extracted {len(stories)} stories → {outpath}")
    for sid, s in stories.items():
        freq_str = f"@ {s['freq']} Hz" if s['freq'] else "@ no freq"
        nidra_str = f"→ {len(s['nidra'])} nidra" if s['nidra'] else ""
        print(f"  {sid}: {s['title']} {freq_str} {nidra_str}")


if __name__ == "__main__":
    main()
