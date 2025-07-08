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

def fetch_members_matching(keyword):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT member_number, member_name 
        FROM member_info
        WHERE member_name LIKE ? OR member_number LIKE ?
        ORDER BY member_name ASC
        LIMIT 20
    """, (f"%{keyword}%", f"%{keyword}%"))
    
    rows = cur.fetchall()
    conn.close()

    if rows:
        return [{"member_number": r[0].strip(), "member_name": r[1]} for r in rows]
    return []

