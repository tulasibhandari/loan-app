from models.database import get_connection
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def save_or_update_member_info(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    # Ensure correct format
    data['member_number'] = str(data['member_number']).strip().zfill(9)  # Moved before SELECT
    cursor.execute("SELECT id FROM member_info WHERE member_number=?", (data['member_number'],))
    row = cursor.fetchone()
     
    if row:
        # update the existing row
        cursor.execute("""
            UPDATE member_info SET
                date=?,
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
                job_address=?
            WHERE member_number=?
        """, (
            data['date'],
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
            data['member_number']  # ✅ this was missing!
        ))
    else:
        # Insert data 
        cursor.execute(""" 
            INSERT OR IGNORE INTO member_info(
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
    
    print(f"🔄 Saving/Updating: {data['member_number']}")
    conn.commit()
    print("✅ DB commit complete")
    conn.close()

def save_loan_info(data):
    conn = get_connection()
    cursor = conn.cursor()
    
    # ✅ ADDED Later to  Ensure consistent format
    data['member_number'] = str(data['member_number']).strip().zfill(9)

    # Log input data
    logging.debug(f"Saving loan for member: {data['member_number']}, data: {data}")
    # Check for active, pending or approved loans
    cursor.execute("""
        SELECT loan_type FROM loan_info
        WHERE member_number = ? AND status IN ('pending', 'active','approved')
    """, (data["member_number"],))
    existing_loans = cursor.fetchall()
    logging.debug(f"Existing loans for {data['member_number']}: {existing_loans}")

    if existing_loans:
        if all(loan[0] != "खरखाँचो" for loan in existing_loans):
            conn.close()
            raise ValueError("New Loan can not be assign for this member.")
        
        # Validate numeric and date fields
        try:
            if not data["loan_amount"].replace(",", "").isdigit():
                raise ValueError("Loan amount must be numeric.")
            if not all(data[field].replace(",","").isdigit() for field in ["loan_completion_year",
                                            "loan_completion_month", "loan_completion_day"]):
                raise ValueError("Loan completion date (Year, month, day) must be numbers.")
        except KeyError as e:
            conn.close()
            raise ValueError(f"Mandatory fields are missing: {e}")

        # Proceeding with saving the loan
    try:
        cursor.execute("""
            INSERT INTO loan_info(
                member_number, loan_type, interest_rate, loan_duration,
                repayment_duration,
                loan_amount, loan_amount_in_words, loan_completion_year,
                loan_completion_month,
                loan_completion_day,
                status
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data["member_number"],
            data["loan_type"],
            data["interest_rate"],
            data["loan_duration"],
            data["repayment_duration"],
            data["loan_amount"],
            data["loan_amount_in_words"],
            data["loan_completion_year"],
            data["loan_completion_month"],
            data["loan_completion_day"],
            "pending"
        ))
        conn.commit()
        logging.debug(f"Loan saved successfully for {data['member_number']}")
    except sqlite3.Error as e:
        conn.close()
        logging.debug(f"Database error while saving loan: {e}")
        raise ValueError(f"Database Error: {e}")
    finally:
        conn.close()  
    
def fetch_all_loans():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        m.member_number,
        m.member_name,
        l.loan_type,
        l.loan_amount,
        a.approved_loan_amount,
        CASE
            WHEN a.approved_loan_amount IS NOT NULL THEN 'Approved'
            ELSE 'Pending'
        END as status,
        COALESCE(a.approval_date, '')
    FROM member_info m
    JOIN loan_info l ON m.member_number = l.member_number
    LEFT JOIN approval_info a ON m.member_number = a.member_number
    ORDER BY a.approval_date DESC        
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_loan_info_members():
    """
    Fetch members with loan details from the loan_info table for ReportsTab.
    Returns: List of tuples (member_number, member_name, loan_type, status)
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT l.member_number, m.member_name, l.loan_type, l.status
            FROM loan_info l
            JOIN member_info m ON l.member_number = m.member_number
            WHERE l.status IN ('pending', 'active', 'approved')
            ORDER BY l.member_number
        """
        cursor.execute(query)
        members = cursor.fetchall()
        logging.debug(f"Fetched members from loan_info: {members}")  # Log the raw data
        logging.debug(f"Number of members fetched: {len(members)}")
        return members
    except sqlite3.Error as e:
        logging.error(f"Database error in fetch_loan_info_members: {e}")
        return []
    finally:
        conn.close()

def check_collateral_basic(member_number):
    """ Check if collateral basic data exists for the given member_number"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM collateral_basic WHERE member_number=?", (member_number,))
        result = cursor.fetchone()
        count = result[0] if result else 0 # Extract integer from tuple
        logging.debug(f"Collateral basic count for member_number {member_number}:{count}")
        return count > 0
    except sqlite3.Error as e:
        logging.error(f"Database error in checking check_collateral_basic: {e}")
        raise ValueError(f" Database Error: खरखाँचो धितो विवरण जाँच गर्दा त्रुटि: {e}")
    finally:
        conn.close()

def check_collateral_properties(member_number):
    """ Check if collateral properties exist for the given number"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM collateral_properties WHERE member_number =?", (member_number, ))
        result = cursor.fetchone()
        count = result[0] if result else 0 # Extract integer from tuple
        logging.debug(f"Collateral properties count for member_number {member_number}: {count}")
        return count > 0
    except sqlite3.Error as e:
        logging.error(f"Database error in checking check_collateral_basic: {e}")
        raise ValueError(f" Database Error: धितो सम्पत्ति विवरण जाँच गर्दा त्रुटि: {e}")
    finally:
        conn.close()

