from models.database import get_connection

def create_loan_scheme_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS loan_schemes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   loan_type TEXT UNIQUE,
                   interest_rate REAL
                   )
    """)

    conn.commit()
    conn.close()


def add_or_update_loan_scheme(loan_type, interest_rate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO loan_schemes(loan_type, interest_rate)
            VALUES (?,?)
            ON CONFLICT(loan_type) DO UPDATE SET interest_rate=excluded.interest_rate
    """, (loan_type, interest_rate)
    )
    
    conn.commit()
    conn.close()

def fetch_all_loan_schemes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT loan_type, interest_rate FROM loan_schemes")
    results = cursor.fetchall()
    conn.close()
    return results