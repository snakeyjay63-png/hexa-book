#!/usr/bin/env python3
"""Generate art.html files from audit markdown articles.

De vorm groeit uit de tekst. Niet template → kleur wisselen.
De generator leest de tekst en afleidt de visuele structuur.

Elk artikel heeft een eigen hoek, eigen energie, eigen structuur.
De HTML is de visuele manifestatie daarvan.

Intro (4 talen) bepaalt NIET de structuur — de body wel.
"""

import os, glob, re, html as html_mod

AUDIT_DIR = os.path.dirname(os.path.abspath(__file__))


def analyze_text(md_body, filename):
    """Analyseer de tekst en extract visuele eigenschappen.
    
    Splits in intro (meertalig) vs body (inhoudelijke structuur).
    De body bepaalt de visuele vorm, de intro bepaalt de taal-lagen.
    """
    analysis = {
        'title': '',
        'languages': [],
        'structure': 'prose',
        'tone': 'neutral',
        'density': 0.5,
        'direction': 'ltr',
        'has_code': False,
        'has_table': False,
        'has_diagram': False,
        'section_count': 0,
        'language_count': 1,
        'verse_ratio': 0,
        'code_ratio': 0,
        'raw_length': len(md_body),
    }
    
    lines = md_body.split('\n')
    
    # Titel
    for line in lines[:20]:
        if line.startswith('# ') and not line.startswith('## '):
            analysis['title'] = line[2:].strip()
            break
    
    # Talen detecteren (volledige tekst)
    has_arabic = bool(re.search(r'[\u0600-\u06FF]', md_body))
    has_sanskrit = bool(re.search(r'[\u0900-\u097F]', md_body))
    has_greek = bool(re.search(r'[\u0370-\u03FF]', md_body))
    has_dutch = bool(re.search(r'(Muziek|Muziek is|De Terminal|Boek|#\d+)', md_body))
    has_english = bool(re.search(r'(Music|return|sound|lens|count|interface)', md_body, re.I))
    
    if has_arabic: analysis['languages'].append('ar')
    if has_sanskrit: analysis['languages'].append('sa')
    if has_greek: analysis['languages'].append('gr')
    if has_dutch: analysis['languages'].append('nl')
    if has_english: analysis['languages'].append('en')
    
    analysis['language_count'] = len(analysis['languages'])
    if has_arabic and has_sanskrit and has_greek:
        analysis['direction'] = 'mixed'
    elif has_arabic:
        analysis['direction'] = 'rtl'
    
    # Code blocks
    code_blocks = re.findall(r'```.*?```', md_body, re.DOTALL)
    analysis['has_code'] = len(code_blocks) > 0
    analysis['code_ratio'] = len(code_blocks) / max(len(md_body), 1) if code_blocks else 0
    
    # Tabellen & diagrammen
    analysis['has_table'] = bool(re.search(r'\|.*\|.*\|', md_body))
    analysis['has_diagram'] = bool(re.search(r'(┌|┐|└|┘|├|┤|┬|┴|┼)', md_body))
    
    # Secties
    analysis['section_count'] = len(re.findall(r'^## ', md_body, re.MULTILINE))
    
    # ── Body apart analyseren (na intro) ──
    first_h2 = md_body.find('\n## ')
    body_only = md_body[first_h2:] if first_h2 > 0 else md_body
    
    # ── STRUCTUUR (uit body, niet intro) ──
    struct_scores = {'verse': 0, 'terminal': 0, 'technical': 0, 'dark': 0, 'prose': 0}
    
    body_lines = [l for l in body_only.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('---')]
    short_lines = [l for l in body_lines if len(l.strip()) < 60]
    
    # Verse: korte regels + meertalig in body
    body_has_multi = bool(re.search(r'[\u0600-\u06FF]', body_only) and re.search(r'[\u0900-\u097F]', body_only))
    if len(short_lines) > len(body_lines) * 0.5 and body_has_multi:
        struct_scores['verse'] += 3
    if analysis['language_count'] >= 4:
        struct_scores['verse'] += 1
    if analysis['language_count'] >= 3:
        struct_scores['verse'] += 1
    
    # Terminal
    if re.search(r'(Terminal|CPU|command:|GPU|SYNTH)', body_only, re.I):
        struct_scores['terminal'] += 3
    if re.search(r'(Moog|ARP|Buchla|Oberheim|Roland)', body_only):
        struct_scores['terminal'] += 2
    if re.search(r'(140 BPM|filter sweep|arpeggio|breakdown)', body_only, re.I):
        struct_scores['terminal'] += 2
    
    # Technical
    if re.search(r'(ReturnCycle|conventie|architectuur|invariant|validat)', body_only, re.I):
        struct_scores['technical'] += 3
    if analysis['code_ratio'] > 0.3:
        struct_scores['technical'] += 2
    if re.search(r'(def |try |const |fn |struct )', body_only):
        struct_scores['technical'] += 2
    if analysis['has_table'] and analysis['section_count'] > 5:
        struct_scores['technical'] += 1
    
    # Dark
    if re.search(r'(dark|donker|crush|distort|chaos|zwart|noise|scream|bijtend|ruw|drukkend)', body_only, re.I):
        struct_scores['dark'] += 3
    if re.search(r'(sch|black|dark|crush|noise|chaos)', body_only):
        struct_scores['dark'] += 2
    
    # Prose default
    struct_scores['prose'] += analysis['section_count'] * 0.3
    
    analysis['structure'] = max(struct_scores, key=struct_scores.get)
    
    # ── TONE (uit filename + body keywords) ──
    fname = os.path.basename(filename).lower()
    tone_scores = {
        'neutral': 0, 'fire': 0, 'stone': 0, 'wave': 0,
        'dark': 0, 'light': 0, 'spiral': 0, 'organic': 0,
    }
    
    if 'agni' in fname or 'dimensie-1' in fname: tone_scores['fire'] += 3
    if 'vasana' in fname or 'dimensie-2' in fname: tone_scores['stone'] += 3
    if 'e-audio' in fname or 'dimensie-3' in fname: tone_scores['wave'] += 3
    if 'f-retur' in fname or 'dimensie-8' in fname: tone_scores['spiral'] += 3
    if 'aarde' in fname: tone_scores['organic'] += 3
    if 'dimensie-5' in fname or 'dimensie-4' in fname: tone_scores['organic'] += 2
    if 'dimensie-6' in fname: tone_scores['spiral'] += 2
    if 'dimensie-7' in fname: tone_scores['light'] += 3
    if 'dimensie-9' in fname or 'cycle' in fname: tone_scores['spiral'] += 2
    if 'dimensie-10' in fname: tone_scores['stone'] += 2
    if 'dimensie-11' in fname: tone_scores['fire'] += 2
    if 'dimensie-12' in fname: tone_scores['stone'] += 2
    if 'dimensie-13' in fname: tone_scores['organic'] += 2
    if 'dimensie-14' in fname: tone_scores['spiral'] += 2
    if 'dimensie-15' in fname: tone_scores['light'] += 2
    if 'dimensie-16' in fname: tone_scores['spiral'] += 2
    if 'dark-psy' in fname or 'dark' in fname: tone_scores['dark'] += 4
    if 'forest-psy' in fname: tone_scores['organic'] += 3
    if 'full-on' in fname: tone_scores['stone'] += 2
    if 'progressive-psy' in fname: tone_scores['organic'] += 3
    if 'hi-tech' in fname: tone_scores['spiral'] += 3
    if 'genre-interface' in fname: tone_scores['organic'] += 2
    
    # Body keywords override
    if re.search(r'(crush|distort|chaos|zwart)', body_only, re.I): tone_scores['dark'] += 3
    if re.search(r'(warm|zacht|flow|organisch)', body_only, re.I): tone_scores['organic'] += 2
    if re.search(r'(vuur|fire|agni|brand)', body_only, re.I): tone_scores['fire'] += 2
    
    analysis['tone'] = max(tone_scores, key=tone_scores.get)
    
    # ── DENSITY ──
    density = 0.5
    if analysis['structure'] == 'technical': density = 0.7
    elif analysis['structure'] == 'verse': density = 0.4
    elif analysis['structure'] == 'terminal': density = 0.6
    elif analysis['structure'] == 'dark': density = 0.8
    elif analysis['language_count'] >= 4: density = 0.35
    analysis['density'] = density
    
    return analysis


