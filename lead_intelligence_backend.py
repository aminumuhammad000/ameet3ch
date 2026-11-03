"""
Amee Technology Lead Intelligence Platform
Backend API Engine: Authentication, Business Discovery, CRM, Double Opt-in,
Campaigns, Brevo Synchronization, Automations, Analytics, and Security.
"""

import os
import re
import csv
import io
import json
import secrets
import urllib.parse
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple

from lead_intelligence_db import (
    get_db_connection,
    hash_password,
    verify_password
)
from discovery_engine import (
    discover_businesses,
    extract_website_content,
    parse_extracted_data,
    audit_website_intelligence,
    normalize_domain
)
import brevo_service
from campaign_templates import (
    render_template,
    list_all_templates,
    TEMPLATES
)

# Authentication Helpers
def create_admin_session(user_id: int, ip_address: str = "", user_agent: str = "") -> str:
    """Creates a cryptographic 32-byte session token valid for 7 days."""
    token = secrets.token_hex(32)
    now = datetime.now(timezone.utc)
    expires = (now + timedelta(days=7)).isoformat()
    now_iso = now.isoformat()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO admin_sessions (token, user_id, ip_address, user_agent, expires_at, created_at)
    VALUES (?, ?, ?, ?, ?, ?);
    """, (token, user_id, ip_address, user_agent, expires, now_iso))
    conn.commit()
    conn.close()
    return token

def authenticate_session(token: str) -> Optional[Dict[str, Any]]:
    """Validates an admin session token, returning user details if active."""
    if not token:
        return None
    now_iso = datetime.now(timezone.utc).isoformat()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT s.token, s.expires_at, u.id, u.username, u.email, u.role
    FROM admin_sessions s
    JOIN admin_users u ON s.user_id = u.id
    WHERE s.token = ? AND s.expires_at > ? AND u.is_active = 1;
    """, (token, now_iso))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def log_audit_event(admin_username: str, action: str, target_type: str = "", target_id: str = "", ip_address: str = "", details: Dict[str, Any] = None):
    """Records an immutable security audit event."""
    now_iso = datetime.now(timezone.utc).isoformat()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO audit_logs (admin_username, action, target_type, target_id, ip_address, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (admin_username, action, target_type, str(target_id), ip_address, json.dumps(details or {}), now_iso))
    conn.commit()
    conn.close()

