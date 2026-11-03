"""
Amee Technology Lead Intelligence Platform
Brevo API Service (Official REST API v3 Integration)
Provides verified connectivity, subscriber synchronization, campaign management,
and webhook processing with complete permission separation and suppression enforcement.
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

BREVO_BASE_URL = "https://api.brevo.com/v3"

def get_brevo_config() -> Dict[str, str]:
    """Retrieves Brevo environment configuration safely."""
    api_key = os.environ.get("BREVO_API_KEY", "").strip()
    sender_email = os.environ.get("BREVO_SENDER_EMAIL", "support@ameetechnology.com.ng").strip()
    sender_name = os.environ.get("BREVO_SENDER_NAME", "Amee Technology").strip()
    return {
        "api_key": api_key,
        "sender_email": sender_email,
        "sender_name": sender_name,
        "is_configured": bool(api_key and not api_key.startswith("your_"))
    }

def _make_brevo_request(endpoint: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Makes a server-side authenticated HTTP request to Brevo API v3."""
    config = get_brevo_config()
    if not config["is_configured"]:
        return {
            "success": False,
            "error": "Brevo API key is not configured in environment (BREVO_API_KEY missing).",
            "mocked": True,
            "status_code": 0
        }

    url = f"{BREVO_BASE_URL}{endpoint}"
    headers = {
        "api-key": config["api_key"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            body = resp.read().decode("utf-8")
            return {
                "success": True,
                "status_code": resp.getcode(),
                "data": json.loads(body) if body else {}
            }
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
        except Exception:
            err_json = {"raw": err_body}
        return {
            "success": False,
            "status_code": e.code,
            "error": err_json.get("message", f"HTTP Error {e.code}"),
            "details": err_json
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "error": str(e)
        }

def test_brevo_connection() -> Dict[str, Any]:
    """Tests Brevo API key validity against the /account endpoint."""
    config = get_brevo_config()
    if not config["is_configured"]:
        return {
            "connected": False,
            "configured": False,
            "message": "BREVO_API_KEY environment variable is not set. Add your Brevo API key to .env to activate live sync.",
            "account": None
        }

    res = _make_brevo_request("/account", method="GET")
    if res.get("success"):
        acct = res.get("data", {})
        # Redact sensitive values before returning
        safe_account = {
            "email": acct.get("email"),
            "companyName": acct.get("companyName"),
            "plan": acct.get("plan", []),
            "relay": acct.get("relay", {})
        }
        return {
            "connected": True,
            "configured": True,
            "message": f"Successfully connected to Brevo account: {acct.get('companyName', acct.get('email'))}",
            "account": safe_account
        }
    else:
        return {
            "connected": False,
            "configured": True,
            "message": f"Brevo API error: {res.get('error')}",
            "status_code": res.get("status_code")
        }

def get_or_create_contact_list(list_name: str = "Amee Technology Confirmed Subscribers") -> Dict[str, Any]:
    """Retrieves or creates a Brevo contact list for confirmed marketing subscribers."""
    res = _make_brevo_request("/contacts/lists?limit=50", method="GET")
    if res.get("success"):
        lists = res.get("data", {}).get("lists", [])
        for lst in lists:
            if lst.get("name") == list_name:
                return {"success": True, "list_id": lst.get("id"), "created": False}
        
        # Create list if missing
        create_res = _make_brevo_request("/contacts/lists", method="POST", payload={"name": list_name, "folderId": 1})
        if create_res.get("success"):
            return {"success": True, "list_id": create_res.get("data", {}).get("id"), "created": True}

    return {"success": False, "error": res.get("error", "Unable to verify or create Brevo contact list.")}

def sync_confirmed_subscriber(subscriber: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synchronizes an eligible, confirmed subscriber to Brevo.
    Enforces strict consent check: subscriber MUST be confirmed.
    Implements idempotency via updateEnabled=True.
    """
    if subscriber.get("status") != "confirmed":
        return {
            "success": False,
            "error": "Consent rule violation: Only confirmed subscribers with double opt-in can be synced to Brevo.",
            "skipped": True
        }

    config = get_brevo_config()
    if not config["is_configured"]:
        return {
            "success": True,
            "mocked": True,
            "message": "Brevo API key not set. Subscriber recorded locally in SQLite database."
        }

    email = subscriber["email"]
    first_name = subscriber.get("first_name", "")
    business_name = subscriber.get("business_name", "")
    industry = subscriber.get("industry", "")
    preferred_topics = subscriber.get("preferred_topics", [])
    if isinstance(preferred_topics, list):
        topics_str = ", ".join(preferred_topics)
    else:
        topics_str = str(preferred_topics or "")

    attributes = {
        "FIRSTNAME": first_name,
        "BUSINESS_NAME": business_name,
        "INDUSTRY": industry,
        "TOPICS": topics_str
    }

    payload = {
        "email": email,
        "attributes": attributes,
        "updateEnabled": True, # Idempotent update if contact already exists
    }

    # Add to default list if available
    list_info = get_or_create_contact_list()
    if list_info.get("success") and list_info.get("list_id"):
        payload["listIds"] = [int(list_info["list_id"])]

    res = _make_brevo_request("/contacts", method="POST", payload=payload)
    return res

def suppress_unsubscribed_contact(email: str) -> Dict[str, Any]:
    """Marks a contact as unsubscribed in Brevo and suppresses future marketing emails."""
    config = get_brevo_config()
    if not config["is_configured"]:
        return {"success": True, "mocked": True, "message": "Brevo key not configured; local suppression active."}

    encoded_email = urllib.parse.quote(email)
    payload = {
        "emailBlacklisted": True,
        "smsBlacklisted": True
    }
    return _make_brevo_request(f"/contacts/{encoded_email}", method="PUT", payload=payload)

def send_transactional_email(to_email: str, to_name: str, subject: str, html_content: str) -> Dict[str, Any]:
    """Sends a transactional email via Brevo or fallback."""
    config = get_brevo_config()
    if not config["is_configured"]:
        # Fallback to local simulation / logging
        return {
            "success": True,
            "mocked": True,
            "message": f"Simulated delivery to {to_email} (Brevo API key not set)."
        }

    payload = {
        "sender": {
            "name": config["sender_name"],
            "email": config["sender_email"]
        },
        "to": [
            {
                "email": to_email,
                "name": to_name
            }
        ],
        "subject": subject,
        "htmlContent": html_content
    }

    return _make_brevo_request("/smtp/email", method="POST", payload=payload)

def process_brevo_webhook(event_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes incoming webhook events from Brevo:
    - sent, delivered, opened, click, hard_bounce, soft_bounce, unsubscribe, spam
    Updates local database records and enforces suppression.
    """
    from lead_intelligence_db import get_db_connection
    event_type = event_payload.get("event")
    email = event_payload.get("email")
    message_id = event_payload.get("message-id") or event_payload.get("messageId")
    now_iso = datetime.now(timezone.utc).isoformat()

    conn = get_db_connection()
    cur = conn.cursor()

    # Log webhook event
    cur.execute("""
    INSERT INTO brevo_sync_logs (email, sync_action, status, payload, created_at)
    VALUES (?, 'webhook_event', 'success', ?, ?);
    """, (email, json.dumps(event_payload), now_iso))

    # If unsubscribe or hard bounce, suppress subscriber immediately
    if event_type in ["unsubscribe", "hard_bounce", "spam"]:
        cur.execute("""
        UPDATE subscribers 
        SET status = 'unsubscribed', unsubscribe_timestamp = ?, updated_at = ?
        WHERE email = ?;
        """, (now_iso, now_iso, email))

    # Update delivery tracking if matching campaign
    if message_id:
        if event_type == "opened":
            cur.execute("""
            UPDATE campaign_deliveries SET status = 'opened', opened_at = ?
            WHERE message_id = ?;
            """, (now_iso, message_id))
        elif event_type == "click":
            cur.execute("""
            UPDATE campaign_deliveries SET status = 'clicked', clicked_at = ?
            WHERE message_id = ?;
            """, (now_iso, message_id))
        elif event_type in ["hard_bounce", "soft_bounce"]:
            cur.execute("""
            UPDATE campaign_deliveries SET status = 'bounced', bounced_at = ?
            WHERE message_id = ?;
            """, (now_iso, message_id))

    conn.commit()
    conn.close()

    return {"success": True, "event_processed": event_type, "email": email}

if __name__ == "__main__":
    status = test_brevo_connection()
    print("[TEST] Brevo Status:", status)
