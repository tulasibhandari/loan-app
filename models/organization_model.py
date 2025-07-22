# models/organization_model.py
from models.database import get_connection

def save_organization_profile(name, address, logo_path):
    """ Save or update organization  profile """
    conn = get_connection()
    cursor = conn.cursor()

    # Insert only if table is empty 
    cursor.execute("SELECT COUNT(*) FROM organization_profile")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
            INSERT INTO organization_profile (company_name, address, logo_path)
            VALUES (?,?,?)
        """, (name, address, logo_path))
    else:
        cursor.execute("""
            UPDATE organization_profile
            SET company_name = ?, address = ?, logo_path = ?
            WHERE id = 1
        """, (name, address, logo_path))
    conn.commit()
    conn.close()

def get_organization_profile():
    """ Fetch ogranization profile details """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT company_name, address, logo_path FROM organization_profile LIMIT 1 ")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"company_name": row[0], "address": row[1], "logo_path": row[2]}
    return None