# -------------------------------------------------------------
# PHASE 2: DASHBOARD STATISTICS (Real Database Queries Only)
# -------------------------------------------------------------
def get_dashboard_statistics() -> Dict[str, Any]:
    """Retrieves real database statistics for the Lead Intelligence overview."""
    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Total Discovered Businesses
    cur.execute("SELECT COUNT(*) AS total FROM discovered_businesses;")
    total_discovered = cur.fetchone()["total"]

    # 2. Total Qualified Prospects
    cur.execute("SELECT COUNT(*) AS total FROM prospects WHERE status = 'Qualified';")
    total_qualified = cur.fetchone()["total"]

    # Total Prospects in CRM
    cur.execute("SELECT COUNT(*) AS total FROM prospects;")
    total_prospects = cur.fetchone()["total"]

    # 3. Businesses with Public Email Addresses
    cur.execute("SELECT COUNT(*) AS total FROM discovered_businesses WHERE public_email IS NOT NULL AND public_email != '';")
    with_public_email = cur.fetchone()["total"]

    # 4. Total Confirmed Subscribers
    cur.execute("SELECT COUNT(*) AS total FROM subscribers WHERE status = 'confirmed';")
    total_confirmed_subscribers = cur.fetchone()["total"]

    # 5. Pending Subscriber Confirmations (Double Opt-in)
    cur.execute("SELECT COUNT(*) AS total FROM subscribers WHERE status = 'pending_confirmation';")
    pending_confirmations = cur.fetchone()["total"]

    # 6. Active Campaigns
    cur.execute("SELECT COUNT(*) AS total FROM email_campaigns WHERE status IN ('scheduled', 'sending');")
    active_campaigns = cur.fetchone()["total"]

    # 7. Total Emails Delivered
    cur.execute("SELECT COALESCE(SUM(emails_delivered), 0) AS total FROM email_campaigns;")
    emails_delivered = cur.fetchone()["total"]

    # 8. Clicks & Opens & Click-Through Rate
    cur.execute("SELECT COALESCE(SUM(clicks_count), 0) AS clicks, COALESCE(SUM(opens_count), 0) AS opens FROM email_campaigns;")
    row_engagement = cur.fetchone()
    total_clicks = row_engagement["clicks"]
    total_opens = row_engagement["opens"]
    ctr = round((total_clicks / emails_delivered * 100), 1) if emails_delivered > 0 else 0.0

    # 9. Unsubscribes
    cur.execute("SELECT COUNT(*) AS total FROM subscribers WHERE status = 'unsubscribed';")
    unsubscribes = cur.fetchone()["total"]

    # 10. Leads Converted into Paying Customers
    cur.execute("SELECT COUNT(*) AS total FROM prospects WHERE status = 'Converted';")
    leads_converted = cur.fetchone()["total"]

    # Recent Audit Log Activity
    cur.execute("""
    SELECT admin_username, action, target_type, target_id, details, created_at 
    FROM audit_logs ORDER BY id DESC LIMIT 6;
    """)
    recent_activity = [dict(r) for r in cur.fetchall()]

    # Opportunities by Amee Technology Service
    cur.execute("""
    SELECT assigned_service, COUNT(*) as count 
    FROM prospects 
    WHERE assigned_service IS NOT NULL AND assigned_service != ''
    GROUP BY assigned_service ORDER BY count DESC LIMIT 6;
    """)
    service_breakdown = [dict(r) for r in cur.fetchall()]

    # Prospects by Status
    cur.execute("SELECT status, COUNT(*) as count FROM prospects GROUP BY status;")
    status_breakdown = {r["status"]: r["count"] for r in cur.fetchall()}

    conn.close()

    return {
        "total_discovered_businesses": total_discovered,
        "total_qualified_prospects": total_qualified,
        "total_prospects": total_prospects,
        "businesses_with_public_email": with_public_email,
        "total_confirmed_subscribers": total_confirmed_subscribers,
        "pending_subscriber_confirmations": pending_confirmations,
        "active_campaigns": active_campaigns,
        "emails_delivered": emails_delivered,
        "total_clicks": total_clicks,
        "total_opens": total_opens,
        "click_through_rate": ctr,
        "unsubscribes": unsubscribes,
        "leads_converted": leads_converted,
        "status_breakdown": status_breakdown,
        "service_breakdown": service_breakdown,
        "recent_activity": recent_activity
    }

