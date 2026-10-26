#!/usr/bin/env python3
"""
Ameetech Business & Economics Academy | Static Site & PDF Generator
Builds the complete static academy site, lesson pages, category indexes,
search index, and genuine offline-readable branded PDF study guides.
"""

import os
import sys
import json
import subprocess
import html
from academy_data import CATEGORIES, LESSONS, CATEGORY_MAP, LESSON_MAP

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ACADEMY_ROOT = os.path.join(BASE_DIR, "academy", "business-economics")
DOWNLOADS_DIR = os.path.join(ACADEMY_ROOT, "downloads")
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap.xml")

SITE_BASE_URL = "https://ameetechnology.com.ng"

def get_shared_header(current_path=""):
    return """
    <!-- Header Navigation -->
    <header>
        <div class="mobile">
            <ul>
                <li><a href="/#services" class="nav" title="Our Services">Services</a></li>
                <li><a href="/#portfolio" class="nav" title="Our Portfolio">Portfolio</a></li>
                <li><a href="https://toolkits.ameetechnology.com.ng" class="nav" title="Free Business Toolkits" target="_blank" rel="noopener noreferrer"><i class="fa-solid fa-toolbox"></i> Toolkits</a></li>
                <li><a href="/blog/" class="nav" title="Articles & Guides">Blog</a></li>
                <li><a href="/academy/business-economics/" class="nav" title="Business & Economics Academy" style="color:var(--primary-color);font-weight:700;"><i class="fa-solid fa-graduation-cap"></i> Academy</a></li>
                <li><a href="/#about" class="nav" title="About Amee Technology Ltd">About</a></li>
            </ul>
        </div>

        <nav>
            <div class="logo">
                <a href="/" style="display:flex;align-items:center;gap:10px;text-decoration:none;color:inherit;">
                    <img src="/images/ameelogo.png" alt="Amee Technology Logo" width="46" height="46">
                    <span class="logo-text">Amee Technology</span>
                </a>
            </div>
            <ul>
                <li><a href="/#services" title="Our Services">Services</a></li>
                <li><a href="/#portfolio" title="Our Portfolio">Portfolio</a></li>
                <li><a href="https://toolkits.ameetechnology.com.ng" title="Free Business Toolkits" target="_blank" rel="noopener noreferrer"><i class="fa-solid fa-toolbox" style="margin-right: 4px; color: var(--primary);"></i> Toolkits</a></li>
                <li><a href="/blog/" title="Articles & Insights">Blog</a></li>
                <li><a href="/academy/business-economics/" title="Business & Economics Academy" style="color:var(--primary-color);font-weight:700;"><i class="fa-solid fa-graduation-cap"></i> Academy</a></li>
                <li><a href="/#about" title="About Amee Technology Ltd">About</a></li>
                <li class="nav-cta">
                    <a href="https://wa.me/2348100015498?text=Hello%20Amee%20Technology%2C%20I%20am%20exploring%20the%20Business%20%26%20Economics%20Academy." target="_blank" rel="noopener noreferrer" title="Chat on WhatsApp">
                        <i class="fa-brands fa-whatsapp"></i> Chat on WhatsApp
                    </a>
                </li>
            </ul>
            <div class="menu">
                <i class="fa-solid fa-bars" title="Menu"></i>
                <i class="fa-solid fa-xmark" title="Close Menu"></i>
            </div>
        </nav>
    </header>
    """

def get_shared_footer():
    return """
    <!-- start of the footer element  -->
    <footer class="site-footer">
        <div class="footer-inner">

            <!-- Column 1: Brand -->
            <div class="footer-col footer-brand">
                <div class="footer-logo">
                    <img src="/images/ameelogo.png" alt="Amee Technology Ltd" loading="lazy">
                    <span>Amee Technology</span>
                </div>
                <p class="footer-tagline">Building premium digital products, AI systems, and empowering entrepreneurs with practical economics and business education across Africa.</p>
                <div class="footer-socials">
                    <a href="https://web.facebook.com/profile.php?id=61550987333969" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
                    <a href="https://www.instagram.com/amee.tech" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
                    <a href="https://www.tiktok.com/@amee.tech?_t=ZM-8t3mEOfPgTF&_r=1" target="_blank" rel="noopener noreferrer" aria-label="TikTok"><i class="fa-brands fa-tiktok"></i></a>
                    <a href="https://www.youtube.com/@ameetech" target="_blank" rel="noopener noreferrer" aria-label="YouTube"><i class="fa-brands fa-youtube"></i></a>
                    <a href="https://linkedin.com/in/aminu-muhammad-ameetech" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
                </div>
            </div>

            <!-- Column 2: Academy & Services -->
            <div class="footer-col">
                <h4 class="footer-heading">Academy Tracks</h4>
                <ul class="footer-links">
                    <li><a href="/academy/business-economics/economics-fundamentals/">Economics Fundamentals</a></li>
                    <li><a href="/academy/business-economics/accounting-financial-literacy/">Accounting & Profitability</a></li>
                    <li><a href="/academy/business-economics/business-models-strategy/">Business Models & Moats</a></li>
                    <li><a href="/academy/business-economics/marketing-consumer-behaviour/">CAC, LTV & Marketing</a></li>
                    <li><a href="/academy/business-economics/digital-business-technology-economics/">Digital & SaaS Economics</a></li>
                    <li><a href="/#services">Custom Software & AI</a></li>
                </ul>
            </div>

            <!-- Column 3: Company -->
            <div class="footer-col">
                <h4 class="footer-heading">Company & Guides</h4>
                <ul class="footer-links">
                    <li><a href="/#about">About Us</a></li>
                    <li><a href="/#portfolio">Portfolio</a></li>
                    <li><a href="/#stories">Customer Stories</a></li>
                    <li><a href="/blog/">Blog & Insights</a></li>
                    <li><a href="https://toolkits.ameetechnology.com.ng" target="_blank" rel="noopener noreferrer">Free Business Toolkits</a></li>
                    <li><a href="/ameebot.html">AmeeBot AI</a></li>
                    <li><a href="/privacy-policy.html">Privacy Policy</a></li>
                </ul>
            </div>

            <!-- Column 4: Contact -->
            <div class="footer-col footer-contact-col">
                <h4 class="footer-heading">Get In Touch</h4>
                <ul class="footer-contact-list">
                    <li><i class="fa-solid fa-location-dot"></i> <span>Kano, Nigeria</span></li>
                    <li><i class="fa-solid fa-phone"></i> <a href="tel:+2348100015498">+234 810 001 5498</a></li>
                    <li><i class="fa-solid fa-envelope"></i> <a href="mailto:support@ameetechnology.com.ng">support@ameetechnology.com.ng</a></li>
                    <li><i class="fa-brands fa-whatsapp"></i> <a href="https://wa.me/2348100015498" target="_blank" rel="noopener noreferrer">Chat on WhatsApp</a></li>
                </ul>
                <a href="https://wa.me/2348100015498?text=Hello%20Ameetech%2C%20I%20would%20like%20to%20discuss%20a%20project." target="_blank" rel="noopener noreferrer" class="footer-cta-btn">
                    Start a Project <i class="fa-solid fa-arrow-up-right"></i>
                </a>
            </div>

        </div>

        <!-- Bottom bar -->
        <div class="footer-bottom">
            <p>&copy; 2026 Amee Technology Ltd. All rights reserved. &bull; <a href="/privacy-policy.html">Privacy Policy</a></p>
            <p class="footer-made">Crafted with <i class="fa-solid fa-heart" style="color:#a855f7"></i> in Nigeria</p>
        </div>
    </footer>
    <!-- end of the footer element  -->
    """

