#!/usr/bin/env python3
"""
audit-batcher.py — Toestandsmachine voor audit pipeline.

Elke rol updateert zichzelf in manifest.
Elke rol kan valideren vanuit eigen positie.
Rol = functie = naam = betekenis.

Gebruik:
  python3 tools/audit-batcher.py status                    # huidige toestand
  python3 tools/audit-batcher.py role orchestrator review.md  # orchestrator rol
  python3 tools/audit-batcher.py role coordinator B01      # coordinator rol
  python3 tools/audit-batcher.py role editor B01 P001      # editor rol
  python3 tools/audit-batcher.py validate                  # volledige validatie
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# ──────────────────────────────────────────
# Config
# ──────────────────────────────────────────

MAX_BATCH_SIZE = 3
MAX_SPAWN_DEPTH = 1  # subagent limiet: max 1 laag
HEXA_BOOK_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = str(HEXA_BOOK_ROOT / "manifest" / "pipeline.json")

# ──────────────────────────────────────────
# Toestand: elke rol updateert zichzelf
# ──────────────────────────────────────────

INITIAL_STATE = {
    "pipeline_id": "",
    "article_file": "",
    "audit_file": "",
    "review_file": "",
    "state": "idle",
    "roles": {
        "orchestrator": {
            "state": "idle",
            "updated": None,
            "points": [],
            "batches": [],
            "validation": None,
        },
        "coordinators": {},  # per batch: { "B01": { ... } }
    },
    "editors": {},  # per punt: { "P001": { ... } }
    "merged": {
        "state": "idle",
        "updated": None,
        "patches": [],
        "conflicts": [],
    },
    "history": [],  # log van alle state changes
}


def load_manifest(path: str = MANIFEST_PATH) -> Dict[str, Any]:
    """Laad manifest of maak nieuw."""
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return INITIAL_STATE.copy()


def save_manifest(state: Dict[str, Any], path: str = MANIFEST_PATH):
    """Bewaar manifest + log toestandswijziging."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S %z")
    state["history"].append({
        "time": timestamp,
        "state": state["state"],
    })
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def log_change(role: str, action: str, detail: str = ""):
    """Log toestandswijziging."""
    manifest = load_manifest()
    manifest["history"].append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "role": role,
        "action": action,
        "detail": detail,
    })
    save_manifest(manifest)


# ──────────────────────────────────────────
# Rol: Orchestrator (diepte 0)
# ──────────────────────────────────────────

def role_orchestrator(article_path: str, audit_path: str, review_path: str):
    """
    Orchestrator: artikel → audit → review → batches → update manifest.
    Artikel = bron + doel. Audit = werkveld. Review = punten.
    """
    print("\n" + "=" * 60)
    print("  ROL: ORCHESTRATOR (diepte 0)")
    print("  Viveka: Ik zie het hele beeld. Ik splijt in batches.")
    print("=" * 60)

    # Review parsen voor punten
    parsed = parse_review_file(review_path)
    batches = group_points(parsed["points"])

    # Update manifest
    manifest = load_manifest()
    manifest["pipeline_id"] = parsed["id"]
    manifest["article_file"] = article_path
    manifest["audit_file"] = audit_path
    manifest["review_file"] = review_path
    manifest["state"] = "batched"
    manifest["roles"]["orchestrator"].update({
        "state": "done",
        "updated": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "points_count": len(parsed["points"]),
        "batches": [{
            "id": b["batch_id"],
            "points": b["points"],
            "range": b["line_range"],
            "state": "pending",
        } for b in batches],
        "validation": "ok",
    })

    # Maak coordinator slots
    for batch in batches:
        manifest["roles"]["coordinators"][batch["batch_id"]] = {
            "state": "pending",
            "points": [p["id"] for p in batch["points"]],
            "line_range": batch["line_range"],
        }

    save_manifest(manifest)
    log_change("orchestrator", "batched", f"{len(parsed['points'])} punten → {len(batches)} batches")

    print(f"✅ {len(parsed['points'])} punten → {len(batches)} batches")
    for b in manifest["roles"]["orchestrator"]["batches"]:
        print(f"   {b['id']}: {b['points']} (regels {b['range'][0]}-{b['range'][1]})")
    print(f"\nManifest → {MANIFEST_PATH}")


# ──────────────────────────────────────────
# Rol: Coordinator (diepte 1)
# ──────────────────────────────────────────

