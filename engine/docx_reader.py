#!/usr/bin/env python3
"""Read .docx files and extract plain text.

Usage:
  python3 docx_reader.py <file.docx>                  # stdout
  python3 docx_reader.py <file.docx> output.txt       # write to file
  python3 docx_reader.py <file.docx> -l <lines>       # limit lines
"""

import sys
import os
import zipfile
import xml.etree.ElementTree as ET

WNS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract_text(docx_path):
    """Extract all paragraph text from a .docx file."""
    if not docx_path.endswith((".docx", ".DOCX")):
        print(f"Error: not a .docx file: {docx_path}", file=sys.stderr)
        sys.exit(1)

    with zipfile.ZipFile(docx_path, "r") as zf:
        if "word/document.xml" not in zf.namelist():
            print(f"Error: no document.xml in {docx_path}", file=sys.stderr)
            sys.exit(1)

        with zf.open("word/document.xml") as f:
            tree = ET.parse(f)

    lines = []
    for p in tree.iter(WNS + "p"):
        text_parts = []
        for r in p.iter(WNS + "r"):
            for t in r.iter(WNS + "t"):
                if t.text and t.text.strip():
                    text_parts.append(t.text)
        line = " ".join(text_parts)
        if line.strip():
            lines.append(line)

    return lines


def main():
    if len(sys.argv) < 2:
        print("Usage: docx_reader.py <file.docx> [output.txt] [-l <lines>]", file=sys.stderr)
        sys.exit(1)

    docx_path = sys.argv[1]
    output_path = None
    line_limit = None

    # Parse optional args
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "-l" and i + 1 < len(sys.argv):
            line_limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] != "-l":
            output_path = sys.argv[i]
            i += 1
        else:
            i += 1

    lines = extract_text(docx_path)

    if line_limit:
        lines = lines[:line_limit]

    text = "\n".join(lines) + "\n"

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✓ {len(lines)} lines → {output_path}", file=sys.stderr)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
