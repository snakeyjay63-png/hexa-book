#!/usr/bin/env bash
# import.sh — Simpelste manier om hexa-book te importeren
#
# Gebruik:
#   curl -sL <url>/import.sh | bash

set -euo pipefail

REPO="https://github.com/<user>/hexa-book"
BRANCH="main"

echo "→ HEXA-BOEK import"
echo "  Repo: $REPO"
echo "  Branch: $BRANCH"
echo ""

# Check of we al in een hexa-book dir zitten
if [ -d "articles" ] && [ -d "audit" ]; then
    echo "✓ Al in hexa-book directory"
else
    # Download tarball
    echo "↓ Download..."
    curl -sL "${REPO}/archive/refs/heads/${BRANCH}.tar.gz" | tar xz
    DIR="hexa-book-${BRANCH}"
    if [ -d "$DIR" ]; then
        echo "✓ Extracted: $DIR"
        echo ""
        echo "  cd $DIR"
        echo "  cat articles/hexa-book-001.md"
    fi
fi

# Toon structuur
echo ""
echo "═ STRUCTUUR ═"
find . -maxdepth 2 -name '*.md' -o -name '*.py' -o -name '*.zig' 2>/dev/null | head -40
echo ""

# Tel artikels
ARTICLES=$(find articles -name 'hexa-book-*.md' 2>/dev/null | wc -l)
echo "  Artikels: $ARTICLES"
echo "  Audits: $(find audit -name '*.md' 2>/dev/null | wc -l)"
echo "  Engine scripts: $(find engine -name '*.py' 2>/dev/null | wc -l)"