# -------------------------------------------------------------
# PHASE 3 & 4: BUSINESS DISCOVERY & WEBSITE AUDIT
# -------------------------------------------------------------
def run_business_discovery(params: Dict[str, Any], admin_username: str = "admin") -> Dict[str, Any]:
    """
    Executes search across approved registries, saves new discovered entities
    to the database with duplicate prevention, and logs audit.
    """
    query = params.get("query", "")
    country = params.get("country", "Nigeria")
    state = params.get("state", "")
    city = params.get("city", "")
    industry = params.get("industry", "")
    category = params.get("category", "")
    website_url = params.get("website_url", "")

    items = discover_businesses(
        query=query,
        country=country,
        state=state,
        city=city,
        industry=industry,
        category=category,
        website_url=website_url
    )

    conn = get_db_connection()
    cur = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()
    saved_count = 0

    for item in items:
        domain = normalize_domain(item.get("website_url", "")) or f"no-web-{secrets.token_hex(4)}"
        
        # Check if exists
        cur.execute("SELECT id FROM discovered_businesses WHERE normalized_domain = ?", (domain,))
        existing = cur.fetchone()
        
        if existing:
            bus_id = existing["id"]
        else:
            cur.execute("""
            INSERT INTO discovered_businesses (
                name, website_url, normalized_domain, description, industry, category,
                country, state, city, public_email, public_phone, social_links,
                services_offered, contact_page_url, source_url, discovery_timestamp,
                confidence_score, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'discovered', ?, ?);
            """, (
                item.get("name"),
                item.get("website_url", ""),
                domain,
                item.get("description", ""),
                item.get("industry", ""),
                item.get("category", ""),
                item.get("country", "Nigeria"),
                item.get("state", ""),
                item.get("city", ""),
                item.get("public_email", ""),
                item.get("public_phone", ""),
                json.dumps(item.get("social_links", {})),
                json.dumps(item.get("services_offered", [])),
                item.get("contact_page_url", ""),
                item.get("source_url", "Search"),
                now_iso,
                item.get("confidence_score", 50),
                now_iso,
                now_iso
            ))
            bus_id = cur.lastrowid
            saved_count += 1

            # Save audit findings if present
            if item.get("audit"):
                audit = item["audit"]
                cur.execute("""
                INSERT INTO website_intelligence (
                    business_id, checked_at, has_https, mobile_optimized, response_time_ms,
                    has_contact_info, has_meta_tags, has_cta, has_booking, has_online_payment,
                    status_code, findings, generated_opportunities
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    bus_id,
                    now_iso,
                    1 if audit.get("has_https") else 0,
                    1 if audit.get("mobile_optimized") else 0,
                    audit.get("response_time_ms", 0),
                    1 if audit.get("has_contact_info") else 0,
                    1 if audit.get("has_meta_tags") else 0,
                    1 if audit.get("has_cta") else 0,
                    1 if audit.get("has_booking") else 0,
                    1 if audit.get("has_online_payment") else 0,
                    audit.get("status_code", 200),
                    json.dumps(audit.get("findings", [])),
                    json.dumps(audit.get("opportunities", []))
                ))

    conn.commit()
    conn.close()

    log_audit_event(admin_username, "discover_businesses", "search", "", "", {"query": query, "found": len(items), "saved": saved_count})

    return {
        "success": True,
        "total_found": len(items),
        "newly_saved": saved_count,
        "results": items
    }

# -------------------------------------------------------------
# PHASE 5: LEAD CRM (Prospect Management)
# -------------------------------------------------------------
def get_prospects(filters: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieves paginated and filtered prospects with lead scores and timeline."""
    conn = get_db_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM prospects WHERE 1=1"
    params = []

    status = filters.get("status")
    if status and status != "All":
        sql += " AND status = ?"
        params.append(status)

    industry = filters.get("industry")
    if industry:
        sql += " AND industry LIKE ?"
        params.append(f"%{industry}%")

    service = filters.get("assigned_service")
    if service:
        sql += " AND assigned_service = ?"
        params.append(service)

    search = filters.get("search")
    if search:
        sql += " AND (business_name LIKE ? OR public_email LIKE ? OR city LIKE ? OR notes LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])

    # Sorting
    sort_by = filters.get("sort_by", "created_at")
    sort_dir = "DESC" if filters.get("sort_dir", "desc").lower() == "desc" else "ASC"
    if sort_by in ["business_name", "lead_score", "created_at", "follow_up_date", "status"]:
        sql += f" ORDER BY {sort_by} {sort_dir}"
    else:
        sql += " ORDER BY id DESC"

    # Pagination
    limit = int(filters.get("limit", 50))
    offset = int(filters.get("offset", 0))

    cur.execute(sql + " LIMIT ? OFFSET ?", params + [limit, offset])
    prospects = [dict(r) for r in cur.fetchall()]

    # Total count query
    count_sql = "SELECT COUNT(*) as count FROM (" + sql + ")"
    cur.execute(count_sql, params)
    total_count = cur.fetchone()["count"]

    conn.close()

    return {
        "success": True,
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "prospects": prospects
    }

def create_or_promote_prospect(data: Dict[str, Any], admin_username: str = "admin") -> Dict[str, Any]:
    """Promotes a discovered business to a prospect or manually creates one."""
    conn = get_db_connection()
    cur = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()

    business_name = data.get("business_name") or data.get("name", "Untitled Prospect")
    website = data.get("website") or data.get("website_url", "")
    public_email = data.get("public_email", "")

    # Calculate smart lead score (0-100)
    score = 40
    if website: score += 10
    if public_email: score += 20
    if data.get("public_phone"): score += 10
    if data.get("assigned_service"): score += 10
    if data.get("notes"): score += 10

    cur.execute("""
    INSERT INTO prospects (
        business_id, business_name, website, industry, country, state, city,
        public_email, public_phone, source_url, date_discovered, lead_score,
        assigned_service, notes, follow_up_date, status, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        data.get("business_id"),
        business_name,
        website,
        data.get("industry", "General Business"),
        data.get("country", "Nigeria"),
        data.get("state", "Kano"),
        data.get("city", "Kano"),
        public_email,
        data.get("public_phone", ""),
        data.get("source_url", "Manual Input"),
        now_iso,
        min(100, score),
        data.get("assigned_service", "Web design and development"),
        data.get("notes", "Initial review created."),
        data.get("follow_up_date", (datetime.now(timezone.utc) + timedelta(days=3)).strftime("%Y-%m-%d")),
        data.get("status", "New"),
        now_iso,
        now_iso
    ))
    prospect_id = cur.lastrowid

    # Record activity
    cur.execute("""
    INSERT INTO prospect_activities (prospect_id, admin_username, activity_type, description, created_at)
    VALUES (?, ?, 'created', ?, ?);
    """, (prospect_id, admin_username, f"Prospect created with status '{data.get('status', 'New')}'", now_iso))

    conn.commit()
    conn.close()

    log_audit_event(admin_username, "create_prospect", "prospect", str(prospect_id), "", {"name": business_name})

    return {"success": True, "prospect_id": prospect_id, "lead_score": score}

def update_prospect(prospect_id: int, updates: Dict[str, Any], admin_username: str = "admin") -> Dict[str, Any]:
    """Updates a prospect's status, notes, follow-up, or service, logging timeline activity."""
    conn = get_db_connection()
    cur = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()

    cur.execute("SELECT * FROM prospects WHERE id = ?", (prospect_id,))
    existing = cur.fetchone()
    if not existing:
        conn.close()
        return {"success": False, "error": "Prospect not found."}

    fields = []
    values = []
    activity_desc = []

    for key in ["status", "lead_score", "assigned_service", "notes", "follow_up_date", "public_email", "public_phone"]:
        if key in updates:
            fields.append(f"{key} = ?")
            values.append(updates[key])
            if updates[key] != existing[key]:
                activity_desc.append(f"{key}: '{existing[key]}' -> '{updates[key]}'")

    if not fields:
        conn.close()
        return {"success": True, "message": "No changes applied."}

    fields.append("updated_at = ?")
    values.append(now_iso)
    values.append(prospect_id)

    cur.execute(f"UPDATE prospects SET {', '.join(fields)} WHERE id = ?", values)

    if activity_desc:
        cur.execute("""
        INSERT INTO prospect_activities (prospect_id, admin_username, activity_type, description, created_at)
        VALUES (?, ?, 'status_change', ?, ?);
        """, (prospect_id, admin_username, "; ".join(activity_desc), now_iso))

    conn.commit()
    conn.close()

    log_audit_event(admin_username, "update_prospect", "prospect", str(prospect_id), "", {"changes": activity_desc})

    return {"success": True, "updated": True}

def get_prospect_detail(prospect_id: int) -> Dict[str, Any]:
    """Fetches full prospect details with activity timeline and associated website intelligence."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prospects WHERE id = ?", (prospect_id,))
    prospect = cur.fetchone()
    if not prospect:
        conn.close()
        return {"success": False, "error": "Prospect not found."}

    res = dict(prospect)

    cur.execute("SELECT * FROM prospect_activities WHERE prospect_id = ? ORDER BY id DESC", (prospect_id,))
    res["activities"] = [dict(r) for r in cur.fetchall()]

    # If linked to a business_id, fetch audit
    if res.get("business_id"):
        cur.execute("SELECT * FROM website_intelligence WHERE business_id = ? ORDER BY id DESC LIMIT 1", (res["business_id"],))
        intel = cur.fetchone()
        if intel:
            intel_dict = dict(intel)
            intel_dict["findings"] = json.loads(intel_dict["findings"]) if intel_dict.get("findings") else []
            intel_dict["generated_opportunities"] = json.loads(intel_dict["generated_opportunities"]) if intel_dict.get("generated_opportunities") else []
            res["website_intelligence"] = intel_dict

    conn.close()
    return {"success": True, "prospect": res}

def export_prospects_csv() -> str:
    """Exports all CRM prospects to a formatted CSV string."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, business_name, website, industry, city, state, public_email, public_phone, lead_score, assigned_service, status, follow_up_date, notes FROM prospects ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Business Name", "Website", "Industry", "City", "State", "Email", "Phone", "Lead Score", "Assigned Service", "Status", "Follow-up Date", "Notes"])
    for r in rows:
        writer.writerow([r["id"], r["business_name"], r["website"], r["industry"], r["city"], r["state"], r["public_email"], r["public_phone"], r["lead_score"], r["assigned_service"], r["status"], r["follow_up_date"], r["notes"]])
    
    return output.getvalue()