def role_coordinator(batch_id: str, review_path: Optional[str] = None):
    """
    Coordinator: haal batch op → genereer instructies → update manifest.
    """
    manifest = load_manifest()
    coord = manifest["roles"]["coordinators"].get(batch_id)
    if not coord:
        print(f"Fout: batch {batch_id} niet gevonden")
        return 1

    print("\n" + "=" * 60)
    print(f"  ROL: COORDINATOR — {batch_id} (diepte 1)")
    print(f"  Viveka: Ik zie mijn batch. Ik coördineer mijn punten.")
    print(f"  Punten: {', '.join(coord['points'])}")
    print(f"  Regels: {coord['line_range'][0]}-{coord['line_range'][1]}")
    print("=" * 60)

    # Update coordinator state
    manifest["roles"]["coordinators"][batch_id].update({
        "state": "active",
        "updated": time.strftime("%Y-%m-%d %H:%M:%S %z"),
    })

    # Genereer instructies per punt
    for pid in coord["points"]:
        manifest["editors"][pid] = {
            "batch": batch_id,
            "state": "pending",
            "instruction": "",
        }

    save_manifest(manifest)
    log_change("coordinator", "activated", batch_id)

    # Print instructies
    print(f"\nInstructies voor {batch_id}:")
    for pid in coord["points"]:
        print(f"  {pid}: [te laden uit review]")

    return 0


# ──────────────────────────────────────────
# Rol: Editor (diepte 2)
# ──────────────────────────────────────────

def role_editor(batch_id: str, point_id: str):
    """
    Editor: fix één punt → update manifest.
    """
    manifest = load_manifest()
    editor = manifest["editors"].get(point_id)
    if not editor:
        print(f"Fout: punt {point_id} niet gevonden")
        return 1

    print("\n" + "=" * 60)
    print(f"  ROL: EDITOR — {point_id} (diepte 2)")
    print(f"  Viveka: Ik zie één punt. Ik maak de edit.")
    print(f"  Batch: {batch_id}")
    print("=" * 60)

    # Update editor state
    manifest["editors"][point_id].update({
        "state": "in_progress",
        "updated": time.strftime("%Y-%m-%d %H:%M:%S %z"),
    })

    save_manifest(manifest)
    log_change("editor", "started", f"{point_id} in {batch_id}")

    print(f"\nPunt {point_id} — edit gereed voor verwerking")
    return 0


# ──────────────────────────────────────────
# Validatie: elke rol kan valideren
# ──────────────────────────────────────────

def validate_pipeline(role: Optional[str] = None) -> Dict[str, Any]:
    """
    Valideer pipeline vanuit specifieke rol of volledig.
    """
    manifest = load_manifest()
    result = {
        "valid": True,
        "role": role or "full",
        "checks": [],
        "errors": [],
    }

    if role == "orchestrator" or role is None:
        orch = manifest["roles"]["orchestrator"]
        if orch["state"] == "done":
            result["checks"].append("✅ Orchestrator: batches gedefinieerd")
        else:
            result["errors"].append("❌ Orchestrator: nog niet gedaan")
            result["valid"] = False

    if role == "coordinator" or role is None:
        for bid, coord in manifest["roles"]["coordinators"].items():
            state = coord.get("state", "pending")
            if state == "done":
                result["checks"].append(f"✅ {bid}: voltooid")
            elif state == "active":
                result["checks"].append(f"⏳ {bid}: actief")
            else:
                result["checks"].append(f"⬜ {bid}: pending")

    if role == "editor" or role is None:
        for pid, editor in manifest["editors"].items():
            state = editor.get("state", "pending")
            if state == "done":
                result["checks"].append(f"✅ {pid}: edit voltooid")
            elif state == "in_progress":
                result["checks"].append(f"⏳ {pid}: aan het werk")
            else:
                result["checks"].append(f"⬜ {pid}: pending")

    return result


# ──────────────────────────────────────────
# Parser helpers (gebaseerd op eerdere versie)
# ──────────────────────────────────────────