def derive_color(analysis):
    """Kleur afleiden uit tekst-analyse."""
    tone = analysis['tone']
    structure = analysis['structure']
    
    palettes = {
        'fire':    {'bg': '#0a0608', 'fg': '#f0c8a0', 'accent': '#e87040', 'glow': '#ff602088'},
        'stone':   {'bg': '#0c0c10', 'fg': '#b8b8c8', 'accent': '#8888a0', 'glow': '#6666aacc'},
        'wave':    {'bg': '#060a0f', 'fg': '#a0c8e0', 'accent': '#4090d0', 'glow': '#2080e088'},
        'organic': {'bg': '#060a06', 'fg': '#a0d8a0', 'accent': '#40b040', 'glow': '#20a04088'},
        'spiral':  {'bg': '#0a0610', 'fg': '#c8a0e0', 'accent': '#9050d0', 'glow': '#7040c088'},
        'light':   {'bg': '#0a0a08', 'fg': '#e0d8a0', 'accent': '#d0b040', 'glow': '#e0c02088'},
        'dark':    {'bg': '#040406', 'fg': '#808090', 'accent': '#404050', 'glow': '#20204088'},
        'neutral': {'bg': '#0a0a0f', 'fg': '#c0c0d0', 'accent': '#7070a0', 'glow': '#5050a088'},
    }
    
    p = palettes.get(tone, palettes['neutral'])
    
    if structure == 'terminal':
        p = {'bg': '#040804', 'fg': '#80c880', 'accent': '#40a040', 'glow': '#20a02088'}
    
    return p


