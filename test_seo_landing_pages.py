#!/usr/bin/env python3
"""
Unit tests for Amee Technology SEO Landing Pages:
- /vtu-app-development/
- /website-design-kano/
- /mobile-app-development-kano/
- /custom-web-application-development/
"""

import os
import re
import json
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    {
        "path": os.path.join(REPO_ROOT, "vtu-app-development", "index.html"),
        "url": "https://ameetechnology.com.ng/vtu-app-development/",
        "form_name": "vtu-lead-enquiry",
        "expected_h1": "VTU Application Development in Nigeria",
        "service_name": "VTU Application Development & Telecom Software",
    },
    {
        "path": os.path.join(REPO_ROOT, "website-design-kano", "index.html"),
        "url": "https://ameetechnology.com.ng/website-design-kano/",
        "form_name": "website-design-kano-lead",
        "expected_h1": "Website Design & Development in Kano",
        "service_name": "Website Design & Development in Kano",
    },
    {
        "path": os.path.join(REPO_ROOT, "mobile-app-development-kano", "index.html"),
        "url": "https://ameetechnology.com.ng/mobile-app-development-kano/",
        "form_name": "mobile-app-kano-lead",
        "expected_h1": "Mobile App Development in Kano",
        "service_name": "Mobile Application Development in Kano",
    },
    {
        "path": os.path.join(REPO_ROOT, "custom-web-application-development", "index.html"),
        "url": "https://ameetechnology.com.ng/custom-web-application-development/",
        "form_name": "custom-web-app-lead",
        "expected_h1": "Custom Web Application Development",
        "service_name": "Custom Web Application Development",
    },
]

class TestSeoLandingPages(unittest.TestCase):

    def test_css_and_js_exist(self):
        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, "seo-landing.css")), "seo-landing.css missing")
        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, "landing.js")), "landing.js missing")

    def test_pages_structure_and_seo(self):
        for page in PAGES:
            self.assertTrue(os.path.exists(page["path"]), f"Page missing: {page['path']}")
            with open(page["path"], "r", encoding="utf-8") as f:
                html = f.read()

            # Canonical
            canonical_match = re.search(r'<link\s+rel=[\"\']canonical[\"\']\s+href=[\"\'](.*?)[\"\']', html)
            self.assertIsNotNone(canonical_match, f"Missing canonical in {page['path']}")
            self.assertEqual(canonical_match.group(1), page["url"])

            # Single H1
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
            self.assertEqual(len(h1s), 1, f"Expected 1 H1, found {len(h1s)} in {page['path']}")
            clean_h1 = re.sub(r'<[^>]+>', ' ', h1s[0])
            clean_h1 = ' '.join(clean_h1.split()).lower().replace("&amp;", "&")
            self.assertIn(page["expected_h1"].lower(), clean_h1)

            # Meta Description
            meta_desc = re.search(r'<meta\s+name=[\"\']description[\"\']\s+content=[\"\'](.*?)[\"\']', html)
            self.assertIsNotNone(meta_desc, f"Missing meta description in {page['path']}")
            self.assertTrue(120 <= len(meta_desc.group(1)) <= 195, f"Meta desc length out of bounds: {len(meta_desc.group(1))}")

            # Open Graph Tags
            self.assertIn('property="og:title"', html)
            self.assertIn('property="og:description"', html)
            self.assertIn('property="og:url"', html)
            self.assertIn('property="og:image"', html)

            # Netlify Form
            self.assertIn(f'name="{page["form_name"]}"', html)
            self.assertIn('data-netlify="true"', html)

            # JSON-LD Structured Data
            scripts = re.findall(r'<script\s+type=[\"\']application/ld\+json[\"\']>(.*?)</script>', html, re.DOTALL)
            self.assertGreaterEqual(len(scripts), 1, f"Missing JSON-LD in {page['path']}")
            for s in scripts:
                parsed = json.loads(s.strip())
                self.assertEqual(parsed["@context"], "https://schema.org")
                types = [x.get("@type") for x in parsed.get("@graph", [])]
                self.assertTrue("FAQPage" in types or "Service" in types or "BreadcrumbList" in types)

    def test_sitemap_inclusion(self):
        tree = ET.parse(os.path.join(REPO_ROOT, "sitemap.xml"))
        root = tree.getroot()
        urls = [elem.text for elem in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        for page in PAGES:
            self.assertIn(page["url"], urls, f"{page['url']} missing from sitemap.xml")

    def test_internal_links_in_index_and_services(self):
        with open(os.path.join(REPO_ROOT, "index.html"), "r", encoding="utf-8") as f:
            index_html = f.read()
        with open(os.path.join(REPO_ROOT, "services", "index.html"), "r", encoding="utf-8") as f:
            services_html = f.read()

        for page in PAGES:
            slug = page["url"].replace("https://ameetechnology.com.ng/", "")
            self.assertIn(slug, index_html, f"Slug {slug} missing in index.html")
            self.assertIn(slug, services_html, f"Slug {slug} missing in services/index.html")

if __name__ == "__main__":
    unittest.main()
