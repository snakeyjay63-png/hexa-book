#!/usr/bin/env python3
"""Generate sitemap.json for hexa-book site."""

import json
import os
import glob
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.dirname(os.path.abspath(__file__))

def gen():
    os.chdir(REPO_ROOT)

    articles = []
    for f in sorted(glob.glob('articles/*.md')):
        name = os.path.basename(f).replace('.md', '')
        with open(f) as fh:
            lines = fh.readlines()
        title = name.replace('-', ' ').title()
        for l in lines[:10]:
            if l.startswith('# '):
                title = l[2:].strip()
                break
        art_file = f.replace('.md', '.art.html')
        has_art = os.path.exists(art_file)
        if has_art:
            try:
                with open(art_file) as af:
                    head = af.read(2000)
                m = re.search(r'<title>(.+?)</title>', head)
                if m:
                    title = m.group(1).split(' | ')[0]
            except Exception:
                pass
        articles.append({'file': f, 'name': name, 'title': title, 'art': has_art})

    audits = []
    for f in sorted(glob.glob('audit/*.md')):
        name = os.path.basename(f).replace('.md', '')
        title = name.replace('-', ' ').title()
        with open(f) as fh:
            content = fh.read()
        # Extract title from first # header
        for l in content.split('\n')[:15]:
            if l.startswith('# ') and not l.startswith('##'):
                title = l[2:].strip()
                break
        tests = 'n/a'
        for l in content.split('\n')[:30]:
            if 'tests:' in l:
                tests = l.split('tests:')[-1].strip()
                break
        audits.append({'file': f, 'name': name, 'title': title, 'tests': tests})

    audits_zig = []
    for f in sorted(glob.glob('audit/*.zig')):
        name = os.path.basename(f).replace('.zig', '')
        title = name.replace('-', ' ').title()
        # Try matching .md for a real title
        md_f = f.replace('.zig', '.md')
        if os.path.exists(md_f):
            with open(md_f) as fh:
                for l in fh:
                    if l.startswith('# ') and not l.startswith('##'):
                        title = l[2:].strip()
                        break
        audits_zig.append({'file': f, 'name': name, 'title': title})

    stupas = []
    # Direct .art.html files (kunstwerk gegenereerd uit .md)
    for f in sorted(glob.glob('audit/*.art.html')):
        name = os.path.basename(f).replace('.art.html', '')
        title = name.replace('-', ' ').title()
        # Try to read title from the art file
        try:
            with open(f) as fh:
                head = fh.read(2000)
            m = re.search(r'<title>(.+?)</title>', head)
            if m:
                title = m.group(1).split(' | ')[0]
        except Exception:
            pass
        # If title is just the filename (raw or formatted), try the .md source for ## header
        if title == name or title == name.replace('-', ' ').title():
            md_src = f.replace('.art.html', '.md')
            if os.path.exists(md_src):
                try:
                    with open(md_src) as fh:
                        md_head = fh.read(2000)
                    # Look for ## header (these files often skip # and start at ##)
                    m2 = re.search(r'^## (.+)$', md_head, re.MULTILINE)
                    if m2:
                        title = m2.group(1).strip()
                    else:
                        # Or check for `article:` in frontmatter
                        m3 = re.search(r'article:\s*"([^"]+)"', md_head)
                        if m3:
                            raw = m3.group(1)
                            title = raw.replace('-', ' ').title()
                except Exception:
                    pass
        stupas.append({'file': f, 'name': name, 'title': title, 'art': True})
    # Legacy .html files without .art.html
    for f in sorted(glob.glob('audit/*.html')):
        if '.art.html' in f:
            continue
        name = os.path.basename(f).replace('.html', '')
        title = name.replace('-', ' ').title()
        art_file = f.replace('.html', '.art.html')
        if not os.path.exists(art_file):
            stupas.append({'file': f, 'name': name, 'title': title})

    talen = []
    for f in sorted(glob.glob('charveld/taalen/*.md')):
        name = os.path.basename(f).replace('.md', '')
        title = name.replace('-', ' ').title()
        with open(f) as fh:
            for l in fh:
                if l.startswith('# ') and not l.startswith('##'):
                    title = l[2:].strip()
                    break
        talen.append({'file': f, 'name': name, 'title': title})

    media = []
    for ext in ['*.webm', '*.mp4', '*.wav', '*.mp3', '*.ogg']:
        for f in sorted(glob.glob('engine/' + ext)):
            name = os.path.basename(f)
            size = os.path.getsize(f)
            size_str = f'{size/1024:.0f}KB' if size < 1024*1024 else f'{size/1024/1024:.1f}MB'
            media_type = 'video' if ext in ('*.webm', '*.mp4') else 'audio'
            media.append({'file': f, 'name': name, 'size': size_str, 'type': media_type})

    sitemap = {
        'articles': articles,
        'audits': audits,
        'audits_zig': audits_zig,
        'stupas': stupas,
        'talen': talen,
        'media': media,
    }

    out_path = os.path.join(SITE_DIR, 'sitemap.json')
    with open(out_path, 'w') as fh:
        json.dump(sitemap, fh, indent=2, ensure_ascii=False)

    print(f'✓ sitemap.json: {len(articles)} articles, {len(audits)} audits, {len(stupas)} stupas, {len(talen)} talen, {len(media)} media')

if __name__ == '__main__':
    gen()
