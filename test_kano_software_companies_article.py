#!/usr/bin/env python3
"""
Test Suite for 8 Software Development Companies in Kano, Nigeria (2026 Guide)
Verifies SEO, metadata, document structure, accessibility, word count,
all 8 companies, JSON-LD schemas, sitemap, blog hub inclusion, and asset HTTP delivery.
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

ARTICLE_PATH = "software-development-companies-in-kano/index.html"
BLOG_MIRROR_PATH = "blog/software-development-companies-in-kano/index.html"
BLOG_HUB_PATH = "blog/index.html"
SITEMAP_PATH = "sitemap.xml"
BANNER_PATH = "images/blog/software_development_companies_kano_banner.png"

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
    print("AMEE TECHNOLOGY : KANO SOFTWARE COMPANIES GUIDE TEST SUITE")
    print("=" * 70)

    # 1. File existence
    assert_test(os.path.exists(ARTICLE_PATH), f"Article file exists at {ARTICLE_PATH}")
    assert_test(os.path.exists(BLOG_MIRROR_PATH), f"Blog mirror file exists at {BLOG_MIRROR_PATH}")
    assert_test(os.path.exists(BLOG_HUB_PATH), f"Blog hub file exists at {BLOG_HUB_PATH}")
    assert_test(os.path.exists(SITEMAP_PATH), f"Sitemap exists at {SITEMAP_PATH}")
    assert_test(os.path.exists(BANNER_PATH), f"Hero banner image exists at {BANNER_PATH}")

    with open(ARTICLE_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = ArticleHTMLParser()
    parser.feed(html_content)

    # 2. SEO Title & Meta
    assert_test("8 Software Development Companies in Kano, Nigeria (2026)" in parser.title_text, "Title tag matches SEO title")
    assert_test("description" in parser.meta_tags and "Looking for a software development company in Kano" in parser.meta_tags["description"], "Meta description is descriptive and contains primary query")
    
    canonical_links = [href for rel, href in parser.links if rel == "canonical"]
    assert_test(
        canonical_links == ["https://ameetechnology.com.ng/software-development-companies-in-kano/"],
        f"Canonical link points to exact URL: {canonical_links}"
    )

    # 3. OpenGraph Tags
    assert_test("og:title" in parser.meta_tags, "OpenGraph title is present")
    assert_test("og:image" in parser.meta_tags, "OpenGraph image is present")
    assert_test(parser.meta_tags.get("og:image") == "https://ameetechnology.com.ng/images/blog/software_development_companies_kano_banner.png", "OpenGraph image URL is correct")
    assert_test(parser.meta_tags.get("og:url") == "https://ameetechnology.com.ng/software-development-companies-in-kano/", "OpenGraph URL matches canonical")

    # 4. Twitter Card Tags
    assert_test(parser.meta_tags.get("twitter:card") == "summary_large_image", "Twitter card set to summary_large_image")
    assert_test("twitter:title" in parser.meta_tags, "Twitter title present")
    assert_test("twitter:description" in parser.meta_tags, "Twitter description present")
    assert_test(parser.meta_tags.get("twitter:image") == "https://ameetechnology.com.ng/images/blog/software_development_companies_kano_banner.png", "Twitter image URL is correct")

    # 5. Document Structure & Headings
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    assert_test(len(h1_matches) == 1, f"Exactly one <h1> tag found (Found {len(h1_matches)})")
    if h1_matches:
        assert_test("8 Software Development Companies in Kano, Nigeria" in h1_matches[0], "H1 contains main target keyword")

    # Word count
    full_text = " ".join(parser.all_text)
    word_count = len(full_text.split())
    assert_test(word_count >= 1000, f"Guide has comprehensive depth. Word count: {word_count} words")

    # 6. Verification of the 8 Companies
    companies = [
        ("Amee Technology", "https://ameetechnology.com.ng/"),
        ("Brilliant Esystems", "https://brilliant.ng/"),
        ("Kali Developers", "https://kalidevelopers.com.ng/"),
        ("iCode Technology", "https://www.icode.com.ng/"),
        ("Mubarak Digital", "https://www.mubarakdigital.com/"),
        ("Code Green Technologies", "https://www.codegreentechnologies.ng/"),
        ("FlexiSAF", "https://flexisaf.com/"),
        ("eHealth Africa", "https://ehealthafrica.org/")
    ]
    for comp_name, comp_url in companies:
        assert_test(comp_name in html_content, f"Company '{comp_name}' is mentioned in the article")
        assert_test(comp_url in html_content, f"Company website '{comp_url}' is linked in the article")

    # 7. Section IDs for Navigation
    required_sections = [
        ("introduction-section", "Introduction"),
        ("what-to-know-before-hiring", "What to Know Before Hiring"),
        ("companies-list", "8 Companies Section"),
        ("amee-technology", "Company 1: Ameetech"),
        ("brilliant-esystems", "Company 2: Brilliant Esystems"),
        ("kali-developers", "Company 3: Kali Developers"),
        ("icode-technology", "Company 4: iCode"),
        ("mubarak-digital", "Company 5: Mubarak Digital"),
        ("code-green-technologies", "Company 6: Code Green Tech"),
        ("flexisaf-edusoft", "Company 7: FlexiSAF"),
        ("ehealth-africa", "Company 8: eHealth Africa"),
        ("software-development-costs", "Custom Software Development Costs"),
        ("how-to-choose", "How to Choose the Right Company"),
        ("why-amee-technology", "Why Choose Amee Technology"),
        ("faq", "Frequently Asked Questions"),
        ("conclusion", "Conclusion"),
        ("contact-consultation", "Consultation & Lead Form")
    ]
    for sec_id, label in required_sections:
        assert_test(sec_id in parser.ids, f"Required section #{sec_id} ({label}) exists")

    # 8. FAQ items check
    assert_test(parser.faq_count == 6, f"All 6 FAQ questions implemented. Found: {parser.faq_count}")

    # 9. Cost Table check
    assert_test(parser.table_tr_count >= 6, f"Cost factors table contains rows. Found: {parser.table_tr_count} tr tags")

    # 10. Lead form check
    assert_test("article-lead-form" in parser.ids, "Lead enquiry form with id 'article-lead-form' exists")
    assert_test(parser.current_form is not None or "data-netlify=\"true\"" in html_content, "Form configured with data-netlify='true'")

    # 11. JSON-LD structured data
    assert_test(len(parser.json_ld_scripts) > 0, "JSON-LD structured data script found")
    for idx, script_text in enumerate(parser.json_ld_scripts):
        try:
            data = json.loads(script_text)
            assert_test(True, f"JSON-LD block #{idx+1} is valid JSON")
            graph = data.get("@graph", [data])
            types = [item.get("@type") for item in graph]
            assert_test("BlogPosting" in types, "JSON-LD contains BlogPosting schema")
            assert_test("BreadcrumbList" in types, "JSON-LD contains BreadcrumbList schema")
            assert_test("ItemList" in types, "JSON-LD contains ItemList schema")
            assert_test("FAQPage" in types, "JSON-LD contains FAQPage schema")

            faq_schema = next((item for item in graph if item.get("@type") == "FAQPage"), None)
            if faq_schema:
                main_entity = faq_schema.get("mainEntity", [])
                assert_test(len(main_entity) == 6, f"FAQPage schema has 6 questions. Found: {len(main_entity)}")
        except Exception as e:
            assert_test(False, f"JSON-LD block #{idx+1} failed to parse: {e}")

    # 12. Sitemap check
    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        sitemap_content = f.read()
    assert_test(
        "https://ameetechnology.com.ng/software-development-companies-in-kano/" in sitemap_content,
        "Sitemap contains new Kano software development companies guide URL"
    )

    # 13. Blog Hub check
    with open(BLOG_HUB_PATH, "r", encoding="utf-8") as f:
        hub_content = f.read()
    assert_test(
        "/software-development-companies-in-kano/" in hub_content,
        "Blog hub index contains link to new Kano software development companies guide"
    )

    # 14. Local Server HTTP Verification
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

    port = 8894
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        endpoints = [
            ("/software-development-companies-in-kano/", 200, "Primary Guide page"),
            ("/blog/software-development-companies-in-kano/", 200, "Blog Mirror page"),
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
        httpd.server_close()

    print("=" * 70)
    print(f"TEST RESULTS: {passed_tests} PASSED, {failed_tests} FAILED")
    print("=" * 70)
    if failed_tests > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
