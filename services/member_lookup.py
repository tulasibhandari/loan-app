# services/member_lookup.py
from models.database import get_connection

def fetch_member_data(keyword):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM member_info 
            WHERE member_number = ? OR member_name LIKE ?
            LIMIT 1
    """, (keyword, f"%{keyword}%"))
    
    row = cur.fetchone()
    conn.close()

    if row:
        columns = [desc[0] for desc in cur.description]
        return dict(zip(columns, row))
    return None