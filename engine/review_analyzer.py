#!/usr/bin/env python3
"""
Review Analyzer — Factorio pipeline
Reviews parsen, cross-refereren met artikelen, en prioriteren.
"""

import glob
import re
import sys
from pathlib import Path
from datetime import datetime

# Paths
REVIEW_DIR = Path(__file__).parent.parent / "review"
ARTICLES_DIR = Path(__file__).parent.parent / "articles"
AUDIT_DIR = Path(__file__).parent.parent / "audit"

# Review patterns
REVIEW_PATTERN = r"review-(\d{3})-(\d{4}-\d{2}-\d{2})-(hexa-book-\d+(?:-.*)?).md"
YAML_HEADER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def parse_yaml_simple(text):
    """Parse simple YAML header (key: value lines)."""
    result = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            val = val.strip().strip('"').strip("'")
            # Convert types
            if val.isdigit():
                val = int(val)
            elif val.replace(".", "").isdigit():
                val = float(val)
            elif val.lower() in ("true", "false"):
                val = val.lower() == "true"
            result[key.strip()] = val
    return result

def load_reviews(status=None):
    """Load all reviews from pipeline."""
    reviews = []
    for folder in ["00-inbox", "01-active", "02-done", "03-discard"]:
        folder_path = REVIEW_DIR / folder
        if not folder_path.exists():
            continue
        for fpath in sorted(folder_path.glob("*.md")):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Parse YAML header
            header_match = YAML_HEADER.match(content)
            if header_match:
                meta = parse_yaml_simple(header_match.group(1))
                body = content[header_match.end():]
            else:
                meta = {}
                body = content
            
            meta["_folder"] = folder
            meta["_path"] = str(fpath)
            meta["_body"] = body
            
            if status is None or meta.get("status") == status:
                reviews.append(meta)
    
    return reviews

def load_article(article_id):
    """Load article content."""
    # Try articles/ first, then audit/
    article_id_str = str(article_id).zfill(3)
    
    # Check articles/
    for pattern in [f"hexa-book-{article_id}.md", f"hexa-book-{article_id_str}.md"]:
        article_path = ARTICLES_DIR / pattern
        if article_path.exists():
            with open(article_path, "r", encoding="utf-8") as f:
                return f.read()
    
    # Check audit/ - try both 2-digit and 3-digit formats
    for num_digits in [2, 3]:
        pad = str(num_digits).zfill(num_digits)
        pattern = f"{pad}-artikel-{pad}-dimensie-{pad}.md"
        article_path = AUDIT_DIR / pattern
        if article_path.exists():
            with open(article_path, "r", encoding="utf-8") as f:
                return f.read()
    
    return None

def extract_review_points(body):
    """Extract review points as structured data."""
    points = []
    
    # Find numbered sections
    sections = re.split(r"\n## \d+\. ", body)
    for section in sections:
        header_match = re.match(r"(\d+)\. ([^\n]+)\n", section)
        if header_match:
            num = int(header_match.group(1))
            title = header_match.group(2)
            content = section[header_match.end():]
            
            # Extract operators mentioned
            operators = re.findall(r"operator_status\((\w+)\)", content)
            executions = re.findall(r"execution_status\((\w+)\)", content)
            validations = re.findall(r"validatie_status\((\w+)\)", content)
            
            points.append({
                "num": num,
                "title": title,
                "operators": operators,
                "executions": executions,
                "validations": validations,
                "content": content[:500]  # First 500 chars for preview
            })
    
    return points

def cross_ref_review(review, article_content, article_num=None):
    """Cross-reference review points with article content."""
    issues = []
    
    # Check if operators mentioned exist in article
    for match in re.finditer(r"operator_status\((\w+)\)", review["_body"]):
        op = match.group(1)
        if f"operator_status({op})" not in article_content:
            issues.append(f"MISSING_OP: {op}")
    
    # Check if execution_status is defined
    if "execution_status" in review["_body"] and "execution_status" not in article_content:
        issues.append("MISSING_CONCEPT: execution_status not defined in article")
    
    # Check if routes mentioned exist
    for route in re.finditer(r"route.*?([A-Z]+_[\w]+)", review["_body"]):
        route_name = route.group(1)
        if route_name not in article_content:
            issues.append(f"MISSING_ROUTE: {route_name}")
    
    # Vṛtti declaration check (new audit rule)
    if article_num is not None:
        vrttis, vrtti_issues = check_vrtti_declaration(article_content, article_num)
        issues.extend(vrtti_issues)
        if vrttis:
            print(f"  ✓ Vṛttis: {', '.join(vrttis)}")
    
    return issues

