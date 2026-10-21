#!/usr/bin/env python3
"""
Test Suite for Ameetech AI for Nigerian Small Businesses Blog Article
Verifies SEO, metadata, document structure, accessibility, word count,
JSON-LD schemas, sitemap, blog hub inclusion, and asset HTTP delivery.
"""

import os
import sys
import json
import re
import http.server
import socketserver
import threading
import urllib.request
from html.parser import HTMLParser

ARTICLE_PATH = "blog/how-nigerian-businesses-use-ai-to-save-time/index.html"
BLOG_HUB_PATH = "blog/index.html"
SITEMAP_PATH = "sitemap.xml"
BANNER_PATH = "images/blog/ai_small_business_nigeria_banner.png"

passed_tests = 0
failed_tests = 0

def assert_test(condition, desc):
    global passed_tests, failed_tests
    if condition:
        print(f"[PASS] {desc}")
        passed_tests += 1
    else:
        print(f"[FAIL] {desc}")
        failed_tests += 1

class ArticleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.attrs_by_tag = {}
        self.h1_tags = []
        self.h2_tags = []
        self.h3_tags = []
        self.links = []
        self.meta_tags = {}
        self.title_text = ""
        self.in_title = False
        self.json_ld_scripts = []
        self.in_json_ld = False
        self.current_script = ""
        self.ids = set()
        self.in_form = False
        self.current_form = None
        self.all_text = []
        self.faq_count = 0
        self.table_tr_count = 0

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tags.append(tag)
        if "id" in attr_dict:
            self.ids.add(attr_dict["id"])

        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = attr_dict.get("name") or attr_dict.get("property")
            content = attr_dict.get("content")
            if name and content:
                self.meta_tags[name] = content
        elif tag == "link":
            rel = attr_dict.get("rel")
            href = attr_dict.get("href")
            if rel and href:
                self.links.append((rel, href))
        elif tag == "script" and attr_dict.get("type") == "application/ld+json":
            self.in_json_ld = True
            self.current_script = ""
        elif tag == "details" and "faq-item" in attr_dict.get("class", ""):
            self.faq_count += 1
        elif tag == "tr":
            self.table_tr_count += 1
        elif tag == "form":
            self.in_form = True
            self.current_form = attr_dict

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            self.json_ld_scripts.append(self.current_script)
            self.current_script = ""
        elif tag == "form":
            self.in_form = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data
        elif self.in_json_ld:
            self.current_script += data
        else:
            cleaned = data.strip()
            if cleaned:
                self.all_text.append(cleaned)


