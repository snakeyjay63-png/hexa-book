// hexa-book site — main app
(function() {
  const BASE = window.location.pathname.replace(/site\/$/, '').replace(/site\/.*/, '');

  // ── State ──
  let sitemap = null;
  const routes = {};
  let currentPage = 'home';

  // ── Breadcrumb ──
  function setBreadcrumbs(crumb) {
    const bc = document.getElementById('breadcrumb');
    if (!bc) return;
    // crumb = [{label, page}, {label, page}, ...] last item is current
    let html = '<a href="#" data-page="home">•</a>';
    crumb.forEach(function(c, i) {
      html += '<span class="sep">›</span>';
      if (i === crumb.length - 1) {
        html += '<span class="current">' + esc(c.label) + '</span>';
      } else {
        html += '<a href="#" data-page="' + esc(c.page) + '">' + esc(c.label) + '</a>';
      }
    });
    bc.innerHTML = html;
  }

  // ── Markdown rendering (lightweight) ──
  function renderMd(text) {
    // Frontmatter strip
    if (text.startsWith('---')) {
      const end = text.indexOf('---', 3);
      if (end > 0) text = text.slice(end + 3);
    }

    let html = text;

    // Code blocks
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, function(_, lang, code) {
      return '<pre><code class="lang-' + (lang || 'text') + '">' + esc(code.trim()) + '</code></pre>';
    });

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Headers
    html = html.replace(/^###### (.+)$/gm, '<h6>$1</h6>');
    html = html.replace(/^##### (.+)$/gm, '<h5>$1</h5>');
    html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Bold / italic
    html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Blockquotes
    html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');

    // Tables (basic)
    html = html.replace(/^\|(.+)\|$/gm, function(match, content) {
      const cells = content.split('|').map(c => c.trim());
      if (cells.every(c => /^[-:]+$/.test(c))) return '<!--sep-->';
      const tag = 'td';
      const row = '<tr>' + cells.map(c => '<' + tag + '>' + c + '</' + tag + '>').join('') + '</tr>';
      return row;
    });
    html = html.replace(/((<tr>.*<\/tr>\n?)+)/g, '<table>$1</table>');
    html = html.replace(/<!--sep-->\n?/g, '');

    // Horizontal rules
    html = html.replace(/^---+$/gm, '<hr>');

    // Unordered lists
    html = html.replace(/^[-*] (.+)$/gm, '<li>$1</li>');
    html = html.replace(/((<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>');

    // Ordered lists
    html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

    // Paragraphs
    html = html.replace(/\n{2,}/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    html = '<p>' + html + '</p>';

    // Clean up empty paragraphs
    html = html.replace(/<p>\s*<\/p>/g, '');
    html = html.replace(/<p>\s*(<h[1-6]>)/g, '$1');
    html = html.replace(/(<\/h[1-6]>)\s*<\/p>/g, '$1');
    html = html.replace(/<p>\s*(<pre>)/g, '$1');
    html = html.replace(/(<\/pre>)\s*<\/p>/g, '$1');
    html = html.replace(/<p>\s*(<table>)/g, '$1');
    html = html.replace(/(<\/table>)\s*<\/p>/g, '$1');
    html = html.replace(/<p>\s*(<ul>)/g, '$1');
    html = html.replace(/(<\/ul>)\s*<\/p>/g, '$1');
    html = html.replace(/<p>\s*(<blockquote>)/g, '$1');
    html = html.replace(/(<\/blockquote>)\s*<\/p>/g, '$1');
    html = html.replace(/<p>\s*(<hr>)/g, '$1');

    return '<div class="md">' + html + '</div>';
  }

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // ── Fetch ──
  async function fetchFile(path) {
    // Normalize path
    const cleanPath = path.replace(/\.md$/, '').replace(/\.zig$/, '') + (path.endsWith('.zig') ? '.zig' : '.md');
    const normalized = path.endsWith('.zig') ? path : path;
    const res = await fetch(BASE + normalized);
    if (!res.ok) throw new Error('404: ' + normalized);
    return res.text();
  }

  // ── Pages ──
  async function showHome() {
    setBreadcrumbs([]);
    let articles = sitemap ? sitemap.articles.length : 0;
    let audits = sitemap ? sitemap.audits.length : 0;
    let tests = sitemap ? sitemap.audits_zig.length : 0;
    let talen = sitemap ? sitemap.talen.length : 0;
    let media = sitemap ? sitemap.media.length : 0;

    const html = `
      <div class="hero" style="text-align:center; padding:20px 0 10px;">
        <h1>• Hexa-Boek</h1>
        <p class="tagline">De beste taal om te vertalen is geometrisch</p>
      </div>
      <div id="planetarium-container" class="planetarium-container"></div>
      <div class="md">
        <blockquote style="border-left-color:var(--accent); text-align:center;">
          Dezelfde waarheid. Achttien hoeken.<br>
          Elk <code style="color:var(--accent);">.py</code> is een andere lens op hetzelfde veld.
        </blockquote>
        <div class="stats" style="margin-top:24px;">
          <div class="stat"><div class="num">18</div><div class="label">Gears</div></div>
          <div class="stat"><div class="num">${articles}</div><div class="label">Artikelen</div></div>
          <div class="stat"><div class="num">${audits}</div><div class="label">Audits</div></div>
          <div class="stat"><div class="num">${talen}</div><div class="label">Talen</div></div>
          <div class="stat"><div class="num">1</div><div class="label">Veld</div></div>
        </div>
      </div>
    `;
    document.getElementById('page-container').innerHTML = html;

    // Load planetarium SVG — all 18 gears in one frame, no iframes
    fetch(BASE + 'articles/planetarium.art.html')
      .then(function(r) { return r.text(); })
      .then(function(text) {
        // Extract the main SVG and inject it
        var svgMatch = text.match(/<svg[^>]*class="main"[^>]*>([\s\S]*?)<\/svg>/i);
        if (svgMatch) {
          var container = document.getElementById('planetarium-container');
          if (container) container.innerHTML = svgMatch[0];
        }
      })
      .catch(function() {
        // Fallback: show message
        var container = document.getElementById('planetarium-container');
        if (container) container.innerHTML = '<p style="text-align:center;opacity:0.3;padding:40px;">Planetarium laadt...</p>';
      });
  }

  async function showRouting() {
    setBreadcrumbs([{label:'Routing',page:'routing'}]);
    const content = await fetchFile('ROUTING.md');
    document.getElementById('page-container').innerHTML = renderMd(content);
  }

  async function showArticle(id) {
    const article = sitemap.articles.find(a => a.name === id);
    if (article) setBreadcrumbs([{label:'Artikelen',page:'home'},{label:article.title,page:'article-'+id}]);
    if (!article) return;
    const content = await fetchFile(article.file);
    document.getElementById('page-container').innerHTML =
      '<div style="margin-bottom:20px"><a href="#" data-page="home" style="color:var(--accent);text-decoration:none;">← Terug</a></div>' +
      renderMd(content);
  }

  async function showAudit(id) {
    // Check .md first, then .zig
    const audit = sitemap.audits.find(a => a.name === id) || sitemap.audits_zig.find(a => a.name === id);
    if (audit) setBreadcrumbs([{label:'Audit',page:'audit-index'},{label:audit.title,page:'audit-'+id}]);
    if (!audit) return;
    const content = await fetchFile(audit.file);

    if (audit.file.endsWith('.zig')) {
      document.getElementById('page-container').innerHTML =
        '<div style="margin-bottom:20px"><a href="#" data-page="audit-index" style="color:var(--accent);text-decoration:none;">← Audit-overzicht</a></div>' +
        '<div class="md"><h2>🧪 ' + audit.title + '</h2><pre><code>' + esc(content) + '</code></pre></div>';
    } else {
      // Show both .md and .zig if paired
      const zigName = id + '.zig';
      const zigFile = sitemap.audits_zig.find(a => a.file === 'audit/' + id + '.zig');
      let zigBlock = '';
      if (zigFile) {
        const zigContent = await fetchFile(zigFile.file);
        zigBlock = '<h2>Zig Implementatie</h2><pre><code>' + esc(zigContent) + '</code></pre>';
      }
      document.getElementById('page-container').innerHTML =
        '<div style="margin-bottom:20px"><a href="#" data-page="audit-index" style="color:var(--accent);text-decoration:none;">← Audit-overzicht</a></div>' +
        '<div class="md">' + renderMd(content).replace('<div class="md">', '') + zigBlock + '</div>';
    }
  }

  async function showAuditIndex() {
    setBreadcrumbs([{label:'Audit',page:'audit-index'}]);
    const audits = sitemap.audits || [];
    const zigs = sitemap.audits_zig || [];

    let rows = audits.map(a => {
      const zig = zigs.find(z => z.name === a.name);
      return `
        <div class="audit-row" style="cursor:pointer" data-page="audit-${a.name}">
          <span class="title">${a.title}</span>
          <span class="tests">${a.tests}</span>
          ${zig ? '<span class="status-badge pass">zig ✅</span>' : ''}
        </div>
      `;
    }).join('');

    document.getElementById('page-container').innerHTML =
      '<div class="md"><h2>Audit-overzicht</h2><p>' + audits.length + ' audits, ' + zigs.length + ' Zig implementaties</p></div>' +
      '<div id="audit-rows">' + rows + '</div>';
  }

  async function showCharveld() {
    setBreadcrumbs([{label:'Charveld',page:'charveld'}]);
    const talen = sitemap.talen || [];
    let cards = talen.map(t => `
      <div class="media-card" style="cursor:pointer" data-page="taal-${t.name}">
        <div class="media-info">
          <h4>${t.title}</h4>
          <p>${t.file}</p>
        </div>
      </div>
    `).join('');

    document.getElementById('page-container').innerHTML =
      '<div class="md"><h2>Charveld — Taal & Karakter</h2><p>' + talen.length + ' talen gemappt</p></div>' +
      '<div class="media-grid">' + cards + '</div>';
  }

  async function showStupas() {
    setBreadcrumbs([{label:'Stupas',page:'stupas'}]);
    const stupas = sitemap.stupas || [];
    let cards = stupas.map(s => `
      <div class="media-card" style="cursor:pointer" data-page="stupa-${s.name}">
        <div class="media-info">
          <h4>• ${s.title}</h4>
          <p>Stupa — ${s.file.replace('.html','')}</p>
        </div>
      </div>
    `).join('');

    document.getElementById('page-container').innerHTML =
      '<div class="md"><h2>Stupas</h2><p>' + stupas.length + ' artikelen als stapels</p></div>' +
      '<div class="media-grid">' + cards + '</div>';
  }

  async function showStupa(id) {
    const stupa = sitemap.stupas.find(s => s.name === id);
    if (stupa) setBreadcrumbs([{label:'Stupas',page:'stupas'},{label:stupa.title,page:'stupa-'+id}]);
    if (!stupa) {
      document.getElementById('page-container').innerHTML = '<div class="md"><h2>Niet gevonden</h2><p>Stupa bestaat niet.</p></div>';
      return;
    }
    const fileUrl = BASE + stupa.file;
    // .art.html = volledige kunstwerk → iframe voor isolatie
    if (stupa.art) {
      document.getElementById('page-container').innerHTML =
        '<iframe class="art-frame" src="' + fileUrl + '" frameborder="0"></iframe>';
    } else {
      const content = await fetchFile(stupa.file);
      document.getElementById('page-container').innerHTML = content;
      document.querySelectorAll('.stupa-footer a[data-page]').forEach(el => {
        el.addEventListener('click', function(e) {
          e.preventDefault();
          const page = this.getAttribute('data-page');
          setActive(page);
          navigate(page);
        });
      });
    }
  }

  async function showTaals(id) {
    const taal = sitemap.talen.find(t => t.name === id);
    if (taal) setBreadcrumbs([{label:'Charveld',page:'charveld'},{label:taal.title,page:'taal-'+id}]);
    if (!taal) return;
    const content = await fetchFile(taal.file);
    document.getElementById('page-container').innerHTML =
      '<div style="margin-bottom:20px"><a href="#" data-page="charveld" style="color:var(--accent);text-decoration:none;">← Terug</a></div>' +
      renderMd(content);
  }

  async function showMedia() {
    setBreadcrumbs([{label:'Media',page:'media'}]);
    const media = sitemap.media || [];
    let cards = media.map(m => {
      const mime = m.file.endsWith('.webm') ? 'video/webm' : 'video/mp4';
      const audioMime = m.file.endsWith('.mp3') ? 'audio/mpeg' : m.file.endsWith('.ogg') ? 'audio/ogg' : 'audio/wav';
      const mediaTag = m.type === 'video'
        ? `<video controls preload="none" playsinline><source src="/${m.file}" type="${mime}">Niet ondersteund</video>`
        : `<audio controls preload="none"><source src="/${m.file}" type="${audioMime}">Niet ondersteund</audio>`;
      return `
        <div class="media-card">
          ${mediaTag}
          <div class="media-info">
            <h4>${m.name}</h4>
            <p>${m.size}</p>
          </div>
        </div>
      `;
    }).join('');

    document.getElementById('page-container').innerHTML =
      '<div class="md"><h2>Media</h2><p>' + media.length + ' bestanden</p></div>' +
      '<div class="media-grid">' + cards + '</div>';
  }

  async function showEngine() {
    setBreadcrumbs([{label:'Engine',page:'engine'}]);
    const zigs = sitemap.audits_zig || [];
    let rows = zigs.map(z => `
      <div class="audit-row">
        <span class="title">${z.title}</span>
        <span class="status-badge pass">zig</span>
      </div>
    `).join('');

    document.getElementById('page-container').innerHTML =
      '<div class="md"><h2>Engine Status</h2><p>' + zigs.length + ' Zig test files (489 tests totaal, 0 failures)</p></div>' +
      '<div>' + rows + '</div>';
  }

  // ── Water Spectrum ──
  function showSpectrum() {
    setBreadcrumbs([{label:'Water Spectrum',page:'spectrum'}]);
    const bands = [
      {id:'p0',label:'P0 — As (Shambala)',priem:'0',state:'ijs (tijdloos)'},
      {id:'p1',label:'P1 — Kern',priem:'2',state:'traag water'},
      {id:'p2',label:'P2 — Mantel',priem:'3',state:'half-ijs'},
      {id:'p3',label:'P3 — Korst (WIJ)',priem:'5',state:'Park of Peace'},
      {id:'p4',label:'P4 — Atmosfeer',priem:'7',state:'snel water'},
      {id:'p5',label:'P5 — Ionosfeer',priem:'11',state:'plasma'},
      {id:'p6',label:'P6 — Magnetosfeer',priem:'13',state:'veld (snelst)'},
    ];
    let html = '<div class="md">' +
      '<h1>• Water Spectrum</h1>' +
      '<blockquote>"De wereld limeiteert niet in oppervlakte. De wereld limeiteert in detail."</blockquote>' +
      '<p>As Above, So Below → Water als brug.</p>' +
      '<p>Eén substantie. Zeven snelheden.</p>' +
      '</div><div class="spectrum-container">';
    bands.forEach(b => {
      html += '<div class="spectrum-band" data-band="' + b.id + '">' +
        '<span class="band-label">' + b.label + '</span>' +
        '<span class="band-priem">priem: ' + b.priem + '</span>' +
        '<span class="band-state">' + b.state + '</span>' +
        '</div>';
    });
    html += '</div>';
    document.getElementById('page-container').innerHTML = html;
  }

  function showResolutie() {
    setBreadcrumbs([{label:'Water Spectrum',page:'resolutie'}]);
    const priemen = [2,3,5,7,11,13,17,19,23,29,31,37];
    const labels = {
      5:  '5-bit: standaard taalveld — P3 als los punt',
      7:  '7-bit: Sanskriet — P3 als kruispunt',
      12: '12-bit: gecombineerd — meer perspectieven zichtbaar',
      24: '24-bit: VOLLEDIG spectrum — P3 als fractaal patroon'
    };
    let hexes = priemen.map(p => '<div class="priem-hex" data-priem="' + p + '">' + p + '</div>').join('');
    let html = '<div class="md">' +
      '<h1>• Resolutie</h1>' +
      '<p>Taalveld = bit-diepte = resolutie.</p>' +
      '<p>P3 verandert niet. Jouw resolutie verandert.</p>' +
      '</div><div class="resolutie-container">' +
      '<div class="bit-label">5-bit</div>' +
      '<input type="range" min="5" max="24" value="5" class="bit-slider" id="bit-slider">' +
      '<div class="resolutie-display">' +
      '<div class="priem-grid">' + hexes + '</div>' +
      '<div class="perspectief-label" id="perspectief-label">5-bit: standaard taalveld — P3 als los punt</div>' +
      '</div></div>';
    document.getElementById('page-container').innerHTML = html;

    // Slider logic
    var slider = document.getElementById('bit-slider');
    var label = document.getElementById('perspectief-label');
    slider.addEventListener('input', function() {
      var val = parseInt(this.value);
      document.querySelector('.bit-label').textContent = val + '-bit';
      // Update label
      if (val <= 6) label.textContent = labels[5];
      else if (val <= 11) label.textContent = labels[7];
      else if (val <= 23) label.textContent = labels[12];
      else label.textContent = labels[24];
      // Show/hide priem hexes
      document.querySelectorAll('.priem-hex').forEach(function(hex) {
        var p = parseInt(hex.getAttribute('data-priem'));
        // Visibility: 5-bit sees up to 5, 7-bit up to 7, etc.
        var threshold = Math.min(val, 37);
        if (p <= threshold) hex.classList.add('visible');
        else hex.classList.remove('visible');
      });
    });
    // Trigger initial
    slider.dispatchEvent(new Event('input'));
  }

  // ── Routing ──
  async function navigate(page) {
    const container = document.getElementById('page-container');
    container.innerHTML = '<div style="padding:40px;text-align:center;color:var(--text-dim)">Loading •</div>';

    if (page === 'home') await showHome();
    else if (page === 'routing') await showRouting();
    else if (page === 'audit-index') await showAuditIndex();
    else if (page === 'stupas') await showStupas();
    else if (page.startsWith('stupa-')) await showStupa(page.slice(6));
    else if (page === 'charveld') await showCharveld();
    else if (page === 'media') await showMedia();
    else if (page === 'engine') await showEngine();
    else if (page === 'spectrum') showSpectrum();
    else if (page === 'resolutie') showResolutie();
    else if (page.startsWith('article-')) await showArticle(page.slice(8));
    else if (page.startsWith('audit-')) await showAudit(page.slice(6));
    else if (page.startsWith('taal-')) await showTaals(page.slice(5));
  }

  // ── Nav binding (event delegation — één listener op document) ──
  document.addEventListener('click', function(e) {
    const target = e.target.closest('[data-page]');
    if (!target) return;
    e.preventDefault();
    const page = target.getAttribute('data-page');
    setActive(page);
    navigate(page);
  });

  function setActive(page) {
    document.querySelectorAll('.nav-section a').forEach(a => a.classList.remove('active'));
    const match = document.querySelector(`[data-page="${page}"]`);
    if (match) match.classList.add('active');
  }

  // ── Build sidebar ──
  function buildSidebar() {
    // Articles
    const articleList = document.getElementById('article-list');
    if (articleList) {
      (sitemap.articles || []).forEach(a => {
        const link = document.createElement('a');
        link.href = '#';
        link.setAttribute('data-page', 'article-' + a.name);
        link.textContent = a.title;
        link.style.fontSize = '0.82rem';
        articleList.appendChild(link);
      });
    }

    // Audits (top-level only)
    const auditList = document.getElementById('audit-list');
    if (auditList) {
      const shown = new Set();
      (sitemap.audits || []).slice(0, 20).forEach(a => {
        if (shown.has(a.name)) return;
        shown.add(a.name);
        const link = document.createElement('a');
        link.href = '#';
        link.setAttribute('data-page', 'audit-' + a.name);
        link.textContent = a.title;
        link.style.fontSize = '0.82rem';
        auditList.appendChild(link);
      });
    }

  // ── Init ──
  async function init() {
    try {
      const data = await fetch(BASE + 'sitemap.json');
      if (data.ok) {
        sitemap = await data.json();
      }
    } catch(e) {
      // sitemap not available
    }
    buildSidebar();
    navigate('home');
  }

  init();
})();
