from models.user_model import create_user_table, add_user

# ✅ Create the table if it doesn't exist
create_user_table()

# ✅ Then add your admin user
add_user("admin", "admin", role="admin", post="System Administrator", full_name_nepali="एडमिन")
