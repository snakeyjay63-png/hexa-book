# Hexa-Boek Site

Statische website voor het Hexa-Boek project.

## Lokaal draaien

```bash
# Sitemap genereren (als artikels/media zijn toegevoegd)
python3 site/gen_sitemap.py

# Server starten
python3 site/serve.py 8787

# Open: http://localhost:8787/site/
```

## Media

Audio en video files zitten in `engine/`. Deze zijn te groot voor GitHub (>100MB limiet).
Lokaal: media werkt direct. GitHub Pages: alleen tekst en code.

## Structuur

```
site/
├── index.html      ← hoofdpagina
├── css/main.css    ← styling
├── js/app.js       ← app logica
├── sitemap.json    ← content index (auto-generateerd)
├── serve.py        ← lokaal server
└── README.md       ← dit bestand
```

## GitHub Pages

Werkend via GitHub Pages workflow. Deploy bij elke push naar `main`.
URL: `https://snakeyjay63-png.github.io/hexa-book/`
