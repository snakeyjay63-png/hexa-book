#!/usr/bin/env python3
"""
nidra_router.py — Nidrā Cross-Reference Graph Router

Parses nidrā cross-references from articles and ROUTING.md,
builds a dependency graph, detects broken refs / circular deps,
and propagates change-impact through the graph.

Usage:
    python3 engine/nidra_router.py           # full report
    python3 engine/nidra_router.py --graph   # dot / adjacency
    python3 engine/nidra_router.py --broken  # only broken refs
    python3 engine/nidra_router.py --circular # only circular deps
    python3 engine/nidra_router.py --propagate 002  # who depends on 002?
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ── Constants ──────────────────────────────────────────────

HEXA_BOOK_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = HEXA_BOOK_ROOT / "articles"
ROUTING_MD = HEXA_BOOK_ROOT / "ROUTING.md"

# Article filename → 3-digit id mapping (e.g. "hexa-book-003.md" → "003")
ARTICLE_ID_RE = re.compile(r"hexa-book-(\d{3})\.md")

# Nidrā reference patterns
# Matches: "Artikel 002", "Artikel 003", "Artikel 002, deel 1", "Artikel 017", etc.
ARTICLE_REF_RE = re.compile(r"Artikel\s+(\d{1,3})", re.IGNORECASE)

# ROUTING.md nidrā-pointer table pattern:
# | `hexa-book-003.md` | ... | → 002, 001, 017 | ...
ROUTING_NIDRA_RE = re.compile(
    r"`hexa-book-(\d{3})\.md`[^\|]*\|[^\|]*→\s*((?:\d{2,3}\s*,\s*)*\d{2,3})"
)

# Also match "→ 002, 012, 017" style references in article nidrā tables
# and "Artikel 002" style references
NIDRA_SECTION_RE = re.compile(r"^##\s+Nidrā", re.MULTILINE)


@dataclass
class NidraEdge:
    """A single nidrā edge: source → target."""
    source: str       # 3-digit article id, e.g. "003"
    target: str       # 3-digit article id, e.g. "002"
    context: str = "" # description / route name


@dataclass
class NidraRouter:
    """Nidrā cross-reference graph router."""

    graph: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    reverse_graph: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    edges: list[NidraEdge] = field(default_factory=list)
    all_known_ids: set[str] = field(default_factory=set)
    broken_refs: list[NidraEdge] = field(default_factory=list)
    _parsed: bool = False

    # ── Parsing ──────────────────────────────────────────

    def parse(self) -> dict:
        """Build the nidrā graph from articles + ROUTING.md. Returns adjacency."""
        self._discover_articles()
        self._parse_routing_md()
        self._parse_articles()
        self._detect_broken()
        self._parsed = True
        return dict(self.graph)

    def _discover_articles(self) -> None:
        """Discover all article IDs from the articles/ directory."""
        if not ARTICLES_DIR.exists():
            return
        for f in ARTICLES_DIR.iterdir():
            m = ARTICLE_ID_RE.search(f.name)
            if m:
                self.all_known_ids.add(m.group(1))

    def _parse_routing_md(self) -> None:
        """Parse nidrā-pointers table from ROUTING.md."""
        if not ROUTING_MD.exists():
            return
        text = ROUTING_MD.read_text(encoding="utf-8")
        for m in ROUTING_NIDRA_RE.finditer(text):
            source = m.group(1).zfill(3)
            targets_raw = m.group(2)
            targets = [t.strip().zfill(3) for t in targets_raw.split(",")]
            for target in targets:
                self._add_edge(source, target, context=f"ROUTING.md")

    def _parse_articles(self) -> None:
        """Parse nidrā references from article .md files."""
        if not ARTICLES_DIR.exists():
            return
        for f in ARTICLES_DIR.iterdir():
            m = ARTICLE_ID_RE.search(f.name)
            if not m:
                continue
            source_id = m.group(1)
            text = f.read_text(encoding="utf-8")
            self._extract_article_refs(text, source_id, f.name)

    def _extract_article_refs(
        self, text: str, source_id: str, filename: str
    ) -> None:
        """Extract 'Artikel NNN' references from an article, especially nidrā section."""
        # Find nidrā section boundaries
        nidra_match = NIDRA_SECTION_RE.search(text)
        if nidra_match:
            nidra_section = text[nidra_match.start():]
            # Only parse references in the nidrā section
            for m in ARTICLE_REF_RE.finditer(nidra_section):
                target = m.group(1).zfill(3)
                if target != source_id:
                    self._add_edge(source_id, target, context=filename)
        else:
            # Fallback: parse entire file for "Artikel NNN" refs
            for m in ARTICLE_REF_RE.finditer(text):
                target = m.group(1).zfill(3)
                if target != source_id:
                    self._add_edge(source_id, target, context=filename)

    def _add_edge(self, source: str, target: str, context: str = "") -> None:
        """Add a nidrā edge (source → target)."""
        self.graph.setdefault(source, set()).add(target)
        self.reverse_graph.setdefault(target, set()).add(source)
        edge = NidraEdge(source=source, target=target, context=context)
        # Avoid duplicate edges
        if edge not in self.edges:
            self.edges.append(edge)

    def _detect_broken(self) -> None:
        """Detect references to articles that don't exist."""
        self.broken_refs = []
        for edge in self.edges:
            if edge.target not in self.all_known_ids:
                self.broken_refs.append(edge)

    # ── Validation ───────────────────────────────────────

    def validate(self) -> list:
        """Return list of broken cross-refs (source → nonexistent target)."""
        if not self._parsed:
            self.parse()
        return list(self.broken_refs)

    # ── Propagation ──────────────────────────────────────

    def propagate(self, changed: str) -> list[str]:
        """Given a changed article ID, return all articles that depend on it (direct + transitive)."""
        if not self._parsed:
            self.parse()
        changed = changed.zfill(3)
        # BFS through reverse graph (who references 'changed'?)
        visited: set[str] = set()
        queue = [changed]
        while queue:
            current = queue.pop(0)
            for dependent in self.reverse_graph.get(current, set()):
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)
        visited.discard(changed)  # exclude self
        return sorted(visited)

    # ── Circular Detection ───────────────────────────────

    def circular(self) -> list[list[str]]:
        """Detect circular dependencies using DFS cycle detection."""
        if not self._parsed:
            self.parse()
        cycles: list[list[str]] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()
        path: list[str] = []

        def _dfs(node: str) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.graph.get(node, set()):
                if neighbor not in visited:
                    _dfs(neighbor)
                elif neighbor in rec_stack:
                    # Found a cycle: extract it
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    # Normalize: rotate to smallest element first
                    min_idx = cycle[:-1].index(min(cycle[:-1]))
                    normalized = cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]]
                    if normalized not in cycles:
                        cycles.append(normalized)

            path.pop()
            rec_stack.discard(node)

        for node in sorted(self.graph.keys()):
            if node not in visited:
                _dfs(node)

        return cycles

    # ── Graph Output ─────────────────────────────────────

    def to_dot(self) -> str:
        """Export graph as Graphviz DOT format."""
        if not self._parsed:
            self.parse()
        lines = ["digraph nidra_graph {", '    rankdir=LR;', ""]
        # Nodes
        for node in sorted(self.all_known_ids):
            label = f"Art.{node}"
            shape = "ellipse"
            if node in self.broken_refs_targets():
                shape = "diamond"
            color = "red" if any(
                br.target == node for br in self.broken_refs
            ) else "black"
            lines.append(
                f'    "{node}" [label="{label}" shape={shape} color="{color}"];'
            )
        lines.append("")
        # Edges
        for edge in self.edges:
            style = "dashed" if edge in self.broken_refs else "solid"
            lines.append(
                f'    "{edge.source}" -> "{edge.target}" [style="{style}"];'
            )
        lines.append("}")
        return "\n".join(lines)

    def adjacency(self) -> str:
        """Human-readable adjacency list."""
        if not self._parsed:
            self.parse()
        lines = []
        for source in sorted(self.graph.keys()):
            targets = sorted(self.graph[source])
            lines.append(f"  {source} → {', '.join(targets)}")
        return "\n".join(lines)

    def broken_refs_targets(self) -> set[str]:
        """Return set of target IDs that are broken (don't exist)."""
        return {br.target for br in self.broken_refs}

    # ── Summary ──────────────────────────────────────────

    def summary(self) -> str:
        """Print full nidrā graph summary."""
        if not self._parsed:
            self.parse()

        lines = []
        lines.append("=" * 60)
        lines.append("  NIDRĀ ROUTER — Cross-Reference Graph")
        lines.append("=" * 60)
        lines.append("")

        # Graph overview
        lines.append(f"  Articles discovered: {len(self.all_known_ids)}")
        lines.append(f"  Nidrā edges:         {len(self.edges)}")
        lines.append(f"  Broken refs:         {len(self.broken_refs)}")

        cycles = self.circular()
        lines.append(f"  Circular deps:       {len(cycles)}")
        lines.append("")

        # Adjacency
        lines.append("--- Adjacency List ---")
        for source in sorted(self.graph.keys()):
            targets = sorted(self.graph[source])
            lines.append(f"  {source} → {', '.join(targets)}")
        lines.append("")

        # Broken refs
        if self.broken_refs:
            lines.append("--- Broken Cross-References ---")
            for br in self.broken_refs:
                lines.append(
                    f"  ❌ {br.source} → {br.target} "
                    f"(article {br.target} does not exist)"
                )
            lines.append("")

        # Circular deps
        if cycles:
            lines.append("--- Circular Dependencies ---")
            for cycle in cycles:
                lines.append(f"  🔁 {' → '.join(cycle)}")
            lines.append("")

        # Reverse index (who depends on me?)
        lines.append("--- Dependency Index (reverse) ---")
        for target in sorted(self.reverse_graph.keys()):
            dependents = sorted(self.reverse_graph[target])
            lines.append(f"  {target} ← {', '.join(dependents)}")
        lines.append("")

        return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────

def main():
    router = NidraRouter()
    router.parse()

    args = sys.argv[1:]

    if "--propagate" in args:
        idx = args.index("--propagate")
        if idx + 1 < len(args):
            changed = args[idx + 1]
            dependents = router.propagate(changed)
            print(f"\n📡 If article {changed.zfill(3)} changes, these articles depend on it:")
            for dep in dependents:
                print(f"   → Article {dep}")
            if not dependents:
                print("   (none)")
            return

    if "--graph" in args:
        print(router.to_dot())
        return

    if "--broken" in args:
        broken = router.validate()
        if broken:
            print("❌ Broken nidrā references:")
            for br in broken:
                print(f"   {br.source} → {br.target} ({br.context})")
        else:
            print("✅ No broken nidrā references.")
        return

    if "--circular" in args:
        cycles = router.circular()
        if cycles:
            print("🔁 Circular dependencies detected:")
            for cycle in cycles:
                print(f"   {' → '.join(cycle)}")
        else:
            print("✅ No circular dependencies.")
        return

    # Default: full summary
    print(router.summary())


if __name__ == "__main__":
    main()
