#!/usr/bin/env python3
"""
Generates the 30 structured Ameetech social media flyer prompts.
"""
import json
import csv
from pathlib import Path

FLYER_DATA = [
    {
        "id": "FLYER-001",
        "title": "Custom Enterprise Web Application Development",
        "category": "Software Engineering",
        "filename": "ameetech-01-enterprise-web-apps.png",
        "image_prompt": (
            "Modern, premium square 1080x1080 promotional social media flyer for Ameetech, "
            "a leading Nigerian technology company. Pristine clean white background with bold "
            "vibrant purple accents (#6C2BD9) and elegant soft violet gradients. Center visual shows a sleek "
            "3D glassmorphic web dashboard with responsive data widgets, server architecture nodes, and code elements. "
            "Minimalist corporate aesthetic, polished shadows, strong visual hierarchy. Ameetech logo space top left, "
            "bold typography 'Custom Enterprise Web Applications', clean footer bar containing 'ameetechnology.com.ng' "
            "and WhatsApp icon with '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-002",
        "title": "Native & Cross-Platform Mobile App Development",
        "category": "Mobile Apps",
        "filename": "ameetech-02-mobile-app-development.png",
        "image_prompt": (
            "High-end square social media flyer for Ameetech mobile app engineering. Studio white background "
            "with striking Ameetech purple (#6C2BD9) curved accents. Centerpiece features two floating isometric "
            "smartphones displaying sleek mobile banking and productivity apps with silky UI interactions. "
            "Modern African tech innovation vibe, clean typography, badge reading 'iOS & Android Solutions', "
            "Ameetech branding, footer with website 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-003",
        "title": "VTU & Bill Payments Portal Engineering",
        "category": "Fintech & Telecom",
        "filename": "ameetech-03-vtu-telecom-portals.png",
        "image_prompt": (
            "Professional promotional square flyer for Ameetech VTU platform development. Clean white backdrop, "
            "bold royal purple (#6C2BD9) graphic highlights, restrained lilac ambient glow. Center isometric 3D "
            "illustration of digital airtime, data bundle transactions, lightning-fast payment nodes, and secure fintech "
            "API rails. Premium modern design, mobile-optimized typography, Ameetech logo in corner, footer featuring "
            "'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-004",
        "title": "Ameebot AI Customer Service Automation",
        "category": "AI & Automation",
        "filename": "ameetech-04-ameebot-ai-automation.png",
        "image_prompt": (
            "Sleek square promotional social media flyer for Ameetech AI automation. Pure white studio environment "
            "with energetic Ameetech purple (#6C2BD9) accent waves. Center visual of an intelligent, friendly 3D geometric "
            "AI assistant sphere connected to multi-channel chat bubbles and automated CRM workflows. Crisp layout, "
            "readable headers, Ameetech logo emblem, bottom banner with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-005",
        "title": "Custom ERP & Business Operations Portals",
        "category": "Enterprise Solutions",
        "filename": "ameetech-05-erp-business-portals.png",
        "image_prompt": (
            "Corporate square social flyer for Ameetech Business Portals & ERP systems. Elegant white setting with deep "
            "purple (#6C2BD9) modular frames. 3D isometric representation of integrated enterprise software: finance, "
            "supply chain, human resources, and real-time executive analytics in synchronized harmony. High contrast, "
            "authoritative executive tech branding, official Ameetech identity, 'ameetechnology.com.ng', WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-006",
        "title": "High-Fidelity UI/UX Product Design & Prototyping",
        "category": "UI/UX & Design",
        "filename": "ameetech-06-uiux-product-design.png",
        "image_prompt": (
            "Inspiring square design-focused promotional graphic for Ameetech UI/UX services. Minimalist white canvas "
            "with vibrant purple (#6C2BD9) design rulers, artboards, and wireframe overlays. Center shows layered Figma-style "
            "design components floating with modern typography, micro-interactions, and design token hierarchies. "
            "Top-tier creative tech presentation, Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-007",
        "title": "E-Commerce Platforms & Payment Integrations",
        "category": "E-Commerce",
        "filename": "ameetech-07-ecommerce-platforms.png",
        "image_prompt": (
            "Contemporary square social media flyer for Ameetech E-commerce development. Clean white backdrop with bold "
            "purple (#6C2BD9) checkout accent ribbons. 3D isometric digital shopping cart integrated with secure Nigerian "
            "and international payment gateways, card tokens, and instant order delivery status indicators. High visual clarity, "
            "Ameetech branding, clear contact bar with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-008",
        "title": "Corporate Tech Brand Identity & Design Systems",
        "category": "Branding",
        "filename": "ameetech-08-brand-identity-systems.png",
        "image_prompt": (
            "Sophisticated square promotional flyer for Ameetech Brand Identity services. Crisp white background with "
            "vivid purple (#6C2BD9) brand guidelines swatch book and geometric grid patterns. Central 3D mockups of corporate "
            "stationery, vector logos, responsive typography scales, and cohesive digital assets. Premium Nigerian tech studio feel, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-009",
        "title": "Cloud Infrastructure, Docker & DevOps Optimization",
        "category": "Cloud & DevOps",
        "filename": "ameetech-09-cloud-devops-optimization.png",
        "image_prompt": (
            "Tech-forward square social media flyer for Ameetech Cloud & DevOps solutions. Pure white environment with "
            "energetic deep purple (#6C2BD9) server rack illumination and cloud pipelines. 3D isometric cloud cluster with "
            "interconnected Docker containers, CI/CD pipeline gears, and high-availability load balancers. Clean tech layout, "
            "Ameetech branding, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-010",
        "title": "Secure REST & GraphQL API Engineering",
        "category": "Backend Engineering",
        "filename": "ameetech-10-secure-api-engineering.png",
        "image_prompt": (
            "Precision-engineered square social media flyer for Ameetech API architecture services. White modern background "
            "with bold purple (#6C2BD9) interconnected data pathways and security shield glyphs. Center visual of modular API "
            "gateways, encrypted endpoints, fast response telemetry graphs, and JSON data structures. Highly professional layout, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-011",
        "title": "EdTech Systems & Online Learning Platforms",
        "category": "EdTech",
        "filename": "ameetech-11-edtech-learning-platforms.png",
        "image_prompt": (
            "Clean square social media flyer for Ameetech EdTech & LMS solutions. White open background with vibrant "
            "purple (#6C2BD9) interactive study elements. Central 3D illustration of an interactive digital classroom tablet, "
            "graduation cap icon, live video lecture modules, and course progress tracking badges. Modern educational tech look, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-012",
        "title": "Ameetech Business & Economics Academy Cohorts",
        "category": "Academy & Education",
        "filename": "ameetech-12-business-economics-academy.png",
        "image_prompt": (
            "Prestigious square promotional flyer for Ameetech Business & Economics Academy. Pristine white background with "
            "luxurious Ameetech purple (#6C2BD9) accents and restrained gradient borders. Center showcases 3D business growth "
            "barometer, financial modeling graphs, executive certificates, and strategic roadmaps. Authoritative leadership aesthetic, "
            "official Ameetech Academy branding, 'ameetechnology.com.ng', WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-013",
        "title": "WhatsApp Business Cloud Automation & Lead Bots",
        "category": "Automation",
        "filename": "ameetech-13-whatsapp-business-automation.png",
        "image_prompt": (
            "Vibrant, professional square social flyer for Ameetech WhatsApp Business Cloud API integration. Clean white backdrop "
            "with signature Ameetech purple (#6C2BD9) accents and subtle green notification touches. Center shows a smartphone with "
            "automated customer journey triggers, instant catalog checkout, and 24/7 smart auto-reply bubbles. Mobile-first hierarchy, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-014",
        "title": "Clinic & Hospital HealthTech Management Software",
        "category": "HealthTech",
        "filename": "ameetech-14-healthtech-clinic-management.png",
        "image_prompt": (
            "Reassuring and modern square social media flyer for Ameetech HealthTech systems. Crisp white backdrop with bold "
            "purple (#6C2BD9) healthcare accents and subtle medical cross patterns. 3D isometric hospital tablet displaying "
            "electronic health records (EHR), patient appointment scheduling, pharmacy inventory, and lab results. Clean medical-tech "
            "polish, Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-015",
        "title": "Commercial Real Estate & Property Listing Portals",
        "category": "PropTech",
        "filename": "ameetech-15-real-estate-property-portals.png",
        "image_prompt": (
            "High-impact square social media flyer for Ameetech Real Estate Portals. White architectural setting with "
            "rich purple (#6C2BD9) framing. Center visual of a modern isometric architectural building surrounded by interactive "
            "map location pins, virtual tour badges, and verified property listing cards. Sophisticated Nigerian PropTech feel, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-016",
        "title": "Logistics, Dispatch & Fleet Tracking Systems",
        "category": "Logistics Tech",
        "filename": "ameetech-16-logistics-fleet-tracking.png",
        "image_prompt": (
            "Dynamic square social flyer for Ameetech Logistics & Fleet Management platforms. Clean white ground with bold "
            "Ameetech purple (#6C2BD9) transit lines and route milestones. Center 3D isometric delivery van, GPS satellite tracking "
            "compass, package scanning barcode radar, and real-time transit telemetry. High-tech logistics precision, Ameetech branding, "
            "footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-017",
        "title": "School Management & Student Information Systems",
        "category": "EdTech",
        "filename": "ameetech-17-school-management-systems.png",
        "image_prompt": (
            "Polished square promotional flyer for Ameetech School & University Information Systems. Bright white canvas with "
            "royal purple (#6C2BD9) badges. 3D isometric composition with digital student report cards, automated attendance scanners, "
            "school fee payment ledger, and parent communication portal screens. Educational excellence, Ameetech logo, "
            "footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-018",
        "title": "Microfinance, SACCO & Cooperative Lending Software",
        "category": "Fintech",
        "filename": "ameetech-18-microfinance-cooperative-software.png",
        "image_prompt": (
            "Trustworthy square social media flyer for Ameetech Cooperative & Microfinance platforms. Crisp white background "
            "with secure purple (#6C2BD9) vault and ledger accents. Center 3D isometric illustration of loan disbursement workflows, "
            "member savings ledgers, repayment schedules, and automated interest calculators. Bank-grade fintech aesthetic, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-019",
        "title": "Cloud Point-of-Sale (POS) & Multi-Store Inventory",
        "category": "Retail Tech",
        "filename": "ameetech-19-cloud-pos-inventory-systems.png",
        "image_prompt": (
            "Modern square social graphic for Ameetech Cloud POS and Retail systems. White background with bold Ameetech purple "
            "(#6C2BD9) checkout terminal accents. Center visual showcases an elegant touchscreen POS terminal, receipt printer, "
            "cloud inventory sync arrows, and multi-branch stock reconciliation metrics. Retail innovation, Ameetech branding, "
            "footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-020",
        "title": "Web Application Cybersecurity Hardening & Audits",
        "category": "Cybersecurity",
        "filename": "ameetech-20-cybersecurity-hardening-audits.png",
        "image_prompt": (
            "Authoritative square promotional flyer for Ameetech Cybersecurity & Application Hardening. Minimal white backdrop with "
            "luminous deep purple (#6C2BD9) security grid lines. 3D holographic security shield with cryptographic padlock, "
            "vulnerability scanner readout, zero-trust authentication badges, and SSL encryption lockets. Confident Nigerian "
            "cybersecurity agency feel, Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-021",
        "title": "Enterprise Performance SEO & Search Growth",
        "category": "Growth Marketing",
        "filename": "ameetech-21-performance-seo-growth.png",
        "image_prompt": (
            "Results-driven square social media flyer for Ameetech Performance SEO & Search Visibility. White clean aesthetic "
            "with vibrant purple (#6C2BD9) rank growth charts. Center features a 3D upward trending search engine rankings curve, "
            "SERP snippet preview, keyword target radar, and organic traffic acceleration rockets. Clean typography, Ameetech branding, "
            "footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-022",
        "title": "Corporate 3D Motion Graphics & Tech Media Production",
        "category": "Media Production",
        "filename": "ameetech-22-motion-graphics-media-tech.png",
        "image_prompt": (
            "Creative square social media flyer for Ameetech Tech Media Production & Motion Graphics. Clean white environment "
            "with dynamic purple (#6C2BD9) rendering timelines and cinematic camera lenses. Center 3D isometric video editing "
            "workstation with keyframe timelines, 4K render monitors, and fluid motion particles. Artistic tech precision, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-023",
        "title": "Corporate Software Training & Digital Upskilling",
        "category": "Talent & Training",
        "filename": "ameetech-23-corporate-tech-upskilling.png",
        "image_prompt": (
            "Inspiring square social flyer for Ameetech Corporate Software Training programs. Bright white backdrop with "
            "bold purple (#6C2BD9) tech badge accents. Center visual portrays an executive tech workshop hub with laptop workstations, "
            "collaborative code screens, skill level progress rings, and career graduation laurels. Professional human-centered feel, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-024",
        "title": "Business Intelligence & Executive Analytics Dashboards",
        "category": "Data & BI",
        "filename": "ameetech-24-business-intelligence-dashboards.png",
        "image_prompt": (
            "Executive-grade square social media flyer for Ameetech Business Intelligence & Analytics. White minimal background "
            "with refined purple (#6C2BD9) analytics dials. Centerpiece 3D multi-layered analytics dashboard with interactive "
            "revenue heatmaps, cohort retention graphs, predictive KPI forecast gauges, and real-time data feeds. Ameetech logo, "
            "footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-025",
        "title": "AgriTech Marketplaces & Smart Commodity Distribution",
        "category": "AgriTech",
        "filename": "ameetech-25-agritech-marketplaces.png",
        "image_prompt": (
            "Forward-looking square social flyer for Ameetech AgriTech platforms. White clean background with rich purple (#6C2BD9) "
            "digital supply chain graphics and subtle natural green leaf accents. Center 3D tablet displaying farm-to-market trade "
            "exchanges, grain commodity pricing, cold-chain transport tracking, and direct farmer payout gates. Ameetech logo, "
            "footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-026",
        "title": "Hotel Booking Engines & Hospitality Guest Portals",
        "category": "Hospitality Tech",
        "filename": "ameetech-26-hotel-booking-engines.png",
        "image_prompt": (
            "Refined square social media flyer for Ameetech Hospitality Management Systems. Clean white setting with rich "
            "purple (#6C2BD9) luxury motifs. Center 3D isometric hospitality kiosk showing instant room reservation calendars, "
            "contactless QR guest check-in, housekeeping management, and POS billing integrations. Ameetech branding, "
            "footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-027",
        "title": "Digital Event Ticketing & QR Access Verification",
        "category": "Event Tech",
        "filename": "ameetech-27-digital-ticketing-qr-access.png",
        "image_prompt": (
            "Modern square social graphic for Ameetech Event Ticketing Solutions. Pristine white background with bold "
            "purple (#6C2BD9) event wristband and VIP pass motifs. Center 3D floating digital ticket stub with encrypted "
            "QR code, high-speed gate scanner beam, and real-time attendee admissions analytics. Sleek tech agency finish, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-028",
        "title": "Legacy System Modernization & Cloud Migration",
        "category": "Modernization",
        "filename": "ameetech-28-legacy-cloud-migration.png",
        "image_prompt": (
            "Strategic square social media flyer for Ameetech Legacy Modernization services. White studio background with "
            "vibrant purple (#6C2BD9) architectural evolution arrows. Center 3D transformation visual: monolithic legacy server "
            "blocks seamlessly refactoring into sleek microservices and lightning-fast cloud containers. Clean enterprise hierarchy, "
            "Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-029",
        "title": "Startup Fast-Track MVP Engineering Program",
        "category": "Startups & MVPs",
        "filename": "ameetech-29-startup-fasttrack-mvp.png",
        "image_prompt": (
            "High-energy square social flyer for Ameetech Startup MVP Fast-Track. Clean white canvas with bold Ameetech purple "
            "(#6C2BD9) rocket trajectory arcs. Center 3D isometric startup product launchpad with modular product features, agile sprint "
            "milestone charts, and investor-ready prototype mobile screens. Modern tech founder appeal, Ameetech logo, "
            "footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    },
    {
        "id": "FLYER-030",
        "title": "Dedicated Nigerian Engineering Teams for Global Scale",
        "category": "Dedicated Teams",
        "filename": "ameetech-30-dedicated-engineering-teams.png",
        "image_prompt": (
            "Empowering square social media flyer for Ameetech Dedicated Engineering Teams. Pure white environment with "
            "bold purple (#6C2BD9) global connectivity lines extending from Nigeria across the globe. Center visual of a high-tech "
            "collaborative engineering workspace, dual monitors with full-stack code repositories, agile scrum boards, and global "
            "time-zone clock synchronizers. Global standards, Ameetech logo, footer with 'ameetechnology.com.ng' and WhatsApp '+234 810 001 5498'."
        ),
        "status": "pending",
        "website": "ameetechnology.com.ng",
        "whatsapp": "+234 810 001 5498"
    }
]

def main():
    prompts_dir = Path("prompts")
    prompts_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = prompts_dir / "flyer-prompts.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(FLYER_DATA, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(FLYER_DATA)} records to {json_path}")
    
    csv_path = prompts_dir / "flyer-prompts.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "category", "filename", "image_prompt", "status", "website", "whatsapp"])
        writer.writeheader()
        for row in FLYER_DATA:
            writer.writerow(row)
    print(f"Wrote {len(FLYER_DATA)} records to {csv_path}")

if __name__ == "__main__":
    main()