def generate_visual(analysis, color):
    """Genereer visuele achtergrond gebaseerd op tekst-eigenschappen."""
    tone = analysis['tone']
    structure = analysis['structure']
    accent = color['accent']
    glow = color['glow']
    
    visuals = []
    
    # Multi-taal → taal-lagen
    if analysis['language_count'] >= 3:
        langs = analysis['languages']
        lang_visual = f'\n  <!-- TAAAL-LAGEN: {len(langs)} talen -->\n  <div class="lang-layers">'
        for i, lang in enumerate(langs):
            opacity = 0.15 - (i * 0.03)
            lang_visual += f'\n    <div class="lang-layer lang-{lang}" style="opacity:{opacity}"></div>'
        lang_visual += '\n  </div>'
        visuals.append(lang_visual)
    
    if structure == 'terminal':
        visuals.append(f'''
  <!-- TERMINAL: grid + scanlines -->
  <div class="terminal-bg">
    <svg class="terminal-grid" viewBox="0 0 100 100" preserveAspectRatio="none">
      <pattern id="tgrid" width="2" height="2" patternUnits="userSpaceOnUse">
        <rect width="2" height="2" fill="none" stroke="{accent}" stroke-width="0.05" opacity="0.1"/>
      </pattern>
      <rect width="100" height="100" fill="url(#tgrid)"/>
    </svg>
    <div class="scanlines"></div>
  </div>''')
    
    if structure == 'dark' or tone == 'dark':
        visuals.append(f'''
  <!-- DARK: noise + druk -->
  <div class="dark-bg">
    <div class="noise-layer"></div>
    <div class="vertical-pressure" style="background:linear-gradient(to bottom, {glow}, transparent)"></div>
  </div>''')
    
    if tone == 'fire':
        embers = ''.join(f'<div class="ember ember-{i}" style="--x:{10+i*12}%;--d:{4+i*2}s;--sz:{1+((i%3))*1}px"></div>' for i in range(8))
        visuals.append(f'''
  <!-- AGNI: opstijgende deeltjes -->
  <div class="fire-bg">
    {embers}
  </div>''')
    
    if tone == 'wave':
        waves = ''.join(f'<path class="wave-line wave-{i}" d="M0,{40+i*5} Q25,{35+i*3} 50,{40+i*5} T100,{40+i*5}" fill="none" stroke="{accent}" stroke-width="{2+i}" opacity="{0.20 - i*0.02}"></path>' for i in range(5))
        visuals.append(f'''
  <!-- AUDIO: golflagen -->
  <svg class="wave-bg" viewBox="0 0 100 100" preserveAspectRatio="none">
    {waves}
  </svg>''')
    
    if tone == 'spiral':
        rings = ''.join(f'<circle class="spiral-ring ring-{i}" cx="50" cy="50" r="{5+i*8}" fill="none" stroke="{accent}" stroke-width="{3-i//2}" opacity="{0.20 - i*0.02}"></circle>' for i in range(6))
        visuals.append(f'''
  <!-- SPIRAL: concentrische cirkels -->
  <svg class="spiral-bg" viewBox="0 0 100 100">
    {rings}
  </svg>''')
    
    if tone == 'organic':
        flows = ''.join(f'<path class="flow-line flow-{i}" d="M{i*15},100 Q{20+i*10},{60+i*5} {30+i*10},{20+i*3} T{i*15+50},0" fill="none" stroke="{accent}" stroke-width="0.3" opacity="0.15"></path>' for i in range(4))
        visuals.append(f'''
  <!-- ORGANIC: stromende lijnen -->
  <svg class="organic-bg" viewBox="0 0 100 100">
    {flows}
  </svg>''')
    
    if structure == 'technical':
        visuals.append(f'''
  <!-- TECHNICAL: blueprint grid -->
  <div class="blueprint-bg">
    <svg class="blueprint-grid" viewBox="0 0 100 100" preserveAspectRatio="none">
      <defs>
        <pattern id="bgrid" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="{accent}" stroke-width="0.08" opacity="0.08"/>
        </pattern>
        <pattern id="bgrid-lg" width="50" height="50" patternUnits="userSpaceOnUse">
          <path d="M 50 0 L 0 0 0 50" fill="none" stroke="{accent}" stroke-width="0.12" opacity="0.12"/>
        </pattern>
      </defs>
      <rect width="100" height="100" fill="url(#bgrid)"/>
      <rect width="100" height="100" fill="url(#bgrid-lg)"/>
    </svg>
  </div>''')
    
    if structure == 'verse':
        visuals.append(f'''
  <!-- VERSE: minimalistisch -->
  <div class="verse-bg">
    <div class="verse-dot" style="background:{accent};box-shadow:0 0 30px {glow}"></div>
  </div>''')
    
    return '\n'.join(visuals) if visuals else ''


