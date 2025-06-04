import pandas as pd
from models.database import get_connection

def import_members_from_excel(excel_path):
    df = pd.read_excel(excel_path)
    df.columns = df.columns.str.strip().str.replace('\xa0', '').str.replace(' ', '_')

    print("📄 Excel Columns:", df.columns.tolist())

    inserted = 0

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        try:
            cur.execute("""
                INSERT OR IGNORE INTO member_info (
                    member_number, member_name, address, ward_no, phone, dob_bs,
                    citizenship_no, father_name, grandfather_name,
                    spouse_name, spouse_phone, business_name,
                    business_address, job_name, job_address
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(row.get("member_number", "")).split('.')[0].zfill(9),
                str(row.get("member_name", "")).strip(),
                str(row.get("address", "")).strip(),
                str(row.get("ward_no", "")).strip(),
                str(row.get("phone", "")).strip().split('.')[0],
                str(row.get("dob_bs", "")).strip(),
                str(row.get("citizenship_no", "")).strip(),
                str(row.get("father_name", "")).strip(),
                str(row.get("grandfather_name", "")).strip(),
                # str(row.get("spouse_name", "")).strip(),
                # str(row.get("spouse_phone", "")).strip(),
                # str(row.get("business_name", "")).strip(),
                # str(row.get("business_address", "")).strip(),
                # str(row.get("job_name", "")).strip(),
                # str(row.get("job_address", "")).strip(),
                row.get("spouse_phone") or None,
                row.get("business_name") or None,
                row.get("business_address") or None,
                row.get("job_name") or None,
                row.get("job_address") or None
                        ))
            inserted += 1
        except Exception as e:
            print("❌ Error inserting row:", e)

    conn.commit()
    conn.close()
    return inserted
