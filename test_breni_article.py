import os
import re
import json
import unittest
import http.server
import socketserver
import threading
import urllib.request
from PIL import Image

class TestBrenArticle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article_path = os.path.join(os.path.dirname(__file__), 'blog', 'abubakar-sadik-umar-breni-founder-story', 'index.html')
        cls.banner_path = os.path.join(os.path.dirname(__file__), 'images', 'blog', 'abubakar_sadik_umar_breni_banner.png')
        cls.hub_path = os.path.join(os.path.dirname(__file__), 'blog', 'index.html')
        cls.sitemap_path = os.path.join(os.path.dirname(__file__), 'sitemap.xml')

        with open(cls.article_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()

        # Start a local HTTP test server on port 8894
        cls.port = 8894
        socketserver.TCPServer.allow_reuse_address = True
        handler = http.server.SimpleHTTPRequestHandler
        cls.server = socketserver.TCPServer(("", cls.port), handler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.server.shutdown()
            cls.server.server_close()
        except Exception:
            pass

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.article_path), "Article index.html must exist")

    def test_banner_image(self):
        self.assertTrue(os.path.exists(self.banner_path), "Banner image must exist")
        with Image.open(self.banner_path) as img:
            self.assertEqual(img.size, (1200, 550), "Banner dimensions must be exactly 1200x550")
            self.assertEqual(img.format, "PNG", "Banner must be a PNG image")

    def test_seo_metadata(self):
        # SEO Title
        self.assertIn("<title>Abubakar Sadik Umar: The Story Behind BRENi | Ameetech Blog</title>", self.content)
        
        # Meta description
        self.assertIn('name="description"', self.content)
        self.assertIn("Discover how Abubakar Sadik Umar is rethinking education through BRENi", self.content)
        
        # Canonical URL
        self.assertIn('<link rel="canonical" href="https://ameetechnology.com.ng/blog/abubakar-sadik-umar-breni-founder-story/">', self.content)
        
        # Open Graph
        self.assertIn('<meta property="og:type" content="article">', self.content)
        self.assertIn('content="https://ameetechnology.com.ng/images/blog/abubakar_sadik_umar_breni_banner.png"', self.content)
        
        # Twitter card
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', self.content)

    def test_youtube_embed(self):
        # Check for the nocookie YouTube embed
        self.assertIn("https://www.youtube-nocookie.com/embed/TXSeG47UwYo", self.content)
        self.assertIn("Fagen Hikima interview", self.content)

    def test_breadcrumbs(self):
        self.assertIn('<nav class="article-breadcrumbs" aria-label="Breadcrumb">', self.content)
        self.assertIn('<a href="/">Home</a>', self.content)
        self.assertIn('<a href="/blog/">Blog</a>', self.content)
        self.assertIn('<span class="current">BRENi Founder Story</span>', self.content)

    def test_table_of_contents_anchors(self):
        # Extract all href="#id" from the toc-list
        toc_matches = re.findall(r'<ul class="toc-list">.*?</ul>', self.content, re.DOTALL)
        self.assertTrue(len(toc_matches) > 0, "TOC list must exist")
        toc_html = toc_matches[0]
        anchors = re.findall(r'href="#([a-zA-Z0-9_-]+)"', toc_html)
        self.assertTrue(len(anchors) >= 10, f"Expected at least 10 TOC items, found {len(anchors)}")

        for anchor in anchors:
            pattern = re.compile(rf'id=["\']{anchor}["\']')
            self.assertTrue(bool(pattern.search(self.content)), f"TOC target id='{anchor}' must exist in the HTML")

    def test_content_sections(self):
        sections = [
            "One-Size-Fits-All",
            "Cognitive Science",
            "learner",
            "TikTok",
            "Sacrifices Behind Building a Startup",
            "Why the Right Co-Founder Matters",
            "Your wife can make you or break you",
            "roller coaster",
            "Building a Legacy Beyond the Business",
            "Fagen Hikima"
        ]
        for section in sections:
            self.assertIn(section.lower(), self.content.lower(), f"Article must mention: {section}")

    def test_json_ld_schema(self):
        json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.content, re.DOTALL)
        self.assertTrue(len(json_ld_matches) > 0, "JSON-LD schema script must exist")
        
        parsed = json.loads(json_ld_matches[0].strip())
        self.assertIn("@graph", parsed)
        graph = parsed["@graph"]
        
        types = [item["@type"] for item in graph]
        self.assertIn("BlogPosting", types)
        self.assertIn("BreadcrumbList", types)
        self.assertIn("VideoObject", types)
        self.assertIn("FAQPage", types)

        # Check VideoObject properties
        video_obj = next(item for item in graph if item["@type"] == "VideoObject")
        self.assertIn("TXSeG47UwYo", video_obj["embedUrl"])
        self.assertEqual(video_obj["name"], "Abubakar Sadik Umar, BRENi founder — Fagen Hikima interview")

    def test_hub_and_sitemap_inclusion(self):
        # Check blog hub
        with open(self.hub_path, 'r', encoding='utf-8') as f:
            hub_content = f.read()
        self.assertIn('/blog/abubakar-sadik-umar-breni-founder-story/', hub_content)
        self.assertIn('abubakar_sadik_umar_breni_banner.png', hub_content)

        # Check sitemap
        with open(self.sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        self.assertIn('<loc>https://ameetechnology.com.ng/blog/abubakar-sadik-umar-breni-founder-story/</loc>', sitemap_content)

    def test_http_serving_200(self):
        url = f"http://localhost:{self.port}/blog/abubakar-sadik-umar-breni-founder-story/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            self.assertIn("Rethinking Education", body)
            self.assertIn("TXSeG47UwYo", body)

if __name__ == '__main__':
    unittest.main()
