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
    fetch_witness_detail
)

def extract_bs_date_parts(bs_date_str):
    """
    Input: '2082-03-05' string
    Returns: dict with year, month, day, roj (weekday)
    """
    try:
        year, month, day = map(int, bs_date_str.split("-"))
        bs_date = nepali_date(year, month, day)
        

        # Nepali Weekday (0 = Sunday, 6 = Saturday)
        roj_map = {
            0: "१", # आईतबार
            1: "२", # सोमबार
            2: "३", # मंगलबार
            3: "४", # बुधबार
            4: "५", # बिहीबार
            5: "६", # शुक्रबार
            6: "७"  # शनिबार
        }
        return {
            "bs_year": convert_to_nepali_digits(str(year)),
            "bs_month": convert_to_nepali_digits(str(month)),
            "bs_day": convert_to_nepali_digits(str(day)),
            "bs_roj": convert_to_nepali_digits(roj_map.get(bs_date.weekday(),""))
        }
    except Exception as e:
        print("Error extracting BS date parts:", e)
        return {}



def prepare_report_context(member_number, entered_by_name="", entered_by_post="", approved_by_name="", approved_by_post=""):
    member_info = fetch_member_info(member_number)
    loan_info = fetch_loan_info(member_number)
    collateral_basic = fetch_collateral_basic(member_number)

    affiliations = fetch_collateral_affiliations(member_number)
    properties = fetch_collateral_properties(member_number)
    family = fetch_collateral_family_details(member_number)
    income_expense = fetch_income_expense(member_number)
    project_details = fetch_project_detail(member_number)
    approval_data = fetch_approval_info(member_number)

    print("✅ Approval Data:", approval_data)
    

   
    for member in family:
        if "age" in member:
            member["age"] = convert_to_nepali_digits(member["age"])
            
        if "monthly_income" in member:
            member["monthly_income"] = convert_to_nepali_digits(member["monthly_income"])

 
    income = [item for item in income_expense if item["type"] == "income"]
    expense = [item for item in income_expense if item["type"] == "expense"]
    # bs_parts = extract_bs_date_parts(member_info.get("date", "")) # fetch nepali date from member_info table
    bs_today_str = nepali_date.today().strftime("%Y-%m-%d")
    bs_parts = extract_bs_date_parts(bs_today_str)
    print("Simplified BS Date:", bs_parts, type(bs_parts))

    # -- Age calculation --
    dob_bs = member_info.get("dob_bs", "")
    age = calculate_nepali_age(dob_bs)
    age_nep = convert_to_nepali_digits(age) if age!= "" else ""
    # -- end of Age calculation --

    # --Preparing witness details for report
    witnesses = fetch_witness_detail(member_number)
    print("Witness Details:", witnesses)

    # Optionally convert age to Nepali in witness details
    for w in witnesses:
        if "age" in w:
            w['age'] = convert_to_nepali_digits(w['age'])
    
    # -- End of witness details
    
    context = {
        **member_info,
        **loan_info,
        **collateral_basic,
        "monthly_saving_nep" : convert_to_nepali_digits(collateral_basic.get("monthly_saving", "")),
        "child_saving_nep": convert_to_nepali_digits(collateral_basic.get("child_saving", "")),
        "total_saving_nep": convert_to_nepali_digits(collateral_basic.get("total_saving", "")),
        "affiliations": affiliations,
        "properties": properties,
        "family_details": family,
        "monthly_income": income,
        "monthly_expense": expense,
        "date_bs": convert_to_nepali_digits(member_info.get("date", "")),
        "member_number":convert_to_nepali_digits(member_info.get("member_number", "")),
        "prepared_by_name": approval_data.get("entered_by",""),
        "prepared_by_post": approval_data.get("entered_post",""),
        "approved_by_name": approval_data.get("approved_by",""),
        "approved_by_post": approval_data.get("approved_post", ""),
        "interest_rate_nep": convert_to_nepali_digits(loan_info.get("interest_rate", "")),
        "email": member_info.get("email", ''),
        "profession": member_info.get("profession", ''),
        "facebook_detail": member_info.get("facebook_detail", ''),
        "whatsapp_detail": member_info.get("whatsapp_detail", ''),
        "project_details":project_details,
        "approved_loan_amount": approval_data.get("approved_loan_amount", ""),
        "approved_loan_amount_words": approval_data.get("approved_loan_amount_words", ""),
        "approved_date_bs": convert_to_nepali_digits(approval_data.get("approval_date","")),
        **bs_parts, # <== Inject bs_year, bs_month, bs_day, bs_roj
        "dob_bs": dob_bs,
        "age": age_nep,
        "bs_year_lastdate": convert_to_nepali_digits(loan_info.get("loan_completion_year", "")),
        "bs_month_lastdate": convert_to_nepali_digits(loan_info.get("loan_completion_month", "")),
        "bs_day_lastdate": convert_to_nepali_digits(loan_info.get("loan_completion_day", "")),
        "witnesses": witnesses
        
    }
    print("🔑 Context Keys Available:", context.keys())
    print("✅ Approved Date BS:", repr(context.get("approved_date_bs")))

    print ("Collateral Basic:", collateral_basic)
     # 🧪 Print affiliation data for debugging
    print("🧪 Affiliation Data:")
    
    for aff in affiliations:
        print(aff)

    # Print properties details
    print("Properties Data:")
    for property in properties:
        print(property)

    

    return context

    
   