# -------------------------------------------------------------
# PHASE 6: EMAIL SUBSCRIPTION SYSTEM (Double Opt-In, NDPA 2023)
# -------------------------------------------------------------
def register_public_subscription(data: Dict[str, Any], ip_address: str = "") -> Dict[str, Any]:
    """
    Handles public email newsletter signup.
    Requires explicit consent. Stores as 'pending_confirmation' and sends confirmation email.
    """
    first_name = (data.get("first_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    business_name = (data.get("business_name") or "").strip()
    industry = (data.get("industry") or "").strip()
    preferred_topics = data.get("preferred_topics", [])
    consent_given = data.get("consent_given", False)

    if not email or "@" not in email:
        return {"success": False, "error": "A valid business email address is required."}
    if not first_name:
        return {"success": False, "error": "First name is required."}
    if not consent_given:
        return {"success": False, "error": "You must check the consent box to receive technology insights under NDPA 2023."}

    conn = get_db_connection()
    cur = conn.cursor()

    # Check existing subscriber
    cur.execute("SELECT * FROM subscribers WHERE email = ?", (email,))
    existing = cur.fetchone()
    now_iso = datetime.now(timezone.utc).isoformat()
    confirm_token = secrets.token_urlsafe(32)
    unsub_token = secrets.token_urlsafe(32)
    consent_text = "I explicitly consent to receiving business technology insights, website growth strategies, and service updates from Amee Technology Ltd under the Nigeria Data Protection Act 2023."

    if existing:
        if existing["status"] == "confirmed":
            conn.close()
            return {"success": True, "already_confirmed": True, "message": "You are already an active subscriber. Thank you!"}
        elif existing["status"] == "unsubscribed":
            # Re-subscription requires new explicit consent
            cur.execute("""
            UPDATE subscribers 
            SET status = 'pending_confirmation', confirmation_token = ?, unsubscribe_token = ?,
                consent_wording = ?, updated_at = ?, preferred_topics = ?, first_name = ?
            WHERE email = ?;
            """, (confirm_token, unsub_token, consent_text, now_iso, json.dumps(preferred_topics), first_name, email))
        else: # pending_confirmation
            cur.execute("""
            UPDATE subscribers 
            SET confirmation_token = ?, preferred_topics = ?, updated_at = ?
            WHERE email = ?;
            """, (confirm_token, json.dumps(preferred_topics), now_iso, email))
    else:
        cur.execute("""
        INSERT INTO subscribers (
            first_name, email, business_name, industry, preferred_topics,
            consent_wording, consent_version, source_page, status,
            confirmation_token, unsubscribe_token, ip_address, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, 'v1.0-2026', ?, 'pending_confirmation', ?, ?, ?, ?, ?);
        """, (
            first_name, email, business_name, industry, json.dumps(preferred_topics),
            consent_text, data.get("source_page", "/"), confirm_token, unsub_token,
            ip_address, now_iso, now_iso
        ))

    conn.commit()
    conn.close()

    # Dispatch double opt-in confirmation email
    confirm_url = f"https://ameetechnology.com.ng/api/subscribe/confirm?token={confirm_token}"
    email_html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:auto;padding:24px;border:1px solid #E2E8F0;border-radius:8px;">
      <h2 style="color:#6C2BD9;">Confirm Your Subscription to Amee Technology Insights</h2>
      <p>Hello {first_name},</p>
      <p>Thank you for subscribing to practical business technology insights and growth strategies from Amee Technology Ltd.</p>
      <p>To adhere to the Nigeria Data Protection Act 2023 and ensure no one signed up with your address without permission, please click the button below to confirm your subscription:</p>
      <p style="text-align:center;margin:32px 0;">
        <a href="{confirm_url}" style="background-color:#6C2BD9;color:#ffffff;padding:14px 28px;text-decoration:none;border-radius:6px;font-weight:bold;">Confirm Subscription</a>
      </p>
      <p style="font-size:13px;color:#64748B;">If you did not request this, you can safely ignore this email; no emails will be sent without confirmation.</p>
    </div>
    """
    brevo_service.send_transactional_email(email, first_name, "Confirm Your Subscription to Amee Technology Insights", email_html)

    return {
        "success": True,
        "message": "Please check your inbox to confirm your email subscription.",
        "confirmation_token": confirm_token
    }

def confirm_subscriber(token: str) -> Dict[str, Any]:
    """Confirms double opt-in subscriber, synchronizes with Brevo, and triggers automations."""
    if not token:
        return {"success": False, "error": "Missing confirmation token."}

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM subscribers WHERE confirmation_token = ?", (token,))
    subscriber = cur.fetchone()

    if not subscriber:
        conn.close()
        return {"success": False, "error": "Invalid or expired confirmation link."}

    now_iso = datetime.now(timezone.utc).isoformat()
    cur.execute("""
    UPDATE subscribers 
    SET status = 'confirmed', confirmation_timestamp = ?, updated_at = ?
    WHERE id = ?;
    """, (now_iso, now_iso, subscriber["id"]))
    conn.commit()

    sub_dict = dict(subscriber)
    sub_dict["status"] = "confirmed"
    sub_dict["preferred_topics"] = json.loads(sub_dict["preferred_topics"]) if sub_dict.get("preferred_topics") else []

    # Sync to Brevo contact list
    brevo_res = brevo_service.sync_confirmed_subscriber(sub_dict)
    cur.execute("""
    INSERT INTO brevo_sync_logs (subscriber_id, email, sync_action, status, brevo_contact_id, error_message, created_at)
    VALUES (?, ?, 'create_contact', ?, ?, ?, ?);
    """, (
        subscriber["id"],
        subscriber["email"],
        "success" if brevo_res.get("success") else "failed",
        str(brevo_res.get("data", {}).get("id", "")),
        brevo_res.get("error", ""),
        now_iso
    ))
    conn.commit()
    conn.close()

    # Trigger welcome automation workflow
    trigger_automation_event("subscriber_confirmed", {"subscriber": sub_dict})

    return {"success": True, "email": subscriber["email"], "first_name": subscriber["first_name"]}

def unsubscribe_subscriber(token: str) -> Dict[str, Any]:
    """Processes immediate one-click unsubscribe, suppressing future campaigns."""
    if not token:
        return {"success": False, "error": "Missing unsubscribe token."}

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM subscribers WHERE unsubscribe_token = ? OR email = ?", (token, token))
    subscriber = cur.fetchone()

    if not subscriber:
        conn.close()
        return {"success": False, "error": "Subscriber record not found."}

    now_iso = datetime.now(timezone.utc).isoformat()
    cur.execute("""
    UPDATE subscribers 
    SET status = 'unsubscribed', unsubscribe_timestamp = ?, updated_at = ?
    WHERE id = ?;
    """, (now_iso, now_iso, subscriber["id"]))
    conn.commit()
    conn.close()

    # Suppress in Brevo
    brevo_service.suppress_unsubscribed_contact(subscriber["email"])
    trigger_automation_event("subscriber_unsubscribed", {"email": subscriber["email"]})

    return {"success": True, "email": subscriber["email"]}

# -------------------------------------------------------------
# PHASE 8: EMAIL CAMPAIGN BUILDER
# -------------------------------------------------------------
def get_campaigns() -> List[Dict[str, Any]]:
    """Returns all campaigns with live delivery and engagement metrics."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM email_campaigns ORDER BY id DESC")
    campaigns = [dict(r) for r in cur.fetchall()]
    conn.close()
    return campaigns

def create_campaign(data: Dict[str, Any], admin_username: str = "admin") -> Dict[str, Any]:
    """Creates a new draft campaign."""
    conn = get_db_connection()
    cur = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()

    name = data.get("name", "Untitled Campaign")
    subject = data.get("subject", "")
    preview_text = data.get("preview_text", "")
    template_id = data.get("template_id", "general_newsletter")
    email_body = data.get("email_body", "")
    target_audience = data.get("target_audience", "all_confirmed")
    schedule_time = data.get("schedule_time", "")

    if not email_body and template_id:
        tpl_rendered = render_template(template_id, {"subject": subject})
        email_body = tpl_rendered["html"]

    cur.execute("""
    INSERT INTO email_campaigns (
        name, subject, preview_text, sender_name, sender_email,
        template_id, email_body, target_audience, schedule_time,
        status, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?);
    """, (
        name, subject, preview_text,
        data.get("sender_name", "Amee Technology"),
        data.get("sender_email", "support@ameetechnology.com.ng"),
        template_id, email_body, target_audience, schedule_time,
        now_iso, now_iso
    ))
    campaign_id = cur.lastrowid
    conn.commit()
    conn.close()

    log_audit_event(admin_username, "create_campaign", "campaign", str(campaign_id), "", {"name": name})

    return {"success": True, "campaign_id": campaign_id}

def send_campaign(campaign_id: int, admin_confirmation: bool = False, admin_username: str = "admin") -> Dict[str, Any]:
    """
    Sends campaign strictly to confirmed eligible marketing subscribers.
    Requires explicit admin confirmation flag.
    Includes unsubscribe link and physical mailing address.
    """
    if not admin_confirmation:
        return {"success": False, "error": "Admin confirmation is required before launching an email campaign."}

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM email_campaigns WHERE id = ?", (campaign_id,))
    campaign = cur.fetchone()
    if not campaign:
        conn.close()
        return {"success": False, "error": "Campaign not found."}

    # Query confirmed subscribers ONLY
    cur.execute("SELECT * FROM subscribers WHERE status = 'confirmed';")
    eligible_subscribers = [dict(r) for r in cur.fetchall()]

    if not eligible_subscribers:
        conn.close()
        return {"success": False, "error": "No confirmed subscribers available to receive this campaign."}

    now_iso = datetime.now(timezone.utc).isoformat()
    cur.execute("UPDATE email_campaigns SET status = 'sending', updated_at = ? WHERE id = ?", (now_iso, campaign_id))
    conn.commit()

    sent_count = 0
    for sub in eligible_subscribers:
        unsub_url = f"https://ameetechnology.com.ng/api/subscribe/unsubscribe?token={sub['unsubscribe_token']}"
        pref_url = f"https://ameetechnology.com.ng/subscribe/preferences.html?email={urllib.parse.quote(sub['email'])}"
        
        # Render personalized content
        rendered = render_template(
            campaign["template_id"] or "general_newsletter",
            {
                "subject": campaign["subject"],
                "first_name": sub["first_name"],
                "unsubscribe_url": unsub_url,
                "preferences_url": pref_url
            }
        )

        res = brevo_service.send_transactional_email(
            sub["email"],
            sub["first_name"],
            campaign["subject"],
            rendered["html"]
        )

        # Log campaign delivery
        msg_id = res.get("data", {}).get("messageId", f"msg-{secrets.token_hex(6)}")
        cur.execute("""
        INSERT INTO campaign_deliveries (campaign_id, subscriber_id, email, status, message_id, created_at)
        VALUES (?, ?, ?, 'sent', ?, ?);
        """, (campaign_id, sub["id"], sub["email"], msg_id, now_iso))
        sent_count += 1

    cur.execute("""
    UPDATE email_campaigns 
    SET status = 'sent', total_recipients = ?, emails_delivered = ?, sent_at = ?, updated_at = ?
    WHERE id = ?;
    """, (sent_count, sent_count, now_iso, now_iso, campaign_id))
    conn.commit()
    conn.close()

    log_audit_event(admin_username, "send_campaign", "campaign", str(campaign_id), "", {"recipients": sent_count})

    return {"success": True, "recipients_sent": sent_count}

# -------------------------------------------------------------
# PHASE 9: MARKETING AUTOMATION ENGINE
# -------------------------------------------------------------
def trigger_automation_event(event_name: str, payload: Dict[str, Any]):
    """Processes automation rules matching trigger events."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM automations WHERE trigger_event = ? AND is_active = 1", (event_name,))
    workflows = cur.fetchall()

    now_iso = datetime.now(timezone.utc).isoformat()
    for wf in workflows:
        action = json.loads(wf["action_json"])
        sub = payload.get("subscriber", {})
        
        if action.get("action") == "send_email" and sub:
            tpl_id = action.get("template", "general_newsletter")
            subject = action.get("subject", "Amee Technology Insights")
            unsub_url = f"https://ameetechnology.com.ng/api/subscribe/unsubscribe?token={sub.get('unsubscribe_token', '')}"
            rendered = render_template(tpl_id, {"subject": subject, "first_name": sub.get("first_name", "Partner"), "unsubscribe_url": unsub_url})
            
            brevo_service.send_transactional_email(sub["email"], sub.get("first_name", ""), subject, rendered["html"])
            
            cur.execute("""
            INSERT INTO automation_logs (automation_id, subscriber_id, status, details, created_at)
            VALUES (?, ?, 'success', ?, ?);
            """, (wf["id"], sub.get("id"), json.dumps({"sent_template": tpl_id}), now_iso))

            cur.execute("UPDATE automations SET execution_count = execution_count + 1 WHERE id = ?", (wf["id"],))

    conn.commit()
    conn.close()

def get_automations() -> List[Dict[str, Any]]:
    """Returns configured automations and execution counts."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM automations ORDER BY id ASC")
    items = [dict(r) for r in cur.fetchall()]
    conn.close()
    return items