def run_tests():
    print("=" * 70)
    print("AMEETECH TECHNOLOGY — AI FOR SMALL BUSINESSES ARTICLE TEST SUITE")
    print("=" * 70)

    # 1. File existence
    assert_test(os.path.exists(ARTICLE_PATH), f"Article file exists at {ARTICLE_PATH}")
    assert_test(os.path.exists(BLOG_HUB_PATH), f"Blog hub file exists at {BLOG_HUB_PATH}")
    assert_test(os.path.exists(SITEMAP_PATH), f"Sitemap exists at {SITEMAP_PATH}")
    assert_test(os.path.exists(BANNER_PATH), f"Hero banner image exists at {BANNER_PATH}")

    with open(ARTICLE_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = ArticleHTMLParser()
    parser.feed(html_content)

    # 2. SEO Title & Meta
    assert_test("7 Practical Ways Nigerian Small Businesses Can Use AI to Save Time" in parser.title_text, "Title tag matches SEO title")
    assert_test("description" in parser.meta_tags and len(parser.meta_tags["description"]) > 50, "Meta description is descriptive")
    
    canonical_links = [href for rel, href in parser.links if rel == "canonical"]
    assert_test(
        canonical_links == ["https://ameetechnology.com.ng/blog/how-nigerian-businesses-use-ai-to-save-time/"],
        f"Canonical link points to exact URL: {canonical_links}"
    )

    # 3. OpenGraph Tags
    assert_test("og:title" in parser.meta_tags, "OpenGraph title is present")
    assert_test("og:image" in parser.meta_tags, "OpenGraph image is present")
    assert_test(parser.meta_tags.get("og:image") == "https://ameetechnology.com.ng/images/blog/ai_small_business_nigeria_banner.png", "OpenGraph image points to custom banner")

    # 4. Heading structure
    h1_matches = re.findall(r"<h1[^>]*>(.*?)</h1>", html_content, re.DOTALL)
    assert_test(len(h1_matches) == 1, f"Exactly one H1 found (Found: {len(h1_matches)})")
    if h1_matches:
        assert_test("7 Practical Ways Nigerian Small Businesses Can Use AI to Save Time" in h1_matches[0], "H1 matches target heading")

    # 5. Word count
    full_text = " ".join(parser.all_text)
    word_count = len(full_text.split())
    assert_test(word_count >= 2000, f"Word count within target range (~2,000-4,000). Current: {word_count} words")

    # 6. Required Sections
    required_sections = [
        ("what-are-ai-tools", "What Are AI Tools"),
        ("social-media-content", "1. Social Media Content"),
        ("product-descriptions", "2. Product Descriptions"),
        ("marketing-calendar", "3. Marketing Calendar"),
        ("customer-service-faqs", "4. Customer Service and FAQs"),
        ("business-documents", "5. Business Documents & Admin"),
        ("analyze-data", "6. Data & Feedback Analysis"),
        ("workflow-automation", "7. Workflow Automation"),
        ("tools-to-try", "Recommended AI Tools Comparison"),
        ("better-results-framework", "5-Part Prompt Framework"),
        ("common-mistakes", "Mistakes to Avoid"),
        ("seven-day-plan", "7-Day Action Plan"),
        ("how-ameetech-helps", "How Ameetech Helps"),
        ("faq", "Frequently Asked Questions"),
        ("final-thoughts", "Final Thoughts"),
        ("contact-consultation", "Conversion Consultation")
    ]
    for sec_id, label in required_sections:
        assert_test(sec_id in parser.ids, f"Required section #{sec_id} ({label}) exists")

    # 7. FAQ items check
    assert_test(parser.faq_count == 6, f"All 6 FAQ questions implemented. Found: {parser.faq_count}")

    # 8. Tables check
    assert_test(parser.table_tr_count >= 15, f"Tables contain substantive rows. Found: {parser.table_tr_count} tr tags")

    # 9. Lead form check
    assert_test("article-lead-form" in parser.ids, "Lead enquiry form with id 'article-lead-form' exists")
    assert_test(parser.current_form is not None or "data-netlify=\"true\"" in html_content, "Form configured with data-netlify='true'")

    # 10. JSON-LD structured data
    assert_test(len(parser.json_ld_scripts) > 0, "JSON-LD structured data script found")
    for idx, script_text in enumerate(parser.json_ld_scripts):
        try:
            data = json.loads(script_text)
            assert_test(True, f"JSON-LD block #{idx+1} is valid JSON")
            graph = data.get("@graph", [data])
            types = [item.get("@type") for item in graph]
            assert_test("BlogPosting" in types, "JSON-LD contains BlogPosting schema")
            assert_test("BreadcrumbList" in types, "JSON-LD contains BreadcrumbList schema")
            assert_test("FAQPage" in types, "JSON-LD contains FAQPage schema")

            faq_schema = next((item for item in graph if item.get("@type") == "FAQPage"), None)
            if faq_schema:
                main_entity = faq_schema.get("mainEntity", [])
                assert_test(len(main_entity) == 6, f"FAQPage schema has 6 questions. Found: {len(main_entity)}")
        except Exception as e:
            assert_test(False, f"JSON-LD block #{idx+1} failed to parse: {e}")

    # 11. Sitemap check
    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        sitemap_content = f.read()
    assert_test(
        "https://ameetechnology.com.ng/blog/how-nigerian-businesses-use-ai-to-save-time/" in sitemap_content,
        "Sitemap contains new AI article URL"
    )

    # 12. Blog Hub check
    with open(BLOG_HUB_PATH, "r", encoding="utf-8") as f:
        hub_content = f.read()
    assert_test(
        "/blog/how-nigerian-businesses-use-ai-to-save-time/" in hub_content,
        "Blog hub index contains link to new AI article"
    )

    # 13. Local Server HTTP Verification
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

    port = 8893
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        endpoints = [
            ("/blog/how-nigerian-businesses-use-ai-to-save-time/", 200, "AI Article page"),
            ("/blog/", 200, "Blog hub"),
            ("/style.css", 200, "Core style.css"),
            ("/blog.css", 200, "blog.css"),
            ("/blog.js", 200, "blog.js"),
            ("/sitemap.xml", 200, "sitemap.xml"),
            (f"/{BANNER_PATH}", 200, "Hero banner image"),
            ("/images/ameelogo.png", 200, "Logo image"),
            ("/images/Aminu_Muhammad.jpeg", 200, "Author avatar image")
        ]
        for path, expected_status, desc in endpoints:
            req = urllib.request.Request(f"http://127.0.0.1:{port}{path}")
            try:
                with urllib.request.urlopen(req) as resp:
                    assert_test(resp.status == expected_status, f"HTTP GET {path} returned {resp.status} ({desc})")
            except Exception as e:
                assert_test(False, f"HTTP GET {path} failed: {e}")
    finally:
        httpd.shutdown()

    print("=" * 70)
    print(f"TEST RESULTS: {passed_tests} PASSED, {failed_tests} FAILED")
    print("=" * 70)
    if failed_tests > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
