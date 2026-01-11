from models.database import get_connection
import os

def save_guranteer_details(data):
    try:
        conn = get_connection()
        db_path = conn if hasattr(conn, 'get_db_path') else "Unknown path"  # Fallback if path isn’t accessible
        print(f"Using database connection: {db_path}")
        cursor = conn.cursor()
        print(f"Attempting to create table 'guranteer_details'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guranteer_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_number TEXT,
                guarantor_member_number TEXT,
                guarantor_name TEXT,
                guarantor_address TEXT,
                guarantor_ward TEXT,
                guarantor_phone TEXT,
                guarantor_citizenship TEXT,
                guarantor_grandfather TEXT,
                guarantor_father TEXT,
                guarantor_issue_dist TEXT,
                guarantor_age TEXT
            )
        """)
        print("Table creation executed, checking table existence...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='guranteer_details';")
        table_exists = cursor.fetchone()
        print(f"Table 'guranteer_details' exists: {bool(table_exists)}")
        print("Inserting data...")
        cursor.execute("""
            INSERT INTO guranteer_details (
                member_number,
                guarantor_member_number,
                guarantor_name,
                guarantor_address,
                guarantor_ward,
                guarantor_phone,
                guarantor_citizenship,
                guarantor_grandfather,
                guarantor_father,
                guarantor_issue_dist,
                guarantor_age
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['member_number'],
            data['guarantor_member_number'],
            data['guarantor_name'],
            data['guarantor_address'],
            data['guarantor_ward'],
            data['guarantor_phone'],
            data['guarantor_citizenship'],
            data['guarantor_grandfather'],
            data['guarantor_father'],
            data['guarantor_issue_dist'],
            data['guarantor_age']
        ))
        conn.commit()
        print("Data committed successfully")
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving guarantor details: {e}")
        if conn:
            conn.close()
        return False