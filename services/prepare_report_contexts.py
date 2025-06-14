from services.report_fetchers import (
    fetch_member_info,
    fetch_loan_info,
    fetch_collateral_basic,
    fetch_collateral_affiliations,
    fetch_collateral_properties,
    fetch_collateral_family_details,
    fetch_income_expense
)

def prepare_report_context(member_number):
    member_info = fetch_member_info(member_number)
    loan_info = fetch_loan_info(member_number)
    collateral_basic = fetch_collateral_basic(member_number)

    affiliations = fetch_collateral_affiliations(member_number)
    properties = fetch_collateral_properties(member_number)
    family = fetch_collateral_family_details(member_number)
    income_expense = fetch_income_expense(member_number)

    income = [item for item in income_expense if item["type"] == "income"]
    expense = [item for item in income_expense if item["type"] == "expense"]

    context = {
        **member_info,
        **loan_info,
        **collateral_basic,
        "affiliations": affiliations,
        "properties": properties,
        "family_details": family,
        "monthly_income": income,
        "monthly_expense": expense
    }
    return context