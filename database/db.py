import sqlite3


DATABASE_NAME = "data/irtiqa.db"


# =========================
# CONNECT DATABASE
# =========================

def get_connection():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    return conn