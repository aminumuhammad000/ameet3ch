#!/usr/bin/env python3
"""
Test Suite for Ameetech Business & Economics Academy.
Verifies Landing Page, Categories, Lessons, Quizzes, Search Index,
PDF Generation, API Endpoints, Phone Normalization, Rate Limiting, and SEO.
"""

import os
import re
import json
import unittest
import urllib.request
import urllib.error
import threading
import time
import socketserver
from html.parser import HTMLParser

from academy_data import CATEGORIES, LESSONS, CATEGORY_MAP, LESSON_MAP
from academy_backend import (
    normalize_nigerian_phone,
    validate_email_address,
    process_guide_request,
    check_rate_limit,
    get_aggregate_stats,
    init_db
)

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
ACADEMY_ROOT = os.path.join(REPO_ROOT, "academy", "business-economics")
DOWNLOADS_DIR = os.path.join(ACADEMY_ROOT, "downloads")
SITEMAP_PATH = os.path.join(REPO_ROOT, "sitemap.xml")

class AcademyTestSuite(unittest.TestCase):

    def setUp(self):
        init_db()
        from academy_backend import get_db
        conn = get_db()
        conn.execute("DELETE FROM rate_limits")
        conn.commit()
        conn.close()

    def test_01_landing_page_exists_and_valid(self):
        landing_file = os.path.join(ACADEMY_ROOT, "index.html")
        self.assertTrue(os.path.exists(landing_file), "Academy landing page index.html must exist")
        with open(landing_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<title>Ameetech Business & Economics Academy", content)
        self.assertIn('id="academy-search-input"', content)
        self.assertIn('class="category-grid"', content)
        self.assertIn('class="study-guide-cta-box"', content)
        self.assertIn("Frequently Asked Questions", content)
        self.assertIn('"@type": "EducationalOrganization"', content)

    def test_02_all_8_categories_generated(self):
        self.assertEqual(len(CATEGORIES), 8, "There must be exactly 8 curriculum categories")
        for cat in CATEGORIES:
            cat_dir = os.path.join(ACADEMY_ROOT, cat["slug"])
            cat_index = os.path.join(cat_dir, "index.html")
            self.assertTrue(os.path.exists(cat_index), f"Category page for {cat['slug']} must exist")
            with open(cat_index, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(cat["name"], content)
            self.assertIn('"@type": "Course"', content)
            self.assertIn('"@type": "BreadcrumbList"', content)

    def test_03_all_lesson_pages_generated_and_structured(self):
        for lesson in LESSONS:
            cat = CATEGORY_MAP[lesson["category_id"]]
            lesson_file = os.path.join(ACADEMY_ROOT, cat["slug"], lesson["slug"], "index.html")
            self.assertTrue(os.path.exists(lesson_file), f"Lesson file {lesson_file} must exist")
            with open(lesson_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(lesson["title"], content)
            self.assertIn("Learning Objectives", content)
            self.assertIn("Key Takeaways", content)
            self.assertIn("Knowledge Check", content)
            self.assertIn("quiz-option-btn", content)
            self.assertIn('data-action="open-guide-modal"', content)
            self.assertIn('"@type": "LearningResource"', content)
            self.assertIn('"@type": "Article"', content)

    def test_04_genuine_pdf_study_guides_exist_and_non_empty(self):
        self.assertTrue(os.path.exists(DOWNLOADS_DIR), "Downloads directory must exist")
        for lesson in LESSONS:
            pdf_file = os.path.join(DOWNLOADS_DIR, f"{lesson['slug']}-study-guide.pdf")
            self.assertTrue(os.path.exists(pdf_file), f"PDF file {pdf_file} must exist")
            size = os.path.getsize(pdf_file)
            self.assertGreater(size, 20000, f"PDF file {pdf_file} must be greater than 20KB")
            with open(pdf_file, "rb") as f:
                header = f.read(5)
            self.assertEqual(header, b"%PDF-", f"{pdf_file} must start with standard PDF magic bytes %PDF-")

    def test_05_search_index_json_valid(self):
        search_file = os.path.join(ACADEMY_ROOT, "academy-search.json")
        self.assertTrue(os.path.exists(search_file), "academy-search.json must exist")
        with open(search_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertGreaterEqual(len(data), len(LESSONS))
        for item in data:
            self.assertIn("title", item)
            self.assertIn("url", item)
            self.assertIn("category", item)
            self.assertIn("summary", item)

    def test_06_phone_normalization(self):
        # Nigerian local numbers
        self.assertEqual(normalize_nigerian_phone("08100015498"), "+2348100015498")
        self.assertEqual(normalize_nigerian_phone("0803 123 4567"), "+2348031234567")
        self.assertEqual(normalize_nigerian_phone("2348100015498"), "+2348100015498")
        self.assertEqual(normalize_nigerian_phone("+2348100015498"), "+2348100015498")
        # International numbers
        self.assertEqual(normalize_nigerian_phone("+1 555 123 4567"), "+15551234567")
        self.assertEqual(normalize_nigerian_phone("+44 7911 123456"), "+447911123456")
        # Invalid
        self.assertEqual(normalize_nigerian_phone("abcd"), "")
        self.assertEqual(normalize_nigerian_phone("123"), "")

    def test_07_email_validation(self):
        self.assertTrue(validate_email_address("learner@example.com"))
        self.assertTrue(validate_email_address("aminu.muhammad@ameetechnology.com.ng"))
        self.assertFalse(validate_email_address("invalid-email"))
        self.assertFalse(validate_email_address("@missinguser.com"))

    def test_08_request_processing_and_consent_tracking(self):
        # WhatsApp delivery request
        payload_wa = {
            "name": "Bello Kano",
            "delivery_method": "whatsapp",
            "whatsapp": "08100015498",
            "guide_slug": "scarcity-and-opportunity-cost",
            "promotional_consent": True
        }
        res_wa = process_guide_request(payload_wa, ip_address="192.168.1.10")
        self.assertTrue(res_wa["success"])
        self.assertIn("request_id", res_wa)
        self.assertEqual(res_wa["delivery_method"], "whatsapp")
        self.assertTrue(res_wa["direct_download_url"].endswith(".pdf"))

        # Email delivery request
        payload_em = {
            "name": "Amina Sani",
            "delivery_method": "email",
            "email": "amina@example.com",
            "guide_slug": "revenue-gross-operating-net-profit",
            "promotional_consent": False
        }
        res_em = process_guide_request(payload_em, ip_address="192.168.1.11")
        self.assertTrue(res_em["success"])
        self.assertEqual(res_em["delivery_method"], "email")

        # Stats check
        stats = get_aggregate_stats()
        self.assertGreaterEqual(stats["total_requests"], 2)
        self.assertGreaterEqual(stats["whatsapp_requests"], 1)
        self.assertGreaterEqual(stats["email_requests"], 1)

    def test_09_anti_abuse_rate_limiting(self):
        test_ip = "10.0.0.99"
        # 5 allowed requests
        for _ in range(5):
            self.assertTrue(check_rate_limit(test_ip, max_requests=5, window_seconds=60))
        # 6th must fail
        self.assertFalse(check_rate_limit(test_ip, max_requests=5, window_seconds=60))

    def test_10_sitemap_includes_academy(self):
        with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
            sitemap_content = f.read()
        self.assertIn("https://ameetechnology.com.ng/academy/business-economics/", sitemap_content)
        self.assertIn("https://ameetechnology.com.ng/academy/business-economics/economics-fundamentals/", sitemap_content)
        self.assertIn("https://ameetechnology.com.ng/academy/business-economics/economics-fundamentals/scarcity-and-opportunity-cost/", sitemap_content)

if __name__ == "__main__":
    unittest.main()