# ─── CSS Builder (geen .format() meer — f-strings + L-brace escape) ───

CSS_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: {bg};
    color: {fg};
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 300;
    line-height: 1.7;
    overflow-x: hidden;
    min-height: 100vh;
  }

  /* === VISUAL LAYERS === */
  .lang-layers, .terminal-bg, .dark-bg, .fire-bg, .wave-bg, .spiral-bg, .organic-bg, .blueprint-bg, .verse-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
  }
"""

CSS_LANG = """
  .lang-layer {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: radial-gradient(ellipse at 50% 50%, {glow}, transparent 70%);
  }
  .lang-ar { transform: rotate(5deg); }
  .lang-sa { transform: rotate(-3deg); }
  .lang-gr { transform: rotate(2deg); }
  .lang-nl { transform: rotate(-1deg); }
  .lang-en { transform: rotate(0deg); }
"""

CSS_TERMINAL = """
  .terminal-grid { width: 100%; height: 100%; }
  .scanlines {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      {accent}08 2px,
      {accent}08 4px
    );
    animation: scan 8s linear infinite;
  }
  @keyframes scan {
    0% { background-position: 0 0; }
    100% { background-position: 0 100px; }
  }
"""

CSS_DARK = """
  .noise-layer {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    opacity: 0.5;
  }
  .vertical-pressure {
    position: absolute;
    top: 0; left: 20%;
    width: 60%; height: 100%;
    animation: pressure 6s ease-in-out infinite alternate;
  }
  @keyframes pressure {
    0% { opacity: 0.3; transform: scaleY(1); }
    100% { opacity: 0.6; transform: scaleY(1.02); }
  }
