import os

projects_data = [
    {
        "slug": "ibdata",
        "title": "IBData Platform",
        "badge": "Fintech / VTU Infrastructure",
        "subtitle": "High-Throughput Telecommunications & Utility Payment Engine",
        "desc": "A mission-critical fintech and telecommunications engine engineered by Amee Technology Ltd. Processing over 50,000 monthly transactions with sub-second automated delivery of mobile data, airtime, cable TV, and electricity tokens.",
        "live_url": "https://ibdata.com.ng/",
        "display_url": "ibdata.com.ng",
        "main_image": "../images/ibdata.png",
        "client": "IBData Digital Services",
        "year": "2024 - Present",
        "role": "Full-Stack Software Architecture, VTU APIs, Payment Orchestration",
        "tags": ["VTU APIs", "Next.js", "Node.js", "PostgreSQL", "Webhooks", "Fintech"],
        "metrics": [
            {"num": "50,000+", "lbl": "Monthly Transactions"},
            {"num": "99.98%", "lbl": "Automated Delivery Rate"},
            {"num": "<200ms", "lbl": "Webhook Callback Latency"},
            {"num": "24/7", "lbl": "System Availability"}
        ],
        "overview": "IBData needed an enterprise-grade platform capable of handling surging volumes of daily telecom recharges and digital bill payments without human intervention. Amee Technology architected a resilient event-driven platform integrating multiple telecom switches, automated wallet funding, and intelligent fallback routing.",
        "features": [
            {"title": "Automated Multi-Network Vending", "desc": "Instant automated top-ups for MTN, Airtel, Glo, and 9mobile via prioritized multi-switch API gateways."},
            {"title": "Instant Virtual Account Wallets", "desc": "Automated dedicated virtual bank accounts for users with real-time Monnify & Paystack webhooks."},
            {"title": "Double-Entry Cryptographic Ledger", "desc": "Bank-grade transactional consistency preventing double crediting, negative balances, or race conditions."},
            {"title": "Automated Webhook Reconciliations", "desc": "Nightly background reconciliations comparing provider debits against user ledger orders."},
            {"title": "Enterprise Reseller API", "desc": "Secure RESTful endpoints allowing third-party developers to connect external websites to IBData's inventory."},
            {"title": "Biometric & 2FA Security", "desc": "Multi-factor authentication protecting user wallets and merchant balance withdrawals."}
        ],
        "gallery": [
            {"img": "../images/ibdata.png", "title": "Customer Dashboard", "sub": "Real-time wallet balance & instant vending screen"},
            {"img": "../images/hero_dashboard_graphic.png", "title": "Merchant Administration", "sub": "Granular transaction audits & switch routing"},
            {"img": "../images/custom_software_dev.png", "title": "API Engine Overview", "sub": "High-throughput microservices architecture"}
        ]
    },
    {
        "slug": "vtstack",
        "title": "VTStack Telecoms",
        "badge": "Telecoms Provider & Reseller Portal",
        "subtitle": "Unified Telecoms API Gateway & Reseller Management Dashboard",
        "desc": "A modern telecommunications service provider platform and reseller dashboard with automated customer support workflows, wholesale telecom inventory distribution, and real-time revenue telemetry.",
        "live_url": "https://vtstack.com.ng/",
        "display_url": "vtstack.com.ng",
        "main_image": "../images/vtstack.png",
        "client": "VTStack Communications",
        "year": "2024 - Present",
        "role": "Platform Architecture, Reseller Hierarchy, Automated Support",
        "tags": ["Telecoms", "Dashboard", "Reseller Hierarchy", "FastAPI", "React", "AI Support"],
        "metrics": [
            {"num": "45%", "lbl": "Customer Support Automated"},
            {"num": "200+", "lbl": "Active Reseller Integrations"},
            {"num": "0.4s", "lbl": "Average API Response Time"},
            {"num": "100%", "lbl": "Audit Trail Coverage"}
        ],
        "overview": "VTStack required an all-in-one telecommunications hub that could empower corporate resellers to purchase and distribute telecom products while offering automated customer dispute resolution and transparent balance controls.",
        "features": [
            {"title": "Wholesale Reseller Tier Pricing", "desc": "Dynamic commission and discount levels automatically adjusted based on monthly reseller sales volume."},
            {"title": "Automated Support Ticket Bot", "desc": "AI customer support integration that auto-verifies failed network transactions and re-queries provider logs."},
            {"title": "Multi-Switch Redundancy", "desc": "Intelligent automated failover routing transactions to alternate gateways during telco network downtimes."},
            {"title": "Real-Time Sales Telemetry", "desc": "Comprehensive visual charts displaying hourly transaction velocity, gross margins, and active users."},
            {"title": "Developer Sandbox & Documentation", "desc": "Interactive API documentation allowing partners to test API requests with mock balances before going live."},
            {"title": "Automated Settlement Engine", "desc": "Daily automated settlement summaries exported directly to accounting formats."}
        ],
        "gallery": [
            {"img": "../images/vtstack.png", "title": "Reseller Control Center", "sub": "Inventory balance and live service status"},
            {"img": "../images/digital_solutions.png", "title": "Operations Dashboard", "sub": "Multi-switch telemetry and latency monitor"},
            {"img": "../images/hero_dashboard_graphic-.png", "title": "Financial Reconciliations", "sub": "Settlement summaries and revenue ledgers"}
        ]
    },
    {
        "slug": "ameedata",
        "title": "AmeeData Ecosystem",
        "badge": "Consumer Mobile Billing",
        "subtitle": "Next-Gen Mobile Billing, Utility Management & Digital Wallets",
        "desc": "A streamlined consumer mobile billing and digital wallet application built for ultra-fast utility recharge, smart data bundles, bill payments, and user cashback rewards across Nigeria.",
        "live_url": "https://ameedata.com.ng/",
        "display_url": "ameedata.com.ng",
        "main_image": "../images/ameedata.png",
        "client": "AmeeData Nigeria",
        "year": "2024 - Present",
        "role": "End-to-End Product Design (UI/UX), Frontend & Backend Development",
        "tags": ["Mobile Billing", "UI/UX", "Next.js", "Digital Wallets", "Cashback Rewards"],
        "metrics": [
            {"num": "<8 sec", "lbl": "Fast 2-Tap Checkout Flow"},
            {"num": "30,000+", "lbl": "Happy Active Consumers"},
            {"num": "100%", "lbl": "Instant Delivery Guarantee"},
            {"num": "4.9/5", "lbl": "User Satisfaction Rating"}
        ],
        "overview": "AmeeData was envisioned as the cleanest, most intuitive mobile billing application in Nigeria. Amee Technology designed a frictionless interface that eliminated the tedious multi-step recharge processes common in traditional apps.",
        "features": [
            {"title": "2-Tap Recharge Flow", "desc": "Smart number detection that automatically identifies telecom network and presets favorite data bundles."},
            {"title": "Automated Virtual Bank Accounts", "desc": "Unique dedicated accounts with instantaneous bank transfer detection and auto-credit."},
            {"title": "Customer Loyalty & Cashback", "desc": "Automated micro-cashback engine rewarding users on every airtime and data transaction."},
            {"title": "Dark / Light Adaptive Interface", "desc": "High-contrast visual design system tested under direct sunlight for outdoor mobile users."},
            {"title": "Instant Transaction PDF Slips", "desc": "One-click generation of verified branded payment receipts for business tax records."},
            {"title": "Zero-Loss Reversal Engine", "desc": "Automated instant refund trigger whenever upstream provider networks fail to deliver."}
        ],
        "gallery": [
            {"img": "../images/ameedata.png", "title": "Mobile UI/UX Design", "sub": "Clean typography and 2-tap recharge screen"},
            {"img": "../images/ui_ux_brand.png", "title": "Design System Specs", "sub": "Figma component tokens and color systems"},
            {"img": "../images/custom_software_dev.png", "title": "Payment Flow Engine", "sub": "Instant virtual account callback pipeline"}
        ]
    },
    {
        "slug": "denish",
        "title": "Denish Logistics",
        "badge": "On-Demand Delivery & Logistics",
        "subtitle": "Courier Dispatch, Food Ordering & Urban Logistics Platform",
        "desc": "An on-demand courier logistics and multi-vendor delivery platform connecting food merchants, parcel senders, and dispatch riders with automated route dispatching.",
        "live_url": "https://denishng.com/",
        "display_url": "denishng.com",
        "main_image": "../images/denish.svg",
        "client": "Denish Logistics Ltd",
        "year": "2024 - Present",
        "role": "Logistics Dispatch Engine, Merchant Web App, Rider Tracking",
        "tags": ["Logistics", "Delivery", "Geolocation", "Dispatch Algorithm", "E-Commerce"],
        "metrics": [
            {"num": "65%", "lbl": "Reduction in Dispatch Wait Time"},
            {"num": "1,000s", "lbl": "Parcels Safely Delivered"},
            {"num": "<25 min", "lbl": "Average City Delivery Time"},
            {"num": "99.4%", "lbl": "Proof-of-Delivery Accuracy"}
        ],
        "overview": "Denish sought to modernize urban package delivery and restaurant logistics in Kano and Northern Nigerian commercial centers. Amee Technology engineered a real-time dispatch ecosystem connecting customers, vendors, and bike couriers.",
        "features": [
            {"title": "Intelligent Proximity Dispatch", "desc": "Algorithms that match incoming package orders to the closest available courier in real time."},
            {"title": "Live Map Package Tracking", "desc": "Interactive GPS live tracking allowing customers to see their courier's transit location live."},
            {"title": "Merchant Storefront & Menu Manager", "desc": "Simple admin tools for restaurants and retailers to manage inventory, price changes, and opening hours."},
            {"title": "Digital Proof of Delivery (POD)", "desc": "Cryptographic OTP verification and digital signature capture ensuring packages reach the correct recipient."},
            {"title": "Multi-Drop Delivery Routing", "desc": "Optimized delivery route sequencing allowing a single courier to efficiently drop multiple parcels."},
            {"title": "Rider Payout & Performance Tracker", "desc": "Automated calculation of courier tips, trip bonuses, and automated weekly bank payouts."}
        ],
        "gallery": [
            {"img": "../images/denish.svg", "title": "Denish Brand Identity", "sub": "High-contrast emerald vector identity"},
            {"img": "../images/digital_solutions.png", "title": "Dispatch Control Center", "sub": "Courier map tracking and order routing"},
            {"img": "../images/custom_software_dev.png", "title": "Merchant Ordering Flow", "sub": "Fast checkout and live rider assignment"}
        ]
    },
    {
        "slug": "peeritrade",
        "title": "Peeritrade Escrow",
        "badge": "P2P Trading & Escrow Protocol",
        "subtitle": "Fraud-Proof Peer-to-Peer Escrow Trading Platform",
        "desc": "A secure peer-to-peer digital asset and football ticket trading platform with multi-signature escrow holding, encrypted chat, dispute resolution workflows, and zero fraud track record.",
        "live_url": "https://peeritrade.com/",
        "display_url": "peeritrade.com",
        "main_image": "../images/peeritrade.png",
        "client": "Peeritrade Global",
        "year": "2024 - Present",
        "role": "Escrow Architecture, Dispute Workflow, UX Design, Security Audits",
        "tags": ["Escrow", "P2P Trading", "Fintech Security", "Encrypted Chat", "WebSockets"],
        "metrics": [
            {"num": "100%", "lbl": "Escrow Funds Protection"},
            {"num": "0", "lbl": "Unresolved Dispute Incidents"},
            {"num": "<3 min", "lbl": "Average Trade Settlement Time"},
            {"num": "Bank-Grade", "lbl": "Cryptographic Trade Vaults"}
        ],
        "overview": "Peer-to-peer commerce in emerging markets is heavily plagued by fraud, payment reversals, and trust deficits. Amee Technology designed and built Peeritrade with a military-grade escrow mechanism that holds seller assets and buyer funds until mutual condition verification.",
        "features": [
            {"title": "Multi-Step Escrow Lockup", "desc": "Assets are cryptographically locked in escrow before the buyer is permitted to transmit payment."},
            {"title": "Encrypted Real-Time Trade Chat", "desc": "End-to-end WebSocket chat with image upload for payment receipts and automated timer warnings."},
            {"title": "Arbitration & Dispute Portal", "desc": "Dedicated admin arbitration desk where certified moderators inspect payment proofs and enforce settlements."},
            {"title": "Reputation & Trust Badging", "desc": "Automated trader rating system based on completed trades, response velocity, and verification levels."},
            {"title": "Anti-Phishing & Session Shields", "desc": "Strict IP location binding, biometric confirmations, and device fingerprinting to prevent account takeovers."},
            {"title": "Instant Bank Payout Rail", "desc": "Automated settlement to local bank accounts once buyer and seller confirm satisfaction."}
        ],
        "gallery": [
            {"img": "../images/peeritrade.png", "title": "Trade Execution Screen", "sub": "Live countdown timer and payment receipt upload"},
            {"img": "../images/ui_ux_brand.png", "title": "High-Trust UX Architecture", "sub": "Step-by-step escrow safety prompts"},
            {"img": "../images/custom_software_dev.png", "title": "Dispute Resolution Engine", "sub": "Automated ledger locking and admin review portal"}
        ]
    },
    {
        "slug": "medicata",
        "title": "Medicata Health AI",
        "badge": "HealthTech & Clinical AI",
        "subtitle": "Intelligent Symptom Triage, Telemedicine & Medical Notes Platform",
        "desc": "A unified AI healthcare platform featuring 24/7 natural-language symptom triage, intelligent doctor matchmaking, digital prescription generation, and automated clinical summaries.",
        "live_url": "https://medicata.ng/",
        "display_url": "medicata.ng",
        "main_image": "../images/medicata.png",
        "client": "Medicata Healthcare Ltd",
        "year": "2024 - Present",
        "role": "Healthcare AI Architecture, Clinical NLP, Telemedicine Video Flow, UI/UX",
        "tags": ["HealthTech", "AI Triage", "Clinical NLP", "Telemedicine", "HIPAA Ready"],
        "metrics": [
            {"num": "92%", "lbl": "Diagnostic Triage Match"},
            {"num": "24/7", "lbl": "Instant Medical Guidance"},
            {"num": "<60 sec", "lbl": "Doctor Matchmaking Speed"},
            {"num": "100%", "lbl": "Patient Privacy Encryption"}
        ],
        "overview": "Access to immediate clinical consultation is critically constrained in Africa. Amee Technology engineered Medicata to bridge the healthcare gap using medical NLP that evaluates patient symptoms, assesses emergency severity, and prepares clinical charts for physicians.",
        "features": [
            {"title": "Conversational Symptom Triage", "desc": "Patients describe ailments in plain English or local vernacular; the AI asks clarifying medical questions."},
            {"title": "Emergency Urgency Classifier", "desc": "Red-flags critical symptoms (stroke, cardiac distress, hemorrhage) for immediate emergency intervention."},
            {"title": "Automated Clinical Notes (SOAP)", "desc": "Generates structured Subjective, Objective, Assessment, and Plan summaries for certified doctors."},
            {"title": "Live Telemedicine Consultations", "desc": "Encrypted WebRTC video calling between patients and certified medical specialists."},
            {"title": "Digital Pharmacy & e-Prescriptions", "desc": "Tamper-proof digital prescription codes that patients can present at registered local pharmacies."},
            {"title": "Patient Health Vault", "desc": "Encrypted medical history archive with chronological vitals logs, lab test uploads, and doctor notes."}
        ],
        "gallery": [
            {"img": "../images/medicata.png", "title": "Medicata Patient Portal", "sub": "Natural language symptom evaluation interface"},
            {"img": "../images/ai_automation.png", "title": "Clinical NLP Architecture", "sub": "Medical ontology mapping and risk stratification"},
            {"img": "../images/ui_ux_brand.png", "title": "Empathetic Healthcare UX", "sub": "Accessible typography and calming color palette"}
        ]
    },
    {
        "slug": "connecta",
        "title": "Connecta Talent",
        "badge": "African Talent Marketplace",
        "subtitle": "AI-Powered Freelance Marketplace & Escrow Contract Platform",
        "desc": "A pan-African talent and freelance marketplace linking elite software developers, designers, and visual creators with worldwide clients using AI semantic matching and milestone escrow.",
        "live_url": "https://myconnecta.ng/",
        "display_url": "myconnecta.ng",
        "main_image": "../images/connecta.png",
        "client": "Connecta Africa",
        "year": "2024 - Present",
        "role": "Full-Stack Marketplace Platform, AI Skill Matchmaker, Smart Milestones",
        "tags": ["Marketplace", "AI Matching", "African Talent", "Escrow Milestones", "Next.js"],
        "metrics": [
            {"num": "<5 min", "lbl": "Talent Matchmaking Time"},
            {"num": "1,500+", "lbl": "Vetted African Creatives"},
            {"num": "100%", "lbl": "Guaranteed Milestone Escrow"},
            {"num": "Global", "lbl": "International Client Billing"}
        ],
        "overview": "African tech and creative talent faces significant friction landing international contracts due to payment barriers and credibility verification. Amee Technology built Connecta as an end-to-end marketplace with AI project matching and escrow protection.",
        "features": [
            {"title": "AI Semantic Skill Matching", "desc": "Vector embeddings analyze client job briefs and recommend the top 3 best-suited freelancers instantly."},
            {"title": "Milestone-Based Escrow Contracts", "desc": "Clients fund deliverables in advance; funds release only after work inspection and client sign-off."},
            {"title": "Automated Portfolio Verification", "desc": "Automated GitHub, Dribbble, and Behance sync verifying that submitted code and designs are authentic."},
            {"title": "Multi-Currency Global Invoicing", "desc": "Enables clients in the US, UK, and Europe to pay via Stripe while freelancers receive funds in Naira or USD."},
            {"title": "Built-In Dispute Mitigation", "desc": "Clear revision caps and escrow arbitration protocols that prevent scope creep and non-payment."},
            {"title": "Direct Work Messaging & File Sharing", "desc": "High-speed collaboration workspace with shared file previews and revision version control."}
        ],
        "gallery": [
            {"img": "../images/connecta.png", "title": "Connecta Marketplace Hub", "sub": "Talent search and verified badge credentials"},
            {"img": "../images/ai_automation.png", "title": "AI Matching Engine", "sub": "Semantic resume and brief scoring pipeline"},
            {"img": "../images/custom_software_dev.png", "title": "Milestone Escrow Vault", "sub": "Automated stage funding and release checks"}
        ]
    },
    {
        "slug": "asasurealty",
        "title": "ASASU Realty Portal",
        "badge": "Enterprise PropTech & Commissions",
        "subtitle": "Real Estate Sales Tracking & Automated Agent Commission Suite",
        "desc": "A dedicated enterprise property sales, agent hierarchy, and multi-tier commission calculation portal built for ASASU Realty to eliminate spreadsheet disputes and automate agent payouts.",
        "live_url": "https://asasurealty-commission.com.ng/",
        "display_url": "asasurealty-commission.com.ng",
        "main_image": "../images/asasurealty.svg",
        "client": "ASASU Realty Ltd",
        "year": "2024 - Present",
        "role": "Commission Architecture, Agent Hierarchy, Payment Settlement Engine",
        "tags": ["PropTech", "Commission Engine", "Real Estate", "Agent Portal", "Ledger Accounting"],
        "metrics": [
            {"num": "₦100M+", "lbl": "Property Sales Tracked"},
            {"num": "7 to 1", "lbl": "Days Cut in Commission Payouts"},
            {"num": "0", "lbl": "Disputed Agent Calculations"},
            {"num": "100%", "lbl": "Sales Audit Transparency"}
        ],
        "overview": "ASASU Realty manages an expansive network of real estate agents and high-value property portfolios. Manual calculations caused delays and friction. Amee Technology engineered a custom portal that calculates tiered commissions instantly upon property sale verification.",
        "features": [
            {"title": "Multi-Level Agent Hierarchy", "desc": "Supports primary sales agents, team leaders, and regional agency overrides with automated splits."},
            {"title": "Property Sales Ledger", "desc": "Centralized database of all estate plots, payment milestones, deed transfers, and buyer documentation."},
            {"title": "Instant Commission Calculator", "desc": "Eliminates calculation errors by applying contract percentage formulas automatically on deposit receipt."},
            {"title": "Agent Mobile Dashboard", "desc": "Realtors track sales progress, pending disbursements, and download official payment certificates from their phones."},
            {"title": "One-Click Bank Payouts", "desc": "Direct integration with corporate banking APIs to disburse approved agent commissions in a single click."},
            {"title": "Tamper-Proof Audit Logging", "desc": "Every property price change, contract approval, and payment voucher is permanently logged."}
        ],
        "gallery": [
            {"img": "../images/asasurealty.svg", "title": "ASASU Realty Brand Interface", "sub": "Clean corporate blue and navy branding"},
            {"img": "../images/digital_solutions.png", "title": "Commission Ledger Dashboard", "sub": "Real-time agent payout formulas and balances"},
            {"img": "../images/hero_dashboard_graphic.png", "title": "Sales Contract Records", "sub": "Property plot allocations and payment vouchers"}
        ]
    },
    {
        "slug": "northcdesigners",
        "title": "North C Designers",
        "badge": "Creative Tech Summit 2.0",
        "subtitle": "Roots & Vectors: The Premier Northern Creative Designers Summit Platform",
        "desc": "The official digital platform for the Northern Creative Designers Summit 2.0 (Roots & Vectors) — the premier annual gathering uniting designers, software developers, and visual storytellers across Northern Nigeria.",
        "live_url": "https://northcdesigners.netlify.app/",
        "display_url": "northcdesigners.netlify.app",
        "main_image": "../images/northcdesigners.png",
        "client": "Northern Creative Designers (NCDS)",
        "year": "2026",
        "role": "Full Platform Engineering, Arewa Motif Visuals, Attendee Registration & Awards",
        "tags": ["Summit Platform", "Next.js", "Arewa Design", "Event Tech", "Creative Community"],
        "metrics": [
            {"num": "1,000+", "lbl": "Summit Attendees Registered"},
            {"num": "19 Dec", "lbl": "Kano 2026 Summit Date"},
            {"num": "Roots & Vectors", "lbl": "Signature Summit Theme"},
            {"num": "100%", "lbl": "Responsive Design System"}
        ],
        "overview": "Northern Creative Designers Summit needed a world-class digital home to reflect the renaissance of Arewa creative design, celebrate local design pioneers, and facilitate ticket bookings, keynote schedules, hackathon sprints, and creative design awards in Kano, Nigeria.",
        "features": [
            {"title": "Arewa Motif Digital Identity", "desc": "Bespoke digital design system incorporating traditional northern Nigerian motifs into modern CSS and vector graphics."},
            {"title": "Tailored Attendee Pathways", "desc": "Dynamic interactive filtering for founders, UI/UX designers, developers, and agency executives."},
            {"title": "Live Hackathon & Sprint Schedules", "desc": "Detailed agenda breakdowns, speaker profiles, and live stage session countdown timers."},
            {"title": "Exhibition & Design Awards Portal", "desc": "Nomination submission portal and exhibition gallery showcasing groundbreaking Northern creative work."},
            {"title": "Instant Ticket & Seat Reservation", "desc": "Frictionless attendee onboarding with QR ticket issuance and automated confirmation emails."},
            {"title": "Sponsor & Partner Showcase", "desc": "High-impact visual tiers giving prominent exposure to regional and international tech sponsors."}
        ],
        "gallery": [
            {"img": "../images/northcdesigners.png", "title": "Summit Brand Logo & Identity", "sub": "Official Roots & Vectors Northern Creative Designers logo"},
            {"img": "../images/about_tech_graphic.png", "title": "Community Gathering Sprints", "sub": "Live hackathon tracks and speaker lineups"},
            {"img": "../images/ui_ux_brand.png", "title": "Cultural Vector System", "sub": "Arewa geometric motifs mapped into digital UI components"}
        ]
    }
]

