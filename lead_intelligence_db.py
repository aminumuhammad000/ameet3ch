"""
Amee Technology Lead Intelligence, CRM & Email Marketing Platform
Database Models, Initialization, Seed Data, and Migration Scripts
Compatible with Python 3.10+ and SQLite3 with WAL mode and strict relational constraints.
"""

import os
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timezone

DB_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(DB_DIR, "lead_intelligence.sqlite")

def get_db_connection():
    """Returns a connection to the Lead Intelligence SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Generates a PBKDF2-HMAC-SHA256 password hash with salt."""
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()
    return hashed, salt

def verify_password(password: str, hashed: str, salt: str) -> bool:
    """Verifies a password against PBKDF2-HMAC-SHA256 hash and salt."""
    new_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(new_hash, hashed)

def init_db(seed_admin: bool = True):
    """Initializes all tables, indexes, and initial configurations."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Admin Users & Role-Based Access
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'admin', -- 'admin', 'operator', 'analyst'
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        last_login TEXT
    );
    """)

    # 2. Admin Sessions (Cryptographic Token Authentication)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_sessions (
        token TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        ip_address TEXT,
        user_agent TEXT,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE CASCADE
    );
    """)

    # 3. Discovered Businesses (Discovery Engine)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discovered_businesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        website_url TEXT,
        normalized_domain TEXT UNIQUE,
        description TEXT,
        industry TEXT,
        category TEXT,
        country TEXT NOT NULL DEFAULT 'Nigeria',
        state TEXT,
        city TEXT,
        public_email TEXT,
        public_phone TEXT,
        social_links TEXT, -- JSON: { twitter, facebook, linkedin, instagram }
        services_offered TEXT, -- JSON array
        contact_page_url TEXT,
        source_url TEXT NOT NULL,
        discovery_timestamp TEXT NOT NULL,
        confidence_score INTEGER DEFAULT 50, -- 0-100
        status TEXT NOT NULL DEFAULT 'discovered', -- 'discovered', 'reviewed', 'qualified', 'ignored'
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # 4. Website Intelligence & Technical Audit Findings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS website_intelligence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        checked_at TEXT NOT NULL,
        has_https INTEGER DEFAULT 0,
        mobile_optimized INTEGER DEFAULT 0,
        response_time_ms INTEGER DEFAULT 0,
        has_contact_info INTEGER DEFAULT 0,
        has_meta_tags INTEGER DEFAULT 0,
        has_cta INTEGER DEFAULT 0,
        has_booking INTEGER DEFAULT 0,
        has_online_payment INTEGER DEFAULT 0,
        status_code INTEGER DEFAULT 0,
        findings TEXT, -- JSON array of specific detected flaws
        generated_opportunities TEXT, -- JSON array of matched Amee Tech services & rationales
        FOREIGN KEY (business_id) REFERENCES discovered_businesses(id) ON DELETE CASCADE
    );
    """)

    # 5. Lead CRM (Prospects)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prospects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER,
        business_name TEXT NOT NULL,
        website TEXT,
        industry TEXT,
        country TEXT NOT NULL DEFAULT 'Nigeria',
        state TEXT,
        city TEXT,
        public_email TEXT,
        public_phone TEXT,
        source_url TEXT,
        date_discovered TEXT NOT NULL,
        lead_score INTEGER DEFAULT 0, -- 0 to 100
        assigned_service TEXT, -- 'Web design and development', 'AI and automation', etc.
        notes TEXT,
        follow_up_date TEXT,
        status TEXT NOT NULL DEFAULT 'New', -- 'New', 'Needs Review', 'Qualified', 'Contacted', 'Interested', 'Meeting Scheduled', 'Proposal Sent', 'Converted', 'Not Interested', 'Archived'
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (business_id) REFERENCES discovered_businesses(id) ON DELETE SET NULL
    );
    """)

    # 6. CRM Activity Timeline
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prospect_activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prospect_id INTEGER NOT NULL,
        admin_username TEXT NOT NULL,
        activity_type TEXT NOT NULL, -- 'status_change', 'note_added', 'email_outreach', 'meeting', 'audit_run'
        description TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (prospect_id) REFERENCES prospects(id) ON DELETE CASCADE
    );
    """)

    # 7. Subscribers (Double Opt-in, NDPA 2023 Compliant)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        business_name TEXT,
        industry TEXT,
        preferred_topics TEXT, -- JSON array: ['Web Development', 'AI Automation', ...]
        consent_wording TEXT NOT NULL,
        consent_version TEXT NOT NULL DEFAULT 'v1.0-2026',
        source_page TEXT NOT NULL DEFAULT '/',
        status TEXT NOT NULL DEFAULT 'pending_confirmation', -- 'pending_confirmation', 'confirmed', 'unsubscribed'
        confirmation_token TEXT UNIQUE,
        confirmation_timestamp TEXT,
        unsubscribe_token TEXT UNIQUE NOT NULL,
        unsubscribe_timestamp TEXT,
        ip_address TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # 8. Brevo Synchronization Tracking & Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS brevo_sync_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subscriber_id INTEGER,
        email TEXT NOT NULL,
        sync_action TEXT NOT NULL, -- 'create_contact', 'update_attributes', 'suppress_unsubscribe', 'webhook_event'
        status TEXT NOT NULL, -- 'success', 'failed', 'retrying'
        brevo_contact_id TEXT,
        payload TEXT, -- JSON payload sent or received
        error_message TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (subscriber_id) REFERENCES subscribers(id) ON DELETE SET NULL
    );
    """)

    # 9. Email Outreach & Marketing Campaigns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject TEXT NOT NULL,
        preview_text TEXT,
        sender_name TEXT NOT NULL DEFAULT 'Amee Technology',
        sender_email TEXT NOT NULL DEFAULT 'support@ameetechnology.com.ng',
        template_id TEXT,
        email_body TEXT NOT NULL,
        target_audience TEXT NOT NULL DEFAULT 'all_confirmed', -- 'all_confirmed', 'topic:Web Development', etc.
        schedule_time TEXT,
        status TEXT NOT NULL DEFAULT 'draft', -- 'draft', 'scheduled', 'sending', 'sent', 'cancelled'
        total_recipients INTEGER DEFAULT 0,
        emails_delivered INTEGER DEFAULT 0,
        opens_count INTEGER DEFAULT 0,
        clicks_count INTEGER DEFAULT 0,
        bounces_count INTEGER DEFAULT 0,
        unsubscribes_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        sent_at TEXT
    );
    """)

    # 10. Campaign Deliveries & Event Logging
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campaign_deliveries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        subscriber_id INTEGER NOT NULL,
        email TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'sent', -- 'queued', 'sent', 'delivered', 'opened', 'clicked', 'bounced'
        message_id TEXT,
        opened_at TEXT,
        clicked_at TEXT,
        bounced_at TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (campaign_id) REFERENCES email_campaigns(id) ON DELETE CASCADE,
        FOREIGN KEY (subscriber_id) REFERENCES subscribers(id) ON DELETE CASCADE
    );
    """)

    # 11. Marketing Automation Workflows
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS automations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        trigger_event TEXT NOT NULL, -- 'subscriber_confirmed', 'topic_selected', 'link_clicked', 'lead_qualified'
        condition_json TEXT, -- JSON filter criteria
        action_json TEXT NOT NULL, -- JSON definition of email/action to take
        is_active INTEGER NOT NULL DEFAULT 1,
        execution_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # 12. Automation Execution Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS automation_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        automation_id INTEGER NOT NULL,
        subscriber_id INTEGER,
        prospect_id INTEGER,
        status TEXT NOT NULL, -- 'success', 'skipped', 'failed'
        details TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (automation_id) REFERENCES automations(id) ON DELETE CASCADE
    );
    """)

    # 13. System Audit Logs (Security & Compliance)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_username TEXT NOT NULL,
        action TEXT NOT NULL, -- 'login', 'data_export', 'lead_created', 'campaign_dispatched', 'subscriber_deleted'
        target_type TEXT, -- 'prospect', 'subscriber', 'campaign', 'system'
        target_id TEXT,
        ip_address TEXT,
        details TEXT,
        created_at TEXT NOT NULL
    );
    """)

    # 14. System Configuration & Settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_settings (
        setting_key TEXT PRIMARY KEY,
        setting_value TEXT NOT NULL,
        description TEXT,
        updated_at TEXT NOT NULL
    );
    """)

    # 15. Create Performance & Query Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_discovered_domain ON discovered_businesses(normalized_domain);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_discovered_industry ON discovered_businesses(industry);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_discovered_location ON discovered_businesses(state, city);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prospects_status ON prospects(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prospects_service ON prospects(assigned_service);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prospects_score ON prospects(lead_score);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscribers_status ON subscribers(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscribers_token ON subscribers(confirmation_token);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscribers_unsub ON subscribers(unsubscribe_token);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_campaigns_status ON email_campaigns(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at);")

    # Seed Default Administrator if not exists
    if seed_admin:
        cursor.execute("SELECT COUNT(*) as count FROM admin_users;")
        if cursor.fetchone()["count"] == 0:
            now_iso = datetime.now(timezone.utc).isoformat()
            default_pwd = os.environ.get("ADMIN_PASSWORD", "AmeeTech@Admin2026!LeadIntel")
            default_user = os.environ.get("ADMIN_USER", "admin")
            pwd_hash, salt = hash_password(default_pwd)
            cursor.execute("""
            INSERT INTO admin_users (username, email, password_hash, salt, role, is_active, created_at)
            VALUES (?, ?, ?, ?, 'admin', 1, ?);
            """, (default_user, "admin@ameetechnology.com.ng", pwd_hash, salt, now_iso))

    # Seed Default Automations if not exists
    cursor.execute("SELECT COUNT(*) as count FROM automations;")
    if cursor.fetchone()["count"] == 0:
        now_iso = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
        INSERT INTO automations (name, trigger_event, condition_json, action_json, is_active, created_at, updated_at)
        VALUES 
        ('Welcome Confirmed Subscriber', 'subscriber_confirmed', '{}', 
         '{"action": "send_email", "template": "general_newsletter", "subject": "Welcome to Amee Technology Insights"}', 1, ?, ?),
        ('Web Dev Topic Nurturing Sequence', 'topic_selected', '{"topic": "Web Development"}', 
         '{"action": "send_email", "template": "website_development", "subject": "Modern Web Architecture for Growth"}', 1, ?, ?),
        ('AI Automation Topic Sequence', 'topic_selected', '{"topic": "AI Automation"}', 
         '{"action": "send_email", "template": "ai_automation", "subject": "Scaling Operations with AI & WhatsApp Automation"}', 1, ?, ?),
        ('Unsubscribe Marketing Suppression', 'subscriber_unsubscribed', '{}', 
         '{"action": "suppress_marketing", "brevo_sync": true}', 1, ?, ?);
        """, (now_iso, now_iso, now_iso, now_iso, now_iso, now_iso, now_iso, now_iso))

    # Seed Default System Settings
    cursor.execute("SELECT COUNT(*) as count FROM system_settings;")
    if cursor.fetchone()["count"] == 0:
        now_iso = datetime.now(timezone.utc).isoformat()
        settings = [
            ("brevo_sender_email", os.environ.get("BREVO_SENDER_EMAIL", "support@ameetechnology.com.ng"), "Default sender email for campaigns"),
            ("brevo_sender_name", os.environ.get("BREVO_SENDER_NAME", "Amee Technology"), "Default sender name"),
            ("discovery_rate_limit_seconds", "2.0", "Interval between HTTP checks on target domains"),
            ("discovery_timeout_seconds", "6.0", "Timeout for checking external business sites"),
            ("ndpa_consent_text", "I explicitly consent to receiving business technology insights, website growth strategies, and service updates from Amee Technology Ltd under the Nigeria Data Protection Act 2023.", "Current NDPA 2023 legal consent notice"),
            ("retention_period_days", "730", "Subscribed data retention period in days (2 years)")
        ]
        cursor.executemany("""
        INSERT OR REPLACE INTO system_settings (setting_key, setting_value, description, updated_at)
        VALUES (?, ?, ?, ?);
        """, [(k, v, d, now_iso) for k, v, d in settings])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"[OK] Lead Intelligence SQLite Database initialized at: {DB_PATH}")