def get_study_guide_modal_html():
    return """
    <!-- Study Guide Request Modal -->
    <div class="academy-modal-overlay" id="study-guide-modal-overlay">
        <div class="academy-modal" role="dialog" aria-labelledby="modal-guide-title">
            <button class="modal-close-btn" id="modal-close-btn" aria-label="Close modal"><i class="fa-solid fa-xmark"></i></button>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                <div style="width:40px;height:40px;border-radius:10px;background:#F5F3FF;display:flex;align-items:center;justify-content:center;color:#6C2BD9;font-size:1.2rem;">
                    <i class="fa-solid fa-file-pdf"></i>
                </div>
                <div>
                    <h3 id="modal-guide-title" style="margin:0;font-size:1.15rem;">Download Study Guide</h3>
                    <span style="font-size:0.8rem;color:#10B981;font-weight:600;"><i class="fa-solid fa-check-circle"></i> Free Offline Reference</span>
                </div>
            </div>
            <p>Get the complete, illustrated PDF guide with formulas, worked calculations, and review questions delivered directly to you.</p>

            <form id="study-guide-form">
                <input type="hidden" id="guide-slug-input" name="guide_slug" value="">
                
                <div class="form-group">
                    <label for="guide-name">Your Full Name (Optional)</label>
                    <input type="text" id="guide-name" name="name" class="form-input" placeholder="e.g., Aminu Bello">
                </div>

                <div class="form-group">
                    <label>Preferred Delivery Method *</label>
                    <div class="delivery-method-group">
                        <label class="delivery-radio-label">
                            <input type="radio" name="delivery_method" id="delivery-whatsapp" value="whatsapp" checked>
                            <i class="fa-brands fa-whatsapp" style="color:#25D366;font-size:1.1rem;"></i> WhatsApp
                        </label>
                        <label class="delivery-radio-label">
                            <input type="radio" name="delivery_method" id="delivery-email" value="email">
                            <i class="fa-solid fa-envelope" style="color:#6C2BD9;font-size:1.1rem;"></i> Email
                        </label>
                    </div>
                </div>

                <div class="form-group" id="whatsapp-input-group">
                    <label for="guide-whatsapp">WhatsApp Phone Number *</label>
                    <input type="tel" id="guide-whatsapp" name="whatsapp" class="form-input" placeholder="e.g., 0810 001 5498 or +234..." required>
                    <small style="color:#64748B;font-size:0.75rem;margin-top:4px;display:block;">We will send the PDF study guide directly to this number.</small>
                </div>

                <div class="form-group" id="email-input-group" style="display:none;">
                    <label for="guide-email">Email Address *</label>
                    <input type="email" id="guide-email" name="email" class="form-input" placeholder="name@example.com">
                </div>

                <div class="consent-checkbox-wrap">
                    <input type="checkbox" id="guide-consent" name="promotional_consent">
                    <label for="guide-consent">
                        (Optional) Receive occasional updates, practical business masterclasses, and digital growth case studies from Ameetech. You can unsubscribe at any time.
                    </label>
                </div>

                <p style="font-size:0.75rem;color:#94A3B8;margin:8px 0 16px;">
                    We respect your privacy under the NDPR. Your details will strictly be used to deliver the requested educational materials. Review our <a href="/privacy-policy.html" target="_blank" style="color:#6C2BD9;">Privacy Policy</a>.
                </p>

                <button type="submit" class="modal-submit-btn">
                    <i class="fa-solid fa-paper-plane"></i> Send Me The Study Guide
                </button>

                <div class="form-feedback-msg" id="form-feedback-msg"></div>
            </form>
        </div>
    </div>
    """

