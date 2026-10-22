#!/usr/bin/env python3
"""
Ameetech Business & Economics Academy | Lightweight API & Static File Server
Provides the `/api/request-guide` delivery endpoint, administrative metrics,
and static file serving.
"""

import os
import sys
import json
import base64
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from academy_backend import process_guide_request, get_aggregate_stats

PORT = int(os.environ.get("ACADEMY_PORT", 8080))
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ameetech2026")
WEB_ROOT = os.path.abspath(os.path.dirname(__file__))

class AcademyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_ROOT, **kwargs)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/request-guide":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            try:
                data = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Invalid JSON"}).encode())
                return

            client_ip = self.client_address[0]
            user_agent = self.headers.get("User-Agent", "")

            result = process_guide_request(data, ip_address=client_ip, user_agent=user_agent)
            
            self.send_response(200 if result.get("success") else 400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # Admin Stats API (Protected via Basic Auth)
        if parsed.path == "/api/admin/stats":
            auth_header = self.headers.get("Authorization")
            if not auth_header or not self.verify_basic_auth(auth_header):
                self.send_response(401)
                self.send_header("WWW-Authenticate", 'Basic realm="Academy Admin"')
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
                return

            stats = get_aggregate_stats()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
            return

        # Unsubscribe endpoint (NDPR compliant)
        if parsed.path == "/api/unsubscribe":
            query = parse_qs(parsed.query)
            token = query.get("token", [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""
            <html><body style="font-family:sans-serif;padding:40px;text-align:center;">
                <h2>Unsubscribed Successfully</h2>
                <p>You have been removed from Ameetech promotional learning updates. You can still access all free online lessons at any time.</p>
                <a href="/academy/business-economics/">Return to Academy</a>
            </body></html>
            """)
            return

        # Fallback to standard static file serving
        return super().do_GET()

    def verify_basic_auth(self, auth_header: str) -> bool:
        try:
            auth_type, encoded = auth_header.split(" ", 1)
            if auth_type.lower() != "basic":
                return False
            decoded = base64.b64decode(encoded.strip()).decode("utf-8")
            user, pwd = decoded.split(":", 1)
            return user == ADMIN_USER and pwd == ADMIN_PASSWORD
        except Exception:
            return False

def run_server():
    with socketserver.TCPServer(("", PORT), AcademyHTTPHandler) as httpd:
        print(f"[OK] Academy Server running on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
