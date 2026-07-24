#!/usr/bin/env bash
# Simpelste import — curl only, geen git nodig
#
# Gebruik:
#   curl -sL https://raw.githubusercontent.com/<user>/hexa-book/main/import.sh | bash

set -euo pipefail

REPO="hexa-book"
BRANCH="main"
BASE="https://raw.githubusercontent.com/<user>/${REPO}/${BRANCH}"

echo "→ HEXA-BOEK import"
echo ""

# Download artikels
echo "↓ Artikels..."
mkdir -p articles
for i in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
    curl -sL "${BASE}/articles/hexa-book-${i}.md" -o "articles/hexa-book-${i}.md"
done

# Download audits
echo "↓ Audits..."
mkdir -p audit
curl -sL "${BASE}/audit/00-intro.md" -o "audit/00-intro.md"

# Download engine
echo "↓ Engine..."
mkdir -p engine
for f in hexa-book-engine.py audit_status.py docx_reader.py review_analyzer.py validate_freq_lenses.py; do
    curl -sL "${BASE}/engine/${f}" -o "engine/${f}"
done

# Download README + ROUTING
echo "↓ Docs..."
curl -sL "${BASE}/README.md" -o "README.md"
curl -sL "${BASE}/ROUTING.md" -o "ROUTING.md"

echo ""
echo "✓ Import klaar"
echo ""
echo "  cat articles/hexa-book-001.md"
echo "  python3 engine/hexa-book-engine.py"
echo ""
echo "  Artikels: $(ls articles/ | wc -l)"
echo "  Audits: $(ls audit/ | wc -l)"
