"""Local Python server with the exact Vercel API implementation. No dependencies."""
import argparse
import mimetypes
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from api.ai import handler as AIHandler

ROOT = Path(__file__).resolve().parent / 'dist' / 'public'
mimetypes.add_type('text/javascript', '.mjs')
mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('application/wasm', '.wasm')


class LocalHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if urlsplit(self.path).path not in ('/api/ai', '/api/ai.py'):
            self.send_error(404)
            return
        AIHandler.do_POST(self)

    reply = AIHandler.reply
    do_OPTIONS = AIHandler.do_OPTIONS

    def do_GET(self):
        if urlsplit(self.path).path.startswith('/api/'):
            AIHandler.do_GET(self)
        else:
            super().do_GET()

    def list_directory(self, path):
        self.send_error(404)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        super().end_headers()

    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8788)
    args = parser.parse_args()
    if not (ROOT / 'index.html').exists():
        raise SystemExit('Run npm run build first.')
    print(f'Study Pocket: http://{args.host}:{args.port}', flush=True)
    ThreadingHTTPServer((args.host, args.port), partial(LocalHandler, directory=str(ROOT))).serve_forever()
