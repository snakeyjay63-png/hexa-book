#!/usr/bin/env python3
"""Generate Stupa HTML pages from audit articles.

Each Stupa combines .md + .zig + .py into a single visual page.
Design: tiered layers like a Buddhist stupa — text → code → engine.
"""

import os, glob, json, html as html_mod

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_DIR = os.path.join(REPO_ROOT, 'audit')

# Shared CSS for all stupas
STUPA_CSS = r"""
:root {
  --bg1: #0d0d14;
  --bg2: #14141f;
  --bg3: #1c1c2e;
  --text: #e0e0e8;
  --text-dim: #8888a0;
  --accent: #6e7bf2;
  --accent2: #a78bfa;
  --gold: #f0c040;
  --green: #4ade80;
  --red: #f87171;
  --border: #2a2a40;
  --mono: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
  --sans: system-ui, -apple-system, "Segoe UI", sans-serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: var(--bg1);
  color: var(--text);
  font-family: var(--sans);
  line-height: 1.7;
  overflow-x: hidden;
}

/* ── Stupa Container ── */
.stupa {
  max-width: 860px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

/* ── Stupa Crown (top ornament) ── */
.stupa-crown {
  text-align: center;
  padding: 60px 0 30px;
  position: relative;
}

.stupa-crown::before {
  content: "•";
  display: block;
  font-size: 2rem;
  color: var(--gold);
  margin-bottom: 20px;
  animation: pulse 4s ease-in-out infinite;
}

.stupa-crown h1 {
  font-size: 2.2rem;
  color: var(--gold);
  font-weight: 300;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}

.stupa-crown .subtitle {
  font-size: 0.95rem;
  color: var(--text-dim);
  font-style: italic;
}

.stupa-crown .langs {
  margin-top: 12px;
  font-size: 0.82rem;
  color: var(--accent2);
  opacity: 0.7;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

/* ── Stupa Layers ── */
.stupa-layer {
  margin: 0 auto 0;
  position: relative;
}

/* Layer width shrinks as we go up, like a real stupa */
.layer-base { max-width: 100%; }
.layer-body { max-width: 94%; margin: 0 auto; }
.layer-code { max-width: 88%; margin: 0 auto; }
.layer-engine { max-width: 82%; margin: 0 auto; }
.layer-crown-wrap { max-width: 76%; margin: 0 auto; }

/* ── Layer Headers ── */
.layer-header {
  text-align: center;
  padding: 20px 0;
  position: relative;
}

.layer-header::before {
  content: "";
  position: absolute;
  top: 50%;
  left: -20px;
  right: -20px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
}

.layer-label {
  display: inline-block;
  font-family: var(--mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  padding: 4px 14px;
  border-radius: 20px;
  background: var(--bg3);
  border: 1px solid var(--border);
  position: relative;
  z-index: 1;
}

.layer-label.text { color: var(--accent); border-color: var(--accent); }
.layer-label.code { color: var(--accent2); border-color: var(--accent2); }
.layer-label.engine { color: var(--green); border-color: var(--green); }
.layer-label.meta { color: var(--gold); border-color: var(--gold); }

/* ── Content Blocks ── */
.content-block {
  padding: 30px 36px;
}

.content-block p {
  margin-bottom: 1em;
  color: var(--text);
}

.content-block h2 {
  font-size: 1.4rem;
  color: var(--gold);
  margin: 2em 0 0.6em;
  font-weight: 400;
}

.content-block h3 {
  font-size: 1.1rem;
  color: var(--accent);
  margin: 1.6em 0 0.5em;
  font-weight: 400;
}

.content-block h4 {
  font-size: 0.95rem;
  color: var(--accent2);
  margin: 1.2em 0 0.4em;
}

.content-block strong { color: var(--gold); font-weight: 500; }
.content-block em { color: var(--accent2); }

.content-block blockquote {
  border-left: 2px solid var(--gold);
  margin: 1.5em 0;
  padding: 12px 20px;
  background: rgba(240, 192, 64, 0.04);
  border-radius: 0 8px 8px 0;
  color: var(--text-dim);
}

.content-block code {
  font-family: var(--mono);
  font-size: 0.88em;
  background: var(--bg3);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--accent2);
}

.content-block pre {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 20px;
  margin: 1.2em 0;
  overflow-x: auto;
  font-size: 0.85rem;
  line-height: 1.6;
}

.content-block pre code {
  background: none;
  padding: 0;
  color: var(--text);
}

.content-block hr {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  margin: 2em 0;
}

.content-block ul, .content-block ol {
  margin: 1em 0 1em 1.5em;
}

.content-block li {
  margin-bottom: 0.4em;
}

/* ── Code Block (Zig / Python) ── */
.code-block {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  margin: 0;
}

.code-block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 18px;
  background: var(--bg3);
  border-bottom: 1px solid var(--border);
  font-family: var(--mono);
  font-size: 0.75rem;
}

.code-lang {
  color: var(--accent2);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.code-tests {
  color: var(--green);
}

.code-block pre {
  padding: 20px;
  margin: 0;
  overflow-x: auto;
  font-size: 0.82rem;
  line-height: 1.7;
  background: transparent;
  border: none;
  border-radius: 0;
}

.code-block pre code {
  background: none;
  color: var(--text);
  font-family: var(--mono);
}

/* Simple syntax colors */
.code-block .kw { color: var(--accent); }
.code-block .fn { color: var(--accent2); }
.code-block .str { color: var(--green); }
.code-block .cmt { color: var(--text-dim); font-style: italic; }
.code-block .num { color: var(--gold); }

/* ── Meta Layer (YAML frontmatter) ── */
.meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  padding: 20px 0;
}

.meta-item {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 16px;
}

.meta-item .label {
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 4px;
}

.meta-item .value {
  font-size: 0.9rem;
  color: var(--text);
}

.meta-item .value.pass { color: var(--green); }
.meta-item .value.warn { color: var(--gold); }
.meta-item .value.fail { color: var(--red); }

/* ── 3D Status Model ── */
.status-model {
  background: var(--bg3);
  border: 1px solid var(--gold);
  border-radius: 12px;
  padding: 20px 24px;
  margin: 1.5em 0;
}

.status-model h4 {
  color: var(--gold);
  font-size: 0.85rem;
  margin-bottom: 12px;
  font-weight: 500;
}

.status-row {
  display: flex;
  gap: 8px;
  margin-bottom: 6px;
  font-family: var(--mono);
  font-size: 0.82rem;
}

.status-key { color: var(--accent); min-width: 140px; }
.status-val { color: var(--text); }
.status-val.ok { color: var(--green); }

/* ── Back link ── */
.stupa-footer {
  text-align: center;
  padding: 40px 0 20px;
  font-size: 0.82rem;
}

.stupa-footer a {
  color: var(--accent);
  text-decoration: none;
}

.stupa-footer a:hover {
  text-decoration: underline;
}

/* ── Responsive ── */
@media (max-width: 640px) {
  .stupa-crown h1 { font-size: 1.6rem; }
  .content-block { padding: 20px 16px; }
  .layer-body, .layer-code, .layer-engine, .layer-crown-wrap { max-width: 100%; }
  .meta-grid { grid-template-columns: 1fr; }
}
"""

