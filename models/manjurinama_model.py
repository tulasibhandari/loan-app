from models.database import get_connection

def save_manjurinama_details(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE  IF NOT EXISTS manjurinama_details (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       member_number TEXT,
                       person_name TEXT,
                       grandfather_name TEXT,
                       father_name TEXT,
                       age TEXT,
                       district TEXT,
                       muncipality TEXT,
                       wada_no TEXT,
                       tole TEXT
                       )
        """)
        cursor.execute("""
            INSERT INTO manjurinama_details(member_number,
                       person_name,
                       grandfather_name,
                       father_name,
                       age,
                       district,
                       muncipality,
                       wada_no,
                       tole
            ) VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            data['member_number'],
            data['person_name'] ,
            data['grandfather_name'],
            data['father_name'],
            data['age'],
            data['district'],
            data['muncipality'],
            data['wada_no'],
            data['tole']
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving Manjurinama Details: {e}")
        return False

def get_manjurinama_details(member_number):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                SELECT id, member_number, person_name, grandfather_name,
                    father_name, age, district, municipality, wada_no, tole
                FROM manjurinama_details
                WHERE member_number = ?
        """, (member_number,))
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"Error fetching manjurinama details: {e}")
        return False

def update_manjurinama_details(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE manjurinama_details
            SET person_name =?, grandfather_name = ?,
                    father_name = ?, age = ?, district = ?, municipality = ?, wada_no = ?, tole= ?
            WHERE member_number = ?                       
        """, (
            data['person_name'] ,
            data['grandfather_name'],
            data['father_name'],
            data['age'],
            data['district'],
            data['muncipality'],
            data['wada_no'],
            data['tole'],
            data['member_number'],            
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating manjurinama details: {e}")
        return False