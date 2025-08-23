
import sqlite3
from hashlib import sha256
from models.database import get_connection
import random
import string
import smtplib
from email.mime.text import MIMEText
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_user_table():
    conn = get_connection()
    cur = conn.cursor()
    # Check if table exists and add columns if missing
    cur.execute("PRAGMA table_info(users)")
    columns = {row[1] for row in cur.fetchall()}  # Set of column names
    if 'email' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN email TEXT")
        logging.info("Added 'email' column to users table")
        # Set a default email for existing users to avoid NULL issues
        cur.execute("UPDATE users SET email = 'default@example.com' WHERE email IS NULL")
    if 'reset_code' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN reset_code TEXT DEFAULT NULL")
        logging.info("Added 'reset_code' column to users table")
    conn.commit()
    conn.close()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def add_user(username, password, role='user', post='', full_name_nepali='', email=''):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password, role, post, full_name_nepali, email) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, hash_password(password), role, post, full_name_nepali, email))
        conn.commit()
    except sqlite3.IntegrityError:
        print("⚠ Username or email already exists.")
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
    cur = conn.cursor()
    cur.execute("SELECT username, post, full_name_nepali, email FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {'username': row[0], 'post': row[1], 'full_name_nepali': row[2], 'email': row[3]}
    return None

# def get_all_users():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT username, post, full_name_nepali, email FROM users")
#     users = [{'username': row[0], 'post': row[1], 'full_name_nepali': row[2], 'email': row[3]} for row in cur.fetchall()]
#     conn.close()
#     return users

def get_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, password, role, post, full_name_nepali, email FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            'username': row[0],
            'password': row[1],
            'role': row[2],
            'post': row[3],
            'full_name_nepali': row[4],
            'email': row[5]
        }
    return None

def update_user(username, password=None, role=None, post=None, full_name_nepali=None, email=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Build the SET clause dynamically based on provided arguments
        updates = []
        values = []
        if password is not None:
            updates.append("password = ?")
            values.append(hash_password(password))
        if role is not None:
            updates.append("role = ?")
            values.append(role)
        if post is not None:
            updates.append("post = ?")
            values.append(post)
        if full_name_nepali is not None:
            updates.append("full_name_nepali = ?")
            values.append(full_name_nepali)
        if email is not None:
            updates.append("email = ?")
            values.append(email)
        values.append(username)

        if updates:
            cur.execute(f"UPDATE users SET {', '.join(updates)} WHERE username = ?", values)
            conn.commit()
            return cur.rowcount > 0
        return False
    except sqlite3.Error as e:
        logging.error(f"Database error during user update: {e}")
        return False
    finally:
        conn.close()

def delete_user(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return cur.rowcount > 0
    except sqlite3.Error as e:
        logging.error(f"Database error during user deletion: {e}")
        return False
    finally:
        conn.close()


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
                INSERT INTO users (username, password, role, post, full_name_nepali, email)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("admin", hash_password(password), "admin", "Administrator", "एडमिन", "admin@example.com"))
            conn.commit()
            print("✅ Default admin user created: admin / admin123")
    except Exception as e:
        print("❌ Failed to ensure default admin:", e)
    finally:
        conn.close()

def generate_reset_code(username):
    """Generate a random code and send it to the user's email."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "Username not found."

    email = row[0]
    if not email:  # Handle NULL or empty email
        conn.close()
        return False, "No email associated with this username. Please contact support."

    code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # 6-character alphanumeric code
    try:
        cur.execute("UPDATE users SET reset_code = ? WHERE username = ?", (code, username))
        conn.commit()
        # Send email
        msg = MIMEText(f"Your password reset code is: {code}")
        msg['Subject'] = 'Password Reset Code'
        msg['From'] = 'noreplytestmail871@gmail.com'  # Replace with your Gmail address
        msg['To'] = email

        print(f"Attempting to connect to smtp.gmail.com with {msg['From']}")  # Debug print
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('noreplytestmail871@gmail.com', 'mrmf jjux kssd ibzc')  # Use App Password
            server.send_message(msg)
        logging.debug(f"Reset code sent to {email} for {username}")
        return True, "Reset code sent to your email."
    except Exception as e:
        logging.error(f"Failed to generate or send reset code: {e}")
        return False, str(e)
    finally:
        conn.close()

def reset_password(username, code, new_password):
    """Validate the code and reset the password if different from old."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password, reset_code FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False

    old_hashed = row[0]
    saved_code = row[1]
    if saved_code != code:
        conn.close()
        return False

    new_hashed = hash_password(new_password)
    if new_hashed == old_hashed:
        conn.close()
        return False  # Same as old password

    try:
        cur.execute("UPDATE users SET password = ?, reset_code = NULL WHERE username = ?", 
                    (new_hashed, username))
        conn.commit()
        return True
    except sqlite3.Error as e:
        logging.error(f"Database error during password reset: {e}")
        return False
    finally:
        conn.close()

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, post, full_name_nepali, email FROM users")
    users = [{'username': row[0], 'post': row[1], 'full_name_nepali': row[2], 'email': row[3]} for row in cur.fetchall()]
    conn.close()
    return users