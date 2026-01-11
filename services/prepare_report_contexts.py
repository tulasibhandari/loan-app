from nepali_datetime import date as nepali_date
from utils.converter import convert_to_nepali_digits
from utils.age_utils import calculate_nepali_age
from services.report_fetchers import (
    fetch_member_info,
    fetch_loan_info,
    fetch_collateral_basic,
    fetch_collateral_affiliations,
    fetch_collateral_properties,
    fetch_collateral_family_details,
    fetch_income_expense,
    fetch_project_detail,
    fetch_approval_info,
    fetch_witness_detail,
    fetch_guarantor_details
)
from models.database import get_connection
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def normalize_bs_date(date_str):
    """
    Normalize date formats (e.g., 'YYYY/MM/DD' or 'YYYY-MM-DD') to 'YYYY-MM-DD'.
    Returns empty string if invalid.
    """
    if not date_str:
        return ""
    try:
        normalized = date_str.replace('/', '-')
        year, month, day = map(int, normalized.split('-'))
        nepali_date(year, month, day)
        return f"{year:04d}-{month:02d}-{day:02d}"
    except Exception as e:
        logging.error(f"Error normalizing date {date_str}: {e}")
        return ""

def extract_bs_date_parts(bs_date_str):
    """
    Input: '2082-03-05' string
    Returns: dict with year, month, day, roj (weekday)
    """
    try:
        normalized_date = normalize_bs_date(bs_date_str)
        if not normalized_date:
            raise ValueError("Invalid date format")
        year, month, day = map(int, normalized_date.split("-"))
        bs_date = nepali_date(year, month, day)
        roj_map = {
            0: "१",  # आईतबार
            1: "२",  # सोमबार
            2: "३",  # मंगलबार
            3: "४",  # बुधबार
            4: "५",  # बिहीबार
            5: "६",  # शुक्रबार
            6: "७"   # शनिबार
        }
        return {
            "bs_year": convert_to_nepali_digits(str(year)),
            "bs_month": convert_to_nepali_digits(str(month)),
            "bs_day": convert_to_nepali_digits(str(day)),
            "bs_roj": convert_to_nepali_digits(roj_map.get(bs_date.weekday(), ""))
        }
    except Exception as e:
        logging.error(f"Error extracting BS date parts for {bs_date_str}: {e}")
        return {}

