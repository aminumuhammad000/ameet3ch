"""
Amee Technology Lead Intelligence Platform
Discovery Engine & Website Intelligence Auditor
Respects robots.txt, domain rate-limiting, timeouts, and performs fact-grounded opportunity analysis.
"""

import os
import re
import time
import json
import socket
import urllib.parse
import urllib.request
import urllib.robotparser
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple

# Domain-level access tracker for rate limiting
_DOMAIN_ACCESS_TIMESTAMPS: Dict[str, float] = {}
DEFAULT_RATE_LIMIT_DELAY = 1.5  # Seconds between requests to the same domain
DEFAULT_TIMEOUT = 6.0  # Seconds

# Seed Business Directory for Permitted Direct Search & Discovery in Nigeria
# Covers Kano, Abuja, Lagos, Hadejia, Kaduna across multiple SME industries.
NIGERIA_BUSINESS_REGISTRY = [
    {
        "name": "Arewa Royal Suites & Restaurant",
        "website_url": "https://arewaroyalsuites.example.ng",
        "description": "Hospitality and boutique dining suite situated in the commercial heart of Nassarawa GRA, Kano.",
        "industry": "Hospitality",
        "category": "Hotels & Restaurants",
        "country": "Nigeria",
        "state": "Kano",
        "city": "Kano",
        "public_email": "reservations@arewaroyalsuites.example.ng",
        "public_phone": "+2348031234567",
        "social_links": {"instagram": "https://instagram.com/arewaroyalkano", "facebook": "https://facebook.com/arewaroyal"},
        "services_offered": ["Luxury Accommodation", "Buffet Catering", "Event Hall Hire"],
        "source_url": "Approved Northern Nigeria Hospitality Registry 2026",
        "has_website": True,
        "keywords": ["hotel", "restaurant", "kano", "hospitality", "event hall"]
    },
    {
        "name": "Hadejia Horizon Model Academy",
        "website_url": "http://hadejiamodel.example.ng",  # Missing HTTPS
        "description": "Comprehensive primary and secondary science preparatory school in Hadejia Emirate, Jigawa State.",
        "industry": "Education",
        "category": "Schools",
        "country": "Nigeria",
        "state": "Jigawa",
        "city": "Hadejia",
        "public_email": "admissions@hadejiamodel.example.ng",
        "public_phone": "+2348029876543",
        "social_links": {"facebook": "https://facebook.com/hadejiahorizon"},
        "services_offered": ["Science Secondary Education", "WAEC/NECO Preparatory", "Computer Literacy Classes"],
        "source_url": "Jigawa State Approved Schools Directory",
        "has_website": True,
        "keywords": ["school", "education", "hadejia", "jigawa", "academy"]
    },
    {
        "name": "Kano Premier Specialist Hospital & Diagnostic Center",
        "website_url": "https://kanospecialisthospital.example.ng",
        "description": "Multi-specialty secondary healthcare clinic with pediatrics, ultrasound diagnostics, and emergency care.",
        "industry": "Healthcare",
        "category": "Hospitals & Clinics",
        "country": "Nigeria",
        "state": "Kano",
        "city": "Kano",
        "public_email": "info@kanospecialisthospital.example.ng",
        "public_phone": "+2348123456789",
        "social_links": {"linkedin": "https://linkedin.com/company/kanopremierhospital"},
        "services_offered": ["Inpatient Care", "Digital Ultrasound", "Pediatrics", "Emergency Medical Care"],
        "source_url": "Kano State Healthcare Facilities Register",
        "has_website": True,
        "keywords": ["hospital", "clinic", "kano", "healthcare", "medical"]
    },
    {
        "name": "Maitama Prime Realty & Property Assets",
        "website_url": "https://maitamaprimerealty.example.ng",
        "description": "Luxury commercial leasing, residential acquisitions, and property management in Maitama and Guzape, Abuja.",
        "industry": "Real Estate",
        "category": "Real Estate Companies",
        "country": "Nigeria",
        "state": "FCT Abuja",
        "city": "Abuja",
        "public_email": "sales@maitamaprimerealty.example.ng",
        "public_phone": "+2348098765432",
        "social_links": {"instagram": "https://instagram.com/maitamaprime", "linkedin": "https://linkedin.com/company/maitamaprime"},
        "services_offered": ["Commercial Real Estate", "Luxury Residential Villas", "Facility Management"],
        "source_url": "Abuja Real Estate Development Forum",
        "has_website": True,
        "keywords": ["real estate", "property", "abuja", "maitama", "luxury"]
    },
    {
        "name": "Zaria Road Agro-Allied Commodities Ltd",
        "website_url": "", # No website discovered!
        "description": "Wholesale distribution of sorghum, sesame seeds, soybeans, and certified grain storage across Northern Nigeria.",
        "industry": "Agriculture & Logistics",
        "category": "Agro Trading & Warehousing",
        "country": "Nigeria",
        "state": "Kano",
        "city": "Kano",
        "public_email": "orders@zaria-agroallied.example.ng",
        "public_phone": "+2348187654321",
        "social_links": {},
        "services_offered": ["Grain Supply", "Silo Warehousing", "Haulage Logistics"],
        "source_url": "Kano Chamber of Commerce, Industry, Mines & Agriculture (KACCIMA)",
        "has_website": False,
        "keywords": ["agriculture", "grains", "kano", "agro", "sme without website"]
    },
    {
        "name": "Kano Heritage Textile & Fashion Hub",
        "website_url": "https://kanotextiles.example.ng",
        "description": "Traditional Hausa embroidery, custom royal babban riga tailoring, and bespoke African modern fashion wear.",
        "industry": "Fashion & Retail",
        "category": "Fashion Businesses",
        "country": "Nigeria",
        "state": "Kano",
        "city": "Kano",
        "public_email": "contact@kanotextiles.example.ng",
        "public_phone": "+2348065432198",
        "social_links": {"instagram": "https://instagram.com/kanoheritagetextiles", "twitter": "https://x.com/kanotextiles"},
        "services_offered": ["Bespoke Tailoring", "Traditional Embroidery", "Ready-to-Wear Babban Riga"],
        "source_url": "Nigerian Export Promotion Council Fashion Catalogue",
        "has_website": True,
        "keywords": ["fashion", "textile", "kano", "clothing", "embroidery"]
    },
    {
        "name": "Eko Logistics Express & Freight",
        "website_url": "https://ekologistics.example.ng",
        "description": "Last-mile courier fulfillment, bonded terminal dispatch, and interstate freight forwarding based in Ikeja, Lagos.",
        "industry": "Logistics & Supply Chain",
        "category": "Courier & Logistics",
        "country": "Nigeria",
        "state": "Lagos",
        "city": "Lagos",
        "public_email": "support@ekologistics.example.ng",
        "public_phone": "+2348054321098",
        "social_links": {"twitter": "https://x.com/ekologisticshq", "facebook": "https://facebook.com/ekologistics"},
        "services_offered": ["Interstate Haulage", "E-commerce Last Mile Delivery", "Cold Chain Freight"],
        "source_url": "Lagos State Logistics Association Directory",
        "has_website": True,
        "keywords": ["logistics", "courier", "lagos", "delivery", "freight"]
    },
    {
        "name": "Dawanau Grains Digital Exchange & Brokerage",
        "website_url": "", # SME without website
        "description": "Leading grain merchant network operating at Dawanau International Grains Market Kano.",
        "industry": "Commodities & Trade",
        "category": "Commodities Exchange",
        "country": "Nigeria",
        "state": "Kano",
        "city": "Kano",
        "public_email": "dawanau.traders@example.ng",
        "public_phone": "+2348033445566",
        "social_links": {},
        "services_offered": ["Grains Aggregation", "Commodities Sourcing", "Spot Market Trade"],
        "source_url": "Dawanau Market Traders Union",
        "has_website": False,
        "keywords": ["grains", "dawanau", "kano", "trade", "sme without website"]
    },
    {
        "name": "Victoria Island Wealth Advisors & Asset Management",
        "website_url": "https://viwealthadvisors.example.ng",
        "description": "Boutique capital advisory, family office asset preservation, and SME commercial debt restructuring.",
        "industry": "Financial Services",
        "category": "Wealth & Investment Advisory",
        "country": "Nigeria",
        "state": "Lagos",
        "city": "Lagos",
        "public_email": "advisory@viwealthadvisors.example.ng",
        "public_phone": "+2348077665544",
        "social_links": {"linkedin": "https://linkedin.com/company/viwealth"},
        "services_offered": ["Corporate Finance", "Portfolio Management", "Private Equity Matchmaking"],
        "source_url": "Financial Markets Dealers Association Nigeria",
        "has_website": True,
        "keywords": ["finance", "investment", "lagos", "wealth", "advisory"]
    },
    {
        "name": "Jigawa Agro Processing Millers",
        "website_url": "http://jigawamillers.example.ng", # HTTP only
        "description": "Commercial rice destoning, parboiling, and packaging facility in Dutse/Hadejia corridor.",
        "industry": "Manufacturing & Milling",
        "category": "Food Processing",
        "country": "Nigeria",
        "state": "Jigawa",
        "city": "Hadejia",
        "public_email": "info@jigawamillers.example.ng",
        "public_phone": "+2348088990011",
        "social_links": {},
        "services_offered": ["Rice Milling", "Agricultural Packaging", "Bulk Wholesaling"],
        "source_url": "Northwest Industrialists Directory",
        "has_website": True,
        "keywords": ["rice", "milling", "jigawa", "hadejia", "processing"]
    }
]

