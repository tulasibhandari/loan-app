from nepali_datetime import date as nepali_date

def calculate_nepali_age(dob_str):
    """
    Calculate age in years from B.S. DOB string (e.g., '2055-04-23')
    """
    try:
        year, month, day = map(int, dob_str.split("-"))
        dob = nepali_date(year, month, day)
        today = nepali_date.today()
        age = today.year - dob.year
        
        # Adjust if birthday hasn't occured yet this year
        if (today.month, today.day)<(dob.month, dob.day):
            age =- 1
        return age
    except Exception as e:
        print("Failed to calculate age:", e )
        return ""