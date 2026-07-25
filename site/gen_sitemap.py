#!/usr/bin/env python3
"""Generate sitemap.json for hexa-book site."""

import json
import os
import glob

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
        articles.append({'file': f, 'name': name, 'title': title})

    audits = []
    for f in sorted(glob.glob('audit/*.md')):
        name = os.path.basename(f).replace('.md', '')
        title = name.replace('-', ' ').title()
        with open(f) as fh:
            content = fh.read()
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
        audits_zig.append({'file': f, 'name': name, 'title': title})

    stupas = []
    for f in sorted(glob.glob('audit/*.html')):
        # Skip .art.html files (kunstwerk versie is separate)
        if '.art.html' in f:
            continue
        name = os.path.basename(f).replace('.html', '')
        title = name.replace('-', ' ').title()
        # Check for .art.html (kunstwerk versie)
        art_file = f.replace('.html', '.art.html')
        if os.path.exists(art_file):
            stupas.append({'file': art_file, 'name': name, 'title': title, 'art': True})
        else:
            stupas.append({'file': f, 'name': name, 'title': title})

    talen = []
    for f in sorted(glob.glob('charveld/taalen/*.md')):
        name = os.path.basename(f).replace('.md', '')
        title = name.replace('-', ' ').title()
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
