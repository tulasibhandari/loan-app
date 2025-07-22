import sqlite3
import os
import shutil
from datetime import datetime

DB_PATH = r"F:\Tuski\extras\pycodes\loan_app\data\loan_app.db"

def backup_database(db_path):
    """Create a timestamped backup of the current database"""
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{db_path}.{timestamp}.bak"
        shutil.copy2(db_path, backup_path)
        print(f"📦 Backup created at: {backup_path}")
    else:
        print("⚠️ No existing database found. Skipping backup.")

def create_tables():
    """Recreate all tables with full expected schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS member_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        member_number TEXT UNIQUE,
        member_name TEXT,
        phone TEXT,
        dob_bs TEXT,
        citizenship_no TEXT,
        email TEXT,
        profession TEXT,
        facebook_detail TEXT,
        whatsapp_detail TEXT,
        father_name TEXT,
        grandfather_name TEXT,
        spouse_name TEXT,
        spouse_phone TEXT,
        address TEXT,
        ward_no TEXT,
        business_name TEXT,
        business_address TEXT,
        job_name TEXT,
        job_address TEXT
    );

    CREATE TABLE IF NOT EXISTS loan_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_number TEXT,
        loan_type TEXT,
        interest_rate REAL,
        loan_duration TEXT,
        repayment_duration TEXT,
        loan_amount TEXT,
        loan_amount_in_words TEXT,
        loan_completion_year TEXT,
        loan_completion_month TEXT,
        loan_completion_day TEXT
    );

    CREATE TABLE IF NOT EXISTS approval_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_number TEXT,
        approval_date TEXT,
        entered_by TEXT,
        entered_post TEXT,
        approved_by TEXT,
        approved_post TEXT,
        remarks TEXT,
        approved_loan_amount TEXT,
        approved_loan_amount_words TEXT
    );

    CREATE TABLE IF NOT EXISTS report_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_number TEXT,
        report_type TEXT,
        file_path TEXT,
        generated_by TEXT,
        generated_date TEXT
    );

    CREATE TABLE IF NOT EXISTS collateral_basic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_number TEXT,
        monthly_saving TEXT,
        child_saving TEXT,
        total_saving TEXT
    );

    CREATE TABLE IF NOT EXISTS witness_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_number TEXT,
        name TEXT,
        relation TEXT,
        address TEXT,
        tole TEXT,
        ward TEXT,
        age TEXT
    );

    CREATE TABLE IF NOT EXISTS project_detail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_number TEXT,
        project_name TEXT,
        self_investment TEXT,
        requested_loan_amount TEXT,
        total_cost TEXT,
        remarks TEXT
    );

    CREATE TABLE IF NOT EXISTS income_expense (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_number TEXT,
        label TEXT,
        amount TEXT,
        type TEXT
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        post TEXT,
        full_name_nepali TEXT
    );

    CREATE TABLE IF NOT EXISTS loan_scheme (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loan_type TEXT,
        interest_rate REAL
    );
    """)
    conn.commit()
    conn.close()
    print("✅ Full schema recreated successfully.")


def reset_database():
    """Reset the database by dropping all tables and recreating schema"""
    try:
        backup_database(DB_PATH)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"✅ Dropped table: {table}")
            except Exception as e:
                print(f"⚠️ Could not drop table {table}: {e}")

        conn.commit()
        conn.close()

        # Recreate tables
        create_tables()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    confirm = input("⚠️ This will wipe all data! Continue? (yes/no): ")
    if confirm.lower() == "yes":
        reset_database()
    else:
        print("❌ Reset cancelled.")
