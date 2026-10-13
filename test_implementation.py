#!/usr/bin/env python3
"""
Test Suite for Ameetech Technology Marketing Article & Lead Generation Page.
Uses purely Python standard library (no external dependencies required).
"""

import os
import re
import json
import http.server
import socketserver
import threading
import time
import urllib.request
from html.parser import HTMLParser

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
ARTICLE_PATH = os.path.join(REPO_ROOT, "blog", "digital-growth-solutions-for-smes", "index.html")
BLOG_INDEX_PATH = os.path.join(REPO_ROOT, "blog", "index.html")
SITEMAP_PATH = os.path.join(REPO_ROOT, "sitemap.xml")

class SimpleDOMParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.h1_texts = []
        self.h2_texts = []
        self.title_text = ""
        self.in_title = False
        self.in_h1 = False
        self.in_h2 = False
        self.meta_tags = []
        self.link_tags = []
        self.script_blocks = []
        self.in_json_ld = False
        self.current_script = ""
        self.ids = set()
        self.forms = []
        self.current_form = None
        self.all_text = []
        self.faq_count = 0
        self.table_tr_count = 0
        self.in_main_article = False
        self.article_text = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tags.append((tag, attr_dict))

        if "id" in attr_dict:
            self.ids.add(attr_dict["id"])

        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "h2":
            self.in_h2 = True
        elif tag == "meta":
            self.meta_tags.append(attr_dict)
        elif tag == "link":
            self.link_tags.append(attr_dict)
        elif tag == "script" and attr_dict.get("type") == "application/ld+json":
            self.in_json_ld = True
            self.current_script = ""
        elif tag == "details" and "faq-item" in attr_dict.get("class", ""):
            self.faq_count += 1
        elif tag == "tr":
            self.table_tr_count += 1
        elif tag == "form":
            self.current_form = attr_dict
            self.forms.append(attr_dict)
        elif tag == "main" and "article-content" in attr_dict.get("class", ""):
            self.in_main_article = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "h2":
            self.in_h2 = False
        elif tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            self.script_blocks.append(self.current_script)
        elif tag == "form":
            self.current_form = None
        elif tag == "main" and self.in_main_article:
            self.in_main_article = False

    def handle_data(self, data):
        text = data.strip()
        if self.in_title:
            self.title_text += data
        if self.in_h1 and text:
            self.h1_texts.append(text)
        if self.in_h2 and text:
            self.h2_texts.append(text)
        if self.in_json_ld:
            self.current_script += data
        if self.in_main_article and text:
            self.article_text.append(text)
        if text:
            self.all_text.append(text)

