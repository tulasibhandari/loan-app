import sqlite3
from hashlib import sha256
from models.database import get_connection

def create_user_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            post TEXT,
            full_name_nepali TEXT               
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def add_user(username, password, role='user', post='', full_name_nepali=''):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password, role, post, full_name_nepali) VALUES (?, ?, ?, ?, ?)",
                    (username, hash_password(password), role, post, full_name_nepali))
        conn.commit()
    except sqlite3.IntegrityError:
        print("⚠ Username already exists.")
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if row and row[0] == hash_password(password):
        return True
    return False


def get_user_role(username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

def get_user_details(username):
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("SELECT username, post, full_name_nepali from users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {'username': row[0], 'post': row[1], 'full_name_nepali': row[2]}
    return None

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username, post, full_name_nepali FROM users")
    users = [{'username': row[0], 'post': row[1], 'full_name_nepali': row[2]} for row in cur.fetchall()]
    conn.close()
    return users

def ensure_default_admin():
    """Create default admin user if no users exist."""
    conn = get_connection()
    cursor = conn.cursor()
    password = "admin123"
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("""
                INSERT INTO users (username, password, role, post, full_name_nepali)
                VALUES (?, ?, ?, ?, ?)
            """, ("admin", hash_password(password), "admin", "Administrator", "एडमिन"))
            conn.commit()
            print("✅ Default admin user created: admin / admin123")
    except Exception as e:
        print("❌ Failed to ensure default admin:", e)
    finally:
        conn.close()