def parse_frontmatter(text):
    """Parse YAML-ish frontmatter from markdown."""
    meta = {}
    if not text.startswith('---'):
        return meta, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return meta, text
    fm = parts[1].strip()
    body = parts[2].strip()
    for line in fm.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('-'):
            key, _, val = line.partition(':')
            meta[key.strip()] = val.strip().strip('"')
        elif line.startswith('- "'):
            if 'known_exceptions' not in meta:
                meta['known_exceptions'] = []
            if isinstance(meta['known_exceptions'], list):
                meta['known_exceptions'].append(line.strip('- "').rstrip('"'))
    return meta, body


def simple_md_to_html(md_text):
    """Lightweight markdown to HTML — same as site renderer."""
    lines = md_text.split('\n')
    html_lines = []
    in_code = False
    code_buf = []
    in_blockquote = False
    in_list = False

    for raw in lines:
        line = raw.rstrip()

        # Code blocks
        if line.startswith('```'):
            if in_code:
                lang = code_buf.pop(0) if code_buf and code_buf[0].strip() and not code_buf[0].startswith('<') else ''
                inner = '\n'.join(code_buf)
                html_lines.append(f'<pre><code class="{lang}">{html_mod.escape(inner)}</code></pre>')
                code_buf = []
                in_code = False
            else:
                code_first = line[3:].strip()
                code_buf = [code_first if code_first else '']
                in_code = True
            continue

        if in_code:
            code_buf.append(line)
            continue

        # Blockquote
        if line.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            html_lines.append(f'<p>{md_inline(line[2:])}</p>')
            continue
        else:
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False

        # Headers
        if line.startswith('##### '):
            if in_list:
                html_lines.append('</ol>')
                in_list = False
            html_lines.append(f'<h5>{md_inline(line[6:])}</h5>')
        elif line.startswith('#### '):
            if in_list:
                html_lines.append('</ol>')
                in_list = False
            html_lines.append(f'<h4>{md_inline(line[5:])}</h4>')
        elif line.startswith('### '):
            if in_list:
                html_lines.append('</ol>')
                in_list = False
            html_lines.append(f'<h3>{md_inline(line[4:])}</h3>')
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ol>')
                in_list = False
            html_lines.append(f'<h2>{md_inline(line[3:])}</h2>')
        elif line.startswith('# '):
            if in_list:
                html_lines.append('</ol>')
                in_list = False
            html_lines.append(f'<h1>{md_inline(line[2:])}</h1>')
        elif line == '---':
            if in_list:
                html_lines.append('</ol>')
                in_list = False
            html_lines.append('<hr>')
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{md_inline(line[2:])}</li>')
        elif line and line[0].isdigit() and line[1:3] == '. ':
            if not in_list:
                html_lines.append('<ol>')
                in_list = True
            html_lines.append(f'<li>{md_inline(line[3:])}</li>')
        elif line == '':
            if in_list:
                html_lines.append('</ul>' if not any(l.startswith('<ol>') for l in html_lines[-5:]) else '</ol>')
                in_list = False
        else:
            if in_list:
                html_lines.append('</ul>' if not any(l.startswith('<ol>') for l in html_lines[-5:]) else '</ol>')
                in_list = False
            html_lines.append(f'<p>{md_inline(line)}</p>')

    if in_code:
        inner = '\n'.join(code_buf)
        html_lines.append(f'<pre><code>{html_mod.escape(inner)}</code></pre>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


def md_inline(text):
    """Process inline markdown."""
    text = html_mod.escape(text)
    # Bold
    text = text.replace('**', '<strong>').replace('**', '</strong>')
    text = text.replace('__', '<strong>').replace('__', '</strong>')
    # Italic
    text = text.replace('*', '<em>').replace('*', '</em>')
    text = text.replace('_', '<em>').replace('_', '</em>')
    # Inline code
    text = text.replace('`', '<code>').replace('`', '</code>')
    return text


def generate_stupa(md_path):
    """Generate a single Stupa HTML page."""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    meta, md_body = parse_frontmatter(md_text)
    base = os.path.splitext(os.path.basename(md_path))[0]
    strip_prefix = base.lstrip('0123456789-')

    # Find companions
    zig_path = None
    py_path = None
    for zig in sorted(glob.glob(os.path.join(AUDIT_DIR, '*.zig'))):
        zb = os.path.splitext(os.path.basename(zig))[0].lstrip('0123456789-')
        if zb == strip_prefix:
            zig_path = zig
            break
    for py in sorted(glob.glob(os.path.join(AUDIT_DIR, '*.py'))):
        pb = os.path.splitext(os.path.basename(py))[0].lstrip('0123456789-')
        if pb == strip_prefix:
            py_path = py
            break

    # Extract title from content
    title = strip_prefix.replace('-', ' ').title()
    subtitle = ''
    langs = ''
    for line in md_body.split('\n')[:30]:
        if line.startswith('# ') and title.lower().replace(' ', '-') != strip_prefix.lower():
            title = line[2:].strip()
        if line.startswith('## ') and not line.startswith('### '):
            subtitle = line[3:].strip()
            break

    # Build HTML
    layers = []

    # Layer 0: Meta (crown)
    if meta:
        meta_items = []
        for k, v in meta.items():
            cls = ''
            if '21/21' in str(v) or '26/26' in str(v) or 'gevalideerd' in str(v).lower():
                cls = 'pass'
            elif 'ongetest' in str(v).lower() or 'niet_gevalideerd' in str(v).lower():
                cls = 'warn'
            meta_items.append('<div class="meta-item"><div class="label">' + k + '</div><div class="value ' + cls + '">' + html_mod.escape(str(v)) + '</div></div>')
        layers.append(f'''
<div class="stupa-layer layer-crown-wrap">
  <div class="layer-header"><span class="layer-label meta">Metadata</span></div>
  <div class="content-block"><div class="meta-grid">{"".join(meta_items)}</div></div>
</div>
        ''')

    # Layer 1: Main text (base — widest)
    md_html = simple_md_to_html(md_body)
    layers.append(f'''
<div class="stupa-layer layer-base">
  <div class="layer-header"><span class="layer-label text">Tekst</span></div>
  <div class="content-block">{md_html}</div>
</div>
    ''')

    # Layer 2: Zig code
    if zig_path:
        with open(zig_path, 'r', encoding='utf-8') as f:
            zig_content = f.read()
        zig_tests = ''
        for line in zig_content.split('\n')[:5]:
            if 'tests:' in line:
                zig_tests = line.split('tests:')[-1].strip()
                break
        layers.append(f'''
<div class="stupa-layer layer-code">
  <div class="layer-header"><span class="layer-label code">Zig{f' — {zig_tests}' if zig_tests else ''}</span></div>
  <div class="code-block">
    <div class="code-block-header">
      <span class="code-lang">Zig</span>
      <span class="code-tests">{zig_tests}</span>
    </div>
    <pre><code class="zig">{html_mod.escape(zig_content)}</code></pre>
  </div>
</div>
        ''')

    # Layer 3: Python engine
    if py_path:
        with open(py_path, 'r', encoding='utf-8') as f:
            py_content = f.read()
        layers.append(f'''
<div class="stupa-layer layer-engine">
  <div class="layer-header"><span class="layer-label engine">Python Engine</span></div>
  <div class="code-block">
    <div class="code-block-header">
      <span class="code-lang">Python</span>
    </div>
    <pre><code class="python">{html_mod.escape(py_content)}</code></pre>
  </div>
</div>
        ''')

    # Assemble full page
    html = f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stupa — {html_mod.escape(title)}</title>
  <link rel="icon" type="image/svg+xml" href="../../site/favicon.svg">
  <link rel="icon" type="image/x-icon" href="../../site/favicon.ico">
  <style>{STUPA_CSS}</style>
</head>
<body>
  <div class="stupa">
    <div class="stupa-crown">
      <h1>{html_mod.escape(title)}</h1>
      {f'<div class="subtitle">{html_mod.escape(subtitle)}</div>' if subtitle else ''}
    </div>

    {" ".join(layers)}

    <div class="stupa-footer">
      <a href="../../site/index.html">← Hexa-Boek</a> · <a href="INDEX.md">Audit Index</a>
    </div>
  </div>
</body>
</html>'''

    out_path = os.path.join(AUDIT_DIR, base + '.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return out_path


def main():
    md_files = sorted(glob.glob(os.path.join(AUDIT_DIR, '*.md')))
    # Skip INDEX and TEMPLATE
    targets = [f for f in md_files if not any(skip in f for skip in ['INDEX', 'TEMPLATE'])]

    generated = []
    for md_path in targets:
        out = generate_stupa(md_path)
        generated.append(out)
        base = os.path.basename(md_path).replace('.md', '')
        companions = []
        strip = base.lstrip('0123456789-')
        if any(os.path.basename(z).lstrip('0123456789-') == strip for z in glob.glob(os.path.join(AUDIT_DIR, '*.zig'))):
            companions.append('zig')
        if any(os.path.basename(p).lstrip('0123456789-') == strip for p in glob.glob(os.path.join(AUDIT_DIR, '*.py'))):
            companions.append('py')
        comp_str = f' [+{"+".join(companions)}]' if companions else ''
        print(f'  ✓ {base}.html{comp_str}')

    print(f'\n✓ {len(generated)} Stupas generated')


if __name__ == '__main__':
    main()
