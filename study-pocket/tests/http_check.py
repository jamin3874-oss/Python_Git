"""Read-only local HTTP assertions, no Codyssey requests."""
import json
import sys
import urllib.error
import urllib.request

base = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8788'


def request(path, body=None, headers=None):
    req = urllib.request.Request(base + path, data=body, headers=headers or {})
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.headers, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.headers, error.read()


for path, content_type in [('/', 'text/html'), ('/bootstrap.js', 'javascript'), ('/connection.js', 'javascript'), ('/app.js', 'javascript'), ('/workflow.js', 'javascript'), ('/vendor/pdfjs/pdf.min.mjs', 'javascript'), ('/vendor/pdfjs/pdf.worker.min.mjs', 'javascript'), ('/manifest.webmanifest', 'manifest+json'), ('/icons/icon-192.png', 'image/png')]:
    status, headers, body = request(path)
    assert status == 200, (path, status)
    assert content_type in headers.get('Content-Type', ''), (path, headers)
    assert body
for path in ['/.env', '/api/ai.py', '/server.py', '/.git/config']:
    status, _, _ = request(path)
    assert status in (404, 405), (path, status)
status, headers, body = request('/api/ai')
assert status == 200 and 'no-store' in headers.get('Cache-Control', '')
connection = json.loads(body)
assert isinstance(connection.get('server_configured'), bool)
assert connection.get('authenticated') is False
payload = json.dumps({'messages': [{'role': 'user', 'content': 'test'}], 'max_tokens': 32}).encode()
status, _, body = request('/api/ai', payload, {'Content-Type': 'application/json', 'Origin': base})
assert status == 401, (status, body)
assert 'API' in json.loads(body)['error']
status, _, _ = request('/api/ai', payload, {'Content-Type': 'application/json', 'Origin': 'https://evil.example'})
assert status == 403
status, _, body = request('/sw.js')
assert status == 200 and b"startsWith('/api/')" in body
assert b'workflow.js' in body
print('PASS: 9 assets, connection status, source-file isolation, missing key, foreign Origin, API cache exclusion, workflow offline asset')