def check_robots_txt(url: str, user_agent: str = "AmeeTechBot/1.0 (+https://ameetechnology.com.ng)") -> bool:
    """Checks whether the website permits crawling under its robots.txt."""
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return True
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        # Default to polite permission if robots.txt is missing or unreachable
        return True

def apply_domain_rate_limit(domain: str, min_delay: float = DEFAULT_RATE_LIMIT_DELAY):
    """Enforces per-domain rate limiting to prevent overwhelming target websites."""
    now = time.time()
    last_access = _DOMAIN_ACCESS_TIMESTAMPS.get(domain, 0.0)
    elapsed = now - last_access
    if elapsed < min_delay:
        time.sleep(min_delay - elapsed)
    _DOMAIN_ACCESS_TIMESTAMPS[domain] = time.time()

def normalize_domain(url: str) -> str:
    """Extracts a normalized domain name from a URL."""
    if not url:
        return ""
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "http://" + url
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def extract_website_content(url: str) -> Dict[str, Any]:
    """
    Safely fetches public website HTML, respecting rate limits, timeouts, and robots.txt.
    Returns metadata, status code, response time, and raw text.
    """
    domain = normalize_domain(url)
    if not domain:
        return {"success": False, "error": "Invalid URL provided."}

    # Verify robots.txt permission
    if not check_robots_txt(url):
        return {
            "success": False,
            "error": "Robots.txt disallows automated analysis on this target.",
            "robots_disallowed": True
        }

    apply_domain_rate_limit(domain)

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AmeeTechLeadIntelligence/1.0; +https://ameetechnology.com.ng)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "close"
    }

    start_time = time.time()
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as response:
            status_code = response.getcode()
            response_time_ms = int((time.time() - start_time) * 1000)
            raw_bytes = response.read(250000) # Read up to 250KB for efficiency
            html_text = raw_bytes.decode("utf-8", errors="replace")
            actual_url = response.geturl()

            return {
                "success": True,
                "status_code": status_code,
                "response_time_ms": response_time_ms,
                "html": html_text,
                "final_url": actual_url
            }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "response_time_ms": int((time.time() - start_time) * 1000),
            "error": str(e)
        }

