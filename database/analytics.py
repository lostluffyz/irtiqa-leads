from database.db import (
    get_connection
)


# =========================
# TOTAL VERIFIED LEADS
# =========================

def get_total_verified_leads():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT COUNT(*)

    FROM verified_leads

    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total