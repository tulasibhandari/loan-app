from models.database import get_connection

def save_witness(member_number, witness_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO loan_witness (member_number,
                   name,
                   relation,
                   address_mun,
                   ward_no,
                   address_tole,
                   age
                   ) VALUES (?,?,?,?,?,?,?)
    """,(
        member_number,
        witness_data['name'],
        witness_data['relation'],
        witness_data['address_mun'],
        witness_data['ward_no'],
        witness_data['address_tole'],
        witness_data['age'],
    ))
    conn.commit()
    conn.close()

def fetch_witnesses(member_number):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM loan_witness WHERE member_number = ?", (member_number,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

