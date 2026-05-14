from database.db import (
    get_connection
)

# =========================
# CHECK EXISTING LEAD
# =========================

def lead_exists(url):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM raw_leads
        WHERE url = ?
        """,
        (url,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# =========================
# FETCH ALL VERIFIED LEADS
# =========================

def get_all_verified_leads():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM verified_leads

    ORDER BY verified_at DESC

    """)

    results = cursor.fetchall()

    conn.close()

    return results