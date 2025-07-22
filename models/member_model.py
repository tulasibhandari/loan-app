# models/member_model.py

from models.database import get_connection

def save_member_info(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO member_info (
            member_number, member_name, address, ward_no, phone, dob_bs,
            citizenship_no, father_name, grandfather_name, spouse_name,
            spouse_phone, business_name, business_address, job_name, job_address,
            email, profession, facebook_detail, whatsapp_detail
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(member_number) DO UPDATE SET
            member_name=excluded.member_name,
            address=excluded.address,
            ward_no=excluded.ward_no,
            phone=excluded.phone,
            dob_bs=excluded.dob_bs,
            citizenship_no=excluded.citizenship_no,
            father_name=excluded.father_name,
            grandfather_name=excluded.grandfather_name,
            spouse_name=excluded.spouse_name,
            spouse_phone=excluded.spouse_phone,
            business_name=excluded.business_name,
            business_address=excluded.business_address,
            job_name=excluded.job_name,
            job_address=excluded.job_address,
            email=excluded.email,
            profession=excluded.profession,
            facebook_detail=excluded.facebook_detail,
            whatsapp_detail=excluded.whatsapp_detail
    """, (
        data.get("member_number"),
        data.get("member_name"),
        data.get("address"),
        data.get("ward_no"),
        data.get("phone"),
        data.get("dob_bs"),
        data.get("citizenship_no"),
        data.get("father_name"),
        data.get("grandfather_name"),
        data.get("spouse_name"),
        data.get("spouse_phone"),
        data.get("business_name"),
        data.get("business_address"),
        data.get("job_name"),
        data.get("job_address"),
        data.get("email"),
        data.get("profession"),
        data.get("facebook_detail"),
        data.get("whatsapp_detail")
    ))

    conn.commit()
    conn.close()


def update_member_info(data):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE member_info SET
            member_name=?,
            address=?,
            ward_no=?,
            phone=?,
            dob_bs=?,
            citizenship_no=?,
            father_name=?,
            grandfather_name=?,
            spouse_name=?,
            spouse_phone=?,
            business_name=?,
            business_address=?,
            job_name=?,
            job_address=?,
            email=?,
            profession=?,
            facebook_detail=?,
            whatsapp_detail=?
        WHERE member_number=?
    """, (
        data["member_name"],
        data["address"],
        data["ward_no"],
        data["phone"],
        data["dob_bs"],
        data["citizenship_no"],
        data["father_name"],
        data["grandfather_name"],
        data["spouse_name"],
        data["spouse_phone"],
        data["business_name"],
        data["business_address"],
        data["job_name"],
        data["job_address"],
        data["email"],
        data["profession"],
        data["facebook_detail"],
        data["whatsapp_detail"],
        data["member_number"]
    ))

    conn.commit()
    conn.close()

def fetch_all_members():
    """ m['member_number'], m['member_name'], m['phone'], m['dob_bs'], m['citizenship_no'],
                m['address'], m['ward_no'], m['father_name'], m['grandfather_name'],
                m['spouse_name'], m['spouse_phone'], m['email'], m['profession'],
                m['facebook_detail'], m['whatsapp_detail'], m['business_name'],
                m['business_address'], m['job_name'] """
    from models.database import get_connection
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
            SELECT member_number, member_name, address, ward_no, phone, dob_bs, citizenship_no, father_name,
                    grandfather_name, spouse_name, spouse_phone, business_name, business_address,
                    job_name, job_address, email, profession, facebook_detail, whatsapp_detail
            FROM member_info
    """)
    rows = cur.fetchall()
    conn.close()
    return [
        {
            'member_number': r[0],
            'member_name': r[1],
            'address': r[2],
            'ward_no': r[3],
            'phone': r[4],
            'dob_bs': r[5],
            'citizenship_no': r[6],
            'father_name': r[7],
            'grandfather_name': r[8],
            'spouse_name': r[9],
            'spouse_phone': r[10],
            'business_name': r[11],
            'business_address': r[12],
            'job_name': r[13],
            'job_address': r[14],
            'email': r[15],
            'profession': r[16],
            'facebook_detail': r[17],
            'whatsapp_detail': r[18]
        }
        for r in rows
    ]


def delete_member(member_number):
    from models.database import get_connection
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM member_info WHERE member_number=?", (member_number,))
    conn.commit()
    conn.close()
