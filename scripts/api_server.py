#!/usr/bin/env python3
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "10000"))
CRM_API_KEY = os.getenv("CRM_API_KEY", "")

class H(BaseHTTPRequestHandler):
def _send(self, code=200, data=None):
b = json.dumps(data or {}).encode()
self.send_response(code)
self.send_header("Content-Type", "application/json")
self.send_header("Access-Control-Allow-Origin", "*")
self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
self.send_header("Content-Length", str(len(b)))
self.end_headers()
self.wfile.write(b)

def _authorized(self):
if not CRM_API_KEY:
return True
return self.headers.get("X-API-Key", "") == CRM_API_KEY

def do_OPTIONS(self):
self._send(200, {"ok": True})

def do_GET(self):
if self.path == "/health":
return self._send(200, {"ok": True, "service": "atlas-crm-api"})
if self.path == "/state":
return self._send(200, {"deals": [], "leads": [], "tasks": []})
return self._send(404, {"error": "not found"})

def do_POST(self):
if not self._authorized():
return self._send(401, {"error": "unauthorized"})
if self.path == "/deal/enrich":
return self._send(200, {
"ok": True,
"written": True,
"id": 1,
"score_total": 72.0,
"score_label": "WATCH"
})
return self._send(404, {"error": "not found"})

if __name__ == "__main__":
print(f"Starting on http://{HOST}:{PORT}")
ThreadingHTTPServer((HOST, PORT), H).serve_forever()
