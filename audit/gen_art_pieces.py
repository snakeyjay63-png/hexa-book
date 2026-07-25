#!/usr/bin/env python3
"""Generate art.html files from audit markdown articles.

Each article gets a unique visual theme based on its dimension/type.
Pattern: sparks for 1, stone for 2, water for 3, etc.
"""

import os, glob, re, html as html_mod

AUDIT_DIR = os.path.dirname(os.path.abspath(__file__))

# Per-dimension visual themes
THEMES = {
    0: {
        'accent': '#6e7bf2',
        'accent_name': 'lens',
        'visual': 'veld',        # 3-6-9 rings
        'element': 'dot',
    },
    1: {
        'accent': '#f2a66e',
        'accent_name': 'agni',
        'visual': 'sparks',      # rising sparks
        'element': 'flame',
    },
    2: {
        'accent': '#a0a0b8',
        'accent_name': 'vasana',
        'visual': 'grid',        # stone grid
        'element': 'stone',
    },
    3: {
        'accent': '#6ec8f2',
        'accent_name': 'audio',
        'visual': 'waves',       # sine waves
        'element': 'pulse',
    },
    4: {
        'accent': '#f26ea6',
        'accent_name': 'aarde',
        'visual': 'particles',   # earth particles
        'element': 'horizon',
    },
    5: {
        'accent': '#a6f26e',
        'accent_name': 'plant',
        'visual': 'grow',        # growing lines
        'element': 'seed',
    },
    6: {
        'accent': '#c86ef2',
        'accent_name': 'pattern',
        'visual': 'hex',         # hexagonal pattern
        'element': 'center',
    },
    7: {
        'accent': '#f2c86e',
        'accent_name': 'light',
        'visual': 'rays',        # light rays
        'element': 'source',
    },
    8: {
        'accent': '#6ef2c8',
        'accent_name': 'return',
        'visual': 'spiral',      # spiral
        'element': 'core',
    },
    9: {
        'accent': '#f2f26e',
        'accent_name': 'cycle',
        'visual': 'orbit',       # orbiting dots
        'element': 'sun',
    },
    'e': {
        'accent': '#6e7bf2',
        'accent_name': 'audio',
        'visual': 'waves',
        'element': 'pulse',
    },
    'f': {
        'accent': '#c86ef2',
        'accent_name': 'return',
        'visual': 'spiral',
        'element': 'core',
    },
}

def get_theme(dim_or_type):
    """Get theme for a dimension number or special type."""
    if dim_or_type in THEMES:
        return THEMES[dim_or_type]
    # Try to extract dimension number
    m = re.search(r'dimensie[- ]?(\d+)', dim_or_type, re.I)
    if m:
        d = int(m.group(1))
        if d in THEMES:
            return THEMES[d]
    # Default theme
    return THEMES[0]

def parse_frontmatter(text):
    """Parse YAML frontmatter."""
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
    return meta, body

def extract_title(md_body, filename):
    """Extract title from markdown or filename."""
    for line in md_body.split('\n')[:20]:
        line = line.strip()
        if line.startswith('# ') and not line.startswith('## '):
            return line[2:].strip()
    # Fallback: derive from filename
    base = os.path.splitext(os.path.basename(filename))[0]
    return base.replace('-', ' ').title()

def extract_sections(md_body):
    """Extract h2/h3 sections from markdown."""
    sections = []
    current = {'level': 0, 'title': '', 'content': []}
    
    for line in md_body.split('\n'):
        if line.startswith('## '):
            if current['content']:
                sections.append(current)
            current = {'level': 2, 'title': line[3:].strip(), 'content': []}
        elif line.startswith('### '):
            if current['content']:
                sections.append(current)
            current = {'level': 3, 'title': line[4:].strip(), 'content': []}
        else:
            current['content'].append(line)
    
    if current['content']:
        sections.append(current)
    
    return sections

