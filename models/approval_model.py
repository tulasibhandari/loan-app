from models.database import get_connection

def save_approval_info(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO approval_info (member_number, approval_date, entered_by, entered_post, 
                   approved_by, approved_post, approved_loan_amount, approved_loan_amount_words)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["member_number"], data["approval_date"],
        data["entered_by"], data["entered_designation"],
        data["approved_by"], data["approved_designation"],
        data["approved_loan_amount"], data["approved_loan_amount_words"]    
    ))
    conn.commit()
    conn.close()