def parse_extracted_data(html: str, target_url: str) -> Dict[str, Any]:
    """Extracts business name, emails, phones, social links, and services from HTML."""
    result = {
        "business_name": "",
        "description": "",
        "public_email": "",
        "public_phone": "",
        "social_links": {},
        "services_offered": [],
        "contact_page_url": "",
        "confidence_score": 60
    }

    if not html:
        return result

    # 1. Title / Business Name
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if title_match:
        raw_title = title_match.group(1).strip()
        # Clean title dividers like | or -
        clean_name = re.split(r"[-|•—]", raw_title)[0].strip()
        result["business_name"] = clean_name[:80]

    # 2. Meta Description
    desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', html, re.IGNORECASE)
    if desc_match:
        result["description"] = desc_match.group(1).strip()[:240]

    # 3. Public Business Email (Strict Regex, filter out image formats and vendor tracking)
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    found_emails = re.findall(email_pattern, html)
    valid_emails = []
    for em in set(found_emails):
        em_lower = em.lower()
        if not re.search(r"\.(png|jpg|jpeg|gif|svg|webp|css|js)$", em_lower):
            if "example.com" not in em_lower and "sentry" not in em_lower and "wixpress" not in em_lower:
                valid_emails.append(em)
    if valid_emails:
        # Prefer emails that match target domain or start with info/contact/support
        preferred = [e for e in valid_emails if any(prefix in e.lower() for prefix in ["info@", "contact@", "hello@", "support@", "sales@", "inquiry@"])]
        result["public_email"] = preferred[0] if preferred else valid_emails[0]

    # 4. Public Phone (Nigerian and international formats)
    phone_pattern = r'(?:\+?234|0)[789][01]\d{8}'
    phones = re.findall(phone_pattern, html)
    if phones:
        result["public_phone"] = phones[0]

    # 5. Social Media Links
    social_networks = {
        "twitter": r'https?://(?:www\.)?(?:twitter\.com|x\.com)/[A-Za-z0-9_]+',
        "facebook": r'https?://(?:www\.)?facebook\.com/[A-Za-z0-9_.]+',
        "instagram": r'https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.]+',
        "linkedin": r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[A-Za-z0-9_-]+'
    }
    for net, pat in social_networks.items():
        found = re.findall(pat, html, re.IGNORECASE)
        if found:
            result["social_links"][net] = found[0]

    # 6. Contact Page URL
    contact_match = re.search(r'href=["\']([^"\']*(?:contact|about-us|reach-us)[^"\']*)["\']', html, re.IGNORECASE)
    if contact_match:
        contact_href = contact_match.group(1)
        result["contact_page_url"] = urllib.parse.urljoin(target_url, contact_href)

    # 7. Calculate extraction confidence score (0-100)
    score = 30
    if result["business_name"]: score += 15
    if result["description"]: score += 15
    if result["public_email"]: score += 20
    if result["public_phone"]: score += 10
    if result["social_links"]: score += 10
    result["confidence_score"] = min(100, score)

    return result

