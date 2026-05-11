import sqlite3
from pathlib import Path


DB_PATH = Path("data/leads.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # RAW LEADS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_leads (
        lead_id TEXT PRIMARY KEY,

        full_name TEXT,
        job_title TEXT,
        company_name TEXT,

        linkedin_url TEXT,
        company_website TEXT,

        email_raw TEXT,
        phone_raw TEXT,

        location TEXT,
        country TEXT,

        about_text TEXT,
        company_description TEXT,

        source TEXT,
        scrape_date TEXT,

        raw_posts TEXT
    )
    """)

    # VERIFIED LEADS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verified_leads (
        lead_id TEXT PRIMARY KEY,

        email_verified TEXT,
        email_confidence INTEGER,

        phone_valid BOOLEAN,

        linkedin_active BOOLEAN,
        website_active BOOLEAN,

        company_size_confirmed TEXT,

        decision_maker_level TEXT,
        decision_maker_confidence INTEGER,

        industry_tier TEXT,
        industry_type TEXT,

        pain_points TEXT,
        keyword_matches TEXT,
        intent_signals TEXT,

        is_duplicate BOOLEAN,

        enrichment_date TEXT
    )
    """)

    # SCORED LEADS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scored_leads (
        lead_id TEXT PRIMARY KEY,

        qualification_score INTEGER,

        score_breakdown TEXT,

        tier TEXT,

        top_pain_points TEXT,

        outreach_angle TEXT,

        linkedin_message TEXT,
        whatsapp_message TEXT,

        email_subject TEXT,
        email_body TEXT,

        predicted_objection TEXT,
        objection_response TEXT,

        scored_date TEXT,

        ready_for_outreach BOOLEAN
    )
    """)

    conn.commit()
    conn.close()

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()