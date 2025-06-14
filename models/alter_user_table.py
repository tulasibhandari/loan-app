from .database import get_connection

def alter_users_table_add_fullname():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("ALTER TABLE users ADD COLUMN full_name_nepali TEXT")
        print("✅ Column full_name_nepali added to users table.")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("⚠ Column already exists.")
        else:
            print("❌ Error altering users table:", e)
    finally:
        conn.commit()
        conn.close()
