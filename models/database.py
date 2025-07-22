# models/database.py
import sqlite3
import os
import sys

APP_NAME = "LoanApp"

def get_appdata_path():
    """Get a writable data directory for the app (not used since we bundle DB)"""
    if sys.platform == "win32":
        return os.path.join(os.environ['APPDATA'], APP_NAME)
    else:
        return os.path.join(os.path.expanduser("~"), f".{APP_NAME}")

# Determine DB path
if getattr(sys, 'frozen', False):
    # Running from PyInstaller bundle
    BASE_DIR = sys._MEIPASS  # PyInstaller temp directory
    DB_PATH = os.path.join(BASE_DIR, "data", "loan_app.db")
else:
    # Running from source
    DB_PATH = os.path.join("data", "loan_app.db")

print(f"📦 Using database at: {DB_PATH}")

def get_connection():
    """Return a SQLite3 DB connection"""
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    conn.execute("PRAGMA journal_mode=WAL;")

    cur = conn.cursor()

    # Create Member Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS member_info(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                member_number TEXT UNIQUE,
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

    # Collateral Basic
    # cur.execute("""
    # CREATE TABLE IF NOT EXISTS collateral_basic (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     member_number TEXT,
    #     monthly_saving TEXT,
    #     child_saving TEXT,
    #     total_saving TEXT
    #     )
    # """)

    
    #  Create TABLE for collateral affiliations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS collateral_affiliations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_number TEXT,
                institution TEXT,
                address TEXT,
                postition TEXT,
                estimated_income TEXT,
                remarks TEXT
                )
    """)
   
    # Create table for collateral family details
    cur.execute ("""
        CREATE TABLE IF NOT EXISTS collateral_properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_number TEXT,
                owner_name TEXT,
                father_or_spouse TEXT,
                grandfather_or_father_inlaw TEXT,
                district TEXT,
                municipality_vdc TEXT,
                sheet_no TEXT,
                ward_no TEXT,
                plot_no TEXT,
                area TEXT,
                land_type TEXT                
                )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS collateral_family_details(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_number TEXT,
                name TEXT,
                age TEXT,
                relation TEXT,
                member_of_org TEXT,
                occupation TEXT,
                monthly_income TEXT
                )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS collateral_income_expense(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_number TEXT,
            field TEXT,
            amount TEXT,
            type TEXT
            )
    """)
   
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS approval_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_number TEXT NOT NULL,
            approval_date TEXT,
            entered_by TEXT,
            entered_post TEXT,
            approved_by TEXT,
            approved_post TEXT,
            remarks TEXT,
            approved_loan_amount TEXT,
            approved_loan_amount_words TEXT

        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS report_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_number TEXT NOT NULL,
            report_type TEXT, 
            generated_by TEXT,
            file_path TEXT,
            generated_date TEXT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS collateral_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_number TEXT NOT NULL,
            project_name TEXT,
            self_investment TEXT,
            requested_loan_amount TEXT,
            total_cost TEXT,
            remarks TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS loan_witness(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_number TEXT NOT NULL,
                name TEXT,
                relation TEXT,
                address_mun TEXT,
                ward_no TEXT,
                address_tole TEXT,
                age TEXT
                );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS organization_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            address TEXT,
            logo_path TEXT
        );
    """)
    


    # Extend this with other required tables 
    
    conn.commit()
    conn.close()

   