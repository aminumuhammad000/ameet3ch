#!/usr/bin/env python3
"""
Ameetech Security Remediation — Regression Test Suite (Sprint 1)
Covers:
- SEC-01: AmeeBot DOM XSS Sanitization & Inertness
- SEC-02: HTTP Security Headers Validation (_headers, netlify.toml, server)
- SEC-03: Academy Server Authentication & Credential Security
"""

import os
import re
import json
import base64
import unittest
import subprocess
from academy_server import (
    is_admin_auth_configured,
    verify_basic_auth,
    get_admin_credentials,
    AcademyHTTPHandler
)

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))

class TestAmeeBotSecurity(unittest.TestCase):
    """Verifies that all user input in AmeeBot is properly escaped/inert."""

    def test_esc_html_function_in_node(self):
        """Test the enhanced escHtml function with various edge cases and characters."""
        node_script = """
        const { escHtml } = require('./ameebot.js');
        const assert = require('assert');

        // Standard escaping
        assert.strictEqual(escHtml('<b>test</b>'), '&lt;b&gt;test&lt;/b&gt;');
        assert.strictEqual(escHtml('Foo & Bar'), 'Foo &amp; Bar');
        assert.strictEqual(escHtml('"quote" and \\'single\\''), '&quot;quote&quot; and &#39;single&#39;');

        // Null / undefined / non-string safety
        assert.strictEqual(escHtml(null), '');
        assert.strictEqual(escHtml(undefined), '');
        assert.strictEqual(escHtml(123), '123');
        assert.strictEqual(escHtml(false), 'false');

        // Malformed / nested tags
        assert.strictEqual(escHtml('<<SCRIPT>alert(1)//<</SCRIPT>'), '&lt;&lt;SCRIPT&gt;alert(1)//&lt;&lt;/SCRIPT&gt;');

        console.log('OK');
        """
        result = subprocess.run(
            ["node", "-e", node_script],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Node test failed: {result.stderr}")
        self.assertIn("OK", result.stdout)

    def test_xss_payloads_in_report_and_insights(self):
        """Verify representative XSS payloads remain inert across AmeeBot outputs."""
        node_script = """
        const ameebot = require('./ameebot.js');
        const assert = require('assert');

        const payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert(1)>',
            '<svg/onload=alert(document.cookie)>',
            '"><script>alert(1)</script>',
            '\\' onmouseover=\\'alert(1)',
            '<<SCRIPT>alert("XSS");//<</SCRIPT>',
            '<iframe src="javascript:alert(1)">',
            '<body onload=alert(1)>',
            '<a href="javascript:alert(1)">click</a>'
        ];

        for (const payload of payloads) {
            // Test 1: User name in report header
            const answers = {
                name: payload,
                industry: payload,
                goal: payload,
                website: 'No website at all',
                social: 'Not active on social media'
            };

            // Set state in ameebot module context
            const scores = { Branding: 50, Marketing: 30, Sales: 40, Technology: 20, 'Customer Experience': 40, Operations: 30, Finance: 20 };
            const overall = 33;
            const roadmap = { month1: ['Task 1'], month2: ['Task 2'], month3: ['Task 3'] };
            
            // Generate insights with hostile goal
            // We simulate the logic directly
            const strengths = [];
            if (answers.goal) {
                strengths.push(`Clear vision: "${ameebot.escHtml(answers.goal.substring(0,80))}"`);
            }
            const insights = {
                strengths,
                weaknesses: ['No website'],
                risks: ['Risk of competitors'],
                recommendations: { high: ['Fix website'], medium: [], longterm: [] },
                services: [{ icon: 'fa-globe', name: 'Website Development', why: 'Essential', priority: 'High' }]
            };

            const reportHTML = ameebot.buildReportHTML(scores, overall, insights, roadmap, answers);

            // Assert that raw malicious tags NEVER appear unescaped
            assert(!reportHTML.includes('<script>'), `Raw <script> found in report for payload: ${payload}`);
            assert(!reportHTML.includes('<img src=x onerror='), `Raw img onerror found for payload: ${payload}`);
            assert(!reportHTML.includes('<svg/onload='), `Raw svg onload found for payload: ${payload}`);
            assert(!reportHTML.includes('<iframe src='), `Raw iframe found for payload: ${payload}`);
            assert(!reportHTML.includes('<body onload='), `Raw body onload found for payload: ${payload}`);

            // Assert that escaped representation IS present
            assert(reportHTML.includes(ameebot.escHtml(payload)), `Escaped payload must be safely present for: ${payload}`);
        }

        console.log('ALL_PAYLOADS_INERT');
        """
        result = subprocess.run(
            ["node", "-e", node_script],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"XSS payload test failed: {result.stderr}")
        self.assertIn("ALL_PAYLOADS_INERT", result.stdout)

    def test_assessment_calculation_preserved(self):
        """Verify business scoring and analytics logic remains accurate and functional."""
        node_script = """
        const ameebot = require('./ameebot.js');
        const assert = require('assert');

        // Test normal scoring calculation
        const answers = {
            website: 'Yes – modern & up to date',
            social: 'Yes – posting regularly',
            paid_ads: 'Yes – consistently',
            seo: 'Yes – actively',
            sales_method: 'Website / online store',
            followup: 'Yes – structured & consistent',
            sales_challenge: 'Pricing / competition',
            online_pay: 'Yes – multiple methods',
            booking: 'Yes – automated system',
            automation: 'Yes – several are automated',
            crm: 'CRM software (e.g. HubSpot)',
            software: 'Yes – multiple tools',
            manual: 'Most tasks are automated',
            tracking: 'Yes – in accounting software',
            profit: 'Yes – exactly',
            goal: 'Expand to 3 new regions across West Africa'
        };

        const { scores, overall } = ameebot.analyzeAnswers(answers);
        assert(overall >= 80, `Expected high overall score, got ${overall}`);
        assert.strictEqual(scores.Branding, 100);
        assert.strictEqual(scores.Marketing, 100);

        const roadmap = ameebot.generateRoadmap();
        assert(roadmap.month1.length >= 3);
        assert(roadmap.month2.length >= 3);
        assert(roadmap.month3.length >= 3);

        console.log('ANALYTICS_OK');
        """
        result = subprocess.run(
            ["node", "-e", node_script],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Analytics test failed: {result.stderr}")
        self.assertIn("ANALYTICS_OK", result.stdout)


class TestAcademyServerAuthSecurity(unittest.TestCase):
    """Verifies that Academy admin credentials fail securely and never fall back to defaults."""

    def test_auth_unconfigured_when_password_empty(self):
        """When ADMIN_PASSWORD is unset or empty, auth is marked unconfigured and fails securely."""
        orig_user = os.environ.get("ADMIN_USER")
        orig_pwd = os.environ.get("ADMIN_PASSWORD")
        try:
            os.environ["ADMIN_PASSWORD"] = ""
            self.assertFalse(is_admin_auth_configured())
            
            # Any basic auth attempts must return False
            dummy_auth = "Basic " + base64.b64encode(b"admin:ameetech2026").decode()
            self.assertFalse(verify_basic_auth(dummy_auth))

            # Even blank credentials must be rejected
            blank_auth = "Basic " + base64.b64encode(b"admin:").decode()
            self.assertFalse(verify_basic_auth(blank_auth))
        finally:
            if orig_user is not None: os.environ["ADMIN_USER"] = orig_user
            else: os.environ.pop("ADMIN_USER", None)
            if orig_pwd is not None: os.environ["ADMIN_PASSWORD"] = orig_pwd
            else: os.environ.pop("ADMIN_PASSWORD", None)

    def test_legacy_hardcoded_password_rejected(self):
        """The legacy hardcoded password 'ameetech2026' must NOT authenticate when not configured."""
        orig_pwd = os.environ.get("ADMIN_PASSWORD")
        try:
            os.environ.pop("ADMIN_PASSWORD", None)
            legacy_auth = "Basic " + base64.b64encode(b"admin:ameetech2026").decode()
            self.assertFalse(verify_basic_auth(legacy_auth))
        finally:
            if orig_pwd is not None: os.environ["ADMIN_PASSWORD"] = orig_pwd

    def test_valid_auth_with_configured_secret(self):
        """When ADMIN_PASSWORD is appropriately configured, correct credentials succeed and wrong credentials fail."""
        orig_user = os.environ.get("ADMIN_USER")
        orig_pwd = os.environ.get("ADMIN_PASSWORD")
        try:
            test_secret = "SecureRandomAdminPassword2026!#"
            os.environ["ADMIN_USER"] = "secops_admin"
            os.environ["ADMIN_PASSWORD"] = test_secret

            self.assertTrue(is_admin_auth_configured())

            # Correct credentials
            valid_auth = "Basic " + base64.b64encode(f"secops_admin:{test_secret}".encode()).decode()
            self.assertTrue(verify_basic_auth(valid_auth))

            # Wrong password
            wrong_pwd_auth = "Basic " + base64.b64encode(b"secops_admin:WrongPassword!").decode()
            self.assertFalse(verify_basic_auth(wrong_pwd_auth))

            # Wrong username
            wrong_user_auth = "Basic " + base64.b64encode(f"wrong_user:{test_secret}".encode()).decode()
            self.assertFalse(verify_basic_auth(wrong_user_auth))

            # Malformed headers
            self.assertFalse(verify_basic_auth(""))
            self.assertFalse(verify_basic_auth("Bearer token123"))
            self.assertFalse(verify_basic_auth("Basic not_base64_!#%"))
        finally:
            if orig_user is not None: os.environ["ADMIN_USER"] = orig_user
            else: os.environ.pop("ADMIN_USER", None)
            if orig_pwd is not None: os.environ["ADMIN_PASSWORD"] = orig_pwd
            else: os.environ.pop("ADMIN_PASSWORD", None)


class TestSecurityHeaders(unittest.TestCase):
    """Verifies that HTTP security headers are correctly declared and configured across the site."""

    def test_root_headers_file(self):
        headers_path = os.path.join(REPO_ROOT, "_headers")
        self.assertTrue(os.path.exists(headers_path), "_headers file must exist at repository root")
        with open(headers_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("X-Content-Type-Options: nosniff", content)
        self.assertIn("X-Frame-Options: SAMEORIGIN", content)
        self.assertIn("Referrer-Policy: strict-origin-when-cross-origin", content)
        self.assertIn("Content-Security-Policy:", content)
        self.assertIn("frame-ancestors 'self'", content)
        self.assertIn("https://www.googletagmanager.com", content)
        self.assertIn("https://cdn.botpress.cloud", content)

    def test_root_netlify_toml_headers(self):
        toml_path = os.path.join(REPO_ROOT, "netlify.toml")
        self.assertTrue(os.path.exists(toml_path), "netlify.toml must exist at repository root")
        with open(toml_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('X-Content-Type-Options = "nosniff"', content)
        self.assertIn('X-Frame-Options = "SAMEORIGIN"', content)
        self.assertIn('Referrer-Policy = "strict-origin-when-cross-origin"', content)
        self.assertIn('Content-Security-Policy =', content)

    def test_toolkits_security_headers(self):
        toml_path = os.path.join(REPO_ROOT, "toolkits", "netlify.toml")
        headers_path = os.path.join(REPO_ROOT, "toolkits", "public", "_headers")
        
        self.assertTrue(os.path.exists(toml_path), "toolkits/netlify.toml must exist")
        self.assertTrue(os.path.exists(headers_path), "toolkits/public/_headers must exist")

        with open(toml_path, "r", encoding="utf-8") as f:
            t_content = f.read()
        with open(headers_path, "r", encoding="utf-8") as f:
            h_content = f.read()

        for content in [t_content, h_content]:
            self.assertIn("nosniff", content)
            self.assertIn("strict-origin-when-cross-origin", content)
            self.assertIn("DENY", content)
            self.assertIn("Content-Security-Policy", content)


if __name__ == "__main__":
    unittest.main()