def build_academy_landing():
    """Generates /academy/business-economics/index.html"""
    category_cards_html = ""
    for cat in sorted(CATEGORIES, key=lambda x: x["order"]):
        lessons_in_cat = [l for l in LESSONS if l["category_id"] == cat["id"]]
        category_cards_html += f"""
        <a href="/academy/business-economics/{cat['slug']}/" class="category-card">
            <div class="category-icon-wrap" style="background:{cat['color']}15;color:{cat['color']};">
                <i class="fa-solid {cat['icon']}"></i>
            </div>
            <h3>{html.escape(cat['name'])}</h3>
            <p>{html.escape(cat['summary'])}</p>
            <div class="category-card-meta">
                <span><i class="fa-solid fa-book-open"></i> {len(lessons_in_cat)} Core Lesson{'s' if len(lessons_in_cat) != 1 else ''}</span>
                <span style="color:{cat['color']};font-weight:600;">Explore Track &rarr;</span>
            </div>
        </a>
        """

    featured_lessons_html = ""
    for lesson in LESSONS[:6]:
        cat = CATEGORY_MAP[lesson["category_id"]]
        featured_lessons_html += f"""
        <a href="/academy/business-economics/{cat['slug']}/{lesson['slug']}/" class="lesson-card">
            <span class="lesson-tag" style="background:{cat['color']}15;color:{cat['color']};">{html.escape(cat['name'])}</span>
            <h3>{html.escape(lesson['title'])}</h3>
            <p>{html.escape(lesson['summary'])}</p>
            <div class="lesson-meta-bar">
                <span><i class="fa-solid fa-clock"></i> {lesson['reading_time']} read</span>
                <span style="font-weight:600;color:#10B981;"><i class="fa-solid fa-signal"></i> {lesson['level']}</span>
            </div>
        </a>
        """

    faq_html = """
    <div class="faq-list">
        <div class="faq-card open">
            <div class="faq-header">
                <span>Is the Ameetech Business & Economics Academy completely free?</span>
                <i class="fa-solid fa-chevron-down faq-icon"></i>
            </div>
            <div class="faq-body">
                Yes. 100% of our online curriculum, interactive quizzes, formulas, and lessons are completely free and open to the public without any paywall, mandatory registration, or credit card requirement.
            </div>
        </div>
        <div class="faq-card">
            <div class="faq-header">
                <span>How do I receive the downloadable PDF study guides?</span>
                <i class="fa-solid fa-chevron-down faq-icon"></i>
            </div>
            <div class="faq-body">
                On any lesson or course page, simply click "Download PDF Study Guide". Select whether you prefer delivery via WhatsApp or Email, enter your contact information, and your high-resolution offline guide will be sent immediately with a direct fallback download link.
            </div>
        </div>
        <div class="faq-card">
            <div class="faq-header">
                <span>How are these lessons tailored for Nigerian and African businesses?</span>
                <i class="fa-solid fa-chevron-down faq-icon"></i>
            </div>
            <div class="faq-body">
                While our curriculum covers globally recognized economic and corporate finance principles, every lesson features practical examples reflecting Nigerian market realities, including currency inflation, logistics bottlenecks, POS transactions, VAT taxation regulations, and real operational benchmarks from leading African enterprises.
            </div>
        </div>
        <div class="faq-card">
            <div class="faq-header">
                <span>Who should study at this Academy?</span>
                <i class="fa-solid fa-chevron-down faq-icon"></i>
            </div>
            <div class="faq-body">
                Our tracks are structured for ambitious SME founders, startup operators, commercial managers, finance students, and software engineers looking to master business metrics (such as CAC, LTV, MRR, contribution margin, and working capital cycles).
            </div>
        </div>
    </div>
    """

    structured_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "EducationalOrganization",
                "@id": f"{SITE_BASE_URL}/academy/business-economics/#organization",
                "name": "Ameetech Business & Economics Academy",
                "url": f"{SITE_BASE_URL}/academy/business-economics/",
                "description": "Free, open-access Business, Finance, and Economics Academy by Amee Technology Ltd.",
                "publisher": {
                    "@type": "Organization",
                    "name": "Amee Technology Ltd",
                    "url": SITE_BASE_URL,
                    "logo": f"{SITE_BASE_URL}/images/ameelogo.png"
                }
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": SITE_BASE_URL + "/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Business & Economics Academy",
                        "item": f"{SITE_BASE_URL}/academy/business-economics/"
                    }
                ]
            }
        ]
    }

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ameetech Business & Economics Academy | Free Courses & Lessons</title>
    <meta name="description" content="Master economics, accounting, financial literacy, business strategy, CAC & LTV marketing, and digital business with free structured courses and downloadable PDF study guides.">
    <link rel="canonical" href="{SITE_BASE_URL}/academy/business-economics/">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Ameetech Business & Economics Academy | Free Courses & Lessons">
    <meta property="og:description" content="Free structured business, finance, and economics education with downloadable PDF study guides for entrepreneurs and professionals.">
    <meta property="og:url" content="{SITE_BASE_URL}/academy/business-economics/">
    <meta property="og:image" content="{SITE_BASE_URL}/images/ameelogo.png">
    
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.1/css/all.min.css">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/academy/business-economics/academy.css">
    
    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {json.dumps(structured_data, indent=2)}
    </script>
