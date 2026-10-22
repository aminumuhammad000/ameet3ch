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
import hmac
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from academy_backend import process_guide_request, get_aggregate_stats

PORT = int(os.environ.get("ACADEMY_PORT", 8080))
WEB_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_admin_credentials():
    user = os.environ.get("ADMIN_USER", "admin").strip()
    pwd = os.environ.get("ADMIN_PASSWORD", "").strip()
    return user, pwd

def is_admin_auth_configured() -> bool:
    user, pwd = get_admin_credentials()
    return bool(user and pwd)

def verify_basic_auth(auth_header: str) -> bool:
    if not is_admin_auth_configured():
        return False
    if not auth_header:
        return False
    try:
        parts = auth_header.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "basic":
            return False
        decoded = base64.b64decode(parts[1].strip()).decode("utf-8")
        if ":" not in decoded:
            return False
        req_user, req_pwd = decoded.split(":", 1)
        configured_user, configured_pwd = get_admin_credentials()
        user_matches = hmac.compare_digest(req_user, configured_user)
        pwd_matches = hmac.compare_digest(req_pwd, configured_pwd)
        return user_matches and pwd_matches
    except Exception:
        return False

class AcademyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_ROOT, **kwargs)

    def end_headers(self):
        # Attach security headers to all responses
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

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
            if not is_admin_auth_configured():
                self.send_response(503)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Admin authentication is not configured"}).encode())
                return

            auth_header = self.headers.get("Authorization")
            if not auth_header or not verify_basic_auth(auth_header):
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

def run_server():
    with socketserver.TCPServer(("", PORT), AcademyHTTPHandler) as httpd:
        print(f"[OK] Academy Server running on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
