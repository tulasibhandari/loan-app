# context.py

current_session = {
    'member_number': '',
    'member_name': '',
    "loan_type": "", 
}

def clear_session():
    global current_session
    current_session.clear()