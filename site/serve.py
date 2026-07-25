#!/usr/bin/env python3
"""hexa-book local server — serve the site + media from engine/"""

import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
SITE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SITE_DIR)

class Handler(http.server.SimpleHTTPRequestHandler):
    # Force correct MIME types
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.wav': 'audio/wav',
        '.mp3': 'audio/mpeg',
        '.ogg': 'audio/ogg',
        '.ico': 'image/x-icon',
        '.svg': 'image/svg+xml',
    }

    def translate_path(self, path):
        if path.startswith('/site/'):
            return SITE_DIR + path[5:]
        elif path.startswith('/engine/'):
            return os.path.join(REPO_ROOT, 'engine', path[8:])
        elif path.startswith('/audit/') or path.startswith('/articles/') or path.startswith('/charveld/'):
            return os.path.join(REPO_ROOT, path[1:])
        else:
            site_path = os.path.join(SITE_DIR, path.lstrip('/'))
            if os.path.exists(site_path):
                return site_path
            return os.path.join(REPO_ROOT, path.lstrip('/'))

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(REPO_ROOT)
    server = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"Hexa-Boek running on http://localhost:{PORT}")
    print(f"  Site: http://localhost:{PORT}/site/")
    print(f"  Media: http://localhost:{PORT}/engine/")
    server.serve_forever()