def render_project(p, all_p):
    metrics_html = "".join([f"""
        <div class="p-metric-card">
            <div class="num">{m['num']}</div>
            <div class="lbl">{m['lbl']}</div>
        </div>
    """ for m in p["metrics"]])

    features_html = "".join([f"""
        <li class="feature-list-item">
            <i class="fa-solid fa-circle-check"></i>
            <div>
                <h4>{f['title']}</h4>
                <p>{f['desc']}</p>
            </div>
        </li>
    """ for f in p["features"]])

    gallery_html = "".join([f"""
        <div class="gallery-card">
            <div class="gallery-img-wrap">
                <img src="{g['img']}" alt="{g['title']}" loading="lazy" style="{ 'object-fit:contain; padding:20px;' if g['img'].endswith('.svg') or 'northcdesigners' in g['img'] else '' }">
            </div>
            <div class="gallery-card-info">
                <h4>{g['title']}</h4>
                <span>{g['sub']}</span>
            </div>
        </div>
    """ for g in p["gallery"]])

    tags_html = "".join([f'<span class="meta-tag-pill">{t}</span>' for t in p["tags"]])

    # Other project switcher chips (excluding current)
    other_html = "".join([f"""
        <a href="{o['slug']}.html" class="other-project-chip">
            <img src="{o['main_image']}" alt="{o['title']}" style="{ 'object-fit:contain; padding:6px;' if o['main_image'].endswith('.svg') or 'northcdesigners' in o['main_image'] else '' }">
            <div>
                <h5>{o['title']}</h5>
                <span>{o['badge']}</span>
            </div>
        </a>
    """ for o in all_p if o["slug"] != p["slug"]][:4])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['title']} — Case Study & Project Details | Amee Technology</title>
    <meta name="description" content="{p['desc']}">
    <link rel="canonical" href="https://ameetechnology.com.ng/projects/{p['slug']}.html">
    <link rel="stylesheet" href="projects.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.1/css/all.min.css" crossorigin="anonymous">