</head>
<body class="academy-wrapper">
    {get_shared_header()}

    <!-- Academy Hero -->
    <section class="academy-hero">
        <div class="academy-hero-inner">
            <div class="academy-hero-grid">
                <div class="academy-hero-content">
                    <div class="academy-pill">
                        <i class="fa-solid fa-graduation-cap"></i> Free Open-Access Business &amp; Economics Education
                    </div>
                    <h1>Master Commercial Strategy, <span>Finance, &amp; Economics</span></h1>
                    <p>
                        From opportunity costs and break-even math to SaaS metrics, unit economics, and competitive economic moats. Study practical lessons designed for high-impact decision makers across Africa.
                    </p>

                    <!-- Search Field -->
                    <div class="academy-search-box">
                        <i class="fa-solid fa-magnifying-glass academy-search-icon"></i>
                        <input type="text" id="academy-search-input" class="academy-search-input" placeholder="Search lessons, formulas, or concepts (e.g. Break-even, LTV)..." aria-label="Search lessons">
                        <div id="search-results"></div>
                    </div>

                    <!-- Learning Paths Filter -->
                    <div class="learning-paths-row">
                        <span class="learning-paths-label"><i class="fa-solid fa-route"></i> Learning Paths:</span>
                        <div class="learning-paths-pills">
                            <a href="#categories" class="path-badge"><i class="fa-solid fa-seedling"></i> Beginner Fundamentals</a>
                            <a href="#categories" class="path-badge"><i class="fa-solid fa-scale-balanced"></i> Intermediate Financials</a>
                            <a href="#categories" class="path-badge"><i class="fa-solid fa-chess-knight"></i> Advanced Strategy &amp; SaaS</a>
                        </div>
                    </div>
                </div>

                <!-- Hero Highlights Card -->
                <div class="academy-hero-card">
                    <div class="hero-card-header">
                        <div class="hero-card-badge"><i class="fa-solid fa-bolt"></i> Curriculum Highlights</div>
                        <span class="hero-card-status"><i class="fa-solid fa-unlock"></i> Free Access</span>
                    </div>
                    <div class="hero-stats-grid">
                        <div class="hero-stat-item">
                            <span class="stat-number">8</span>
                            <span class="stat-label">Core Tracks</span>
                        </div>
                        <div class="hero-stat-item">
                            <span class="stat-number">10+</span>
                            <span class="stat-label">Specialist Lessons</span>
                        </div>
                        <div class="hero-stat-item">
                            <span class="stat-number">PDF</span>
                            <span class="stat-label">Offline Guides</span>
                        </div>
                        <div class="hero-stat-item">
                            <span class="stat-number">100%</span>
                            <span class="stat-label">Practical Math</span>
                        </div>
                    </div>
                    <div class="hero-card-features">
                        <div class="hero-feature-item"><i class="fa-solid fa-circle-check"></i> <span>Formulas &amp; step-by-step worked calculations</span></div>
                        <div class="hero-feature-item"><i class="fa-solid fa-circle-check"></i> <span>African market case studies &amp; real business data</span></div>
                        <div class="hero-feature-item"><i class="fa-solid fa-circle-check"></i> <span>Interactive knowledge checks with instant answers</span></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Main Academy Container -->
    <main class="academy-container">
        
        <!-- Categories Section -->
        <section id="categories">
            <div class="section-heading-wrap">
                <h2>Explore Academy Disciplines</h2>
                <p>Select a learning track to access foundational theories, mathematical formulas, and real African commercial case studies.</p>
            </div>

            <div class="category-grid">
                {category_cards_html}
            </div>
        </section>

        <!-- Featured Lessons Section -->
        <section style="margin-top: 20px;">
            <div class="section-heading-wrap" style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px;">
                <div>
                    <h2>Featured Core Lessons</h2>
                    <p>Essential curriculum modules every entrepreneur, manager, and operator must master.</p>
                </div>
            </div>

            <div class="lessons-grid">
                {featured_lessons_html}
            </div>
        </section>

        <!-- Curriculum Study Guide Banner -->
        <section class="study-guide-cta-box">
            <div class="study-guide-cta-text">
                <h3><i class="fa-solid fa-file-pdf"></i> Downloadable Study Guides & Formulas Reference</h3>
                <p>Every lesson includes an offline PDF summary guide complete with worked step-by-step calculations, review questions, and executive cheat sheets.</p>
            </div>
            <button class="study-guide-btn" data-action="open-guide-modal" data-guide-title="Comprehensive Academy Curriculum Guide" data-guide-slug="curriculum-overview">
                <i class="fa-solid fa-download"></i> Get Free PDF Guides
            </button>
        </section>

        <!-- FAQ Section -->
        <section style="margin-top: 56px;">
            <div class="section-heading-wrap">
                <h2>Frequently Asked Questions</h2>
                <p>Everything you need to know about Ameetech Business & Economics Academy.</p>
            </div>
            {faq_html}
        </section>

    </main>

    {get_shared_footer()}
    {get_study_guide_modal_html()}

    <script src="/script.js"></script>
    <script src="/academy/business-economics/academy.js"></script>