"""

CSS_FIRE = """
  .ember {
    position: absolute;
    bottom: -5px;
    left: var(--x);
    width: var(--sz);
    height: var(--sz);
    border-radius: 50%;
    background: {accent};
    box-shadow: 0 0 6px {glow};
    animation: ember-rise var(--d) ease-in-out infinite;
  }
  @keyframes ember-rise {
    0% { bottom: -5px; opacity: 0; transform: translateX(0); }
    20% { opacity: 1; }
    80% { opacity: 0.5; }
    100% { bottom: 105vh; opacity: 0; transform: translateX(calc(var(--x) * 0.5)); }
  }
"""

CSS_WAVE = """
  .wave-bg { width: 100%; height: 100%; }
  .wave-line { animation: wave-drift 6s ease-in-out infinite; }
  .wave-1 { animation-delay: -1s; }
  .wave-2 { animation-delay: -2s; }
  .wave-3 { animation-delay: -3s; }
  .wave-4 { animation-delay: -4s; }
  @keyframes wave-drift {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
  }
"""

CSS_SPIRAL = """
  .spiral-bg { width: 100%; height: 100%; top: 50%; left: 50%; transform: translate(-50%, -50%); }
  .spiral-ring {
    transform-origin: 50% 50%;
    animation: spiral-rotate 40s linear infinite;
  }
  .ring-0 { animation-duration: 10s; animation-direction: normal; }
  .ring-1 { animation-duration: 15s; animation-direction: reverse; }
  .ring-2 { animation-duration: 20s; animation-direction: normal; }
  .ring-3 { animation-duration: 25s; animation-direction: reverse; }
  .ring-4 { animation-duration: 30s; animation-direction: normal; }
  .ring-5 { animation-duration: 40s; animation-direction: reverse; }
  @keyframes spiral-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
"""

CSS_ORGANIC = """
  .organic-bg { width: 100%; height: 100%; }
  .flow-line { animation: flow-drift 12s ease-in-out infinite alternate; }
  .flow-1 { animation-delay: -3s; }
  .flow-2 { animation-delay: -6s; }
  .flow-3 { animation-delay: -9s; }
  @keyframes flow-drift {
    0% { transform: translateY(0) scaleX(1); }
    100% { transform: translateY(-10px) scaleX(1.02); }
  }
"""

CSS_BLUEPRINT = """
  .blueprint-grid { width: 100%; height: 100%; }
"""

CSS_VERSE = """
  .verse-dot {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 4px; height: 4px;
    border-radius: 50%;
    animation: verse-pulse 8s ease-in-out infinite;
  }
  @keyframes verse-pulse {
    0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
    50% { transform: translate(-50%, -50%) scale(2); opacity: 0.2; }
  }
"""

CSS_CONTENT_BASE = """
  /* === CONTENT === */
  .content {
    position: relative;
    z-index: 2;
    max-width: 640px;
    margin: 0 auto;
    padding: 12vh 2rem;
  }

  .meta {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: {accent};
    opacity: 0.4;
    margin-bottom: 2rem;
    border-bottom: 1px solid {accent}1a;
    padding-bottom: 1rem;
  }

  .title {
    font-size: 2rem;
    font-weight: 700;
    color: {fg};
    opacity: 0.8;
    margin: 2rem 0 3rem;
    line-height: 1.3;
    text-align: center;
  }
