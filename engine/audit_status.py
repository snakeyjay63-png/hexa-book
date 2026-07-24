#!/usr/bin/env python3
"""
hexa-book audit status — live status van audit-bestanden.
Soort "git status" voor het hexa-book audit proces.
"""

import re
import os
import sys
from pathlib import Path
from datetime import datetime

# Kleuren
RST = "\033[0m"
GRN = "\033[92m"
YEL = "\033[93m"
RED = "\033[91m"
BLU = "\033[94m"
CYN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Paden
HEXA_BOOK_ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = HEXA_BOOK_ROOT / "audit"
ARTICLES_DIR = HEXA_BOOK_ROOT / "articles"


def scan_audit_files():
    """Scan alle audit-bestanden."""
    if not AUDIT_DIR.exists():
        print(f"{RED}Audit directory niet gevonden: {AUDIT_DIR}{RST}")
        return []
    
    files = sorted(AUDIT_DIR.glob("*.md"))
    return [f for f in files if f.name != "README.md"]


def extract_status_counts(content):
    """Tel status indicators in content."""
    # Tel emoji indicators
    done = len(re.findall(r'✅', content))
    warning = len(re.findall(r'⚠', content))
    error = len(re.findall(r'❌', content))
    
    # Tel "Punt N:" patrones (open audit punten)
    points = re.findall(r'Punt\s+(\d+)', content)
    
    # Tel "proposed:" patrones (voorgestelde definities)
    proposed = len(re.findall(r'proposed:', content, re.IGNORECASE))
    
    # Tel status markers
    status_validated = len(re.findall(r'status_validated', content))
    status_defined = len(re.findall(r'status_defined', content))
    status_convention = len(re.findall(r'status_convention', content))
    status_interpretation = len(re.findall(r'status_interpretation', content))
    
    return {
        'done': done,
        'warning': warning,
        'error': error,
        'points': points,
        'proposed': proposed,
        's_validated': status_validated,
        's_defined': status_defined,
        's_convention': status_convention,
        's_interpretation': status_interpretation,
    }


