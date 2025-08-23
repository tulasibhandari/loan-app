
from models.database import get_connection
import logging
import nepali_datetime
import sqlite3

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Try both possible table names
TABLE_NAME = "report_tracking"  # Default, change to "report_tracking" if needed

def save_report_log(data):
    logging.debug(f"Saving Report Log: {data}")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            INSERT INTO {TABLE_NAME} (member_number, report_type, file_path, generated_by, generated_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["member_number"],
            data["report_type"],
            data["file_path"],
            data["generated_by"],
            nepali_datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        logging.debug("Report log saved successfully")
    except sqlite3.Error as e:
        logging.error(f"Error saving report log: {e}")
        raise
    finally:
        conn.close()

def fetch_all_report_logs(date_filter=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if date_filter:
            cursor.execute(f"""
                SELECT member_number, report_type, file_path, generated_by, generated_date
                FROM {TABLE_NAME}
                WHERE date(generated_date) = ?
                ORDER BY generated_date DESC
            """, (date_filter,))
        else:
            cursor.execute(f"""
                SELECT member_number, report_type, file_path, generated_by, generated_date
                FROM {TABLE_NAME}
                ORDER BY generated_date DESC
            """)
        rows = cursor.fetchall()
        logs = [
            {
                "member_number": row[0],
                "report_type": row[1],
                "file_path": row[2],
                "generated_by": row[3],
                "date": row[4] if row[4] and ":" in row[4] else f"{row[4]} 00:00:00"
            } for row in rows
        ]
        logging.debug(f"Fetched {len(logs)} report logs with date_filter={date_filter}")
        return logs
    except sqlite3.Error as e:
        logging.error(f"Error fetching report logs: {e}")
        raise
    finally:
        conn.close()
