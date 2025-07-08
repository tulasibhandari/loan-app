from models.database import get_connection


def save_collateral_info(data: dict, member_number:str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS collateral_basic (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_number TEXT,
                    monthly_saving TEXT,
                    child_saving TEXT,
                    total_saving TEXT )
        """)
            
        cursor.execute("""
            INSERT INTO collateral_basic (
                member_number,
                monthly_saving,
                child_saving,
                total_saving
            ) VALUES (?, ?, ?, ?)
        """, (
            member_number,
            data['monthly_saving'],
            data['child_saving'],
            data['total_saving']
        ))

        conn.commit()
        conn.close()
        print("✅ Collateral Basic info saved to database.")
    except Exception as e:
        print("❌ Error saving collateral info:", e)

def save_affiliated_institutions(member_number, entries):
    conn = get_connection()
    cur = conn.cursor()

    for row in entries:
        cur.execute("""
            INSERT INTO collateral_affiliations (member_number, institution, address, postition, estimated_income, remarks)
            VALUES (?,?,?,?,?,?)
        """, (member_number, *row)
        )
    conn.commit()
    conn.close()

def save_property_info(member_number, entries):
    conn = get_connection()
    cur = conn.cursor()

    for row in entries:
        cur.execute("""
            INSERT INTO collateral_properties(
                member_number,
                owner_name,
                father_or_spouse,
                grandfather_or_father_inlaw,
                district,
                municipality_vdc,
                sheet_no,
                ward_no,
                plot_no,
                area,
                land_type)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (member_number, *row)
        )
    conn.commit()
    conn.close()

def save_family_info(member_number, entries):
    conn = get_connection()
    cur = conn.cursor()

    for row in entries:
        cur.execute("""
            INSERT INTO collateral_family_details (
                member_number,
                name,
                age,
                relation,
                member_of_org,
                occupation,
                monthly_income)
            VALUES (?,?,?,?,?,?,?)
        """, (member_number, *row)
        )
    conn.commit()
    conn.close()

def save_income_expense(member_number, rows):
    conn = get_connection()
    cur = conn.cursor()
    
    for row in rows:
        field, amount, typ = row
        cur.execute("""
            INSERT INTO collateral_income_expense(member_number, field, amount, type)
            VALUES (?,?,?,?)
        """, (member_number, field, amount, typ)
        )
    conn.commit()
    conn.close()
    