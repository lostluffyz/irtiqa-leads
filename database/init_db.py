from database.db import (
    get_connection
)


# =========================
# CREATE TABLES
# =========================

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # =========================
    # RAW LEADS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_leads (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        url TEXT,
        title TEXT,

        emails TEXT,
        phones TEXT,

        text_content TEXT,

        internal_links TEXT,

        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # VERIFIED LEADS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verified_leads (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        raw_lead_id INTEGER,

        company_name TEXT,

        website_url TEXT,

        emails TEXT,

        phones TEXT,

        industry_tier TEXT,
        industry_type TEXT,

        confidence REAL,

        reasoning TEXT,

        pain_points TEXT,

        lead_score INTEGER,

        lead_tier TEXT,

        linkedin_message TEXT,

        verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()


# =========================
# INIT DATABASE
# =========================

if __name__ == "__main__":

    create_tables()

    print(
        "Database tables created successfully."
    )