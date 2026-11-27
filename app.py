from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse, os

DATA_FILE = "/data/notes.txt"
HTML = """<!DOCTYPE html><html><head><title>Alok's Live Clipboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:sans-serif;max-width:700px;margin:40px auto;padding:0 20px;background:#121212;color:#eee}
textarea{width:100%;height:250px;background:#1e1e1e;color:#00ff88;border:1px solid #333;padding:12px;font-size:16px;border-radius:8px}
button{margin-top:12px;padding:10px 24px;background:#00ff88;color:#000;border:none;font-weight:bold;border-radius:6px;cursor:pointer}</style></head>
<body><h2>Live Clipboard & Notes</h2><form method="POST">
<textarea name="content" placeholder="Yahan kuch bhi paste karein...">CONTENT_PLACEHOLDER</textarea><br>
<button type="submit">Save & Sync</button></form></body></html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        os.makedirs("/data", exist_ok=True)
        content = open(DATA_FILE).read() if os.path.exists(DATA_FILE) else ""
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.replace("CONTENT_PLACEHOLDER", content).encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode())
        os.makedirs("/data", exist_ok=True)
        with open(DATA_FILE, "w") as f:
            f.write(post_data.get("content", [""])[0])
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

HTTPServer(("0.0.0.0", 8090), Handler).serve_forever()
