#!/usr/bin/env bash
# zig-version.sh — Zig versie-manager voor hexa-book
#
# Gebruik:
#   ./tools/zig-version.sh status          # huidige versie + audit count
#   ./tools/zig-version.sh convert 0.13 0.16  # converteer alle audits
#   ./tools/zig-version.sh test            # compileer + test alle audits
#   ./tools/zig-version.sh clean           # verwijder binaries

set -euo pipefail
cd "$(dirname "$0")/.."

ZIGTOOL="tools/zigtool/convert.js"
AUDIT_DIR="audit"

case "${1:-status}" in
  status)
    echo "═══ Hexa-Book Zig Status ═══"
    echo "Zig: $(zig version 2>/dev/null || echo 'niet geïnstalleerd')"
    echo "Audits: $(ls $AUDIT_DIR/*.zig 2>/dev/null | wc -l)"
    echo "Zigtool: $([ -f $ZIGTOOL ] && echo '✅' || echo '❌')"
    echo ""
    for f in $AUDIT_DIR/*.zig; do
      echo "  $(basename $f)"
    done
    ;;

  convert)
    FROM="${2:-0.13}"
    TO="${3:-0.16}"
    echo "═══ Zig Convert: $FROM → $TO ═══"
    for f in $AUDIT_DIR/*.zig; do
      echo "→ $(basename $f)"
      node "$ZIGTOOL" --from "$FROM" --to "$TO" "$f" -o "${f}.tmp"
      mv "${f}.tmp" "$f"
    done
    echo "✅ Gedaan. Handmatig fixen → compileren → testen."
    ;;

  test)
    echo "═══ Zig Test ═══"
    FAILED=0
    for f in $AUDIT_DIR/*.zig; do
      NAME=$(basename "$f")
      echo -n "→ $NAME ... "
      if zig test "$f" &>/dev/null; then
        echo "✅"
      else
        echo "❌"
        FAILED=$((FAILED + 1))
      fi
    done
    [ $FAILED -eq 0 ] && echo "✅ Alle audits OK" || echo "⚠️ $FAILED failures"
    exit $FAILED
    ;;

  clean)
    echo "═══ Clean ═══"
    rm -f $AUDIT_DIR/0*-artikel-*  # verwijder binaries
    echo "✅ Binaries verwijderd"
    ;;

  *)
    echo "Gebruik: status | convert <from> <to> | test | clean"
    ;;
esac
