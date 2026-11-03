"""
Amee Technology Lead Intelligence Platform
HTTP Server & REST API Router
Serves static web files, handles public double opt-in & Brevo webhooks,
and protects Lead Intelligence CRM endpoints via cryptographic session tokens.
"""

import os
import sys
import json
import base64
import urllib.parse
import http.server
import socketserver
from datetime import datetime, timezone

from lead_intelligence_db import (
    init_db,
    get_db_connection,
    verify_password
)
import lead_intelligence_backend as backend
import brevo_service

PORT = int(os.environ.get("LEAD_SERVER_PORT", os.environ.get("ACADEMY_PORT", 8080)))
WEB_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_auth_user(headers) -> dict:
    """Verifies Bearer session token or HTTP Basic Auth header."""
    auth = headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:].strip()
        user = backend.authenticate_session(token)
        if user:
            return user

    # Fallback to Basic Auth
    if auth.startswith("Basic "):
        try:
            decoded = base64.b64decode(auth[6:].strip()).decode("utf-8")
            if ":" in decoded:
                username, pwd = decoded.split(":", 1)
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM admin_users WHERE username = ? AND is_active = 1", (username,))
                row = cur.fetchone()
                conn.close()
                if row and verify_password(pwd, row["password_hash"], row["salt"]):
                    return dict(row)
        except Exception:
            pass
    return None

class LeadIntelligenceHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_ROOT, **kwargs)

    def end_headers(self):
        # Security and CORS Headers
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def send_json(self, status_code: int, data: Any):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            return {}
        raw = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(raw)
        except Exception:
            return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Public: Double Opt-in Confirmation Endpoint
        if path == "/api/subscribe/confirm":
            token = query.get("token", [""])[0]
            result = backend.confirm_subscriber(token)
            if result.get("success"):
                # Redirect to confirmation landing page
                self.send_response(302)
                self.send_header("Location", f"/subscribe/confirmed.html?email={urllib.parse.quote(result.get('email', ''))}")
                self.end_headers()
                return
            else:
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h2>Confirmation Link Expired or Invalid</h2><p>Please check your email or subscribe again.</p><p><a href='/'>Return to Home</a></p>")
                return

        # Public: One-Click Unsubscribe Endpoint
        if path == "/api/subscribe/unsubscribe":
            token = query.get("token", [""])[0]
            result = backend.unsubscribe_subscriber(token)
            self.send_response(302)
            self.send_header("Location", f"/subscribe/unsubscribed.html?email={urllib.parse.quote(result.get('email', ''))}")
            self.end_headers()
            return

        # Public / Legacy Academy Unsubscribe Endpoint
        if path == "/api/unsubscribe":
            token = query.get("token", [""])[0]
            backend.unsubscribe_subscriber(token)
            self.send_response(302)
            self.send_header("Location", "/subscribe/unsubscribed.html")
            self.end_headers()
            return

        # Protected Endpoints - Verify Admin
        if path.startswith("/api/admin/"):
            user = get_auth_user(self.headers)
            if not user and path != "/api/admin/login":
                self.send_json(401, {"success": False, "error": "Unauthorized. Valid administrator session required."})
                return

            if path == "/api/admin/verify":
                self.send_json(200, {"success": True, "user": {"username": user["username"], "role": user["role"], "email": user["email"]}})
                return

            if path == "/api/admin/lead-intelligence/stats":
                stats = backend.get_dashboard_statistics()
                self.send_json(200, {"success": True, "stats": stats})
                return

            if path == "/api/admin/lead-intelligence/prospects":
                flat_query = {k: v[0] for k, v in query.items()}
                res = backend.get_prospects(flat_query)
                self.send_json(200, res)
                return

            if path == "/api/admin/lead-intelligence/prospects/export":
                csv_data = backend.export_prospects_csv()
                csv_bytes = csv_data.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="ameetech_prospects.csv"')
                self.send_header("Content-Length", str(len(csv_bytes)))
                self.end_headers()
                self.wfile.write(csv_bytes)
                return

            if path.startswith("/api/admin/lead-intelligence/prospects/"):
                prospect_id = int(path.split("/")[-1])
                res = backend.get_prospect_detail(prospect_id)
                self.send_json(200 if res.get("success") else 404, res)
                return

            if path == "/api/admin/lead-intelligence/subscribers":
                conn = get_db_connection()
                cur = conn.cursor()
                status_filter = query.get("status", ["All"])[0]
                sql = "SELECT id, first_name, email, business_name, industry, preferred_topics, status, confirmation_timestamp, created_at FROM subscribers"
                params = []
                if status_filter != "All":
                    sql += " WHERE status = ?"
                    params.append(status_filter)
                sql += " ORDER BY id DESC LIMIT 100"
                cur.execute(sql, params)
                subscribers = [dict(r) for r in cur.fetchall()]
                conn.close()
                self.send_json(200, {"success": True, "subscribers": subscribers})
                return

            if path == "/api/admin/lead-intelligence/templates":
                tpls = backend.list_all_templates()
                self.send_json(200, {"success": True, "templates": tpls})
                return

            if path == "/api/admin/lead-intelligence/campaigns":
                camps = backend.get_campaigns()
                self.send_json(200, {"success": True, "campaigns": camps})
                return

            if path == "/api/admin/lead-intelligence/automations":
                autos = backend.get_automations()
                self.send_json(200, {"success": True, "automations": autos})
                return

            if path == "/api/admin/lead-intelligence/analytics":
                analytics = backend.get_detailed_analytics()
                self.send_json(200, {"success": True, "analytics": analytics})
                return

            if path == "/api/admin/lead-intelligence/integrations/status":
                status = brevo_service.test_brevo_connection()
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM brevo_sync_logs ORDER BY id DESC LIMIT 10")
                sync_logs = [dict(r) for r in cur.fetchall()]
                conn.close()
                self.send_json(200, {"success": True, "brevo": status, "sync_logs": sync_logs})
                return

            if path == "/api/admin/lead-intelligence/audit-logs":
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50")
                logs = [dict(r) for r in cur.fetchall()]
                conn.close()
                self.send_json(200, {"success": True, "audit_logs": logs})
                return

            if path == "/api/admin/lead-intelligence/settings":
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT setting_key, setting_value, description FROM system_settings")
                settings = {r["setting_key"]: r["setting_value"] for r in cur.fetchall()}
                conn.close()
                self.send_json(200, {"success": True, "settings": settings})
                return

            self.send_json(404, {"error": "Endpoint not found"})
            return

        # Fallback to standard static file serving
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.read_json_body()
        client_ip = self.client_address[0]
        user_agent = self.headers.get("User-Agent", "")

        # Public: Email Subscription Signup
        if path == "/api/subscribe":
            res = backend.register_public_subscription(body, ip_address=client_ip)
            self.send_json(200 if res.get("success") else 400, res)
            return

        # Public: Brevo Webhook Processing
        if path == "/api/webhooks/brevo":
            res = brevo_service.process_brevo_webhook(body)
            self.send_json(200, res)
            return

        # Public / Legacy Academy Guide Request Endpoint
        if path == "/api/request-guide":
            from academy_backend import process_guide_request
            res = process_guide_request(body, ip_address=client_ip, user_agent=user_agent)
            self.send_json(200 if res.get("success") else 400, res)
            return

        # Admin: Login
        if path == "/api/admin/login":
            username = body.get("username", "").strip()
            password = body.get("password", "").strip()
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM admin_users WHERE username = ? AND is_active = 1", (username,))
            user = cur.fetchone()
            conn.close()

            if user and verify_password(password, user["password_hash"], user["salt"]):
                token = backend.create_admin_session(user["id"], client_ip, user_agent)
                backend.log_audit_event(username, "login_success", "auth", str(user["id"]), client_ip)
                self.send_json(200, {
                    "success": True,
                    "token": token,
                    "user": {"id": user["id"], "username": user["username"], "role": user["role"], "email": user["email"]}
                })
            else:
                backend.log_audit_event(username or "unknown", "login_failed", "auth", "", client_ip)
                self.send_json(401, {"success": False, "error": "Invalid username or password credentials."})
            return

        # Protected Endpoints
        user = get_auth_user(self.headers)
        if not user:
            self.send_json(401, {"success": False, "error": "Unauthorized."})
            return

        if path == "/api/admin/logout":
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                token = auth[7:].strip()
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM admin_sessions WHERE token = ?", (token,))
                conn.commit()
                conn.close()
            self.send_json(200, {"success": True, "message": "Logged out."})
            return

        if path == "/api/admin/lead-intelligence/discover":
            res = backend.run_business_discovery(body, admin_username=user["username"])
            self.send_json(200, res)
            return

        if path == "/api/admin/lead-intelligence/prospects":
            res = backend.create_or_promote_prospect(body, admin_username=user["username"])
            self.send_json(200, res)
            return

        if path == "/api/admin/lead-intelligence/campaigns":
            res = backend.create_campaign(body, admin_username=user["username"])
            self.send_json(200, res)
            return

        if path.endswith("/send") and "/campaigns/" in path:
            camp_id = int(path.split("/")[-2])
            admin_confirm = body.get("admin_confirmation", False)
            res = backend.send_campaign(camp_id, admin_confirmation=admin_confirm, admin_username=user["username"])
            self.send_json(200 if res.get("success") else 400, res)
            return

        if path.endswith("/preview") and "/campaigns/" in path:
            tpl_id = body.get("template_id", "general_newsletter")
            subject = body.get("subject", "Amee Technology Preview")
            first_name = body.get("first_name", "Valued Business Leader")
            rendered = backend.render_template(tpl_id, {"subject": subject, "first_name": first_name})
            self.send_json(200, {"success": True, "rendered": rendered})
            return

        if path.endswith("/test-send") and "/campaigns/" in path:
            test_email = body.get("test_email", user["email"])
            camp_id = int(path.split("/")[-2])
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM email_campaigns WHERE id = ?", (camp_id,))
            c = cur.fetchone()
            conn.close()
            if not c:
                self.send_json(404, {"success": False, "error": "Campaign not found"})
                return
            rendered = backend.render_template(c["template_id"] or "general_newsletter", {"subject": f"[TEST] {c['subject']}", "first_name": "Admin Tester"})
            res = brevo_service.send_transactional_email(test_email, "Admin Tester", f"[TEST] {c['subject']}", rendered["html"])
            self.send_json(200, {"success": True, "message": f"Test email dispatched to {test_email}", "provider_response": res})
            return

        if path == "/api/admin/lead-intelligence/integrations/brevo/test":
            res = brevo_service.test_brevo_connection()
            self.send_json(200, res)
            return

        if path == "/api/admin/lead-intelligence/subscribers/sync":
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM subscribers WHERE status = 'confirmed'")
            subs = [dict(r) for r in cur.fetchall()]
            conn.close()
            synced = 0
            for s in subs:
                brevo_service.sync_confirmed_subscriber(s)
                synced += 1
            backend.log_audit_event(user["username"], "manual_brevo_sync", "subscribers", "", client_ip, {"count": synced})
            self.send_json(200, {"success": True, "synced_count": synced})
            return

        if path.endswith("/toggle") and "/automations/" in path:
            auto_id = int(path.split("/")[-2])
            is_active = body.get("is_active", True)
            backend.toggle_automation(auto_id, is_active)
            self.send_json(200, {"success": True, "automation_id": auto_id, "is_active": is_active})
            return

        if path == "/api/admin/lead-intelligence/settings":
            conn = get_db_connection()
            cur = conn.cursor()
            now_iso = datetime.now(timezone.utc).isoformat()
            for k, v in body.items():
                cur.execute("UPDATE system_settings SET setting_value = ?, updated_at = ? WHERE setting_key = ?", (str(v), now_iso, k))
            conn.commit()
            conn.close()
            backend.log_audit_event(user["username"], "update_settings", "system", "", client_ip)
            self.send_json(200, {"success": True, "message": "Settings updated successfully."})
            return

        self.send_json(404, {"error": "Endpoint not found"})

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.read_json_body()
        user = get_auth_user(self.headers)
        if not user:
            self.send_json(401, {"success": False, "error": "Unauthorized."})
            return

        if path.startswith("/api/admin/lead-intelligence/prospects/"):
            prospect_id = int(path.split("/")[-1])
            res = backend.update_prospect(prospect_id, body, admin_username=user["username"])
            self.send_json(200 if res.get("success") else 400, res)
            return

        self.send_json(404, {"error": "Endpoint not found"})

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        user = get_auth_user(self.headers)
        if not user:
            self.send_json(401, {"success": False, "error": "Unauthorized."})
            return

        if path.startswith("/api/admin/lead-intelligence/prospects/"):
            prospect_id = int(path.split("/")[-1])
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM prospects WHERE id = ?", (prospect_id,))
            conn.commit()
            conn.close()
            backend.log_audit_event(user["username"], "delete_prospect", "prospect", str(prospect_id))
            self.send_json(200, {"success": True, "deleted_prospect_id": prospect_id})
            return

        if path.startswith("/api/admin/lead-intelligence/subscribers/"):
            subscriber_id = int(path.split("/")[-1])
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT email FROM subscribers WHERE id = ?", (subscriber_id,))
            sub = cur.fetchone()
            if sub:
                cur.execute("DELETE FROM subscribers WHERE id = ?", (subscriber_id,))
                conn.commit()
                # Suppress right to be forgotten
                brevo_service.suppress_unsubscribed_contact(sub["email"])
                backend.log_audit_event(user["username"], "delete_subscriber_right_to_be_forgotten", "subscriber", str(subscriber_id))
            conn.close()
            self.send_json(200, {"success": True, "deleted_subscriber_id": subscriber_id})
            return

        self.send_json(404, {"error": "Endpoint not found"})

def run_server():
    init_db()
    with socketserver.TCPServer(("", PORT), LeadIntelligenceHTTPHandler) as httpd:
        print(f"[OK] Amee Technology Lead Intelligence Server running on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