</body>
</html>
"""
    landing_path = os.path.join(ACADEMY_ROOT, "index.html")
    with open(landing_path, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"[OK] Generated Landing Page: {landing_path}")

def build_category_pages():
    """Generates /academy/business-economics/<category-slug>/index.html"""
    for cat in CATEGORIES:
        cat_dir = os.path.join(ACADEMY_ROOT, cat["slug"])
        os.makedirs(cat_dir, exist_ok=True)

        cat_lessons = [l for l in LESSONS if l["category_id"] == cat["id"]]
        lessons_html = ""
        for lesson in cat_lessons:
            lessons_html += f"""
            <a href="/academy/business-economics/{cat['slug']}/{lesson['slug']}/" class="lesson-card">
                <span class="lesson-tag" style="background:{cat['color']}15;color:{cat['color']};">{html.escape(cat['name'])}</span>
                <h3>{html.escape(lesson['title'])}</h3>
                <p>{html.escape(lesson['summary'])}</p>
                <div class="lesson-meta-bar">
                    <span><i class="fa-solid fa-clock"></i> {lesson['reading_time']} read</span>
                    <span style="font-weight:600;color:#10B981;"><i class="fa-solid fa-signal"></i> {lesson['level']}</span>
                </div>
            </a>
            """

        cat_url = f"{SITE_BASE_URL}/academy/business-economics/{cat['slug']}/"
        structured_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Course",
                    "@id": f"{cat_url}#course",
                    "name": cat["name"],
                    "description": cat["summary"],
                    "provider": {
                        "@type": "Organization",
                        "name": "Amee Technology Ltd",
                        "url": SITE_BASE_URL
                    },
                    "isAccessibleForFree": True
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home",
                            "item": SITE_BASE_URL + "/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "Academy",
                            "item": f"{SITE_BASE_URL}/academy/business-economics/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "name": cat["name"],
                            "item": cat_url
                        }
                    ]
                }
            ]
        }

        page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(cat['name'])} | Ameetech Business & Economics Academy</title>
    <meta name="description" content="{html.escape(cat['summary'])}">
    <link rel="canonical" href="{cat_url}">
    
    <meta property="og:type" content="website">
    <meta property="og:title" content="{html.escape(cat['name'])} | Ameetech Academy">
    <meta property="og:description" content="{html.escape(cat['summary'])}">
    <meta property="og:url" content="{cat_url}">
    <meta property="og:image" content="{SITE_BASE_URL}/images/ameelogo.png">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.1/css/all.min.css">
    
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/academy/business-economics/academy.css">
    
    <script type="application/ld+json">
    {json.dumps(structured_data, indent=2)}
    </script>
</head>
<body class="academy-wrapper">
    {get_shared_header()}

    <section class="academy-hero" style="background:linear-gradient(135deg, #0D0520 0%, {cat['color']}33 100%);">
        <div class="academy-hero-inner">
            <nav class="lesson-breadcrumbs" style="color:#C4B5FD;margin-bottom:12px;">
                <a href="/" style="color:#CBD5E1;">Home</a> <i class="fa-solid fa-chevron-right" style="font-size:0.7rem;"></i>
                <a href="/academy/business-economics/" style="color:#CBD5E1;">Academy</a> <i class="fa-solid fa-chevron-right" style="font-size:0.7rem;"></i>
                <span>{html.escape(cat['name'])}</span>
            </nav>
            <div class="academy-pill" style="border-color:{cat['color']};color:#FFFFFF;">
                <i class="fa-solid {cat['icon']}"></i> Course Track &bull; {cat['level']}
            </div>
            <h1>{html.escape(cat['name'])}</h1>
            <p>{html.escape(cat['summary'])}</p>
        </div>
    </section>

    <main class="academy-container">
        <div class="section-heading-wrap">
            <h2>Track Curriculum & Lessons</h2>
            <p>Work progressively through these modules to build rigorous, practical understanding.</p>
        </div>

        <div class="lessons-grid">
            {lessons_html}
        </div>

        <section class="study-guide-cta-box" style="margin-top:40px;">
            <div class="study-guide-cta-text">
                <h3><i class="fa-solid fa-file-pdf"></i> Download Complete {html.escape(cat['name'])} Guide</h3>
                <p>Includes complete lecture summaries, formulas, worked examples, and revision flashcards in an offline-ready PDF.</p>
            </div>
            <button class="study-guide-btn" data-action="open-guide-modal" data-guide-title="{html.escape(cat['name'])} Module Guide" data-guide-slug="{cat['slug']}">
                <i class="fa-solid fa-download"></i> Get Track PDF
            </button>
        </section>
    </main>

    {get_shared_footer()}
    {get_study_guide_modal_html()}

    <script src="/script.js"></script>
    <script src="/academy/business-economics/academy.js"></script>
</body>
</html>
"""
        cat_file = os.path.join(cat_dir, "index.html")
        with open(cat_file, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"[OK] Generated Category Page: {cat_file}")