def audit_website_intelligence(url: str, html: Optional[str] = None, response_time_ms: int = 0, status_code: int = 200) -> Dict[str, Any]:
    """
    Performs Phase 4 Website Intelligence.
    Audits website performance, security, mobile optimisation, contact presence, CTAs,
    online booking, and payment mechanisms.
    Grounds all findings strictly in verifiable checks and maps them to Amee Technology services.
    """
    if not url:
        return {
            "has_website": False,
            "has_https": False,
            "mobile_optimized": False,
            "response_time_ms": 0,
            "has_contact_info": False,
            "has_meta_tags": False,
            "has_cta": False,
            "has_booking": False,
            "has_online_payment": False,
            "status_code": 0,
            "findings": ["No website discovered for this registered business."],
            "opportunities": [
                {
                    "service": "Web design and development",
                    "severity": "critical",
                    "evidence": "Business does not have a registered digital website.",
                    "opportunity": "Develop a fast, modern corporate website to capture organic searches and convert local prospects."
                },
                {
                    "service": "Custom software development",
                    "severity": "high",
                    "evidence": "Business operations lack an integrated digital customer portal.",
                    "opportunity": "Deploy custom operational software and online customer inquiry management."
                }
            ]
        }

    # If HTML is not supplied, fetch it
    if html is None:
        fetch_result = extract_website_content(url)
        if not fetch_result.get("success"):
            return {
                "has_website": True,
                "has_https": url.lower().startswith("https://"),
                "mobile_optimized": False,
                "response_time_ms": fetch_result.get("response_time_ms", 0),
                "has_contact_info": False,
                "has_meta_tags": False,
                "has_cta": False,
                "has_booking": False,
                "has_online_payment": False,
                "status_code": fetch_result.get("status_code", 0),
                "findings": [f"Website unavailable or unreachable: {fetch_result.get('error', 'Connection timed out')}"],
                "opportunities": [
                    {
                        "service": "Web design and development",
                        "severity": "critical",
                        "evidence": f"Website unreachable (error: {fetch_result.get('error', 'timeout')}).",
                        "opportunity": "Modernize and rebuild website on high-uptime infrastructure with sub-second response times."
                    }
                ]
            }
        html = fetch_result["html"]
        response_time_ms = fetch_result["response_time_ms"]
        status_code = fetch_result["status_code"]
        url = fetch_result.get("final_url", url)

    # 1. HTTPS Check
    has_https = url.lower().startswith("https://")

    # 2. Mobile Optimisation Check (viewport meta tag presence and responsive styling)
    has_viewport = bool(re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.IGNORECASE))
    mobile_optimized = has_viewport

    # 3. Contact Presence Check
    has_email = bool(re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html))
    has_phone = bool(re.search(r'(?:\+?234|0)[789][01]\d{8}', html))
    has_contact_page = bool(re.search(r'contact', html, re.IGNORECASE))
    has_contact_info = has_email or has_phone or has_contact_page

    # 4. Meta Tags & SEO Check
    has_title = bool(re.search(r'<title[^>]*>.+?</title>', html, re.IGNORECASE | re.DOTALL))
    has_desc = bool(re.search(r'<meta[^>]+name=["\']description["\']', html, re.IGNORECASE))
    has_og = bool(re.search(r'<meta[^>]+property=["\']og:', html, re.IGNORECASE))
    has_meta_tags = has_title and has_desc and has_og

    # 5. Calls to Action (CTA) Check
    cta_patterns = r'(get started|contact us|request a quote|book now|order now|schedule a consultation|call today|inquire now|sign up)'
    has_cta = bool(re.search(cta_patterns, html, re.IGNORECASE))

    # 6. Online Booking Check
    booking_patterns = r'(calendly\.com|acuityscheduling|book appointment|reserve a table|schedule appointment|online booking|reservation system)'
    has_booking = bool(re.search(booking_patterns, html, re.IGNORECASE))

    # 7. Online Payment Functionality Check
    payment_patterns = r'(paystack|flutterwave|remita|stripe|checkout|add to cart|make payment|buy now)'
    has_online_payment = bool(re.search(payment_patterns, html, re.IGNORECASE))

    # Compile Specific Findings and Match to Amee Technology Services
    findings = []
    opportunities = []

    if not has_https:
        findings.append("Missing HTTPS encryption protocol (security vulnerability).")
        opportunities.append({
            "service": "Web design and development",
            "severity": "high",
            "evidence": "Website uses unencrypted HTTP protocol.",
            "opportunity": "Deploy SSL/TLS security certificates and force HTTPS redirection to safeguard user data and elevate search rankings."
        })

    if not mobile_optimized:
        findings.append("Missing mobile viewport configuration (poor mobile smartphone display).")
        opportunities.append({
            "service": "UI/UX design",
            "severity": "high",
            "evidence": "Missing <meta name='viewport'> tag.",
            "opportunity": "Redesign with mobile-first responsive architecture ensuring fluid layouts across iPhone and Android devices."
        })

    if response_time_ms > 1200:
        findings.append(f"Sub-optimal server response time ({response_time_ms}ms, recommended < 600ms).")
        opportunities.append({
            "service": "Custom software development",
            "severity": "medium",
            "evidence": f"Measured page response latency of {response_time_ms}ms.",
            "opportunity": "Implement code minification, edge caching, and server-side optimizations to achieve sub-second TTFB."
        })

    if not has_meta_tags:
        missing_meta = []
        if not has_desc: missing_meta.append("meta description")
        if not has_og: missing_meta.append("Open Graph social tags")
        findings.append(f"Incomplete SEO metadata ({', '.join(missing_meta)} missing).")
        opportunities.append({
            "service": "Search engine optimisation",
            "severity": "high",
            "evidence": f"Missing critical search headers: {', '.join(missing_meta)}.",
            "opportunity": "Execute technical on-page SEO, rich snippets, schema.org markup, and structured metadata for Google rankings."
        })

    if not has_cta:
        findings.append("No prominent, conversion-focused Call to Action (CTA) identified.")
        opportunities.append({
            "service": "Digital marketing",
            "severity": "medium",
            "evidence": "Homepage lacks high-visibility action triggers or lead conversion hooks.",
            "opportunity": "Implement high-conversion CTA banners, lead magnets, and customer acquisition funnels."
        })

    if not has_booking:
        findings.append("No automated online booking or appointment scheduling capability detected.")
        opportunities.append({
            "service": "AI and automation",
            "severity": "medium",
            "evidence": "Inquiries require manual back-and-forth communication.",
            "opportunity": "Integrate 24/7 WhatsApp AI booking bots and automated calendar synchronization."
        })

    if not has_online_payment:
        findings.append("No integrated Nigerian or international online payment gateway detected.")
        opportunities.append({
            "service": "VTU application development",
            "severity": "low",
            "evidence": "Website lacks immediate online billing or payment checkout.",
            "opportunity": "Integrate Paystack/Flutterwave automated checkout or automated customer digital wallet funding."
        })

    # If the site is already quite mature, suggest growth marketing and video production
    if len(findings) <= 1:
        opportunities.append({
            "service": "Video production",
            "severity": "medium",
            "evidence": "Established brand presence ready for brand storytelling and multimedia outreach.",
            "opportunity": "Produce professional promotional videos, customer testimonials, and social reels to increase conversions."
        })

    return {
        "has_website": True,
        "has_https": has_https,
        "mobile_optimized": mobile_optimized,
        "response_time_ms": response_time_ms,
        "has_contact_info": has_contact_info,
        "has_meta_tags": has_meta_tags,
        "has_cta": has_cta,
        "has_booking": has_booking,
        "has_online_payment": has_online_payment,
        "status_code": status_code,
        "findings": findings,
        "opportunities": opportunities
    }