def simple_md_to_html(md_text):
    """Minimal markdown to HTML."""
    lines = md_text.split('\n')
    html_lines = []
    in_code = False
    code_buf = []
    
    for line in lines:
        if line.startswith('```'):
            if in_code:
                inner = '\n'.join(code_buf)
                html_lines.append(f'<pre><code>{html_mod.escape(inner)}</code></pre>')
                code_buf = []
                in_code = False
            else:
                code_buf = []
                in_code = True
            continue
        
        if in_code:
            code_buf.append(line)
            continue
        
        if line.startswith('## '):
            html_lines.append(f'<h2>{html_mod.escape(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{html_mod.escape(line[4:])}</h3>')
        elif line.startswith('- '):
            html_lines.append(f'<li>{html_mod.escape(line[2:])}</li>')
        elif line.strip() == '':
            html_lines.append('')
        else:
            html_lines.append(f'<p>{html_mod.escape(line)}</p>')
    
    return '\n'.join(html_lines)

def generate_visual_html(theme):
    """Generate the visual background HTML based on theme."""
    accent = theme['accent']
    visual = theme['visual']
    element = theme['element']
    accent_name = theme['accent_name']
    
    visuals = {
        'veld': f'''
  <!-- VELD — 3-6-9 ringen -->
  <div class="veld">
    <div class="ring ring-3" style="border-color:{accent}22"></div>
    <div class="ring ring-6" style="border-color:{accent}11"></div>
    <div class="ring ring-9" style="border-color:{accent}0a"></div>
  </div>
  <div class="dot-container">
    <div class="dot" style="background:{accent};box-shadow:0 0 40px {accent}4d"></div>
  </div>''',
        
        'sparks': f'''
  <!-- SPARKS -->
  <div class="spark-field">
    <div class="spark" style="background:{accent};box-shadow:0 0 6px {accent}66"></div>
    <div class="spark" style="background:{accent};box-shadow:0 0 6px {accent}66"></div>
    <div class="spark" style="background:{accent};box-shadow:0 0 6px {accent}66"></div>
    <div class="spark" style="background:{accent};box-shadow:0 0 6px {accent}66"></div>
    <div class="spark" style="background:{accent};box-shadow:0 0 6px {accent}66"></div>
    <div class="spark" style="background:{accent};box-shadow:0 0 6px {accent}66"></div>
  </div>
  <div class="flame" style="background:{accent};box-shadow:0 0 60px {accent}33"></div>''',
        
        'grid': f'''
  <!-- GRID -->
  <div class="grid-field">
    <svg viewBox="0 0 100 100" class="grid-svg">
      <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
        <path d="M 10 0 L 0 0 0 10" fill="none" stroke="{accent}" stroke-width="0.1" opacity="0.2"/>
      </pattern>
      <rect width="100" height="100" fill="url(#grid)"/>
    </svg>
  </div>
  <div class="stone" style="background:{accent}"></div>''',
        
        'waves': f'''
  <!-- WAVES -->
  <svg class="wave-field" viewBox="0 0 100 100" preserveAspectRatio="none">
    <path d="M0,50 Q25,40 50,50 T100,50" fill="none" stroke="{accent}" stroke-width="0.3" opacity="0.2">
      <animate attributeName="d" dur="4s" repeatCount="indefinite"
        values="M0,50 Q25,40 50,50 T100,50;M0,50 Q25,60 50,50 T100,50;M0,50 Q25,40 50,50 T100,50"/>
    </path>
    <path d="M0,50 Q25,45 50,50 T100,50" fill="none" stroke="{accent}" stroke-width="0.2" opacity="0.15">
      <animate attributeName="d" dur="6s" repeatCount="indefinite"
        values="M0,50 Q25,45 50,50 T100,50;M0,50 Q25,55 50,50 T100,50;M0,50 Q25,45 50,50 T100,50"/>
    </path>
  </svg>
  <div class="pulse" style="background:{accent};box-shadow:0 0 40px {accent}4d"></div>''',
        
        'particles': f'''
  <!-- PARTICLES -->
  <canvas id="particle-canvas" class="particle-field"></canvas>
  <div class="horizon" style="border-color:{accent}33"></div>''',
        
        'hex': f'''
  <!-- HEX -->
  <svg class="hex-field" viewBox="0 0 100 100">
    <polygon points="50,10 90,30 90,70 50,90 10,70 10,30" fill="none" stroke="{accent}" stroke-width="0.2" opacity="0.2"/>
    <polygon points="50,20 80,35 80,65 50,80 20,65 20,35" fill="none" stroke="{accent}" stroke-width="0.2" opacity="0.15"/>
    <polygon points="50,30 70,40 70,60 50,70 30,60 30,40" fill="none" stroke="{accent}" stroke-width="0.2" opacity="0.1"/>
  </svg>
  <div class="center" style="background:{accent}"></div>''',
        
        'rays': f'''
  <!-- RAYS -->
  <div class="ray-field">
    <div class="ray" style="background:linear-gradient({accent}22,transparent)"></div>
    <div class="ray" style="background:linear-gradient({accent}18,transparent)"></div>
    <div class="ray" style="background:linear-gradient({accent}11,transparent)"></div>
  </div>
  <div class="source" style="background:{accent};box-shadow:0 0 80px {accent}4d"></div>''',
        
        'spiral': f'''
  <!-- SPIRAL -->
  <svg class="spiral-field" viewBox="0 0 100 100">
    <path d="M50,50 Q60,50 60,40 Q60,30 50,30 Q40,30 40,45 Q40,60 55,60 Q70,60 70,45 Q70,25 50,25 Q25,25 25,50 Q25,75 55,75 Q85,75 85,50 Q85,15 50,15" 
      fill="none" stroke="{accent}" stroke-width="0.3" opacity="0.2">
      <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="60s" repeatCount="indefinite"/>
    </path>
  </svg>
  <div class="core" style="background:{accent};box-shadow:0 0 40px {accent}4d"></div>''',
        
        'orbit': f'''
  <!-- ORBIT -->
  <svg class="orbit-field" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="30" fill="none" stroke="{accent}" stroke-width="0.15" opacity="0.2">
      <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="30s" repeatCount="indefinite"/>
    </circle>
    <circle cx="50" cy="50" r="20" fill="none" stroke="{accent}" stroke-width="0.15" opacity="0.15">
      <animateTransform attributeName="transform" type="rotate" from="360 50 50" to="0 50 50" dur="20s" repeatCount="indefinite"/>
    </circle>
    <circle cx="50" cy="50" r="40" fill="none" stroke="{accent}" stroke-width="0.1" opacity="0.1">
      <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="45s" repeatCount="indefinite"/>
    </circle>
  </svg>
  <div class="sun" style="background:{accent};box-shadow:0 0 60px {accent}4d"></div>''',
    }
    
    return visuals.get(visual, visuals['veld'])

