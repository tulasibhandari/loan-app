from models.database import get_connection

def save_report_log(data):
    print("🧾 Saving Report Log:", data)
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO report_tracking(member_number, report_type, file_path, generated_by, generated_date)
        VALUES (?,?,?,?,?)
    """, (
        data["member_number"], data["report_type"],
        data["generated_by"], data["file_path"],
        data["date"]
    ))

    conn.commit()
    conn.close()
    
def fetch_all_report_logs(date_filter = None):
    conn = get_connection()
    cursor =  conn.cursor()

    if date_filter:
        cursor.execute("""
            SELECT member_number, report_type, generated_by, file_path, generated_date 
            FROM report_tracking
            WHERE generated_date = ?
            ORDER BY generated_date DESC
        """, (date_filter,))
    else:
        cursor.execute("""
            SELECT member_number, report_type, generated_by, file_path, generated_date
            FROM report_tracking 
            ORDER BY generated_date DESC
            """)
    
    rows = cursor.fetchall()
    conn.close()
    return rows