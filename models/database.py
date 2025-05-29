# models/database.py
import sqlite3
from pathlib import Path


DB_PATH = Path("data/loan_app.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True) # Ensure /data exists
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cur = conn.cursor()

    # Create Member Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS member_info(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                member_number TEXT,
                member_name TEXT,
                address TEXT,
                ward_no TEXT,
                phone TEXT,
                dob_bs TEXT,
                citizenship_no TEXT,
                father_name TEXT,
                grandfather_name TEXT,
                spouse_name TEXT,
                spouse_phone TEXT,
                business_name TEXT,
                business_address TEXT,
                job_name TEXT,
                job_address TEXT
                )        
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS loan_info(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    # Extend this with other tables like loan info, collateral info, approval_info

    conn.commit()
    conn.close()