import unittest
import os
import re

class TestNCDPartnershipArticle(unittest.TestCase):
    def test_article_exists(self):
        fpath = "blog/amee-technology-official-software-partner-ncd-summit-2026/index.html"
        self.assertTrue(os.path.exists(fpath), "Article index.html must exist")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Verify title
        self.assertIn("AMEE TECHNOLOGY Named Software Partner for NCD Summit 2026", content)
        # Verify H1
        self.assertIn("AMEE TECHNOLOGY Named Official Software Partner for Northern Creative Designers Summit 2.0", content)
        # Verify Canonical
        self.assertIn("https://ameetechnology.com.ng/blog/amee-technology-official-software-partner-ncd-summit-2026/", content)
        # Verify Event Details
        self.assertIn("19 December 2026", content)
        self.assertIn("Kano, Nigeria", content)
        self.assertIn("9:00 PM", content)
        self.assertIn("Official Software Partner", content)
        self.assertIn("NewsArticle", content)
    
    def test_banner_exists(self):
        webp_path = "images/blog/amee-technology-ncd-summit-2026-software-partner.webp"
        png_path = "images/blog/amee-technology-ncd-summit-2026-software-partner.png"
        self.assertTrue(os.path.exists(webp_path), "Webp banner must exist")
        self.assertTrue(os.path.exists(png_path), "Png banner must exist")

    def test_blog_index_has_announcement(self):
        with open("blog/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("/blog/amee-technology-official-software-partner-ncd-summit-2026/", content)

    def test_sitemap_has_announcement(self):
        with open("sitemap.xml", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("https://ameetechnology.com.ng/blog/amee-technology-official-software-partner-ncd-summit-2026/", content)

    def test_index_page_updates(self):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        # Aisha removed
        self.assertNotIn("Aisha Muhammad Garba", content)
        # AmeeData review removed
        self.assertNotIn("AmeeData</h3>\n                            <span>Mobile Billing Ecosystem", content)
        # Google review present
        self.assertIn("Verified Google Maps Review", content)
        # Service cards have logos
        self.assertIn('images/custom_software_dev.png', content)
        self.assertIn('images/ai_automation.png', content)
        # North C Designers in portfolio
        self.assertIn('projects/northcdesigners.html', content)

if __name__ == "__main__":
    unittest.main()
