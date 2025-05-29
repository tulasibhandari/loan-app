from models.database import get_connection


def save_collateral_info(data: dict):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS collateral_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                       monthly_saving TEXT,
                       child_saving TEXT,
                       total_saving TEXT )
                    """)
        
        cursor.execute("""
            INSERT INTO collateral_info (
                monthly_saving,
                child_saving,
                total_saving
            ) VALUES (?, ?, ?)
        """, (
            data['monthly_saving'],
            data['child_saving'],
            data['total_saving']
        ))

        conn.commit()
        conn.close()
        print("✅ Collateral info saved to database.")
    except Exception as e:
        print("❌ Error saving collateral info:", e)