</head>
<body>

    <!-- Sticky Navigation -->
    <nav class="project-nav">
        <a href="../index.html" class="nav-logo">
            <img src="../images/ameelogo.png" alt="Amee Technology Logo">
            <span>Amee Technology</span>
        </a>
        <div class="nav-links">
            <a href="../index.html">Home</a>
            <a href="../services/">Services</a>
            <a href="../index.html#portfolio" class="active">Portfolio</a>
            <a href="../index.html#other">Team</a>
            <a href="../blog/">Blog</a>
            <a href="https://wa.me/2348100015498" target="_blank" class="nav-cta"><i class="fa-brands fa-whatsapp"></i> Chat on WhatsApp</a>
        </div>
        <button class="nav-toggle" aria-label="Toggle navigation menu" onclick="toggleNav()"><i class="fa-solid fa-bars"></i></button>
    </nav>
    <div class="mobile-nav-drawer" id="mobileNavDrawer">
        <a href="../index.html">Home</a>
        <a href="../services/">Services</a>
        <a href="../index.html#portfolio">Portfolio</a>
        <a href="../index.html#other">Team</a>
        <a href="../blog/">Blog</a>
        <a href="https://wa.me/2348100015498" target="_blank"><i class="fa-brands fa-whatsapp"></i> Chat on WhatsApp</a>
    </div>

    <!-- Breadcrumb -->
    <div class="breadcrumb-bar">
        <a href="../index.html">Home</a>
        <i class="fa-solid fa-chevron-right"></i>
        <a href="../index.html#portfolio">Portfolio</a>
        <i class="fa-solid fa-chevron-right"></i>
        <span class="current">{p['title']}</span>
    </div>

    <!-- Project Hero -->
    <header class="project-hero">
        <div class="project-hero-wrap">
            <span class="project-tag-pill"><i class="fa-solid fa-laptop-code"></i> {p['badge']}</span>
            <h1>{p['title']}: <span>{p['subtitle']}</span></h1>
            <p>{p['desc']}</p>
            <div class="project-hero-actions">
                <a href="{p['live_url']}" target="_blank" rel="noopener noreferrer" class="btn-primary"><i class="fa-solid fa-arrow-up-right-from-square"></i> Visit Live Platform</a>
                <a href="#overview" class="btn-secondary"><i class="fa-solid fa-circle-info"></i> Project Specifications</a>
            </div>
        </div>

        <!-- Primary Browser Preview Frame -->
        <div class="project-browser-frame">
            <div class="browser-bar">
                <div class="browser-dots">
                    <span class="browser-dot red"></span>
                    <span class="browser-dot yellow"></span>
                    <span class="browser-dot green"></span>
                </div>
                <div class="browser-address">
                    <i class="fa-solid fa-lock"></i>
                    <span>https://{p['display_url']}</span>
                </div>
            </div>
            <div class="browser-content">
                <img src="{p['main_image']}" alt="{p['title']} Live Platform Preview" style="{ 'object-fit:contain; padding:40px; background:#111827;' if p['main_image'].endswith('.svg') or 'northcdesigners' in p['main_image'] else '' }">
            </div>
        </div>
    </header>

    <!-- Main Content & Sidebar -->
    <main class="project-details-wrap" id="overview">
        <!-- Main Story -->
        <div class="project-main-content">
            <!-- Overview Block -->
            <div class="project-section-block">
                <h2><i class="fa-solid fa-bullseye"></i> The Challenge & Objective</h2>
                <p>{p['overview']}</p>
                
                <!-- Metrics -->
                <div class="project-metrics-grid">
                    {metrics_html}
                </div>
            </div>

            <!-- Features & Architecture Block -->
            <div class="project-section-block">
                <h2><i class="fa-solid fa-microchip"></i> Key Features Built by Amee Technology</h2>
                <p>Every layer of the platform was crafted to combine strict security, intuitive user journeys, and zero technical debt.</p>
                <ul class="project-features-list">
                    {features_html}
                </ul>
            </div>

            <!-- Image Previews & Visual Proofs -->
            <div class="project-section-block">
                <h2><i class="fa-solid fa-images"></i> Visual Previews & System Artifacts</h2>
                <p>Detailed interface views and design systems powering this live deployment.</p>
                <div class="project-gallery-grid">
                    {gallery_html}
                </div>
            </div>
        </div>

        <!-- Sidebar Meta -->
        <aside class="project-sidebar">
            <div class="meta-card">
                <h3>Project Metadata</h3>

                <div class="meta-row">
                    <span class="meta-label">Client / Organization</span>
                    <span class="meta-value">{p['client']}</span>
                </div>

                <div class="meta-row">
                    <span class="meta-label">Timeline</span>
                    <span class="meta-value">{p['year']}</span>
                </div>

                <div class="meta-row">
                    <span class="meta-label">Amee Technology Role</span>
                    <span class="meta-value">{p['role']}</span>
                </div>

                <div class="meta-row">
                    <span class="meta-label">Live Link (Verified)</span>
                    <span class="meta-value">
                        <a href="{p['live_url']}" target="_blank" rel="noopener noreferrer">
                            {p['display_url']} <i class="fa-solid fa-arrow-up-right"></i>
                        </a>
                    </span>
                </div>

                <div class="meta-row">
                    <span class="meta-label">Tech Stack & Tags</span>
                    <div class="meta-tags-flex">
                        {tags_html}
                    </div>
                </div>
            </div>

            <div class="sidebar-cta-box">
                <h4>Need a Similar System?</h4>
                <p>Let's engineer a secure, scalable platform tailored to your specific business model.</p>
                <a href="https://wa.me/2348100015498?text=Hello%20Amee%20Technology,%20I%20reviewed%20your%20{p['title']}%20case%20study%20and%20want%20to%20discuss%20a%20project" target="_blank" class="btn-primary" style="width:100%; justify-content:center;">
                    <i class="fa-brands fa-whatsapp"></i> Chat on WhatsApp
                </a>
            </div>
        </aside>
    </main>

    <!-- Other Projects Quick Switcher -->
    <section class="other-projects-bar">
        <div style="max-width:1240px; margin:0 auto; text-align:center;">
            <span class="project-tag-pill" style="margin-bottom:8px;">Portfolio Showcase</span>
            <h2 style="font-size:2rem; font-weight:800; color:var(--text-main);">Explore More Projects That Speak</h2>
            <p style="color:var(--text-muted); max-width:600px; margin:0 auto;">Discover other enterprise web applications, mobile platforms, and AI systems shipped by Amee Technology Ltd.</p>
        </div>
        <div class="other-projects-grid">
            {other_html}
        </div>
    </section>

    <!-- Conversion CTA Banner -->
    <section class="project-cta-banner">
        <h2>Have a Groundbreaking Product Idea?</h2>
        <p>Partner with Amee Technology Ltd to architect, design, and ship production-ready digital software that dominates your industry.</p>
        <div class="cta-buttons-row">
            <a href="https://wa.me/2348100015498?text=Hello%20Amee%20Technology,%20I%20have%20a%20project%20in%20mind" target="_blank" class="btn-white"><i class="fa-brands fa-whatsapp"></i> Start WhatsApp Discovery</a>
            <a href="https://forms.gle/zzL8UaQjkGhGcXHs5" target="_blank" class="btn-outline"><i class="fa-solid fa-file-pen"></i> Submit Project Brief</a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="project-footer">
        <div class="footer-top-grid">
            <div class="footer-brand">
                <h3>Amee Technology Ltd</h3>
                <p>Empowering businesses across Nigeria and Africa with high-impact software engineering, artificial intelligence, and digital solutions built to scale.</p>
                <div class="footer-social-links">
                    <a href="https://web.facebook.com/profile.php?id=61550987333969" target="_blank" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
                    <a href="https://www.instagram.com/amee.tech" target="_blank" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
                    <a href="https://www.tiktok.com/@amee.tech?_t=ZM-8t3mEOfPgTF&_r=1" target="_blank" aria-label="TikTok"><i class="fa-brands fa-tiktok"></i></a>
                    <a href="https://www.youtube.com/@ameetech" target="_blank" aria-label="YouTube"><i class="fa-brands fa-youtube"></i></a>
                    <a href="https://linkedin.com/in/aminu-muhammad-ameetech" target="_blank" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
                </div>
            </div>

            <div class="footer-col">
                <h4>Portfolio Items</h4>
                <ul>
                    <li><a href="ibdata.html">IBData VTU</a></li>
                    <li><a href="vtstack.html">VTStack Telecoms</a></li>
                    <li><a href="ameedata.html">AmeeData Platform</a></li>
                    <li><a href="denish.html">Denish Logistics</a></li>
                    <li><a href="peeritrade.html">Peeritrade Escrow</a></li>
                    <li><a href="medicata.html">Medicata Health</a></li>
                    <li><a href="connecta.html">Connecta Talent</a></li>
                    <li><a href="asasurealty.html">ASASU Realty</a></li>
                    <li><a href="northcdesigners.html">North C Designers</a></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Services</h4>
                <ul>
                    <li><a href="../services/custom-software.html">Custom Software</a></li>
                    <li><a href="../services/ai-automation.html">AI & Automation</a></li>
                    <li><a href="../services/business-portals.html">Business Portals</a></li>
                    <li><a href="../services/design-branding.html">Design & Branding</a></li>
                    <li><a href="../services/media-production.html">Media Production</a></li>
                    <li><a href="../services/growth-marketing.html">Growth & Marketing</a></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Contact Us</h4>
                <ul>
                    <li><i class="fa-solid fa-location-dot"></i> Zoo Road, Kano, Nigeria</li>
                    <li><i class="fa-solid fa-phone"></i> +234 810 001 5498</li>
                    <li><i class="fa-solid fa-envelope"></i> support@ameetechnology.com.ng</li>
                    <li><a href="../privacy-policy.html">Privacy Policy</a></li>
                </ul>
            </div>
        </div>

        <div class="footer-bottom-bar">
            <span>&copy; 2026 Amee Technology Ltd. All Rights Reserved.</span>
            <span>Engineered with Precision & Passion in Kano, Nigeria.</span>
        </div>
    </footer>

    <script>
        function toggleNav() {{
            const drawer = document.getElementById('mobileNavDrawer');
            drawer.classList.toggle('open');
        }}
    </script>
</body>
</html>
"""

for p in projects_data:
    fpath = os.path.join("projects", f"{p['slug']}.html")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(render_project(p, projects_data))
    print(f"Generated {fpath}")