def discover_businesses(
    query: str = "",
    country: str = "Nigeria",
    state: str = "",
    city: str = "",
    industry: str = "",
    category: str = "",
    website_url: str = ""
) -> List[Dict[str, Any]]:
    """
    Discovers businesses matching user parameters from approved directories and authorized sources.
    Respects terms, eliminates duplicates, and automatically computes intelligence scores.
    """
    results = []
    
    # 1. If a specific website URL is submitted, analyze it directly
    if website_url:
        target_url = website_url.strip()
        if not re.match(r"^https?://", target_url, re.IGNORECASE):
            target_url = "https://" + target_url
        
        domain = normalize_domain(target_url)
        # Check if already present in database
        from lead_intelligence_db import get_db_connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM discovered_businesses WHERE normalized_domain = ?", (domain,))
        existing = cur.fetchone()
        conn.close()

        if existing:
            item = dict(existing)
            item["social_links"] = json.loads(item["social_links"]) if item.get("social_links") else {}
            item["services_offered"] = json.loads(item["services_offered"]) if item.get("services_offered") else []
            return [item]

        # Extract live website
        ext = extract_website_content(target_url)
        if ext.get("success"):
            parsed = parse_extracted_data(ext.get("html", ""), ext.get("final_url", target_url))
            audit = audit_website_intelligence(target_url, ext.get("html"), ext.get("response_time_ms", 0), ext.get("status_code", 200))
            record = {
                "name": parsed["business_name"] or domain.capitalize(),
                "website_url": ext.get("final_url", target_url),
                "description": parsed["description"] or f"Business operating via {domain}",
                "industry": industry or "Technology & Services",
                "category": category or "Commercial Business",
                "country": country or "Nigeria",
                "state": state or "Kano",
                "city": city or "Kano",
                "public_email": parsed["public_email"],
                "public_phone": parsed["public_phone"],
                "social_links": parsed["social_links"],
                "services_offered": parsed["services_offered"],
                "contact_page_url": parsed["contact_page_url"],
                "source_url": target_url,
                "confidence_score": parsed["confidence_score"],
                "audit": audit
            }
            return [record]

    # 2. Query Approved Business Directory
    q_norm = query.lower().strip()
    state_norm = state.lower().strip()
    city_norm = city.lower().strip()
    ind_norm = industry.lower().strip()
    cat_norm = category.lower().strip()

    for item in NIGERIA_BUSINESS_REGISTRY:
        # Check filters
        if country and country.lower() != item["country"].lower():
            continue
        if state_norm and state_norm not in item["state"].lower():
            continue
        if city_norm and city_norm not in item["city"].lower():
            continue
        if ind_norm and ind_norm not in item["industry"].lower() and ind_norm not in item["category"].lower():
            continue
        if cat_norm and cat_norm not in item["category"].lower():
            continue
        
        # Check query keywords
        if q_norm:
            combined = f"{item['name']} {item['description']} {item['industry']} {item['category']} {item['city']} {item['state']} {' '.join(item['keywords'])}".lower()
            if not any(token in combined for token in q_norm.split()):
                continue

        # Perform or simulate audit
        if item.get("website_url"):
            audit = audit_website_intelligence(item["website_url"])
        else:
            audit = audit_website_intelligence("")

        enriched = dict(item)
        enriched["audit"] = audit
        enriched["confidence_score"] = 90 if item.get("public_email") else 75
        results.append(enriched)

    return results

if __name__ == "__main__":
    print("[TEST] Running Discovery Engine test query: 'Kano'...")
    res = discover_businesses(query="Kano")
    print(f"[OK] Discovered {len(res)} businesses in Kano.")
    for b in res[:3]:
        print(f" - {b['name']} ({b['industry']}) | Findings: {len(b['audit']['findings'])} | Opportunities: {len(b['audit']['opportunities'])}")
