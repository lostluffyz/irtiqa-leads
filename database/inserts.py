import json

from database.db import (
    get_connection
)


# =========================
# SAVE RAW LEAD
# =========================

def save_raw_lead(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO raw_leads (

        url,
        title,

        emails,
        phones,

        text_content,

        internal_links

    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (

        data.get(
            "url",
            ""
        ),

        data.get(
            "title",
            ""
        ),

        json.dumps(
            data.get(
                "emails",
                []
            )
        ),

        json.dumps(
            data.get(
                "phones",
                []
            )
        ),

        data.get(
            "text",
            ""
        ),

        json.dumps(
            data.get(
                "internal_links",
                []
            )
        )
    ))

    conn.commit()

    lead_id = cursor.lastrowid

    conn.close()

    return lead_id


# =========================
# SAVE VERIFIED LEAD
# =========================

def save_verified_lead(

    raw_lead_id,

    data
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
INSERT INTO verified_leads (

    raw_lead_id,

    company_name,
    url,
    website_title,

    industry_tier,
    industry_type,

    confidence,

    reasoning,

    pain_points,

    lead_score,

    lead_tier,

    linkedin_message

)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (

    raw_lead_id,

    data.get(
        "title",
        ""
    ),

    data.get(
        "url",
        ""
    ),

    data.get(
        "title",
        ""
    ),

    data.get(
        "industry_tier",
        ""
    ),

    data.get(
        "industry_type",
        ""
    ),

    data.get(
        "confidence",
        0
    ),

    data.get(
        "reasoning",
        ""
    ),

    json.dumps(
        data.get(
            "pain_points",
            []
        )
    ),

    data.get(
        "score",
        0
    ),

    data.get(
        "tier",
        ""
    ),

    data.get(
        "linkedin_message",
        ""
    )
))

    conn.commit()

    conn.close()