"""

CSS_VERSE_EXTRA = """
  .verse-block {
    margin: 3rem 0;
    padding: 2rem 0;
    border-bottom: 1px solid {accent}1a;
  }
  .verse-block p {
    margin: 0.5rem 0;
    font-size: 0.9rem;
    opacity: 0.7;
  }
  .lang-ar { font-family: 'Noto Sans Arabic', sans-serif; direction: rtl; }
  .lang-sa { font-family: 'Noto Sans Devanagari', sans-serif; }
  .lang-gr { font-family: 'Noto Sans Greek', sans-serif; font-style: italic; }
  .lang-nl { color: {accent}; opacity: 0.8; }
"""

CSS_TERMINAL_EXTRA = """
  .terminal-block {
    background: {accent}0a;
    border: 1px solid {accent}2a;
    border-radius: 2px;
    padding: 1rem;
    margin: 1.5rem 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
  }
  .terminal-header {
    color: {accent};
    opacity: 0.6;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
  }
"""

CSS_TECHNICAL_EXTRA = """
  .code-block {
    background: {accent}08;
    border-left: 2px solid {accent}3a;
    padding: 1rem;
    margin: 1.5rem 0;
    font-size: 0.8rem;
    overflow-x: auto;
  }
  .diagram {
    background: {accent}05;
    border: 1px solid {accent}1a;
    padding: 1rem;
    margin: 1.5rem 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    white-space: pre;
    line-height: 1.4;
  }
"""

CSS_DARK_EXTRA = """
  .dark-section {
    margin: 3rem 0;
    opacity: 0.6;
  }
  .dark-section h2 {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: {accent};
    opacity: 0.5;
    margin-bottom: 1rem;
  }
  .glitch {
    animation: glitch 4s ease-in-out infinite;
  }
  @keyframes glitch {
    0%, 90%, 100% { transform: translate(0); }
    92% { transform: translate(-2px, 1px); }
    94% { transform: translate(2px, -1px); }
    96% { transform: translate(-1px, 2px); }
    98% { transform: translate(1px, -2px); }
  }
"""

CSS_COMMON = """
  h2 {
    font-size: 1.2rem;
    font-weight: 600;
    color: {fg};
    opacity: 0.7;
    margin: 2.5rem 0 1rem;
  }
  
  h3 {
    font-size: 1rem;
    font-weight: 500;
    color: {fg};
    opacity: 0.6;
    margin: 2rem 0 0.8rem;
  }
  
  p {
    margin: 1rem 0;
    font-size: 0.9rem;
    opacity: 0.7;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    font-size: 0.8rem;
  }
  th, td {
    padding: 0.5rem;
    border: 1px solid {accent}1a;
    text-align: left;
  }
  th {
    color: {accent};
    opacity: 0.5;
    font-weight: 400;
    text-transform: uppercase;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
  }
  
  code {
    background: {accent}10;
    padding: 0.1em 0.3em;
    border-radius: 2px;
    font-size: 0.85em;
  }
  
  pre {
    background: {accent}08;
    padding: 1rem;
    margin: 1.5rem 0;
    overflow-x: auto;
    font-size: 0.8rem;
    border-left: 2px solid {accent}2a;
  }
  
  pre code {
    background: none;
    padding: 0;
  }
  
  blockquote {
    border-left: 2px solid {accent}3a;
    padding-left: 1rem;
    margin: 1.5rem 0;
    opacity: 0.6;
    font-style: italic;
  }
  
  .footer {
    margin-top: 6rem;
    padding-top: 2rem;
    border-top: 1px solid {accent}1a;
    font-size: 0.65rem;
    opacity: 0.3;
    text-align: center;
  }
