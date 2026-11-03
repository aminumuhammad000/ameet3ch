"""
Amee Technology Email Outreach & Marketing Platform
Responsive HTML Email Templates with Standard Footers, NDPA 2023 Notice,
Mailing Address, and Verified One-Click Unsubscribe Links.
"""

from typing import Dict, List, Any

BASE_TEMPLATE_WRAPPER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{SUBJECT}}</title>
  <style>
    body { margin: 0; padding: 0; background-color: #F8FAFC; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #1E293B; }
    .email-container { max-width: 600px; margin: 24px auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    .header { background: linear-gradient(135deg, #581CBA 0%, #6C2BD9 100%); padding: 32px 28px; text-align: left; }
    .brand-name { color: #ffffff; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; text-decoration: none; }
    .content { padding: 32px 28px; line-height: 1.65; font-size: 15px; }
    .content h1 { color: #0F172A; font-size: 22px; font-weight: 700; margin-top: 0; line-height: 1.3; }
    .content h2 { color: #1E293B; font-size: 18px; font-weight: 600; margin-top: 24px; }
    .content p { margin: 16px 0; color: #334155; }
    .highlight-box { background-color: #F3E8FF; border-left: 4px solid #6C2BD9; padding: 16px; border-radius: 0 8px 8px 0; margin: 20px 0; }
    .cta-btn { display: inline-block; background-color: #6C2BD9; color: #ffffff !important; padding: 14px 28px; font-size: 15px; font-weight: 700; text-decoration: none; border-radius: 8px; margin: 20px 0; }
    .footer { background-color: #F1F5F9; padding: 24px 28px; font-size: 12px; color: #64748B; line-height: 1.6; border-top: 1px solid #E2E8F0; text-align: center; }
    .footer a { color: #6C2BD9; text-decoration: underline; }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <a href="https://ameetechnology.com.ng" class="brand-name">AMEE TECHNOLOGY</a>
    </div>
    <div class="content">
      {{BODY}}
    </div>
    <div class="footer">
      <p><strong>Amee Technology Ltd</strong> &bull; Commercial ICT, Custom Software & AI Engineering</p>
      <p>Kano Commercial Hub, Kano State, Nigeria &bull; <a href="https://ameetechnology.com.ng">ameetechnology.com.ng</a></p>
      <p>You received this email because you subscribed to business technology insights from Amee Technology.<br>
      Adhering to the Nigeria Data Protection Act 2023.</p>
      <p><a href="{{UNSUBSCRIBE_URL}}">One-Click Unsubscribe</a> &bull; <a href="{{PREFERENCES_URL}}">Manage Preferences</a></p>
    </div>
  </div>
</body>
</html>
"""

TEMPLATES: Dict[str, Dict[str, str]] = {
    "website_development": {
        "id": "website_development",
        "name": "Web Design & High-Performance Development",
        "default_subject": "Transform Your Online Presence with a Modern, High-Speed Business Portal",
        "preview_text": "Is your business website driving actual inquiries and paying clients?",
        "recommended_topic": "Web Development",
        "body": """<h1>Accelerate Your Business with a High-Converting Digital Portal</h1>
<p>Hello {{FIRSTNAME}},</p>
<p>In today's fast-moving market, your business website is your primary digital storefront. When potential clients search for your services, their first impression decides whether they call you or your competitor.</p>
<div class="highlight-box">
  <strong>Key Fact:</strong> Over 72% of modern Nigerian buyers evaluate a company's credibility based on website loading speed, mobile responsiveness, and clear calls to action.
</div>
<h2>How Amee Technology Delivers Results:</h2>
<ul>
  <li><strong>Sub-Second Loading Speeds:</strong> Optimized performance that improves Google search rankings.</li>
  <li><strong>Mobile-First Architecture:</strong> Seamless experience across smartphones, tablets, and desktops.</li>
  <li><strong>Conversion-Focused Design:</strong> Direct WhatsApp hooks, clear quote request forms, and automated lead capture.</li>
  <li><strong>Robust Security:</strong> Forced HTTPS encryption and modern cloud hosting.</li>
</ul>
<p>Whether you need a fresh commercial portal or an upgrade from an outdated site, our engineering team in Kano is ready to build a solution that scales your revenue.</p>
<p style="text-align: center;">
  <a href="https://ameetechnology.com.ng/services/business-portals.html" class="cta-btn">Explore Web Development Solutions</a>
</p>
<p>Best regards,<br><strong>Aminu Muhammad</strong><br>Lead Architect, Amee Technology</p>"""
    },

    "website_redesign": {
        "id": "website_redesign",
        "name": "Website Modernisation & Redesign",
        "default_subject": "Is Your Existing Website Costing You High-Value Customers?",
        "preview_text": "Signs your business website is due for an architectural upgrade.",
        "recommended_topic": "Web Development",
        "body": """<h1>Time for a Digital Facelift? Upgrade Your Existing Web Platform</h1>
<p>Hello {{FIRSTNAME}},</p>
<p>Many thriving businesses build a website once and leave it untouched for years. Meanwhile, mobile browsers update, design standards evolve, and customer expectations rise.</p>
<h2>Common signs your website needs modernization:</h2>
<ul>
  <li>Slow loading times on mobile networks.</li>
  <li>Lack of prominent contact options (WhatsApp / Instant Callback).</li>
  <li>Dated visual branding that doesn't reflect your current business scale.</li>
  <li>Missing security certificates or SSL warnings in browsers.</li>
</ul>
<p>A modern redesign by Amee Technology maintains your existing SEO equity while completely refreshing your interface, doubling your conversion rates, and positioning you as an industry leader.</p>
<p style="text-align: center;">
  <a href="https://wa.me/2348100015498?text=Hi%20Amee%20Technology%2C%20I%20would%20like%20a%20website%20redesign%20consultation" class="cta-btn">Schedule a Free Website Audit</a>
</p>
<p>Warm regards,<br>The Amee Technology Engineering Team</p>"""
    },

    "seo_services": {
        "id": "seo_services",
        "name": "Search Engine Optimisation (SEO) & Organic Growth",
        "default_subject": "Get Discovered on Google: Practical SEO Strategies for Nigerian SMEs",
        "preview_text": "Dominate local searches in Kano, Abuja, Lagos and nationwide.",
        "recommended_topic": "SEO & Growth Marketing",
        "body": """<h1>Dominate High-Intent Search Results on Google</h1>
<p>Hello {{FIRSTNAME}},</p>
<p>Every single day, thousands of decision-makers search Google for the exact products and services your company provides. If you aren't on page one, those valuable inquiries go straight to competitors.</p>
<div class="highlight-box">
  <strong>The Power of Organic SEO:</strong> Unlike paid ads that stop the moment you pause your budget, organic search engine optimization creates a sustainable stream of qualified inbound leads month after month.
</div>
<h2>Our 4-Pillar SEO Engineering Approach:</h2>
<ol>
  <li><strong>Technical Foundation:</strong> Schema.org rich snippets, XML sitemaps, Core Web Vitals optimization.</li>
  <li><strong>Local Search Dominance:</strong> Ranking your business for geo-targeted keywords across Nigerian commercial hubs.</li>
  <li><strong>High-Value Content Architecture:</strong> Authority guides that establish your firm as the trusted leader.</li>
  <li><strong>Conversion Rate Optimization:</strong> Ensuring ranking visitors convert into paying customers.</li>
</ol>
<p style="text-align: center;">
  <a href="https://ameetechnology.com.ng/services/growth-marketing.html" class="cta-btn">Discover Our SEO Methodologies</a>
</p>
<p>To your organic growth,<br><strong>Amee Technology SEO Desk</strong></p>"""
    },

    "mobile_app_development": {
        "id": "mobile_app_development",
        "name": "Mobile Application Development (iOS & Android)",
        "default_subject": "Launch Your Custom Mobile App on Android and iOS",
        "preview_text": "Bring your business directly into your customer's pocket with Flutter & React Native.",
        "recommended_topic": "Mobile Applications",
        "body": """<h1>Engage Your Customers Directly on Mobile Devices</h1>
<p>Hello {{FIRSTNAME}},</p>
<p>Over 84% of internet traffic in Nigeria originates from smartphones. When your business offers a dedicated mobile app, you unlock instant push notifications, frictionless offline access, and direct repeat sales.</p>
<h2>Mobile App Solutions We Build:</h2>
<ul>
  <li><strong>On-Demand Service Apps:</strong> Booking, scheduling, and live artisan/service dispatch.</li>
  <li><strong>Fintech & Wallet Solutions:</strong> Secure payments, VTU airtime/data dispensing, and savings ledgers.</li>
  <li><strong>E-Commerce & Delivery Apps:</strong> Product catalogues, shopping carts, and courier tracking.</li>
  <li><strong>Enterprise Staff Portals:</strong> Field agent monitoring, inventory counts, and internal operations.</li>
</ul>
<p>Built with cross-platform frameworks for high speed and cost efficiency on both Android and Apple iOS devices.</p>
<p style="text-align: center;">
  <a href="https://ameetechnology.com.ng/mobile-app-development-kano/" class="cta-btn">View Mobile App Capabilities</a>
</p>
<p>Best regards,<br>The Amee Technology Mobile Engineering Team</p>"""
    },

    "custom_software": {
        "id": "custom_software",
        "name": "Custom Software & Enterprise Automation",
        "default_subject": "Eliminate Operational Bottlenecks with Tailored Enterprise Software",
        "preview_text": "Custom ERPs, inventory management, and database portals engineered for your workflow.",
        "recommended_topic": "Custom Software",
        "body": """<h1>Tailored Software Engineered for Your Exact Business Workflow</h1>
<p>Hello {{FIRSTNAME}},</p>
<p>Off-the-shelf software packages often force your team into rigid workflows that don't match how your business actually operates in Nigeria. When operations scale, spreadsheets break and critical data slips through the cracks.</p>
<div class="highlight-box">
  <strong>Engineered for Reliability:</strong> We develop secure web-based ERP systems, multi-branch inventory tracking, custom accounting portals, and automated billing engines with PostgreSQL ACID data integrity.
</div>
<h2>What Custom Software Solves:</h2>
<ul>
  <li>Eliminates duplicate manual data entry across departments.</li>
  <li>Provides real-time dashboards for executives to monitor cash flow and inventory.</li>
  <li>Enforces role-based permissions and complete audit trails.</li>
  <li>Connects seamlessly to bank APIs, SMS gateways, and internal databases.</li>
</ul>
<p style="text-align: center;">
  <a href="https://ameetechnology.com.ng/services/custom-software.html" class="cta-btn">Discuss Your Software Requirements</a>
</p>
<p>Sincerely,<br><strong>Aminu Muhammad</strong> &bull; Amee Technology</p>"""
    },

    "ai_automation": {
        "id": "ai_automation",
        "name": "AI Automation & WhatsApp Business Bots",
        "default_subject": "Automate 80% of Customer Inquiries with WhatsApp AI Assistants",
        "preview_text": "Respond instantly, 24/7, without hiring a huge customer support department.",
        "recommended_topic": "AI Automation",
        "body": """<h1>Scale Your Customer Support 24/7 with Intelligent AI Automation</h1>
<p>Hello {{FIRSTNAME}},</p>
<p>Customers expect instant replies. In Nigeria, business happens on WhatsApp. When a client messages at 9:00 PM and doesn't get a response until the next morning, they've often already taken their business elsewhere.</p>
<h2>What WhatsApp AI Automation Does for Your Business:</h2>
<ul>
  <li><strong>Instant 24/7 Replies:</strong> Answers frequently asked questions about pricing, services, and operating hours.</li>
  <li><strong>Automated Appointment Booking:</strong> Qualifies prospects and schedules meetings directly into your calendar.</li>
  <li><strong>CRM Synchronization:</strong> Records customer names, phone numbers, and inquiries into your central database.</li>
  <li><strong>Multi-Language Support:</strong> Seamlessly converses in English, Hausa, Pidgin, and other regional dialects.</li>
</ul>
<p>Integrated officially through Meta's Cloud API to safeguard your phone number against bans.</p>
<p style="text-align: center;">
  <a href="https://ameetechnology.com.ng/services/ai-automation.html" class="cta-btn">See AI Automation in Action</a>
</p>
<p>To your efficiency,<br>The Amee Technology AI Automation Lab</p>"""
    },

    "digital_transformation": {
        "id": "digital_transformation",
        "name": "Digital Transformation & Cloud Migration",
        "default_subject": "Strategic Digital Transformation: Modernizing Northern Nigerian Enterprises",
        "preview_text": "Migrate your files, workflows, and communications securely to the cloud.",
        "recommended_topic": "General Tech",
        "body": """<h1>Empower Your Enterprise Through Strategic Digital Transformation</h1>
<p>Hello {{FIRSTNAME}},</p>
<p>Transitioning from paper-heavy, fragmented systems to a unified cloud infrastructure reduces operating costs by up to 35% while dramatically improving data security and team collaboration.</p>
<h2>Our Transformation Roadmap:</h2>
<ul>
  <li><strong>Cloud Migration:</strong> Securely transition on-premise records to high-availability cloud servers.</li>
  <li><strong>Process Automation:</strong> Automate invoice generation, customer receipts, and email notifications.</li>
  <li><strong>Data Protection Compliance:</strong> Auditing your systems against the Nigeria Data Protection Act 2023.</li>
  <li><strong>Staff Training & Support:</strong> Ensuring your team is confident and productive with the new tools.</li>
</ul>
<p style="text-align: center;">
  <a href="https://ameetechnology.com.ng/#contact" class="cta-btn">Book an Enterprise Consultation</a>
</p>
<p>Warm regards,<br>The Executive Advisory Team &bull; Amee Technology</p>"""
    },

    "general_newsletter": {
        "id": "general_newsletter",
        "name": "Amee Technology Monthly Tech Digest",
        "default_subject": "Amee Technology Insights: Practical Digital Growth Strategies",
        "preview_text": "Fresh technology tactics, cybersecurity best practices, and local business insights.",
        "recommended_topic": "General Tech",
        "body": """<h1>Practical Technology Insights for Your Business</h1>
<p>Hello {{FIRSTNAME}},</p>
<p>Welcome to this edition of the Amee Technology Business & Tech Digest. Each month, we share actionable digital strategies designed specifically for Nigerian SMEs and growing enterprises.</p>
<div class="highlight-box">
  <strong>This Month's Focus:</strong> How modern cloud-native architectures allow small teams to execute operations with the speed and efficiency of multinational corporations.
</div>
<h2>Top Takeaways This Month:</h2>
<ul>
  <li><strong>Why Fast Websites Win:</strong> How lowering your page load speed by 1.2 seconds can improve your conversion rate by 24%.</li>
  <li><strong>Securing Business Data:</strong> Three straightforward steps to ensure compliance with the Nigeria Data Protection Act 2023.</li>
  <li><strong>AI Without the Hype:</strong> Practical automation workflows you can implement right away using WhatsApp Business.</li>
</ul>
<p>We are always here to help you solve technical challenges and architect software that helps your business grow.</p>
<p style="text-align: center;">
  <a href="https://ameetechnology.com.ng/blog/" class="cta-btn">Read More Articles on Our Blog</a>
</p>
<p>Best regards,<br><strong>Aminu Muhammad</strong> & The Amee Technology Team</p>"""
    }
}

def render_template(template_id: str, context: Dict[str, Any]) -> Dict[str, str]:
    """
    Renders an HTML email template with given context variables:
    {{FIRSTNAME}}, {{SUBJECT}}, {{BODY}}, {{UNSUBSCRIBE_URL}}, {{PREFERENCES_URL}}
    """
    tpl = TEMPLATES.get(template_id, TEMPLATES["general_newsletter"])
    subject = context.get("subject", tpl["default_subject"])
    first_name = context.get("first_name", "Valued Partner")
    unsub_url = context.get("unsubscribe_url", "https://ameetechnology.com.ng/subscribe/unsubscribed.html")
    pref_url = context.get("preferences_url", "https://ameetechnology.com.ng/subscribe/preferences.html")

    body_content = tpl["body"].replace("{{FIRSTNAME}}", first_name)
    
    html = BASE_TEMPLATE_WRAPPER.replace("{{SUBJECT}}", subject)
    html = html.replace("{{BODY}}", body_content)
    html = html.replace("{{UNSUBSCRIBE_URL}}", unsub_url)
    html = html.replace("{{PREFERENCES_URL}}", pref_url)

    return {
        "subject": subject,
        "html": html,
        "template_name": tpl["name"],
        "template_id": tpl["id"]
    }

def list_all_templates() -> List[Dict[str, Any]]:
    """Returns a list of all available campaign templates for admin selection."""
    return [
        {
            "id": t["id"],
            "name": t["name"],
            "default_subject": t["default_subject"],
            "preview_text": t["preview_text"],
            "recommended_topic": t["recommended_topic"]
        }
        for t in TEMPLATES.values()
    ]