def build_lesson_pages():
    """Generates /academy/business-economics/<category-slug>/<lesson-slug>/index.html"""
    for lesson in LESSONS:
        cat = CATEGORY_MAP[lesson["category_id"]]
        lesson_dir = os.path.join(ACADEMY_ROOT, cat["slug"], lesson["slug"])
        os.makedirs(lesson_dir, exist_ok=True)

        lesson_url = f"{SITE_BASE_URL}/academy/business-economics/{cat['slug']}/{lesson['slug']}/"
        guide_url = f"{SITE_BASE_URL}/academy/business-economics/downloads/{lesson['slug']}-study-guide.pdf"

        # Build Table of Contents & Body HTML
        toc_items_html = ""
        body_sections_html = ""
        for i, sec in enumerate(lesson["content_sections"]):
            sec_id = f"section-{i+1}"
            heading_clean = sec["heading"]
            toc_items_html += f'<li><a href="#{sec_id}">{html.escape(heading_clean)}</a></li>\n'
            
            # Format markdown-like text to HTML
            sec_body = sec["body"].strip()
            # replace math markers or paragraphs
            paragraphs = sec_body.split("\n\n")
            p_html = ""
            for p in paragraphs:
                p = p.strip()
                if not p:
                    continue
                if p.startswith("*") or p.startswith("-"):
                    items = [f"<li>{html.escape(line.lstrip('*- '))}</li>" for line in p.split("\n") if line.strip()]
                    p_html += f"<ul>{''.join(items)}</ul>"
                elif p.startswith("$$") and p.endswith("$$"):
                    math_content = p.strip("$ ")
                    p_html += f'<div class="formula-card"><strong>Formula:</strong><br>{html.escape(math_content)}</div>'
                elif p.startswith("|"):
                    # Table formatting
                    lines = p.split("\n")
                    table_rows = ""
                    for idx, line in enumerate(lines):
                        if "---" in line:
                            continue
                        cells = [c.strip() for c in line.split("|")[1:-1]]
                        tag = "th" if idx == 0 else "td"
                        cell_html = "".join([f"<{tag}>{html.escape(c)}</{tag}>" for c in cells])
                        table_rows += f"<tr>{cell_html}</tr>"
                    p_html += f"<table>{table_rows}</table>"
                else:
                    p_html += f"<p>{p}</p>"
                    
            body_sections_html += f"""
            <section id="{sec_id}">
                <h2>{html.escape(sec['heading'])}</h2>
                {p_html}
            </section>
            """

        # Objectives List
        objectives_html = "".join([f"<li>{html.escape(obj)}</li>" for obj in lesson["objectives"]])

        # Takeaways List
        takeaways_html = "".join([f"<li>{html.escape(t)}</li>" for t in lesson["takeaways"]])

        # Quizzes
        quiz_cards_html = ""
        for q_idx, q in enumerate(lesson.get("quiz", [])):
            options_html = ""
            for o_idx, opt in enumerate(q["options"]):
                is_correct = "true" if o_idx == q["answer_index"] else "false"
                options_html += f"""
                <button type="button" class="quiz-option-btn" data-correct="{is_correct}">
                    <strong>{chr(65 + o_idx)}.</strong> {html.escape(opt)}
                </button>
                """
            quiz_cards_html += f"""
            <div class="quiz-card">
                <div class="quiz-question">Question {q_idx + 1}: {html.escape(q['question'])}</div>
                <div class="quiz-options">
                    {options_html}
                </div>
                <div class="quiz-explanation">
                    <i class="fa-solid fa-circle-info" style="color:#6C2BD9;"></i> <strong>Explanation:</strong> {html.escape(q['explanation'])}
                </div>
            </div>
            """

        # Related Lessons
        related_lessons_html = ""
        for r_slug in lesson.get("related_slugs", []):
            if r_slug in LESSON_MAP:
                r_lesson = LESSON_MAP[r_slug]
                r_cat = CATEGORY_MAP[r_lesson["category_id"]]
                related_lessons_html += f"""
                <a href="/academy/business-economics/{r_cat['slug']}/{r_lesson['slug']}/" class="lesson-card" style="box-shadow:none;border-color:#E2E8F0;">
                    <span class="lesson-tag" style="background:{r_cat['color']}15;color:{r_cat['color']};">{html.escape(r_cat['name'])}</span>
                    <h3 style="font-size:1rem;">{html.escape(r_lesson['title'])}</h3>
                    <div class="lesson-meta-bar" style="border:none;padding:0;">
                        <span><i class="fa-solid fa-clock"></i> {r_lesson['reading_time']}</span>
                        <span style="color:#6C2BD9;font-weight:600;">Read Lesson &rarr;</span>
                    </div>
                </a>
                """

        # Structured Data
        structured_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "LearningResource",
                    "@id": f"{lesson_url}#lesson",
                    "name": lesson["title"],
                    "description": lesson["summary"],
                    "learningResourceType": "Lesson",
                    "educationalLevel": lesson["level"],
                    "timeRequired": f"PT{lesson['reading_time'].split()[0]}M",
                    "provider": {
                        "@type": "Organization",
                        "name": "Amee Technology Ltd",
                        "url": SITE_BASE_URL
                    },
                    "isAccessibleForFree": True
                },
                {
                    "@type": "Article",
                    "@id": f"{lesson_url}#article",
                    "headline": lesson["title"],
                    "description": lesson["summary"],
                    "author": {
                        "@type": "Person",
                        "name": "Aminu Muhammad",
                        "jobTitle": "Founder and Marketer",
                        "url": "https://aminu-ameetech.netlify.app"
                    },
                    "publisher": {
                        "@type": "Organization",
                        "name": "Amee Technology Ltd",
                        "logo": f"{SITE_BASE_URL}/images/ameelogo.png"
                    },
                    "datePublished": "2026-10-22T00:00:00+01:00",
                    "dateModified": "2026-10-22T00:00:00+01:00"
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home",
                            "item": SITE_BASE_URL + "/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "Academy",
                            "item": f"{SITE_BASE_URL}/academy/business-economics/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "name": cat["name"],
                            "item": f"{SITE_BASE_URL}/academy/business-economics/{cat['slug']}/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 4,
                            "name": lesson["title"],
                            "item": lesson_url
                        }
                    ]
                }
            ]
        }

        page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(lesson['title'])} | Ameetech Academy</title>
    <meta name="description" content="{html.escape(lesson['summary'])}">
    <link rel="canonical" href="{lesson_url}">
    
    <meta property="og:type" content="article">
    <meta property="og:title" content="{html.escape(lesson['title'])}">
    <meta property="og:description" content="{html.escape(lesson['summary'])}">
    <meta property="og:url" content="{lesson_url}">
    <meta property="og:image" content="{SITE_BASE_URL}/images/ameelogo.png">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.1/css/all.min.css">
    
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/academy/business-economics/academy.css">
    
    <script type="application/ld+json">
    {json.dumps(structured_data, indent=2)}
    </script>
