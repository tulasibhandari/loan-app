from models.database import get_connection

def save_project(data):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO collateral_projects (
                   member_number, project_name, self_investment, 
                   requested_loan_amount, total_cost, remarks
                ) VALUES (?,?,?,?,?,?)
    """, (
        data["member_number"],
        data["project_name"],
        data["self_investment"],
        data["requested_loan_amount"],
        data["total_cost"],
        data["remarks"]
   ))
    
    conn.commit()
    conn.close()

def fetch_projects_by_member(member_number):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM collateral_projects WHERE member_number = ?", (member_number,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(columns, row)) for row in rows]
