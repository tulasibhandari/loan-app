from models.database import get_connection


def fetch_member_info(member_number):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM member_info WHERE member_number = ?", (member_number,))
    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    if row:
        return dict(zip(columns, row))
    return {}


def fetch_loan_info(member_number):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM loan_info WHERE member_number = ?", (member_number,))
    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    if row:
        return dict(zip(columns, row))
    return {}


def fetch_collateral_basic(member_number):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM collateral_basic WHERE member_number = ?", (member_number,))
    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    if row:
        return dict(zip(columns, row))
    return {}


def fetch_collateral_properties(member_number):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM collateral_properties WHERE member_number = ?", (member_number,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return [dict(zip(columns, row)) for row in rows] if rows else []


def fetch_collateral_affiliations(member_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM collateral_affiliations WHERE member_number = ?", (member_number,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return [dict(zip(columns, row)) for row in rows] if rows else []


def fetch_collateral_family_details(member_number):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM collateral_family_details WHERE member_number = ?", (member_number,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return [dict(zip(columns, row)) for row in rows] if rows else []


def fetch_income_expense(member_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM collateral_income_expense WHERE member_number = ?", (member_number,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return [dict(zip(columns, row)) for row in rows] if rows else []


def fetch_project_detail(member_number):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM collateral_projects WHERE member_number = ?", (member_number,))
        rows = cursor.fetchall()

        if rows:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []

def fetch_approval_info(member_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM approval_info WHERE member_number = ?", (member_number,))
    row = cursor.fetchone()

    if row:
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return dict(zip(columns, row))
    conn.close()
    return {}

def fetch_witness_detail(member_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * from loan_witness WHERE member_number = ?", (member_number,))
    rows = cursor.fetchall()

    conn.close()

    if rows:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    return []

def fetch_guarantor_details(member_number):
    """ Fetch guarantor details for a member"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guranteer_details WHERE member_number = ?", (member_number,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    return []    