</head>
<body class="academy-wrapper">
    {get_shared_header()}

    <!-- Main Container -->
    <main class="academy-container lesson-main-container">
        <div class="lesson-layout">

            <!-- Sidebar TOC -->
            <aside class="lesson-sidebar">
                <h4>Table of Contents</h4>
                <ul class="toc-nav">
                    {toc_items_html}
                    <li><a href="#key-takeaways">Key Takeaways</a></li>
                    <li><a href="#knowledge-quiz">Knowledge Check</a></li>
                    <li><a href="#study-guide">Study Guide PDF</a></li>
                </ul>

                <hr style="border:none;border-top:1px solid #E2E8F0;margin:20px 0;">

                <div style="font-size:0.82rem;color:#64748B;">
                    <strong>Track:</strong><br>
                    <a href="/academy/business-economics/{cat['slug']}/" style="color:#6C2BD9;text-decoration:none;font-weight:600;">{cat['name']}</a>
                </div>
            </aside>

            <!-- Main Lesson Content -->
            <article class="lesson-article">
                <header class="lesson-header">
                    <nav class="lesson-breadcrumbs">
                        <a href="/">Home</a> <i class="fa-solid fa-chevron-right" style="font-size:0.65rem;"></i>
                        <a href="/academy/business-economics/">Academy</a> <i class="fa-solid fa-chevron-right" style="font-size:0.65rem;"></i>
                        <a href="/academy/business-economics/{cat['slug']}/">{cat['name']}</a> <i class="fa-solid fa-chevron-right" style="font-size:0.65rem;"></i>
                        <span>{html.escape(lesson['title'])}</span>
                    </nav>

                    <h1>{html.escape(lesson['title'])}</h1>

                    <div class="lesson-badge-row">
                        <span><i class="fa-solid fa-clock"></i> {lesson['reading_time']}</span>
                        <span><i class="fa-solid fa-signal"></i> {lesson['level']}</span>
                        <span><i class="fa-solid fa-calendar-check"></i> Updated 2026</span>
                        <span style="color:#10B981;font-weight:600;"><i class="fa-solid fa-circle-check"></i> Free Public Lesson</span>
                    </div>
                </header>

                <!-- Objectives -->
                <div class="learning-objectives-box">
                    <h3><i class="fa-solid fa-bullseye"></i> Learning Objectives</h3>
                    <ul>
                        {objectives_html}
                    </ul>
                </div>

                <!-- Main Body -->
                <div class="lesson-body">
                    {body_sections_html}
                </div>

                <!-- Key Takeaways -->
                <section id="key-takeaways" class="takeaways-box">
                    <h3><i class="fa-solid fa-lightbulb"></i> Key Takeaways</h3>
                    <ul>
                        {takeaways_html}
                    </ul>
                </section>

                <!-- Knowledge Check Quiz -->
                <section id="knowledge-quiz" class="quiz-section">
                    <h3><i class="fa-solid fa-clipboard-question"></i> Knowledge Check</h3>
                    <p style="margin:0 0 16px;color:#64748B;font-size:0.9rem;">Test your understanding of the concepts covered in this lesson:</p>
                    {quiz_cards_html}
                </section>

                <!-- Study Guide Download Box -->
                <section id="study-guide" class="study-guide-cta-box">
                    <div class="study-guide-cta-text">
                        <h3><i class="fa-solid fa-file-pdf"></i> Download {html.escape(lesson['title'])} Study Guide</h3>
                        <p>Get the complete printable PDF reference sheet with formulas, worked calculations, and review notes delivered to your WhatsApp or Email.</p>
                    </div>
                    <button class="study-guide-btn" data-action="open-guide-modal" data-guide-title="{html.escape(lesson['title'])}" data-guide-slug="{lesson['slug']}">
                        <i class="fa-solid fa-download"></i> Get Free Study Guide
                    </button>
                </section>

                <!-- Related Lessons -->
                {f'<section style="margin-top:40px;"><h3 style="margin-bottom:16px;">Related Lessons</h3><div class="lessons-grid" style="grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));">{related_lessons_html}</div></section>' if related_lessons_html else ''}

            </article>

        </div>
    </main>

    {get_shared_footer()}
    {get_study_guide_modal_html()}

    <script src="/script.js"></script>
    <script src="/academy/business-economics/academy.js"></script>
