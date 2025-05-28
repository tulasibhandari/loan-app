# models/loan_model.py
from models.database import get_connection


def save_member_info(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" 
        INSERT INTO member_info(
                   date, member_number, member_name, address, ward_no,
                   phone, dob_bs, citizenship_no, father_name, grandfather_name,
                   spouse_name, spouse_phone, business_name, business_address,
                   job_name, job_address
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data['date'],
        data['member_number'],
        data['member_name'],
        data['address'],
        data['ward_no'],
        data['phone'],
        data['dob_bs'],
        data['citizenship_no'],
        data['father_name'],
        data['grandfather_name'],
        data['spouse_name'],
        data['spouse_phone'],
        data['business_name'],
        data['business_address'],
        data['job_name'],
        data['job_address'],
    ))

    conn.commit()
    conn.close()