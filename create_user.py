from models.user_model import create_user_table, add_user

# ✅ Create the table if it doesn't exist
create_user_table()

# ✅ Then add your admin user
add_user("admin", "admin123", role="admin", post="System Administrator")