def extract_eindstatus(content):
    """Extract Eindstatus sectie indien aanwezig."""
    # Zoek Eindstatus sectie
    eind_match = re.search(
        r'(?:###\s*)?Eindstatus.*?(?:###|$)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    
    if eind_match:
        section = eind_match.group(0)
        # Tel ✅/⚠/❌ in Eindstatus
        done = len(re.findall(r'✅', section))
        warning = len(re.findall(r'⚠', section))
        error = len(re.findall(r'❌', section))
        return {'done': done, 'warning': warning, 'error': error, 'section': section.strip()}
    
    return None


def extract_halve_routes(content):
    """Check op halve routes."""
    routes = []
    
    # Zoek HALF / halve route secties
    if re.search(r'HALF|halve route', content, re.IGNORECASE):
        routes.append('halve_routes_found')
    
    # Zoek expliciete missing markers — alleen halve routes
    missing = re.findall(r'(?:ontbreekt|ontbrekend|nog niet gedefinieerd|niet uitgevoerd|HALVE ROUTE)', content, re.IGNORECASE)
    
    # Filter: telt alleen als er geen "status_defined" of "✅" bij staat
    # (simpeur: tel halve_route secties expliciet)
    halve_route_blocks = re.findall(r'(?:###\s*)?\d+\.\s*.*(?:Hz|DR_freq|W_C|boekreturn|ρ_water|fractaalmodel|ρ_fractal)', content, re.IGNORECASE)
    
    return {'has_halve_routes': bool(routes) or bool(halve_route_blocks), 'missing_count': len(halve_route_blocks) + len(missing)}


def extract_last_modified(filepath):
    """Laatst aangepaste datum."""
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")


def audit_article_file(filepath):
    """Audit een enkel artikelbestand."""
    content = filepath.read_text(encoding='utf-8')
    
    counts = extract_status_counts(content)
    eindstatus = extract_eindstatus(content)
    halve = extract_halve_routes(content)
    last_mod = extract_last_modified(filepath)
    
    return {
        'file': filepath.name,
        'path': str(filepath.relative_to(HEXA_BOOK_ROOT)),
        'counts': counts,
        'eindstatus': eindstatus,
        'halve_routes': halve,
        'last_modified': last_mod,
    }


def print_header():
    """Print header."""
    print(f"\n{BOLD}{'='*60}{RST}")
    print(f"{BOLD}  HEXA-BOEK AUDIT STATUS{RST}")
    print(f"  {DIM}{'=' * 56}{RST}")
    print(f"  {DIM}Audit dir: {AUDIT_DIR.relative_to(HEXA_BOOK_ROOT)}{RST}")
    print(f"  {DIM}Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RST}")
    print(f"{BOLD}{'='*60}{RST}\n")


def print_article_summary(result):
    """Print samenvatting van één artikel."""
    c = result['counts']
    name = result['file']
    
    # Bepaal status kleur
    if c['error'] > 0:
        status_color = RED
        status_icon = "❌"
    elif c['warning'] > 5:
        status_color = YEL
        status_icon = "⚠"
    elif c['error'] == 0 and c['warning'] < 3:
        status_color = GRN
        status_icon = "✅"
    else:
        status_color = CYN
        status_icon = "•"
    
    print(f"{BOLD}{name}{RST}")
    print(f"  {DIM}{result['path']}{RST}")
    print(f"  {DIM}Laatst gewijzigd: {result['last_modified']}{RST}")
    
    # Status indicators
    print(f"  {status_color}{status_icon} ✅ {c['done']}  ⚠ {c['warning']}  ❌ {c['error']}{RST}")
    
    # Status types
    if c['s_validated'] or c['s_defined'] or c['s_convention'] or c['s_interpretation']:
        print(f"  {DIM}    status: validated={c['s_validated']} defined={c['s_defined']} "
              f"convention={c['s_convention']} interpretation={c['s_interpretation']}{RST}")
    
    # Eindstatus indien aanwezig
    if result['eindstatus']:
        es = result['eindstatus']
        print(f"  {BLU}  [Eindstatus] ✅ {es['done']}  ⚠ {es['warning']}  ❌ {es['error']}{RST}")
    
    # Halve routes
    if result['halve_routes']['has_halve_routes']:
        print(f"  {RED}  [HALVE ROUTES] gevonden — {result['halve_routes']['missing_count']} ontbrekende elementen{RST}")
    elif result['halve_routes']['missing_count'] > 0:
        print(f"  {YEL}  [ONTBREKEND] {result['halve_routes']['missing_count']} elementen{RST}")
    
    # Open punten
    if c['points']:
        print(f"  {DIM}  Open punten: {', '.join(c['points'][:5])}{RST}")
    
    # Voorgestelde definities
    if c['proposed'] > 0:
        print(f"  {CYN}  {c['proposed']} voorgestelde definitie(s){RST}")
    
    print()


def print_summary(results):
    """Print globale samenvatting."""
    total_done = sum(r['counts']['done'] for r in results)
    total_warning = sum(r['counts']['warning'] for r in results)
    total_error = sum(r['counts']['error'] for r in results)
    
    eind_articles = sum(1 for r in results if r['eindstatus'])
    halve_route_articles = sum(1 for r in results if r['halve_routes']['has_halve_routes'])
    
    print(f"{BOLD}{'─'*60}{RST}")
    print(f"{BOLD}  SAMENVATTING{RST}")
    print(f"{BOLD}{'─'*60}{RST}")
    print(f"  Audit-bestanden:   {len(results)}")
    print(f"  Met Eindstatus:    {eind_articles}/{len(results)}")
    print(f"  {GRN}  ✅ Gereed:        {total_done}{RST}")
    print(f"  {YEL}  ⚠ Waarschuwing:  {total_warning}{RST}")
    print(f"  {RED}  ❌ Fout:         {total_error}{RST}")
    
    if halve_route_articles > 0:
        print(f"  {RED}  Halve routes:    {halve_route_articles} artikel(s){RST}")
    else:
        print(f"  {GRN}  Halve routes:    ✅ geen — alle routes gesloten{RST}")
    
    print(f"{BOLD}{'─'*60}{RST}\n")


def scan_article_status(filepath):
    """Scan status markers in een artikelbestand."""
    content = filepath.read_text(encoding='utf-8')
    
    s_validated = len(re.findall(r'status_validated', content))
    s_defined = len(re.findall(r'status_defined', content))
    s_convention = len(re.findall(r'status_convention', content))
    s_interpretation = len(re.findall(r'status_interpretation', content))
    s_executed = len(re.findall(r'status_executed', content))
    
    done = len(re.findall(r'✅', content))
    warning = len(re.findall(r'⚠', content))
    error = len(re.findall(r'❌', content))
    
    return {
        's_validated': s_validated,
        's_defined': s_defined,
        's_convention': s_convention,
        's_interpretation': s_interpretation,
        's_executed': s_executed,
        'done': done,
        'warning': warning,
        'error': error,
    }


def check_articles_dir():
    """Check artikelen directory voor status."""
    if not ARTICLES_DIR.exists():
        return
    
    print(f"\n{BOLD}{DIM}Artikelen directory: {ARTICLES_DIR.relative_to(HEXA_BOOK_ROOT)}{RST}")
    print(f"{BOLD}{DIM}{'─'*56}{RST}")
    
    files = sorted(ARTICLES_DIR.glob("*.md"))
    if files:
        for f in files:
            mtime = datetime.fromtimestamp(os.path.getmtime(f))
            status = scan_article_status(f)
            
            total_markers = (status['s_validated'] + status['s_defined'] + 
                           status['s_convention'] + status['s_interpretation'] + 
                           status['s_executed'])
            
            print(f"  {BOLD}{f.name}{RST}")
            print(f"    {DIM}({mtime.strftime('%Y-%m-%d %H:%M')}){RST}")
            
            if total_markers > 0:
                print(f"    {DIM}status: val={status['s_validated']} def={status['s_defined']} "
                      f"conv={status['s_convention']} interp={status['s_interpretation']} "
                      f"exec={status['s_executed']}{RST}")
            
            if status['done'] > 0 or status['warning'] > 0 or status['error'] > 0:
                print(f"    {GRN}✅ {status['done']}{RST}  {YEL}⚠ {status['warning']}{RST}  {RED}❌ {status['error']}{RST}")


def main():
    """Hoofdfunctie."""
    # Check voor --article-only flag
    if "--article-only" in sys.argv:
        print(f"\n{BOLD}{'='*60}{RST}")
        print(f"{BOLD}  HEXA-BOEK ARTIKEL STATUS{RST}")
        print(f"  {DIM}{'=' * 56}{RST}")
        print(f"  {DIM}Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RST}")
        print(f"{BOLD}{'='*60}{RST}\n")
        
        if not ARTICLES_DIR.exists():
            print(f"{RED}Artikelen directory niet gevonden: {ARTICLES_DIR}{RST}")
            return
        
        files = sorted(ARTICLES_DIR.glob("*.md"))
        if not files:
            print(f"{YEL}Geen artikelbestanden gevonden{RST}")
            return
        
        for f in files:
            mtime = datetime.fromtimestamp(os.path.getmtime(f))
            status = scan_article_status(f)
            
            total_markers = (status['s_validated'] + status['s_defined'] + 
                           status['s_convention'] + status['s_interpretation'] + 
                           status['s_executed'])
            
            print(f"{BOLD}{f.name}{RST}")
            print(f"  {DIM}({mtime.strftime('%Y-%m-%d %H:%M')}){RST}")
            
            if total_markers > 0:
                print(f"  {DIM}status: val={status['s_validated']} def={status['s_defined']} "
                      f"conv={status['s_convention']} interp={status['s_interpretation']} "
                      f"exec={status['s_executed']}{RST}")
            
            if status['done'] > 0 or status['warning'] > 0 or status['error'] > 0:
                print(f"  {GRN}✅ {status['done']}{RST}  {YEL}⚠ {status['warning']}{RST}  {RED}❌ {status['error']}{RST}")
            print()
        
        return
    
    # Volledige audit mode (default)
    print_header()
    
    # Scan audit bestanden
    audit_files = scan_audit_files()
    
    if not audit_files:
        print(f"{YEL}Geen audit-bestanden gevonden in {AUDIT_DIR}{RST}")
        return
    
    # Audit elk bestand
    results = []
    for af in audit_files:
        results.append(audit_article_file(af))
    
    # Print resultaten
    for r in results:
        print_article_summary(r)
    
    # Samenvatting
    print_summary(results)
    
    # Artikelen directory
    check_articles_dir()


if __name__ == "__main__":
    main()
