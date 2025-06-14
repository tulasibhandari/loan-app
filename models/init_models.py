# models/init_models.py
from models.database import initialize_db
from models.user_model import create_user_table
from models.loan_scheme_model import create_loan_scheme_table

def initialize_all():
    initialize_db()
    create_user_table()
    create_loan_scheme_table()
    
