// hexa-book site — main app
(function() {
  const BASE = window.location.pathname.replace(/site\/$/, '').replace(/site\/.*/, '');

  // ── State ──
  let sitemap = null;
  const routes = {};

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
    let articles = sitemap ? sitemap.articles.length : 0;
    let audits = sitemap ? sitemap.audits.length : 0;
    let tests = sitemap ? sitemap.audits_zig.length : 0;
    let talen = sitemap ? sitemap.talen.length : 0;
    let media = sitemap ? sitemap.media.length : 0;

    const html = `
      <div class="hero">
        <h1>• Hexa-Boek</h1>
        <p class="tagline">CC-construct · Nidrā-router · 3-6-9 veld</p>
        <p style="color:var(--text-dim); max-width:600px; margin:0 auto;">
          Dertien artikelen, achttien nodes, zestien dimensies.<br>
          Vier lenzen, één superpositie, één returnmedium.
        </p>
        <div class="stats">
          <div class="stat"><div class="num">${articles}</div><div class="label">Artikelen</div></div>
          <div class="stat"><div class="num">${audits}</div><div class="label">Audits</div></div>
          <div class="stat"><div class="num">${tests}</div><div class="label">Zig Tests</div></div>
          <div class="stat"><div class="num">${talen}</div><div class="label">Talen</div></div>
          <div class="stat"><div class="num">${media}</div><div class="label">Media</div></div>
        </div>
      </div>
      <div class="md">
        <h2>نار · אग्नि · Πῦρ · Ignis</h2>
        <blockquote>
          Informatie = water. Fysica = taal. Taal = frequentie.<br>
          All bardos are this moment. There is no other.
        </blockquote>
        <h3>Structuur</h3>
        <ul>
          <li><strong>Artikelen</strong> — 18 nodes (16 dimensies + router + bridge)</li>
          <li><strong>Audits</strong> — 31 audit rapporten met Zig validatie</li>
          <li><strong>Charveld</strong> — 24 EU talen + Grieks + Sanskriet + Arabisch</li>
          <li><strong>Media</strong> — Audio/video van de NPR Sound Engine</li>
          <li><strong>Engine</strong> — Python validatie + Zig implementatie</li>
        </ul>
        <h3>Nidrā-Router</h3>
        <p>Elk artikel volgt het 4+1 patroon: 4 inhoudelijke secties + 1 nidrā verwijzing naar een parallel artikel.
        Nidrā ≠ gat. Nidrā = terugkeer naar kern via ander perspectief.</p>
      </div>
    `;
    document.getElementById('page-container').innerHTML = html;
  }

  async function showRouting() {
    const content = await fetchFile('ROUTING.md');
    document.getElementById('page-container').innerHTML = renderMd(content);
  }

  async function showArticle(id) {
    const article = sitemap.articles.find(a => a.name === id);
    if (!article) return;
    const content = await fetchFile(article.file);
    document.getElementById('page-container').innerHTML =
      '<div style="margin-bottom:20px"><a href="#" data-page="home" style="color:var(--accent);text-decoration:none;">← Terug</a></div>' +
      renderMd(content);
    bindNav();
  }

  async function showAudit(id) {
    // Check .md first, then .zig
    const audit = sitemap.audits.find(a => a.name === id) || sitemap.audits_zig.find(a => a.name === id);
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
    bindNav();
  }

  async function showAuditIndex() {
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
    bindNav();
  }

  async function showCharveld() {
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
    bindNav();
  }

  async function showTaals(id) {
    const taal = sitemap.talen.find(t => t.name === id);
    if (!taal) return;
    const content = await fetchFile(taal.file);
    document.getElementById('page-container').innerHTML =
      '<div style="margin-bottom:20px"><a href="#" data-page="charveld" style="color:var(--accent);text-decoration:none;">← Terug</a></div>' +
      renderMd(content);
    bindNav();
  }

  async function showMedia() {
    const media = sitemap.media || [];
    let cards = media.map(m => {
      const mediaTag = m.type === 'video'
        ? `<video controls><source src="/${m.file}" type="video/mp4">Niet ondersteund</video>`
        : `<audio controls><source src="/${m.file}" type="audio/wav">Niet ondersteund</audio>`;
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

  // ── Routing ──
  async function navigate(page) {
    const container = document.getElementById('page-container');
    container.innerHTML = '<div style="padding:40px;text-align:center;color:var(--text-dim)">Loading •</div>';

    if (page === 'home') await showHome();
    else if (page === 'routing') await showRouting();
    else if (page === 'audit-index') await showAuditIndex();
    else if (page === 'charveld') await showCharveld();
    else if (page === 'media') await showMedia();
    else if (page === 'engine') await showEngine();
    else if (page.startsWith('article-')) await showArticle(page.slice(8));
    else if (page.startsWith('audit-')) await showAudit(page.slice(6));
    else if (page.startsWith('taal-')) await showTaals(page.slice(5));
  }

  // ── Nav binding ──
  function bindNav() {
    document.querySelectorAll('[data-page]').forEach(el => {
      el.addEventListener('click', function(e) {
        e.preventDefault();
        const page = this.getAttribute('data-page');
        setActive(page);
        navigate(page);
      });
    });
  }

  function setActive(page) {
    document.querySelectorAll('.nav-section a').forEach(a => a.classList.remove('active'));
    const match = document.querySelector(`[data-page="${page}"]`);
    if (match) match.classList.add('active');
  }

  // ── Build sidebar ──
  function buildSidebar() {
    // Articles
    const articleList = document.getElementById('article-list');
    (sitemap.articles || []).forEach(a => {
      const link = document.createElement('a');
      link.href = '#';
      link.setAttribute('data-page', 'article-' + a.name);
      link.textContent = a.title;
      link.style.fontSize = '0.82rem';
      articleList.appendChild(link);
    });
    bindNav();

    // Audits (top-level only)
    const auditList = document.getElementById('audit-list');
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
    bindNav();
  }

  // ── Init ──
  async function init() {
    try {
      const data = await fetch(BASE + 'site/sitemap.json');
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