def prepare_report_context(member_number, entered_by_name="", entered_by_post="", approved_by_name="", approved_by_post=""):
    try:
        member_info = fetch_member_info(member_number) or {}
        loan_info = fetch_loan_info(member_number) or {}
        collateral_basic = fetch_collateral_basic(member_number) or {}
        affiliations = fetch_collateral_affiliations(member_number) or []
        properties = fetch_collateral_properties(member_number) or []
        family = fetch_collateral_family_details(member_number) or []
        income_expense = fetch_income_expense(member_number) or []
        project_details = fetch_project_detail(member_number) or []
        approval_data = fetch_approval_info(member_number) or {}
        witnesses = fetch_witness_detail(member_number) or []
        guarantors = fetch_guarantor_details(member_number) or []

        logging.debug(f"✅ Member Info: {member_info}")
        logging.debug(f"✅ Loan Info: {loan_info}")
        logging.debug(f"✅ Approval Data: {approval_data}")
        logging.debug(f"✅ Witness Details: {witnesses}")

        # Process family details
        for member in family:
            if "age" in member:
                member["age"] = convert_to_nepali_digits(str(member["age"])) if member["age"] is not None else ""
            if "monthly_income" in member:
                member["monthly_income"] = convert_to_nepali_digits(str(member["monthly_income"])) if member["monthly_income"] is not None else ""

        # Process income and expense
        income = [item for item in income_expense if item.get("type") == "income"]
        expense = [item for item in income_expense if item.get("type") == "expense"]

        # Calculate today's BS date
        bs_today_str = nepali_date.today().strftime("%Y-%m-%d")
        bs_parts = extract_bs_date_parts(bs_today_str)
        logging.debug(f"Simplified BS Date: {bs_parts}")

        # Age calculation
        dob_bs = member_info.get("dob_bs", "")
        normalized_dob = normalize_bs_date(dob_bs)
        age_nep = ""
        if normalized_dob:
            try:
                age = calculate_nepali_age(normalized_dob)
                if age is not None and age != "":
                    age_nep = convert_to_nepali_digits(str(age))
                    logging.debug(f"Calculated age: {age} (Nepali: {age_nep}) for dob_bs: {normalized_dob}")
                else:
                    logging.warning(f"Age calculation returned empty for dob_bs: {normalized_dob}")
            except Exception as e:
                logging.error(f"Error calculating age for dob_bs {normalized_dob}: {e}")
        else:
            logging.warning(f"No valid dob_bs found for member_number {member_number}: {dob_bs}")

        # Process witness details
        for w in witnesses:
            if "age" in w:
                w['age'] = convert_to_nepali_digits(str(w['age'])) if w['age'] is not None else ""
        

        # Process guarantor details 
        for g in guarantors:
            if "guarantor_age" in g and g["guarantor_age"] is not None:
                g['guarantor_age'] = convert_to_nepali_digits(str(g['guarantor_age']))
            if "guarantor_ward" in g and g["guarantor_ward"] is not None:
                g['guarantor_ward'] = convert_to_nepali_digits(str(g['guarantor_ward']))
            if "guarantor_phone" in g and g["guarantor_phone"] is not None:
                g['guarantor_phone'] = convert_to_nepali_digits(str(g['guarantor_phone']))
            if "guarantor_citizenship" in g and g["guarantor_citizenship"] is not None:
                g['guarantor_citizenship'] = convert_to_nepali_digits(str(g['guarantor_citizenship']))
        # Fetch manjurinama_details from db to use in template
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM manjurinama_details
            WHERE member_number = ?
        """, (member_number,))
        manjurinama_data = cursor.fetchone()
        conn.close()

        manjurinama_details = {}
        if manjurinama_data:
            manjurinama_details = dict(zip([desc[0] for desc in cursor.description], manjurinama_data))
            if "age" in manjurinama_details and manjurinama_details["age"] is not None:
                manjurinama_details["manjuri_age"] = convert_to_nepali_digits(str(manjurinama_details["age"]))
                del manjurinama_details["age"]  # Avoid overriding m_age_np
            
            # Rename grandfather_name and father_name to avoid clash
            if "grandfather_name" in manjurinama_details:
                manjurinama_details["manjuri_grandfather_name"] = manjurinama_details["grandfather_name"]
                del manjurinama_details["grandfather_name"]
            if "father_name" in manjurinama_details:
                manjurinama_details["manjuri_father_name"] = manjurinama_details["father_name"]
                del manjurinama_details["father_name"]
            if "municipality" in manjurinama_details:
                manjurinama_details["manjuri_municipality"] = manjurinama_details["municipality"]
                del manjurinama_details["municipality"]
            if "ward_no" in manjurinama_details:
                manjurinama_details["manjuri_ward_no"] = manjurinama_details["ward_no"]
                del manjurinama_details["ward_no"]
            if "tole" in manjurinama_details:
                manjurinama_details["manjuri_tole"] = manjurinama_details["tole"]
                del manjurinama_details["tole"]


        # Build base context with explicit None handling
        base_context = {
            **member_info,
            **loan_info,
            **approval_data,
            "member_number": convert_to_nepali_digits(str(member_info.get("member_number", ""))),
            "spouse_phone": convert_to_nepali_digits(str(member_info.get("spouse_phone", ""))) if member_info.get("spouse_phone") is not None else "",
            "phone_np": convert_to_nepali_digits(str(member_info.get("phone", ""))) if member_info.get("phone") is not None else "",
            "ward_no_np": convert_to_nepali_digits(str(member_info.get("ward_no", ""))) if member_info.get("ward_no") is not None else "",
            "ctznship_np": convert_to_nepali_digits(str(member_info.get("citizenship_no", ""))) if member_info.get("citizenship_no") is not None else "",
            "email": member_info.get("email", "") or "",
            "profession": member_info.get("profession", "") or "",
            "facebook_detail": member_info.get("facebook_detail", "") or "",
            "whatsapp_detail": member_info.get("whatsapp_detail", "") or "",
            "monthly_saving_nep": convert_to_nepali_digits(str(collateral_basic.get("monthly_saving", ""))) if collateral_basic.get("monthly_saving") is not None else "",
            "child_saving_nep": convert_to_nepali_digits(str(collateral_basic.get("child_saving", ""))) if collateral_basic.get("child_saving") is not None else "",
            "total_saving_nep": convert_to_nepali_digits(str(collateral_basic.get("total_saving", ""))) if collateral_basic.get("total_saving") is not None else "",
            "affiliations": affiliations,
            "properties": properties,
            "family_details": family,
            "monthly_income": income,
            "monthly_expense": expense,
            "date_bs": convert_to_nepali_digits(normalize_bs_date(member_info.get("date", ""))) if member_info.get("date") is not None else "",
            "prepared_by_name": approval_data.get("entered_by", "") or "",
            "prepared_by_post": approval_data.get("entered_designation", "") or "",
            "approved_by_name": approval_data.get("approved_by", "") or "",
            "approved_by_post": approval_data.get("approved_post", "") or "",
            "interest_rate_nep": convert_to_nepali_digits(str(loan_info.get("interest_rate", ""))) if loan_info.get("interest_rate") is not None else "",
            "project_details": project_details,
            "approved_loan_amount": approval_data.get("approved_loan_amount", "") or "",
            "approved_loan_amount_words": approval_data.get("approved_loan_amount_words", "") or "",
            "approved_date_bs": convert_to_nepali_digits(normalize_bs_date(approval_data.get("approval_date", ""))) if approval_data.get("approval_date") is not None else "",
            **bs_parts,
            "dob_bs": normalized_dob,
            "m_age_np": age_nep,
            "bs_year_lastdate": convert_to_nepali_digits(str(loan_info.get("loan_completion_year", ""))) if loan_info.get("loan_completion_year") is not None else "",
            "bs_month_lastdate": convert_to_nepali_digits(str(loan_info.get("loan_completion_month", ""))) if loan_info.get("loan_completion_month") is not None else "",
            "bs_day_lastdate": convert_to_nepali_digits(str(loan_info.get("loan_completion_day", ""))) if loan_info.get("loan_completion_day") is not None else "",
            "witnesses": witnesses,
            "guarantors": guarantors,
            # Additional fields from member_info
            "grandfather_name": member_info.get("grandfather_name", "") or "",
            "father_name": member_info.get("father_name", "") or "",
            # "age": age_nep,
            # Additional from loan_info
            "loan_type": loan_info.get("loan_type", "") or "",
            # From manjurinama_details
            **manjurinama_details
        }

        logging.debug(f"🔑 Context Keys Available: {base_context.keys()}")
        logging.debug(f"✅ m_age_np: {base_context['m_age_np']}")
        logging.debug(f"✅ spouse_phone: {base_context['spouse_phone']}")
        logging.debug(f"✅ Approved Date BS: {base_context['approved_date_bs']}")
        logging.debug(f"Collateral Basic: {collateral_basic}")
        logging.debug("🧪 Affiliation Data:")
        for aff in affiliations:
            logging.debug(aff)
        logging.debug("Properties Data:")
        for prop in properties:
            logging.debug(prop)

        return base_context
    except Exception as e:
        logging.error(f"Error preparing report context for member_number {member_number}: {e}")
        return {}
