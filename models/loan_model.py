# models/loan_model.py
from models.database import get_connection


def save_or_update_member_info(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    # Ensure correct format
    data['member_number'] = str(data['member_number']).strip().zfill(9)  # Moved before SELECT
    cursor.execute("SELECT id FROM member_info WHERE member_number=?", (data['member_number'],))
    row = cursor.fetchone()
     
    if row:
        # update the existing row
        cursor.execute("""
            UPDATE member_info SET
                date=?,
                member_name=?, 
                address=?, 
                ward_no=?,
                phone=?, 
                dob_bs=?, 
                citizenship_no=?, 
                father_name=?, 
                grandfather_name=?,
                spouse_name=?, 
                spouse_phone=?, 
                business_name=?, 
                business_address=?,
                job_name=?, 
                job_address=?
            WHERE member_number=?
        """, (
            data['date'],
            data['member_name'],
            data['address'],
            data['ward_no'],
            data['phone'],
            data['dob_bs'],
            data['citizenship_no'],
            data['father_name'],
            data['grandfather_name'],
            data['spouse_name'],
            data['spouse_phone'],
            data['business_name'],
            data['business_address'],
            data['job_name'],
            data['job_address'],
            data['member_number']  # ✅ this was missing!
        ))
    else:
        # Insert data 
        cursor.execute(""" 
            INSERT OR IGNORE INTO member_info(
                    date, member_number, member_name, address, ward_no,
                    phone, dob_bs, citizenship_no, father_name, grandfather_name,
                    spouse_name, spouse_phone, business_name, business_address,
                    job_name, job_address
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data['date'],
            data['member_number'],
            data['member_name'],
            data['address'],
            data['ward_no'],
            data['phone'],
            data['dob_bs'],
            data['citizenship_no'],
            data['father_name'],
            data['grandfather_name'],
            data['spouse_name'],
            data['spouse_phone'],
            data['business_name'],
            data['business_address'],
            data['job_name'],
            data['job_address'],
            
        ))
    
    print(f"🔄 Saving/Updating: {data['member_number']}")
    conn.commit()
    print("✅ DB commit complete")
    conn.close()

def save_loan_info(data: dict):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loan_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_number TEXT,
                loan_type TEXT,
                interest_rate TEXT,
                loan_duration TEXT,
                repayment_duration TEXT,
                loan_amount TEXT,
                loan_amount_in_words TEXT,
                loan_completion_year TEXT,
                loan_completion_month TEXT,
                loan_completion_day TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO loan_info (
                member_number,
                loan_type,
                interest_rate,
                loan_duration,
                repayment_duration,
                loan_amount,
                loan_amount_in_words,
                loan_completion_year,
                loan_completion_month,
                loan_completion_day
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['member_number'],
            data['loan_type'],
            data['interest_rate'],
            data['loan_duration'],
            data['repayment_duration'],
            data['loan_amount'],
            data['loan_amount_in_words'],
            data['loan_completion_year'],
            data['loan_completion_month'],
            data['loan_completion_day']
        ))

        conn.commit()
        conn.close()
        print("✅ Loan info saved to database.")

    except Exception as e:
        print("❌ Error saving loan info:", e)