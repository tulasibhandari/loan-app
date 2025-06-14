#servicex/fetch_full_member_data.py
from models.database import get_connection

def fetch_all_member_related_data(member_number):
    conn = get_connection()
    cursor = conn.cursor()
    result = {}

    # Fetch from member_info
    cursor.execute("SELECT * FROM member_info WHERE member_number=?", (member_number,))
    row = cursor.fetchone()
    if row:
        columns = [desc[0] for desc in cursor.description]
        result.update({f"member_info.{col}": val for col, val in zip(columns, row)})

    # Fetch from loan_info (assuming one-to-one mapping for now)
    cursor.execute("SELECT * FROM loan_info WHERE member_number=?", (member_number,))
    row = cursor.fetchone()
    if row:
        columns = [desc[0] for desc in cursor.description]
        result.update({f"loan_info.{col}": val for col, val in zip(columns, row)})

    # Fetch from collateral_info (if applicable)
    cursor.execute("SELECT * FROM collateral_basic WHERE member_number=?", (member_number,))
    row = cursor.fetchone()
    if row:
        columns = [desc[0] for desc in cursor.description]
        result.update({f"collateral_info.{col}": val for col, val in zip(columns, row)})

    conn.close()
    return result
