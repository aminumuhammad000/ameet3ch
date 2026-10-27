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

    def test_partners_section(self):
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<!-- Strategic Partners Section (Hidden for now as requested)", content)
        self.assertNotIn('<a href="#partners"', content)
        self.assertIn("North C Designers", content)

    def test_partner_images_exist(self):
        for img in ["images/northcdesigners.png", "images/salafi_technology.png", "images/pioneers_ict.png"]:
            self.assertTrue(os.path.exists(img), f"{img} must exist")
            self.assertGreater(os.path.getsize(img), 1000, f"{img} must be non-empty")

    def test_cleanup_unused_files(self):
        unused_files = [
            "generate_banner.py",
            "generate_breni_banner.py",
            "generate_drone_forge_banner.py",
            "generate_ncd_banner.py",
            "projects/generate_projects.py",
            "images/Aisha_Muhammad_Garba.jpeg",
            "images/ameelogo.jpg",
            "seoquake-audit-ameetechnology.com.ng-2026-09-29.pdf"
        ]
        for f in unused_files:
            self.assertFalse(os.path.exists(f), f"Unused file {f} should have been removed")

    def test_google_maps_reviews_scrollable(self):
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("stories-scrollable", html)
        self.assertIn("stories-scroll-btn", html)
        self.assertIn("Salisu Umar", html)
        self.assertIn("Ibrahim B.", html)
        self.assertIn("Kabiru Sani", html)
        self.assertIn("Usman Danlami", html)
        self.assertIn("Dr. Mansur Aliyu", html)
        self.assertIn("Hauwa Abdullahi", html)
        self.assertIn("Bello Garba", html)
        self.assertIn("Fatima Zahra", html)
        self.assertIn("Abubakar Sadik Umar", html)
        
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        self.assertIn("scrollbar-width: none", css)
        self.assertIn("::-webkit-scrollbar", css)
        self.assertIn("scroll-behavior: smooth", css)

if __name__ == "__main__":
    unittest.main()
