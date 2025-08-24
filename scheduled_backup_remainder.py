import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
from plyer import notification
import time
import schedule

# Load environment variables
load_dotenv()

# Get DB credentials
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

def check_and_remind():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM backup_settings LIMIT 1")
        result = cursor.fetchone()

        if result:
            settings = {
                "id": result[0],
                "folder_path": result[1],
                "backup_folder": result[2],
                "backup_frequency": result[3],
                "backup_time": result[4]
            }

            now = datetime.now().strftime("%H:%M")
            backup_time_formatted = str(settings["backup_time"])[:5]

            print("Checking at:", now, "| Backup time is:", backup_time_formatted)

            if now == backup_time_formatted:
                notification.notify(
                    title="🔔 Backup Reminder",
                    message=f"Don't forget to back up: {settings['folder_path']}",
                    timeout=10
                )
                print("✅ Reminder shown!")

                # Log to database
                # Log to database with 'Reminder' mode
                # Log to database with mode and message
                insert_query = """
                    INSERT INTO backup_logs (folder_path, backup_time, status, mode, message)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    settings["folder_path"],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Success",
                    "Scheduled",
                    "Reminder shown to user."
                ))
                conn.commit()

            else:
                print("⏰ Not yet time.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("❌ Error:", err)

# Schedule to check every minute
schedule.every(1).minutes.do(check_and_remind)

print("🔁 Reminder service started. Waiting for backup time...")

while True:
    schedule.run_pending()
    time.sleep(1)