def toggle_automation(automation_id: int, is_active: bool) -> bool:
    """Enables or disables an automation rule."""
    conn = get_db_connection()
    cur = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()
    cur.execute("UPDATE automations SET is_active = ?, updated_at = ? WHERE id = ?", (1 if is_active else 0, now_iso, automation_id))
    conn.commit()
    conn.close()
    return True

# -------------------------------------------------------------
# PHASE 10: ANALYTICS ENGINE
# -------------------------------------------------------------
def get_detailed_analytics() -> Dict[str, Any]:
    """Generates comprehensive CRM and outreach analytics across industries, locations, and services."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Prospects by Industry
    cur.execute("""
    SELECT industry, COUNT(*) as count 
    FROM prospects 
    WHERE industry IS NOT NULL AND industry != ''
    GROUP BY industry ORDER BY count DESC LIMIT 10;
    """)
    by_industry = [dict(r) for r in cur.fetchall()]

    # Prospects by State / Location
    cur.execute("""
    SELECT state, COUNT(*) as count 
    FROM prospects 
    WHERE state IS NOT NULL AND state != ''
    GROUP BY state ORDER BY count DESC LIMIT 8;
    """)
    by_location = [dict(r) for r in cur.fetchall()]

    # Opportunities by Amee Tech Service
    cur.execute("""
    SELECT assigned_service, COUNT(*) as count 
    FROM prospects 
    WHERE assigned_service IS NOT NULL 
    GROUP BY assigned_service ORDER BY count DESC;
    """)
    by_service = [dict(r) for r in cur.fetchall()]

    # Lead Conversion Funnel
    cur.execute("SELECT status, COUNT(*) as count FROM prospects GROUP BY status;")
    funnel_map = {r["status"]: r["count"] for r in cur.fetchall()}
    funnel_order = ["New", "Needs Review", "Qualified", "Contacted", "Interested", "Meeting Scheduled", "Proposal Sent", "Converted"]
    funnel = [{"stage": stage, "count": funnel_map.get(stage, 0)} for stage in funnel_order]

    # Email Campaign Aggregates
    cur.execute("""
    SELECT 
        COALESCE(SUM(total_recipients), 0) as total_sent,
        COALESCE(SUM(emails_delivered), 0) as total_delivered,
        COALESCE(SUM(opens_count), 0) as total_opens,
        COALESCE(SUM(clicks_count), 0) as total_clicks,
        COALESCE(SUM(bounces_count), 0) as total_bounces,
        COALESCE(SUM(unsubscribes_count), 0) as total_unsubscribes
    FROM email_campaigns;
    """)
    campaign_stats = dict(cur.fetchone())

    # Subscribers Growth Breakdown
    cur.execute("""
    SELECT status, COUNT(*) as count FROM subscribers GROUP BY status;
    """)
    subscriber_stats = {r["status"]: r["count"] for r in cur.fetchall()}

    conn.close()

    return {
        "by_industry": by_industry,
        "by_location": by_location,
        "by_service": by_service,
        "funnel": funnel,
        "campaign_stats": campaign_stats,
        "subscriber_stats": subscriber_stats
    }