def generate_common_css(accent):
    """Generate shared CSS with accent color."""
    return f'''
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: #0a0a0f;
    color: #e0e0e8;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 300;
    line-height: 1.7;
    overflow-x: hidden;
    min-height: 100vh;
  }}

  /* === VELD / VISUAL BACKGROUNDS === */
  .veld, .spark-field, .grid-field, .wave-field, .particle-field, .hex-field, .ray-field, .spiral-field, .orbit-field {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
  }}

  .veld {{ top: 50%; left: 50%; transform: translate(-50%, -50%); }}
  .ring {{
    position: absolute;
    border-radius: 50%;
    border: 1px solid {accent}22;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }}
  .ring-3 {{ width: 30vw; height: 30vw; animation: breathe 9s ease-in-out infinite; }}
  .ring-6 {{ width: 60vw; height: 60vw; animation: breathe 18s ease-in-out infinite; }}
  .ring-9 {{ width: 90vw; height: 90vw; animation: breathe 27s ease-in-out infinite; }}

  @keyframes breathe {{
    0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 1; }}
    50% {{ transform: translate(-50%, -50%) scale(1.04); opacity: 0.6; }}
  }}

  .dot-container, .flame, .stone, .pulse, .horizon, .center, .source, .core, .sun {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1;
    pointer-events: none;
  }}

  .dot, .pulse, .core {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    animation: pulse-dot 6s ease-in-out infinite;
  }}

  .flame {{
    width: 4px;
    height: 4px;
    border-radius: 50%;
    animation: flicker 2s ease-in-out infinite;
  }}

  .stone {{
    width: 8px;
    height: 8px;
  }}

  .horizon {{
    width: 60vw;
    height: 1px;
  }}

  .center {{
    width: 4px;
    height: 4px;
    border-radius: 50%;
  }}

  .source {{
    width: 3px;
    height: 3px;
    border-radius: 50%;
    animation: pulse-dot 4s ease-in-out infinite;
  }}

  .sun {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    animation: pulse-dot 8s ease-in-out infinite;
  }}

  @keyframes pulse-dot {{
    0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.8; }}
    50% {{ transform: translate(-50%, -50%) scale(1.8); opacity: 0.4; }}
  }}

  @keyframes flicker {{
    0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.8; }}
    25% {{ transform: translate(-50%, -50%) scale(1.6); opacity: 1; }}
    50% {{ transform: translate(-50%, -50%) scale(1.2); opacity: 0.6; }}
    75% {{ transform: translate(-50%, -50%) scale(1.8); opacity: 0.9; }}
  }}

  .spark {{
    position: absolute;
    width: 2px;
    height: 2px;
    border-radius: 50%;
    animation: rise linear infinite;
  }}
  .spark:nth-child(1) {{ left: 10%; animation-duration: 8s; animation-delay: 0s; }}
  .spark:nth-child(2) {{ left: 25%; animation-duration: 12s; animation-delay: 2s; width: 3px; height: 3px; }}
  .spark:nth-child(3) {{ left: 40%; animation-duration: 9s; animation-delay: 4s; }}
  .spark:nth-child(4) {{ left: 55%; animation-duration: 11s; animation-delay: 1s; }}
  .spark:nth-child(5) {{ left: 70%; animation-duration: 10s; animation-delay: 3s; }}
  .spark:nth-child(6) {{ left: 85%; animation-duration: 7s; animation-delay: 5s; width: 3px; height: 3px; }}

  @keyframes rise {{
    0% {{ bottom: -10px; opacity: 0; transform: translateX(0); }}
    10% {{ opacity: 1; }}
    90% {{ opacity: 0.6; }}
    100% {{ bottom: 110vh; opacity: 0; transform: translateX(20px); }}
  }}

  .grid-svg, .hex-field, .spiral-field, .orbit-field, .wave-field {{
    width: 100%;
    height: 100%;
  }}

  /* === CONTENT === */
  .content {{
    position: relative;
    z-index: 2;
    max-width: 600px;
    margin: 0 auto;
    padding: 14vh 2rem;
  }}

  .dim-tag {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: {accent};
    opacity: 0.5;
    margin-bottom: 1rem;
  }}

  .lens-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.3em 1em;
    margin-bottom: 4rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid {accent}1f;
  }}

  .lens {{
    font-size: 0.8rem;
    opacity: 0.5;
  }}
  .lens.ar {{ font-family: 'Noto Sans Arabic', sans-serif; direction: rtl; }}
  .lens.sa {{ font-family: 'Noto Sans Devanagari', sans-serif; }}
  .lens.gr {{ font-family: 'Noto Sans Greek', sans-serif; font-style: italic; }}

  .title {{
    font-size: 2.2rem;
    font-weight: 700;
    color: {accent};
    opacity: 0.7;
    margin: 3rem 0;
    text-align: center;
    line-height: 1.3;
  }}

  .title .dr {{
    display: block;
    font-size: 0.9rem;
    font-weight: 300;
    opacity: 0.4;
    margin-top: 0.5rem;
    letter-spacing: 0.15em;
  }}

  .verse {{ margin: 2.5rem 0; }}
  .verse p {{ margin: 0.6rem 0; font-size: 0.88rem; opacity: 0.7; }}
  .verse .ar {{ font-family: 'Noto Sans Arabic', sans-serif; direction: rtl; opacity: 0.5; }}
  .verse .sa {{ font-family: 'Noto Sans Devanagari', sans-serif; opacity: 0.5; }}
  .verse .gr {{ font-family: 'Noto Sans Greek', sans-serif; font-style: italic; opacity: 0.5; }}
  .verse .nl {{ font-style: italic; color: {accent}; opacity: 0.6; }}

  .section {{ margin: 2.5rem 0; }}
  .section p {{ margin: 1rem 0; font-size: 0.88rem; opacity: 0.7; }}
  .section h2 {{
    font-size: 1rem;
    font-weight: 700;
    margin: 3rem 0 1.5rem;
    color: {accent};
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }}
  .section h3 {{
    font-size: 0.85rem;
    font-weight: 700;
    margin: 2rem 0 1rem;
    opacity: 0.6;
  }}

  pre {{
    background: {accent}0a;
    border-left: 2px solid {accent}33;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0;
    overflow-x: auto;
    font-size: 0.78rem;
    line-height: 1.6;
    color: {accent}cc;
  }}

  code {{
    background: {accent}14;
    padding: 0.1em 0.3em;
    border-radius: 3px;
    font-size: 0.82em;
    color: {accent}bb;
  }}

  .status {{
    margin: 3rem 0;
    padding: 1.5rem;
    background: {accent}08;
    border-left: 2px solid {accent}33;
    font-size: 0.78rem;
    line-height: 1.8;
    color: {accent}cc;
  }}

  .lens-optiek {{
    margin: 4rem 0;
    padding: 2rem;
    border: 1px solid {accent}1f;
    border-radius: 4px;
  }}
  .lens-optiek p {{
    margin: 0.8rem 0;
    font-size: 0.8rem;
    opacity: 0.5;
    font-style: italic;
  }}
  .lens-optiek .label {{
    font-weight: 700;
    opacity: 0.7;
    font-style: normal;
    color: {accent};
  }}

  .footer {{
    margin-top: 8rem;
    padding-top: 2rem;
    border-top: 1px solid {accent}1a;
    text-align: center;
    font-size: 0.7rem;
    opacity: 0.3;
    letter-spacing: 0.1em;
  }}
  .footer a {{
    color: {accent};
    text-decoration: none;
    opacity: 0.7;
  }}
  .footer a:hover {{ opacity: 1; }}

  @media (max-width: 600px) {{
    .title {{ font-size: 1.6rem; }}
    .content {{ padding: 10vh 1.2rem; }}
    .ring-3 {{ width: 50vw; height: 50vw; }}
    .ring-6 {{ width: 80vw; height: 80vw; }}
    .ring-9 {{ width: 120vw; height: 120vw; }}
  }}
'''