def check_collateral_projects(member_number):
    """Check if collateral projects exist for the given member_number."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM collateral_projects WHERE member_number = ?", (member_number,))
        result = cursor.fetchone()
        count = result[0] if result else 0 # extract integer from tuple
        logging.debug(f"Collateral projects count for member_number {member_number}: {count}")
        return count > 0
    except sqlite3.Error as e:
        logging.error(f"Database error in check_collateral_projects: {e}")
        raise ValueError(f"डाटाबेस त्रुटि: परियोजना विवरण जाँच गर्दा त्रुटि: {e}")
    finally:
        conn.close()

def check_collateral_affiliations(member_number):
    """Check if collateral affiliations exist for the given member_number."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM collateral_affiliations WHERE member_number = ?", (member_number,))
        result = cursor.fetchone()
        count = result[0] if result else 0 # extract integer from tuple
        logging.debug(f"Collateral affiliations count for member_number {member_number}: {count}")
        return count > 0
    except sqlite3.Error as e:
        logging.error(f"Database error in check_collateral_affiliations: {e}")
        raise ValueError(f"डाटाबेस त्रुटि: सम्बद्धता विवरण जाँच गर्दा त्रुटि: {e}")
    finally:
        conn.close()

def check_collateral_income_expense(member_number):
    """Check if collateral income/expense details exist for the given member_number."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM collateral_income_expense WHERE member_number = ?", (member_number,))
        result = cursor.fetchone()
        count = result[0] if result else 0 # Extract integer from tuple
        logging.debug(f"Collateral income/expense count for member_number {member_number}: {count}")
        return count > 0
    except sqlite3.Error as e:
        logging.error(f"Database error in check_collateral_income_expense: {e}")
        raise ValueError(f"डाटाबेस त्रुटि: आय/व्यय विवरण जाँच गर्दा त्रुटि: {e}")
    finally:
        conn.close()

def check_collateral_family_details(member_number):
    """Check if collateral family details exist for the given member_number."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM collateral_family_details WHERE member_number = ?", (member_number,))
        result = cursor.fetchone()
        count = result[0] if result else 0 # Extract integer from tuple
        logging.debug(f"Collateral family details count for member_number {member_number}: {count}")
        return count > 0
    except sqlite3.Error as e:
        logging.error(f"Database error in check_collateral_family_details: {e}")
        raise ValueError(f"डाटाबेस त्रुटि: परिवार विवरण जाँच गर्दा त्रुटि: {e}")
    finally:
        conn.close()
