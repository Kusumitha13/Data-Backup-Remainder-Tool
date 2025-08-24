import streamlit as st
import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from datetime import time as dtime
import shutil

# Load environment variables
load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# Streamlit Page Setup
st.set_page_config(page_title="Backup Reminder Tool", layout="centered")
# Load external CSS for styling
with open("light_theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💾 Data Backup Reminder Tool")

# Sidebar Tabs
tabs = ["Settings", "Manual Backup", "View Logs"]
selected_tab = st.sidebar.radio("📁 Select an Option", tabs)



# ------------------ TAB 1: Settings ------------------
if selected_tab == "Settings":
    st.subheader("⚙️ Configure or Edit Backup Settings")

    try:
        conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM backup_settings LIMIT 1")
        result = cursor.fetchone()

        if result:
            st.success("✅ Existing settings found. You can update or delete them below:")

            st.markdown("### 📁 Enter Folder/File Names Only (Inside Documents)")
            base_dir = os.path.expanduser("~\\Documents")

            src_folder_name = st.text_input("📝 Source Folder/File Name")
            dst_folder_name = st.text_input("📥 Backup Destination Folder Name")

            folder_path = os.path.join(base_dir, src_folder_name)
            backup_folder = os.path.join(base_dir, dst_folder_name)

            st.code(f"🔍 Full Source Path: {folder_path}")
            st.code(f"🔍 Full Destination Path: {backup_folder}")

            frequency = st.selectbox("⏱️ Backup Frequency", ["Daily", "Weekly"], index=["Daily", "Weekly"].index(result[3]))

            # Convert timedelta to time object for Streamlit
            backup_time_raw = result[4]
            backup_time_obj = (datetime.min + backup_time_raw).time()
            backup_time = st.time_input("🕒 Reminder Time", value=backup_time_obj)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Settings"):
                    cursor.execute("DELETE FROM backup_settings")
                    cursor.execute(
                        """
                        INSERT INTO backup_settings (folder_path, backup_folder, backup_frequency, backup_time)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (folder_path, backup_folder, frequency, backup_time),
                    )
                    conn.commit()
                    st.success("✅ Settings updated successfully!")

            with col2:
                if st.button("🗑️ Delete Settings"):
                    cursor.execute("DELETE FROM backup_settings")
                    conn.commit()
                    st.warning("⚠️ Backup settings have been deleted. Please reconfigure.")

        else:
            st.info("No existing settings. Please add new settings below:")
            folder_path = st.text_input("📂 Folder to Back Up")
            backup_folder = st.text_input("📥 Backup Destination Folder")
            frequency = st.selectbox("⏱️ Backup Frequency", ["Daily", "Weekly"])
            time_str = st.text_input("🕒 Reminder Time (HH:MM)", value="10:30")
            try:
                backup_time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                st.error("❌ Please enter time in HH:MM format.")
                backup_time = None


            if st.button("Save Settings"):
                cursor.execute(
                    """
                    INSERT INTO backup_settings (folder_path, backup_folder, backup_frequency, backup_time)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (folder_path, backup_folder, frequency, backup_time),
                )
                conn.commit()
                st.success("✅ Settings saved successfully!")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")



# ---------------- TAB 2: Manual Backup ----------------
# ---------------- TAB 2: Manual Backup ----------------
elif selected_tab == "Manual Backup":
    st.subheader("🧠 Manual Backup")

    try:
        conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database
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
                "backup_time": result[4],
            }

            st.write(f"🗂️ Default Source Folder: {settings['folder_path']}")
            st.write(f"📥 Default Backup Destination: {settings['backup_folder']}")

            # 👇 Optional override input
            st.markdown("### ✏️ Optional: Change Source and Destination Below")
            st.markdown("### ✏️ Optional: Enter Folder/File Names Only (Inside Documents)")
            custom_src_name = st.text_input("📝 Custom Source Folder/File Name (optional)")
            custom_dst_name = st.text_input("📥 Custom Destination Folder Name (optional)")

            base_dir = os.path.expanduser("~\\Documents")
            custom_src = os.path.join(base_dir, custom_src_name) if custom_src_name else ""
            custom_dest = os.path.join(base_dir, custom_dst_name) if custom_dst_name else ""

            if st.button("Run Manual Backup Now"):
                try:
                    src = custom_src if custom_src else settings["folder_path"]
                    dest_root = custom_dest if custom_dest else settings["backup_folder"]
                    dest = os.path.join(dest_root, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

                    shutil.copytree(src, dest)
                    status = "Success"
                    message = "Manual backup completed successfully."
                    st.success("✅ Backup completed successfully!")

                except Exception as e:
                    status = "Failed"
                    message = f"Manual backup failed: {e}"
                    st.error(f"❌ Backup failed: {e}")

                # Log to DB
                cursor.execute(
                    """
                    INSERT INTO backup_logs (folder_path, backup_time, status, mode, message)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        src,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        status,
                        "Manual",
                        message,
                    )
                )
                conn.commit()
        else:
            st.info("No settings found. Please configure first.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")




# ---------------- TAB 3: View Logs ----------------
# ---------------- TAB 3: View Logs ----------------
elif selected_tab == "View Logs":
    st.subheader("📜 Backup & Reminder Logs")

    try:
        conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM backup_logs ORDER BY backup_time DESC")
        logs = cursor.fetchall()

        if logs:
            # ✅ Match column count exactly
            df = pd.DataFrame(logs, columns=["id", "folder_path", "backup_time", "status", "mode", "message"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No logs found yet.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")