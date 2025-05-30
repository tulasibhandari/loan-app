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
            post TEXT    
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def add_user(username, password, role='user', post=''):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password, role, post) VALUES (?, ?, ?, ?)",
                    (username, hash_password(password), role, post))
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