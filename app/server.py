"""Local demo server: python3 app/server.py [port]  ->  http://127.0.0.1:8765/
Serves the chat UI, the /api/ask endpoint, the local manual PDFs, and logs feedback to app/feedback.jsonl."""
import json, os, sys, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
HERE = os.path.dirname(os.path.abspath(__file__)); DEMO = os.path.dirname(HERE)
sys.path.insert(0, HERE); import engine
E_ = engine.Engine(); BUILD = engine.build_id()
class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=DEMO, **k)
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path in ("/", "/index.html"): self.path = "/app/index.html"
        if self.path == "/api/info":
            return self.json({"build": BUILD, "chunks": E_.N, "manuals": list(E_.manuals.values()), "inbox": engine.INBOX})
        return super().do_GET()
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/api/ask":
            return self.json({**E_.answer(body.get("q", ""), body.get("history") or []), "build": BUILD})
        if self.path == "/api/feedback":
            with open(os.path.join(HERE, "feedback.jsonl"), "a") as f: f.write(json.dumps({"t": time.time(), **body}) + "\n")
            return self.json({"ok": True})
        self.send_error(404)
    def json(self, o):
        b = json.dumps(o).encode(); self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"Aurora spec assistant prototype (build {BUILD}, {E_.N} passages) on http://127.0.0.1:{port}/")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