"""


def generate_css(analysis, color):
    """Genereer CSS gebaseerd op tekst-eigenschappen."""
    tone = analysis['tone']
    structure = analysis['structure']
    accent = color['accent']
    glow = color['glow']
    bg = color['bg']
    fg = color['fg']
    
    def R(s, replacements):
        """Simple replace — no .format() conflicts with CSS braces."""
        for k, v in replacements.items():
            s = s.replace('{' + k + '}', v)
        return s
    
    c = R(CSS_CSS, {'bg': bg, 'fg': fg})
    
    if analysis['language_count'] >= 3:
        c += R(CSS_LANG, {'glow': glow})
    
    if structure == 'terminal':
        c += R(CSS_TERMINAL, {'accent': accent})
    
    if structure == 'dark' or tone == 'dark':
        c += CSS_DARK
    
    if tone == 'fire':
        c += R(CSS_FIRE, {'accent': accent, 'glow': glow})
    
    if tone == 'wave':
        c += CSS_WAVE
    
    if tone == 'spiral':
        c += CSS_SPIRAL
    
    if tone == 'organic':
        c += CSS_ORGANIC
    
    if structure == 'technical':
        c += CSS_BLUEPRINT
    
    if structure == 'verse':
        c += CSS_VERSE
    
    # Content
    c += R(CSS_CONTENT_BASE, {'accent': accent, 'fg': fg})
    
    if structure == 'verse':
        c += R(CSS_VERSE_EXTRA, {'accent': accent})
    elif structure == 'terminal':
        c += R(CSS_TERMINAL_EXTRA, {'accent': accent})
    elif structure == 'technical':
        c += R(CSS_TECHNICAL_EXTRA, {'accent': accent})
    elif structure == 'dark':
        c += R(CSS_DARK_EXTRA, {'accent': accent})
    
    c += R(CSS_COMMON, {'fg': fg, 'accent': accent})
    
    return c


def md_to_html(md_body, analysis):
    """Minimal markdown to HTML, structure-aware."""
    lines = md_body.split('\n')
    html_parts = []
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []
    in_blockquote = False
    quote_buf = []
    
    # Skip frontmatter
    if md_body.startswith('---'):
        parts = md_body.split('---', 2)
        if len(parts) >= 3:
            md_body = parts[2].strip()
            lines = md_body.split('\n')
    
    for line in lines:
        if line.strip() == '---':
            continue
        
        if line.startswith('```'):
            if in_code:
                inner = '\n'.join(code_buf)
                html_parts.append(f'<pre><code>{html_mod.escape(inner)}</code></pre>')
                code_buf = []
                in_code = False
            else:
                in_code = True
                code_buf = []
            continue
        
        if in_code:
            code_buf.append(line)
            continue
        
        if line.startswith('> '):
            if not in_blockquote:
                in_blockquote = True
                quote_buf = []
            quote_buf.append(line[2:])
            continue
        elif in_blockquote:
            html_parts.append(f'<blockquote>{"<br>".join(html_mod.escape(q) for q in quote_buf)}</blockquote>')
            in_blockquote = False
            quote_buf = []
        
        if '|' in line and line.strip():
            if not in_table:
                in_table = True
                table_buf = []
            table_buf.append(line)
            continue
        elif in_table:
            html_parts.append(render_table(table_buf))
            in_table = False
            table_buf = []
        
        if line.startswith('## '):
            html_parts.append(f'<h2>{html_mod.escape(line[3:].strip())}</h2>')
        elif line.startswith('### '):
            html_parts.append(f'<h3>{html_mod.escape(line[4:].strip())}</h3>')
        elif line.startswith('# ') and not line.startswith('## '):
            pass
        elif line.startswith('- '):
            html_parts.append(f'<li>{html_mod.escape(line[2:].strip())}</li>')
        elif line.strip() == '':
            html_parts.append('')
        else:
            processed = html_mod.escape(line.strip())
            if re.search(r'[\u0600-\u06FF]', line):
                processed = f'<span class="lang-ar">{processed}</span>'
            elif re.search(r'[\u0900-\u097F]', line):
                processed = f'<span class="lang-sa">{processed}</span>'
            elif re.search(r'[\u0370-\u03FF]', line):
                processed = f'<span class="lang-gr">{processed}</span>'
            html_parts.append(f'<p>{processed}</p>')
    
    if in_code and code_buf:
        html_parts.append(f'<pre><code>{html_mod.escape("\n".join(code_buf))}</code></pre>')
    if in_blockquote and quote_buf:
        html_parts.append(f'<blockquote>{"<br>".join(html_mod.escape(q) for q in quote_buf)}</blockquote>')
    if in_table and table_buf:
        html_parts.append(render_table(table_buf))
    
    return '\n'.join(html_parts)


def render_table(table_lines):
    """Render markdown table to HTML."""
    if not table_lines:
        return ''
    
    html_out = ['<table>']
    for i, line in enumerate(table_lines):
        cells = [c.strip() for c in line.strip('|').split('|')]
        if all(c.replace('-', '').replace(':', '').strip() == '' for c in cells):
            continue
        tag = 'th' if i == 0 else 'td'
        row = '  <tr>' + ''.join(f'<{tag}>{html_mod.escape(c)}</{tag}>' for c in cells) + '</tr>'
        html_out.append(row)
    
    html_out.append('</table>')
    return '\n'.join(html_out)


def generate_art_html(md_file):
    """Genereer art.html voor een markdown bestand."""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_full = f.read()
    
    analysis = analyze_text(md_full, md_file)
    color = derive_color(analysis)
    
    meta, md_body = parse_frontmatter(md_full)
    title = analysis['title'] or os.path.splitext(os.path.basename(md_file))[0]
    
    visual_html = generate_visual(analysis, color)
    css = generate_css(analysis, color)
    content_html = md_to_html(md_body, analysis)
    
    dim_info = meta.get('article', os.path.basename(md_file))
    structure_label = analysis['structure']
    tone_label = analysis['tone']
    lang_labels = ', '.join(analysis['languages']) if analysis['languages'] else 'nl'
    
    html = f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_mod.escape(title)}</title>
  <meta name="generator" content="gen_art_pieces_v2">
  <meta name="structure" content="{structure_label}">
  <meta name="tone" content="{tone_label}">
  <meta name="languages" content="{lang_labels}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,600;0,700;1,300&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;700&family=Noto+Sans+Devanagari:wght@400;700&family=Noto+Sans+Greek:wght@400;700&display=swap" rel="stylesheet">
  <style>{css}
  </style>
</head>
<body>
{visual_html}

  <main class="content">
    <div class="meta">
      {html_mod.escape(dim_info)} · structuur: {structure_label} · toon: {tone_label}
    </div>
    
    <h1 class="title">{html_mod.escape(title)}</h1>
    
    {content_html}
    
    <div class="footer">
      HEXA-BOEK · {html_mod.escape(title)} · art.html v2
    </div>
  </main>
</body>
</html>'''
    
    return html


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


def main():
    """Genereer art.html voor alle artikelen."""
    md_files = sorted(glob.glob(os.path.join(AUDIT_DIR, '*.md')))
    art_files = [f for f in md_files if not os.path.basename(f).startswith(('TEMPLATE', 'README'))]
    
    generated = 0
    for md_file in art_files:
        base = os.path.splitext(os.path.basename(md_file))[0]
        out_file = os.path.join(AUDIT_DIR, f'{base}.art.html')
        
        try:
            html_content = generate_art_html(md_file)
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            with open(md_file, 'r', encoding='utf-8') as f:
                md_full = f.read()
            analysis = analyze_text(md_full, md_file)
            
            print(f'  {base}: structuur={analysis["structure"]} toon={analysis["tone"]} talen={analysis["language_count"]} code={analysis["code_ratio"]:.1f}')
            generated += 1
        except Exception as e:
            print(f'  ❌ {base}: {e}')
    
    print(f'\n✓ {generated} kunstwerken gegenereerd')


if __name__ == '__main__':
    main()