# Hexa vṛtti definitions
VRITTI_DEFS = {
    "V_0": {"name": "r_null", "dim": 0, "role": "ongedifferentieerd"},
    "V_1": {"name": "r_spark", "dim": 1, "role": "Agni/vonk"},
    "V_2": {"name": "r_duality", "dim": 2, "role": "split"},
    "V_3": {"name": "r_trinity", "dim": 3, "role": "3-6-9 veld"},
    "V_4": {"name": "r_tetra", "dim": 4, "role": "vorm/expansie"},
    "V_5": {"name": "r_penta", "dim": 5, "role": "return zichtbaar"},
}

def extract_vrttis_from_article(content):
    """Extract declared vṛttis from article content."""
    vrttis = []
    for vid in VRITTI_DEFS:
        if vid in content or VRITTI_DEFS[vid]["name"] in content:
            vrttis.append(vid)
    return vrttis

def check_vrtti_declaration(article_content, article_num):
    """Check if vṛttis are correctly declared (not if route is closed).
    
    New audit rule: an article is valid if it declares its vṛtti correctly
    so other articles can pick it up. Route closure may happen elsewhere.
    """
    issues = []
    vrttis = extract_vrttis_from_article(article_content)
    
    # Check for operator_status / execution_status / validatie_status
    has_status = any([
        "operator_status" in article_content,
        "execution_status" in article_content,
        "validatie_status" in article_content,
    ])
    
    if not has_status:
        # Conceptual articles are OK if they declare vṛtti
        if not vrttis:
            issues.append(f"MISSING_VRTTI: Artikel {article_num} declareert geen vṛtti")
    
    return vrttis, issues

def pipeline_summary():
    """Show pipeline status."""
    inbox = len(list((REVIEW_DIR / "00-inbox").glob("*.md")))
    active = len(list((REVIEW_DIR / "01-active").glob("*.md")))
    done = len(list((REVIEW_DIR / "02-done").glob("*.md")))
    discard = len(list((REVIEW_DIR / "03-discard").glob("*.md")))
    
    print("=" * 60)
    print("  REVIEW PIPELINE STATUS")
    print("=" * 60)
    print(f"  Inbox:   {inbox} files")
    print(f"  Active:  {active} files")
    print(f"  Done:    {done} files")
    print(f"  Discard: {discard} files")
    print("=" * 60)
    
    return inbox, active, done, discard

def analyze_review(review_id=None):
    """Analyze a specific review or all reviews."""
    reviews = load_reviews()
    
    if review_id:
        reviews = [r for r in reviews if r.get("id") == int(review_id)]
    
    print("\n" + "=" * 60)
    print("  REVIEW ANALYSIS")
    print("=" * 60)
    
    for review in reviews:
        print(f"\n--- Review {review.get('id', '?')} ---")
        print(f"Target: {review.get('target', 'N/A')}")
        print(f"Status: {review.get('status', 'N/A')}")
        print(f"Points: {review.get('points', 'N/A')}")
        print(f"Severity: {review.get('severity', 'N/A')}")
        print(f"Summary: {review.get('summary', 'N/A')}")
        
        # Load article and cross-reference
        target = review.get("target")
        if target:
            # Extract article number from target (e.g., "hexa-book-002.md" → "2")
            target_num = target.replace("hexa-book-", "").replace(".md", "").lstrip("0") or "0"
            article_content = load_article(target_num)
            if article_content:
                issues = cross_ref_review(review, article_content)
                if issues:
                    print(f"\nCross-reference issues:")
                    for issue in issues:
                        print(f"  ⚠ {issue}")
            else:
                print(f"\n⚠ Article {target} not found")
        
        # Extract points
        points = extract_review_points(review["_body"])
        print(f"\nReview points ({len(points)}):")
        for point in points:
            print(f"  {point['num']}. {point['title'][:50]}...")
            if point['operators']:
                print(f"     Operators: {', '.join(point['operators'])}")

def move_review(review_id, from_folder, to_folder):
    """Move a review between pipeline stages."""
    # Find the review
    for fpath in (REVIEW_DIR / from_folder).glob("*.md"):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        header_match = YAML_HEADER.match(content)
        if header_match:
            meta = parse_yaml_simple(header_match.group(1))
            if meta.get("id") == int(review_id):
                # Move file
                dest = REVIEW_DIR / to_folder / fpath.name
                fpath.rename(dest)
                print(f"✓ Moved review {review_id}: {from_folder} → {to_folder}")
                return True
    
    print(f"✗ Review {review_id} not found in {from_folder}")
    return False

if __name__ == "__main__":
    args = sys.argv[1:]
    
    if not args:
        pipeline_summary()
        analyze_review()
    elif args[0] == "pipeline":
        pipeline_summary()
    elif args[0] == "analyze":
        review_id = args[1] if len(args) > 1 else None
        analyze_review(review_id)
    elif args[0] == "move":
        if len(args) < 4:
            print("Usage: review_analyzer.py move <id> <from> <to>")
            print("Folders: 00-inbox, 01-active, 02-done, 03-discard")
        else:
            move_review(int(args[1]), args[2], args[3])
    else:
        print(f"Unknown command: {args[0]}")
        print("Commands: pipeline, analyze, move")