</body>
</html>
"""
        lesson_file = os.path.join(lesson_dir, "index.html")
        with open(lesson_file, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"[OK] Generated Lesson Page: {lesson_file}")

def generate_pdf_study_guides():
    """Generates genuine, offline-readable, high-quality PDFs for every lesson using Chrome Headless"""
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    for lesson in LESSONS:
        cat = CATEGORY_MAP[lesson["category_id"]]
        pdf_path = os.path.join(DOWNLOADS_DIR, f"{lesson['slug']}-study-guide.pdf")

        # Create styled HTML for printing
        sections_pdf_html = ""
        for sec in lesson["content_sections"]:
            sections_pdf_html += f"""
            <div class="sec">
                <h2>{html.escape(sec['heading'])}</h2>
                <div class="content">{html.escape(sec['body']).replace(chr(10), '<br>')}</div>
            </div>
            """

        objectives_pdf_html = "".join([f"<li>{html.escape(o)}</li>" for o in lesson["objectives"]])
        takeaways_pdf_html = "".join([f"<li>{html.escape(t)}</li>" for t in lesson["takeaways"]])

        quiz_pdf_html = ""
        for i, q in enumerate(lesson.get("quiz", [])):
            options = "<br>".join([f"{chr(65+j)}. {html.escape(opt)}" for j, opt in enumerate(q["options"])])
            correct_opt = chr(65 + q["answer_index"])
            quiz_pdf_html += f"""
            <div style="margin-bottom:14px;padding:10px;background:#f8fafc;border-radius:6px;border:1px solid #e2e8f0;">
                <strong>Q{i+1}: {html.escape(q['question'])}</strong><br>
                <div style="margin:6px 0 6px 10px;font-size:12px;color:#475569;">{options}</div>
                <div style="font-size:11px;color:#065f46;background:#d1fae5;padding:6px;border-radius:4px;">
                    <strong>Correct Answer: {correct_opt}</strong> &bull; {html.escape(q['explanation'])}
                </div>
            </div>
            """

        pdf_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{html.escape(lesson['title'])} | Study Guide</title>
    <style>
        @page {{ size: A4; margin: 20mm 15mm 20mm 15mm; }}
        body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.5; font-size: 13px; margin: 0; padding: 0; }}
        .header {{ border-bottom: 2px solid #6C2BD9; padding-bottom: 12px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: flex-start; }}
        .brand {{ color: #6C2BD9; font-weight: bold; font-size: 16px; letter-spacing: -0.5px; text-transform: uppercase; }}
        .sub {{ font-size: 11px; color: #64748b; margin-top: 2px; }}
        h1 {{ font-size: 20px; color: #0f172a; margin: 0 0 6px; line-height: 1.25; }}
        .meta {{ font-size: 11px; color: #475569; margin-bottom: 14px; }}
        .badge {{ background: #f1f5f9; padding: 3px 8px; border-radius: 4px; font-weight: bold; }}
        .box {{ background: #f5f3ff; border-left: 4px solid #6C2BD9; padding: 12px 14px; margin-bottom: 16px; border-radius: 4px; }}
        .box h3 {{ margin: 0 0 6px; font-size: 13px; color: #4c1d95; }}
        .takeaways {{ background: #ecfdf5; border-left: 4px solid #10b981; padding: 12px 14px; margin-bottom: 16px; border-radius: 4px; }}
        .takeaways h3 {{ margin: 0 0 6px; font-size: 13px; color: #065f46; }}
        ul {{ margin: 0; padding-left: 18px; }}
        li {{ margin-bottom: 4px; }}
        h2 {{ font-size: 14px; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; margin: 16px 0 8px; }}
        .footer {{ border-top: 1px solid #e2e8f0; padding-top: 10px; margin-top: 24px; font-size: 10px; color: #94a3b8; display: flex; justify-content: space-between; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="brand">Ameetech Business & Economics Academy</div>
            <div class="sub">Free Open-Access Professional Curriculum &bull; ameetechnology.com.ng</div>
        </div>
        <div style="text-align:right;">
            <div class="badge">{cat['name']}</div>
            <div class="sub">Level: {lesson['level']} &bull; Rev. 2026</div>
        </div>
    </div>

    <h1>{html.escape(lesson['title'])}</h1>
    <div class="meta">
        <strong>Summary:</strong> {html.escape(lesson['summary'])}
    </div>

    <div class="box">
        <h3>Learning Objectives</h3>
        <ul>{objectives_pdf_html}</ul>
    </div>

    <div class="takeaways">
        <h3>Core Principles & Key Takeaways</h3>
        <ul>{takeaways_pdf_html}</ul>
    </div>

    {sections_pdf_html}

    <div style="margin-top:20px;">
        <h2>Self-Assessment & Review Questions</h2>
        {quiz_pdf_html}
    </div>

    <div class="footer">
        <div>&copy; 2026 Amee Technology Ltd. All rights reserved. Published for educational distribution.</div>
        <div>Online lesson: https://ameetechnology.com.ng/academy/business-economics/{cat['slug']}/{lesson['slug']}/</div>
    </div>
</body>
</html>
"""
        tmp_html_file = f"/tmp/{lesson['slug']}.html"
        with open(tmp_html_file, "w", encoding="utf-8") as f:
            f.write(pdf_html)

        # Run Chrome headless to generate genuine PDF
        cmd = [
            "google-chrome",
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={pdf_path}",
            tmp_html_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            print(f"[OK] Generated Genuine PDF: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
        else:
            print(f"[ERROR] Failed to generate PDF: {pdf_path}")

def build_search_index():
    """Generates academy-search.json for fast client-side querying"""
    search_records = []
    for lesson in LESSONS:
        cat = CATEGORY_MAP[lesson["category_id"]]
        search_records.append({
            "title": lesson["title"],
            "slug": lesson["slug"],
            "category": cat["name"],
            "category_slug": cat["slug"],
            "url": f"/academy/business-economics/{cat['slug']}/{lesson['slug']}/",
            "summary": lesson["summary"],
            "level": lesson["level"],
            "keywords": [
                cat["name"],
                lesson["level"],
                *lesson["objectives"]
            ]
        })

    index_path = os.path.join(ACADEMY_ROOT, "academy-search.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(search_records, f, indent=2)
    print(f"[OK] Generated Search Index: {index_path} ({len(search_records)} items)")

def update_sitemap():
    """Appends all academy pages to sitemap.xml"""
    with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Base Academy URL
    new_urls = [
        f"{SITE_BASE_URL}/academy/business-economics/"
    ]

    for cat in CATEGORIES:
        new_urls.append(f"{SITE_BASE_URL}/academy/business-economics/{cat['slug']}/")

    for lesson in LESSONS:
        cat = CATEGORY_MAP[lesson["category_id"]]
        new_urls.append(f"{SITE_BASE_URL}/academy/business-economics/{cat['slug']}/{lesson['slug']}/")

    # Add each URL if not already present
    added_count = 0
    url_entries = []
    for u in new_urls:
        if u not in content:
            url_entries.append(f"""  <url>
    <loc>{u}</loc>
    <lastmod>2026-10-22</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>""")
            added_count += 1

    if url_entries:
        insert_marker = "</urlset>"
        updated_content = content.replace(insert_marker, "\n".join(url_entries) + "\n" + insert_marker)
        with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"[OK] Updated sitemap.xml (+{added_count} academy URLs)")
    else:
        print("[OK] Sitemap already up to date")

if __name__ == "__main__":
    print("=== Building Ameetech Business & Economics Academy ===")
    build_academy_landing()
    build_category_pages()
    build_lesson_pages()
    generate_pdf_study_guides()
    build_search_index()
    update_sitemap()
    print("=== Build Completed Successfully ===")