def parse_review_file(path: str) -> Dict[str, Any]:
    """Parseert een review markdown naar structuur."""
    import re
    text = Path(path).read_text(encoding="utf-8")
    lines = text.split("\n")

    meta = {}
    if lines and lines[0].strip() == "---":
        end_idx = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), len(lines))
        for line in lines[1:end_idx]:
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    else:
        end_idx = 0

    points = []
    current_point = None
    for i, line in enumerate(lines[end_idx:], start=end_idx + 1):
        m = re.match(r"^### P(\d+):\s+(.+)$", line)
        if m:
            if current_point:
                points.append(current_point)
            current_point = {
                "id": f"P{m.group(1)}",
                "title": m.group(2).strip(),
                "line": i + 1,
                "body": [],
            }
        elif current_point:
            current_point["body"].append(line)
    if current_point:
        points.append(current_point)

    for i, point in enumerate(points):
        start = point["line"]
        end = points[i + 1]["line"] - 1 if i + 1 < len(points) else len(lines)
        point["range"] = [start, min(end, start + 150)]

    return {
        "id": meta.get("id", "unknown"),
        "target": meta.get("target", ""),
        "points": points,
        "total_lines": len(lines),
    }


def group_points(points: List[Dict], max_batch: int = MAX_BATCH_SIZE) -> List[Dict]:
    """Groepeer punten op regelbereik-proximiteit."""
    sorted_points = sorted(points, key=lambda p: p["range"][0])
    batches = []
    current_batch = []
    current_max_end = 0

    for idx, point in enumerate(sorted_points):
        p_start, p_end = point["range"]
        if p_start <= current_max_end and current_batch:
            batches.append({
                "batch_id": f"B{len(batches)+1:02d}",
                "points": current_batch,
                "line_range": [min(p["range"][0] for p in current_batch), max(p["range"][1] for p in current_batch)],
            })
            current_batch = []
            current_max_end = 0
        elif len(current_batch) >= max_batch:
            batches.append({
                "batch_id": f"B{len(batches)+1:02d}",
                "points": current_batch,
                "line_range": [min(p["range"][0] for p in current_batch), max(p["range"][1] for p in current_batch)],
            })
            current_batch = []
            current_max_end = 0

        current_batch.append(point)
        current_max_end = max(current_max_end, p_end)

    if current_batch:
        batches.append({
            "batch_id": f"B{len(batches)+1:02d}",
            "points": current_batch,
            "line_range": [min(p["range"][0] for p in current_batch), max(p["range"][1] for p in current_batch)],
        })

    return batches


# ──────────────────────────────────────────
# CLI
# ──────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    cmd = sys.argv[1]

    if cmd == "role":
        if len(sys.argv) < 3:
            print("Gebruik: role <orchestrator|coordinator|editor> [args...]")
            return 1
        role = sys.argv[2]
        if role == "orchestrator":
            if len(sys.argv) < 6:
                print("Gebruik: role orchestrator <artikel.md> <audit.md> <review.md>")
                print("  Artikel = bron + doel")
                print("  Audit = werkveld")
                print("  Review = punten")
                return 1
            role_orchestrator(sys.argv[3], sys.argv[4], sys.argv[5])
        elif role == "coordinator":
            if len(sys.argv) < 4:
                print("Gebruik: role coordinator <batch_id> [review.md]")
                return 1
            role_coordinator(sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
        elif role == "editor":
            if len(sys.argv) < 5:
                print("Gebruik: role editor <batch_id> <point_id>")
                return 1
            role_editor(sys.argv[3], sys.argv[4])
        else:
            print(f"Onbekende rol: {role}")
            return 1

    elif cmd == "validate":
        role = sys.argv[2] if len(sys.argv) > 2 else None
        result = validate_pipeline(role)
        print(f"\nValidatie ({result['role']}):")
        for check in result["checks"]:
            print(f"  {check}")
        if result["errors"]:
            print("\nFouten:")
            for err in result["errors"]:
                print(f"  {err}")
        print(f"\n{'✅ Geldig' if result['valid'] else '❌ Ongeldig'}")

    elif cmd == "status":
        manifest = load_manifest()
        print(f"\nPipeline: {manifest.get('pipeline_id', 'geen')}")
        print(f"State: {manifest['state']}")
        print(f"\nOrchestrator: {manifest['roles']['orchestrator']['state']}")
        print(f"Coordinators: {len(manifest['roles']['coordinators'])} batches")
        print(f"Editors: {len(manifest['editors'])} punten")
        print(f"Historie: {len(manifest['history'])} stappen")

    elif cmd == "reset":
        save_manifest(INITIAL_STATE.copy())
        print("✅ Pipeline gereset")

    else:
        print(f"Onbekende commando: {cmd}")
        print("Beschikbaar: role, validate, status, reset")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