def generate_art_piece(md_path):
    """Generate a single .art.html from a .md file."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    meta, body = parse_frontmatter(text)
    base = os.path.splitext(os.path.basename(md_path))[0]
    title = extract_title(body, md_path)
    
    # Determine theme
    theme = get_theme(base)
    accent = theme['accent']
    
    # Build HTML
    html = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(title)}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;700&family=Noto+Sans+Devanagari:wght@300;700&family=Noto+Sans+Greek:wght@300;700&family=IBM+Plex+Mono:wght@300;700&display=swap');
{generate_common_css(accent)}
</style>
</head>
<body>

{generate_visual_html(theme)}

  <!-- INHOUD -->
  <div class="content">

    <div class="dim-tag">{html_mod.escape(base).replace('-', ' ')}</div>

    <!-- TITEL -->
    <div class="title">
      {html_mod.escape(title)}
      <span class="dr">{html_mod.escape(base)}</span>
    </div>

    <!-- CONTENT -->
    <div class="section">
{simple_md_to_html(body)}
    </div>

    <!-- FOOTER -->
    <div class="footer">
      <a href="#" data-page="stupas">← terug naar Hexa-Boek</a>
    </div>

  </div>

<script>
  document.querySelector('.footer a').addEventListener('click', function(e) {{
    e.preventDefault();
    if (window.history.length > 1) window.history.back();
    else window.location.hash = 'stupas';
  }});
</script>
</body>
</html>
'''
    
    out_path = md_path.replace('.md', '.art.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return out_path

def main():
    """Generate all art pieces."""
    md_files = sorted(glob.glob(os.path.join(AUDIT_DIR, '*.md')))
    count = 0
    
    for md_path in md_files:
        base = os.path.basename(md_path)
        # Skip INDEX and TEMPLATE
        if base in ('INDEX.md', 'TEMPLATE.md', 'TEMPLATE-genre.md'):
            continue
        
        out_path = md_path.replace('.md', '.art.html')
        # Check if already exists
        if os.path.exists(out_path):
            print(f'  ⊘ {os.path.basename(out_path)} (already exists)')
            continue
        
        generate_art_piece(md_path)
        print(f'  ✓ {os.path.basename(out_path)}')
        count += 1
    
    print(f'\n✓ {count} new art pieces generated')

if __name__ == '__main__':
    main()