def run_tests():
    print("=" * 70)
    print("AMEETECH TECHNOLOGY — MARKETING PAGE IMPLEMENTATION TEST SUITE")
    print("=" * 70)

    passed = 0
    failed = 0

    def assert_test(condition, name, details=""):
        nonlocal passed, failed
        if condition:
            print(f"[PASS] {name}")
            passed += 1
        else:
            print(f"[FAIL] {name}: {details}")
            failed += 1

    # 1. File existence
    assert_test(os.path.isfile(ARTICLE_PATH), "Article file exists at blog/digital-growth-solutions-for-smes/index.html")
    assert_test(os.path.isfile(BLOG_INDEX_PATH), "Blog hub file exists at blog/index.html")
    assert_test(os.path.isfile(os.path.join(REPO_ROOT, "blog.css")), "blog.css stylesheet exists")
    assert_test(os.path.isfile(os.path.join(REPO_ROOT, "blog.js")), "blog.js script exists")

    # Read and parse article HTML
    with open(ARTICLE_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    parser = SimpleDOMParser()
    parser.feed(html)

    # 2. Metadata & SEO Checks
    assert_test("Digital Solutions for Nigerian SMEs | Ameetech Technology" in parser.title_text,
                "Title tag matches recommended SEO title",
                f"Got: '{parser.title_text.strip()}'")

    meta_desc = next((m.get("content") for m in parser.meta_tags if m.get("name") == "description"), None)
    assert_test(meta_desc and len(meta_desc) > 50,
                "Meta description is present and descriptive",
                f"Got: '{meta_desc}'")

    canonical = next((l.get("href") for l in parser.link_tags if l.get("rel") == "canonical"), None)
    assert_test(canonical == "https://ameetechnology.com.ng/blog/digital-growth-solutions-for-smes/",
                "Canonical URL is correct",
                f"Got: '{canonical}'")

    og_title = next((m.get("content") for m in parser.meta_tags if m.get("property") == "og:title"), None)
    og_desc = next((m.get("content") for m in parser.meta_tags if m.get("property") == "og:description"), None)
    og_image = next((m.get("content") for m in parser.meta_tags if m.get("property") == "og:image"), None)
    assert_test(og_title and og_desc and og_image, "Open Graph tags are present")

    # 3. Headings & Hierarchy
    assert_test(len(parser.h1_texts) == 1, "Exactly one H1 tag present", f"Found {len(parser.h1_texts)} H1 tags")
    assert_test(parser.h1_texts and "How Nigerian Small Businesses Can Grow with the Right Digital Solutions" in parser.h1_texts[0],
                "H1 text matches target heading")

    assert_test(len(parser.h2_texts) >= 12, f"Substantive H2 section structure ({len(parser.h2_texts)} H2s found)")

    # 4. Word Count
    article_words = " ".join(parser.article_text).split()
    word_count = len(article_words)
    assert_test(1800 <= word_count <= 3500, f"Word count within target range (~1,800-2,500+). Current: {word_count} words",
                f"Actual word count: {word_count}")

    # 5. Core Sections Verification
    required_sections = [
        ("challenges", "Section 2: Challenges"),
        ("digital-strategy", "Section 3: Strategy"),
        ("website-development", "Section 4: Website Development"),
        ("seo", "Section 5: SEO"),
        ("ui-ux-design", "Section 6: UI/UX"),
        ("mobile-apps", "Section 7: Mobile Apps"),
        ("video-content", "Section 8: Video Content"),
        ("digital-marketing", "Section 9: Digital Marketing"),
        ("decision-guide", "Section 10: Decision Guide"),
        ("growth-roadmap", "Section 11: Roadmap"),
        ("why-ameetech", "Section 12: Why Ameetech"),
        ("faq", "Section 13: FAQ"),
        ("contact-consultation", "Section 14: Conversion"),
        ("editorial-credentials", "Section 15: Author Credentials")
    ]
    for sec_id, label in required_sections:
        assert_test(sec_id in parser.ids, f"Required section #{sec_id} ({label}) exists")

    # 6. FAQ items check
    assert_test(parser.faq_count == 8, f"All 8 FAQ questions implemented. Found: {parser.faq_count}")

    # 7. Comparison Table check
    assert_test(parser.table_tr_count >= 8, f"SME Decision guide table has all 7 rows + header. Found {parser.table_tr_count} tr tags")

    # 8. Conversion Form
    lead_form = next((f for f in parser.forms if f.get("id") == "article-lead-form"), None)
    assert_test(lead_form is not None, "Lead enquiry form with id 'article-lead-form' exists")
    if lead_form:
        assert_test(lead_form.get("data-netlify") == "true", "Form configured with data-netlify='true'")
        assert_test(lead_form.get("method") == "POST", "Form uses method='POST'")

    # 9. JSON-LD Structured Data Validation
    assert_test(len(parser.script_blocks) >= 1, "JSON-LD structured data script found")
    for idx, s in enumerate(parser.script_blocks):
        try:
            data = json.loads(s)
            assert_test(True, f"JSON-LD block #{idx+1} is valid JSON")
            graph = data.get("@graph", [data])
            types = [item.get("@type") for item in graph]
            assert_test("BlogPosting" in types, "JSON-LD contains BlogPosting schema")
            assert_test("BreadcrumbList" in types, "JSON-LD contains BreadcrumbList schema")
            assert_test("FAQPage" in types, "JSON-LD contains FAQPage schema")

            # Check FAQPage count
            faq_schema = next((item for item in graph if item.get("@type") == "FAQPage"), None)
            if faq_schema:
                main_entity = faq_schema.get("mainEntity", [])
                assert_test(len(main_entity) == 8, f"FAQPage schema has 8 questions. Found: {len(main_entity)}")
        except Exception as e:
            assert_test(False, f"JSON-LD block #{idx+1} failed to parse: {e}")

    # 10. Sitemap verification
    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        sitemap_content = f.read()
    assert_test("https://ameetechnology.com.ng/blog/digital-growth-solutions-for-smes/" in sitemap_content,
                "Sitemap contains new article URL")
    assert_test("https://ameetechnology.com.ng/blog/" in sitemap_content,
                "Sitemap contains blog hub URL")

    # 11. Local HTTP Server & Status 200 checks
    port = 8899
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    try:
        endpoints = [
            ("/blog/digital-growth-solutions-for-smes/", 200, "Article page"),
            ("/blog/", 200, "Blog hub"),
            ("/style.css", 200, "Core style.css"),
            ("/blog.css", 200, "blog.css"),
            ("/blog.js", 200, "blog.js"),
            ("/sitemap.xml", 200, "sitemap.xml"),
            ("/images/digital_solutions.png", 200, "Hero image"),
            ("/images/ameelogo.png", 200, "Logo image"),
            ("/images/Aminu_Muhammad.jpeg", 200, "Author avatar image")
        ]
        for path, expected_status, desc in endpoints:
            req = urllib.request.Request(f"http://localhost:{port}{path}")
            with urllib.request.urlopen(req) as resp:
                status = resp.getcode()
                assert_test(status == expected_status, f"HTTP GET {path} returned {expected_status} ({desc})",
                            f"Status: {status}")
    finally:
        httpd.shutdown()
        httpd.server_close()

    print("=" * 70)
    print(f"TEST RESULTS: {passed} PASSED, {failed} FAILED")
    print("=" * 70)

    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
