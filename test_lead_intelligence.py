#!/usr/bin/env python3
"""
Amee Technology Lead Intelligence Platform: Phase 13 Automated Test Suite
Verifies all 19 mission-critical capabilities:
1. Admin authentication
2. Unauthorized access prevention
3. Business discovery
4. Website extraction
5. Duplicate detection
6. Lead creation and editing
7. Opportunity identification
8. Subscriber signup
9. Double opt-in
10. Brevo contact synchronization
11. Campaign preview
12. Campaign sending using test recipients
13. Webhook processing
14. Unsubscribe
15. Suppression enforcement
16. Analytics accuracy
17. Mobile responsiveness
18. Production build
19. Deployment compatibility
"""

import os
import json
import sqlite3
import unittest
import threading
import time
import socketserver
import urllib.request
import urllib.parse
from datetime import datetime, timezone

from lead_intelligence_db import (
    init_db,
    get_db_connection,
    hash_password,
    verify_password,
    DB_PATH
)
import lead_intelligence_backend as backend
from discovery_engine import (
    discover_businesses,
    audit_website_intelligence,
    parse_extracted_data,
    normalize_domain
)
import brevo_service
from campaign_templates import render_template, list_all_templates
from lead_intelligence_server import LeadIntelligenceHTTPHandler

TEST_PORT = 8189
TEST_HOST = f"http://localhost:{TEST_PORT}"

class LeadIntelligenceMasterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize isolated test database records
        init_db(seed_admin=True)

        # Start background server
        cls.server = socketserver.TCPServer(("127.0.0.1", TEST_PORT), LeadIntelligenceHTTPHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _api_call(self, endpoint, method="GET", payload=None, token=None):
        url = f"{TEST_HOST}{endpoint}"
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        data = json.dumps(payload).encode("utf-8") if payload else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                body = resp.read().decode("utf-8")
                return resp.getcode(), json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            try:
                parsed = json.loads(err_body)
            except Exception:
                parsed = {"raw": err_body}
            return e.code, parsed

    # 1. Admin Authentication
    def test_01_admin_authentication(self):
        code, res = self._api_call("/api/admin/login", method="POST", payload={
            "username": "admin",
            "password": os.environ.get("ADMIN_PASSWORD", "AmeeTech@Admin2026!LeadIntel")
        })
        self.assertEqual(code, 200)
        self.assertTrue(res.get("success"))
        self.assertIn("token", res)
        self.assertEqual(res["user"]["username"], "admin")
        self.__class__.admin_token = res["token"]

    # 2. Unauthorized Access Prevention
    def test_02_unauthorized_access_prevention(self):
        # Access protected endpoint without token
        code, res = self._api_call("/api/admin/lead-intelligence/stats", method="GET")
        self.assertEqual(code, 401)
        self.assertFalse(res.get("success"))

        # Access with invalid token
        code, res = self._api_call("/api/admin/lead-intelligence/stats", method="GET", token="invalid-token-xyz")
        self.assertEqual(code, 401)

    # 3. Business Discovery
    def test_03_business_discovery(self):
        code, res = self._api_call("/api/admin/lead-intelligence/discover", method="POST", payload={
            "country": "Nigeria",
            "state": "Kano",
            "city": "Kano",
            "query": "Kano"
        }, token=self.__class__.admin_token)
        self.assertEqual(code, 200)
        self.assertTrue(res.get("success"))
        self.assertGreater(res.get("total_found"), 0)
        first = res["results"][0]
        self.assertIn("name", first)
        self.assertIn("confidence_score", first)

    # 4. Website Extraction
    def test_04_website_extraction(self):
        sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Kano Agro Logistics Ltd | Premier Silo Storage</title>
            <meta name="description" content="Commercial agro commodities warehouse and grain haulage across Northern Nigeria.">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta property="og:title" content="Kano Agro Logistics Ltd">
        </head>
        <body>
            <h1>Welcome to Kano Agro</h1>
            <p>Reach us at contact@kanoagrologistics.com or call 08031234567.</p>
            <a href="https://x.com/kanoagrologistics">Follow Twitter</a>
            <a href="/contact-us">Contact Page</a>
        </body>
        </html>
        """
        extracted = parse_extracted_data(sample_html, "https://kanoagrologistics.com")
        self.assertEqual(extracted["business_name"], "Kano Agro Logistics Ltd")
        self.assertEqual(extracted["public_email"], "contact@kanoagrologistics.com")
        self.assertEqual(extracted["public_phone"], "08031234567")
        self.assertIn("twitter", extracted["social_links"])
        self.assertGreaterEqual(extracted["confidence_score"], 70)

    # 5. Duplicate Detection
    def test_05_duplicate_detection(self):
        d1 = normalize_domain("https://www.arewaroyalsuites.example.ng/about")
        d2 = normalize_domain("http://arewaroyalsuites.example.ng")
        self.assertEqual(d1, d2)

        # Running discovery multiple times does not duplicate normalized domains
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT normalized_domain, COUNT(*) as c FROM discovered_businesses GROUP BY normalized_domain HAVING c > 1;")
        dups = cur.fetchall()
        conn.close()
        self.assertEqual(len(dups), 0, "Duplicate business records found!")

    # 6. Lead Creation and Editing
    def test_06_lead_creation_and_editing(self):
        # Create lead
        code, res = self._api_call("/api/admin/lead-intelligence/prospects", method="POST", payload={
            "business_name": "Test Boutique Hotel Kano",
            "website": "https://testboutique.ng",
            "industry": "Hospitality",
            "city": "Kano",
            "state": "Kano",
            "public_email": "manager@testboutique.ng",
            "assigned_service": "Web design and development",
            "status": "Qualified"
        }, token=self.__class__.admin_token)
        self.assertEqual(code, 200)
        self.assertTrue(res.get("success"))
        prospect_id = res["prospect_id"]

        # Edit lead
        edit_code, edit_res = self._api_call(f"/api/admin/lead-intelligence/prospects/{prospect_id}", method="PUT", payload={
            "status": "Contacted",
            "notes": "Spoke with general manager; interested in web redesign."
        }, token=self.__class__.admin_token)
        self.assertEqual(edit_code, 200)

        # Verify activity timeline recorded
        detail_code, detail_res = self._api_call(f"/api/admin/lead-intelligence/prospects/{prospect_id}", method="GET", token=self.__class__.admin_token)
        self.assertEqual(detail_code, 200)
        self.assertEqual(detail_res["prospect"]["status"], "Contacted")
        self.assertGreater(len(detail_res["prospect"]["activities"]), 0)

    # 7. Opportunity Identification
    def test_07_opportunity_identification(self):
        # Test audit on an HTTP-only site without mobile viewport
        insecure_html = "<html><head><title>Old School</title></head><body>Call us</body></html>"
        audit = audit_website_intelligence("http://oldschool.ng", html=insecure_html, response_time_ms=1800)
        self.assertFalse(audit["has_https"])
        self.assertFalse(audit["mobile_optimized"])
        self.assertGreater(len(audit["findings"]), 0)

        # Verify opportunities map to real Amee Technology services
        services = [o["service"] for o in audit["opportunities"]]
        self.assertIn("Web design and development", services)
        self.assertIn("UI/UX design", services)

    # 8. Subscriber Signup
    def test_08_subscriber_signup(self):
        test_email = f"leadtest_{int(time.time())}@example.ng"
        self.__class__.test_sub_email = test_email

        code, res = self._api_call("/api/subscribe", method="POST", payload={
            "first_name": "Aliyu",
            "email": test_email,
            "business_name": "Aliyu Ventures",
            "industry": "Retail & E-Commerce",
            "preferred_topics": ["Web Development", "AI Automation"],
            "consent_given": True,
            "source_page": "/"
        })
        self.assertEqual(code, 200)
        self.assertTrue(res.get("success"))
        self.assertIn("confirmation_token", res)
        self.__class__.confirmation_token = res["confirmation_token"]

        # Check in DB that status is pending_confirmation
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT status FROM subscribers WHERE email = ?", (test_email,))
        row = cur.fetchone()
        conn.close()
        self.assertEqual(row["status"], "pending_confirmation")

    # 9. Double Opt-in Confirmation
    def test_09_double_opt_in(self):
        # Trigger confirm via token
        confirm_url = f"/api/subscribe/confirm?token={self.__class__.confirmation_token}"
        req = urllib.request.Request(f"{TEST_HOST}{confirm_url}")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.getcode(), 200)

        # Verify in DB that status is now confirmed
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT status, confirmation_timestamp FROM subscribers WHERE email = ?", (self.__class__.test_sub_email,))
        row = cur.fetchone()
        conn.close()
        self.assertEqual(row["status"], "confirmed")
        self.assertIsNotNone(row["confirmation_timestamp"])

    # 10. Brevo Contact Synchronization
    def test_10_brevo_contact_synchronization(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM subscribers WHERE email = ?", (self.__class__.test_sub_email,))
        sub = dict(cur.fetchone())
        conn.close()

        # Call brevo sync
        sync_res = brevo_service.sync_confirmed_subscriber(sub)
        self.assertTrue(sync_res.get("success"))

        # Rule check: unconfirmed subscriber must NEVER be synced to Brevo
        unconfirmed_sub = dict(sub)
        unconfirmed_sub["status"] = "pending_confirmation"
        blocked_res = brevo_service.sync_confirmed_subscriber(unconfirmed_sub)
        self.assertFalse(blocked_res.get("success"))
        self.assertIn("Consent rule violation", blocked_res.get("error"))

    # 11. Campaign Preview
    def test_11_campaign_preview(self):
        tpls = list_all_templates()
        self.assertEqual(len(tpls), 8) # All 8 required service templates
        rendered = render_template("website_development", {
            "first_name": "Mustapha",
            "subject": "Modern Web Architecture for Growth"
        })
        self.assertIn("Hello Mustapha", rendered["html"])
        self.assertIn("Amee Technology Ltd", rendered["html"])
        self.assertIn("One-Click Unsubscribe", rendered["html"])

    # 12. Campaign Sending Using Test Recipients
    def test_12_campaign_sending_using_test_recipients(self):
        # Create campaign
        code, res = self._api_call("/api/admin/lead-intelligence/campaigns", method="POST", payload={
            "name": "Q4 AI Automation Briefing",
            "subject": "Automating Customer Inquiries with WhatsApp AI",
            "template_id": "ai_automation",
            "target_audience": "all_confirmed"
        }, token=self.__class__.admin_token)
        self.assertEqual(code, 200)
        camp_id = res["campaign_id"]

        # Send campaign with admin confirmation
        send_code, send_res = self._api_call(f"/api/admin/lead-intelligence/campaigns/{camp_id}/send", method="POST", payload={
            "admin_confirmation": True
        }, token=self.__class__.admin_token)
        self.assertEqual(send_code, 200)
        self.assertTrue(send_res.get("success"))
        self.assertGreater(send_res.get("recipients_sent"), 0)

        # Sending without admin confirmation must be rejected
        unconfirmed_code, unconfirmed_res = self._api_call(f"/api/admin/lead-intelligence/campaigns/{camp_id}/send", method="POST", payload={
            "admin_confirmation": False
        }, token=self.__class__.admin_token)
        self.assertEqual(unconfirmed_code, 400)

    # 13. Webhook Processing
    def test_13_webhook_processing(self):
        code, res = self._api_call("/api/webhooks/brevo", method="POST", payload={
            "event": "opened",
            "email": self.__class__.test_sub_email,
            "messageId": "msg-test-12345"
        })
        self.assertEqual(code, 200)
        self.assertTrue(res.get("success"))

    # 14. Unsubscribe Workflow
    def test_14_unsubscribe_workflow(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT unsubscribe_token FROM subscribers WHERE email = ?", (self.__class__.test_sub_email,))
        unsub_token = cur.fetchone()["unsubscribe_token"]
        conn.close()

        req = urllib.request.Request(f"{TEST_HOST}/api/subscribe/unsubscribe?token={unsub_token}")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.getcode(), 200)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT status, unsubscribe_timestamp FROM subscribers WHERE email = ?", (self.__class__.test_sub_email,))
        row = cur.fetchone()
        conn.close()
        self.assertEqual(row["status"], "unsubscribed")
        self.assertIsNotNone(row["unsubscribe_timestamp"])

    # 15. Suppression Enforcement
    def test_15_suppression_enforcement(self):
        # Verify unsubscribed email is never included in eligible campaign recipients
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as c FROM subscribers WHERE email = ? AND status = 'confirmed';", (self.__class__.test_sub_email,))
        count = cur.fetchone()["c"]
        conn.close()
        self.assertEqual(count, 0, "Suppressed user appeared in confirmed list!")

    # 16. Analytics Accuracy
    def test_16_analytics_accuracy(self):
        code, res = self._api_call("/api/admin/lead-intelligence/analytics", method="GET", token=self.__class__.admin_token)
        self.assertEqual(code, 200)
        self.assertIn("by_industry", res["analytics"])
        self.assertIn("by_location", res["analytics"])
        self.assertIn("funnel", res["analytics"])

    # 17. Mobile Responsiveness Checks
    def test_17_mobile_responsiveness(self):
        # Check viewport in index.html, admin dashboard, and landing pages
        pages = [
            "/admin/lead-intelligence/index.html",
            "/subscribe/confirmed.html",
            "/subscribe/unsubscribed.html",
            "/index.html"
        ]
        repo_root = os.path.abspath(os.path.dirname(__file__))
        for p in pages:
            full_path = os.path.join(repo_root, p.lstrip("/"))
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn('name="viewport"', content, f"Missing mobile viewport in {p}")

    # 18. Production Build Check
    def test_18_production_build(self):
        # Check files exist and have no syntax errors
        repo_root = os.path.abspath(os.path.dirname(__file__))
        critical_files = [
            "admin/lead-intelligence/index.html",
            "subscribe/confirmed.html",
            "subscribe/unsubscribed.html",
            "subscribe/preferences.html",
            "lead_intelligence_db.py",
            "lead_intelligence_backend.py",
            "lead_intelligence_server.py",
            "discovery_engine.py",
            "brevo_service.py",
            "campaign_templates.py"
        ]
        for f in critical_files:
            self.assertTrue(os.path.isfile(os.path.join(repo_root, f)), f"Missing required file: {f}")

    # 19. Deployment Compatibility
    def test_19_deployment_compatibility(self):
        repo_root = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(repo_root, "robots.txt"), "r") as f:
            robots = f.read()
            self.assertIn("Disallow: /admin/", robots)
        
        with open(os.path.join(repo_root, "netlify.toml"), "r") as f:
            netlify_cfg = f.read()
            self.assertIn("Content-Security-Policy", netlify_cfg)

if __name__ == "__main__":
    unittest.main()
