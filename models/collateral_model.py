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
                    share_amount TEXT,
                    total_saving TEXT )
        """)
        # Check if the table already exists and needs alteration
        cursor.execute("PRAGMA table_info(collateral_basic)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'share_amount' not in columns:
            cursor.execute("ALTER TABLE collateral_basic ADD COLUMN share_amount TEXT")
        
        # Insert or updte data            
        cursor.execute("""
            INSERT INTO collateral_basic (
                member_number,
                monthly_saving,
                child_saving,
                share_amount,
                total_saving
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            member_number,
            data['monthly_saving'],
            data['child_saving'],
            data['share_amount'],
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
    
def get_collateral_basic(headers_only=False):
    if headers_only:
        return ["Member Number", "Monthly Saving", "Child Saving", "Total Saving"]
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT member_number, monthly_saving, child_saving, total_saving FROM collateral_basic")
    data = cur.fetchall()
    conn.close()
    return data

def get_collateral_properties(headers_only=False):
    if headers_only:
        return [
            "Member Number", "Owner Name", "Father/Spouse",
            "Grandfather/Father-in-law", "District", "Municipality/VDC",
            "Sheet No", "Ward No", "Plot No", "Area", "Land Type"
        ]
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT member_number, owner_name, father_or_spouse,
            grandfather_or_father_in_law, district,
            municipality_vdc, sheet_no, ward_no, plot_no, area,
            land_type
        FROM collateral_properties
    """)

    data = cur.fetchall()
    conn.close()
    return data

def get_collateral_family_details(headers_only=False):
    if headers_only:
        return [
            "Member Number", "Name", "Age", "Relation", 
            "Member of Org", "Occupation", "Monthly Income"
        ]
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT member_number, name, age, relation, member_of_org, occupation, monthly_income
        FROM collateral_family_details
    """)
    data = cur.fetchall()
    conn.close()
    return  data

def get_collateral_income_expense(headers_only=False):
    if headers_only:
        return ["Member Number", "Field", "Amount", "Type"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT member_number, field, amount, type FROM collateral_income_expense")

    data = cur.fetchall()
    conn.close()
    return data

def get_collateral_projects(headers_only=False):
    if headers_only:
        return ["Member Number", "Project Name", "Self Investment", "Requested Loan Amount", "Total Cost", "Remarks"]
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT member_number, project_name, self_investment, requested_loan_amount, total_cost, remarks
        FROM collateral_projects 
    """)
    data = cur.fetchall()
    conn.close()
    return data

def get_approved_loans(headers_only=False):
    if headers_only:
        return ["Member Number", "Approved Loan Amount", "Approved Loan Amount (Words)"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT member_number, approved_loan_amount, approved_loan_amount_words FROM approval_info")
    data = cur.fetchall()
    conn.close()
    return data


