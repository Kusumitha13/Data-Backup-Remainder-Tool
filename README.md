# 📂 Data Backup Reminder Tool  

A simple yet effective tool to *remind users to back up their important files* and provide manual backup options. Many people forget to back up their data and regret it later — this project helps avoid that situation by sending reminders and logging backup activities.  

---

##  Features  

- *🔔 Reminder Notifications* – Set when and how often you want to be reminded to back up.  
- *⚙️ Settings Tab* – Configure:  
  - Which folder should be backed up  
  - Backup destination  
  - Reminder time  
- *📦 Manual Backup* – Perform backups on demand by selecting source and destination.  
- *📜 View Logs* – Track all activities including:  
  - Reminder notifications (success/failure)  
  - Manual backups (success/failure)  
- *🗄️ MySQL Logging* – All reminders and manual backup events are stored in a database.  
- *🌐 Streamlit UI* – User-friendly web interface for easy interaction.  

---

##  Tech Stack  

- *Language*: Python  
- *Framework*: Streamlit  
- *Backend Database*: MySQL (via XAMPP)  
- *Libraries Used*:  
  - streamlit – Web UI framework  
  - dotenv – For environment variable management (DB credentials)  
  - os – File and directory operations  
  - mysql-connector – Database connection  
  - datetime – Managing reminder times  
  - plyer – Desktop notifications  
  - schedule – Task scheduling  
  - pandas – Viewing logs in tabular format  
  - shutil – File operations (copying backups)  

---
##  Prerequisites  

- Install *Python 3.8+*  
- Install *XAMPP* and ensure MySQL is running  

##  Setup Instructions  

1. *Clone the repository*  
   ```bash
   git clone https://github.com/Kusumitha13/data-backup-reminder.git

2. *navigate to folder*
  cd data-backup-reminder

3. *install dependencies*
  pip install streamlit mysql-connector-python python-dotenv plyer schedule pandas

4. *set up the database*
1.Open XAMPP and start MySQL.
2.Create a database (example: backup_logs).
3.Create a table for logs (use the SQL file if provided, or manually define columns).
4.Update your .env file with DB credentials.

5. *run the application*
streamlit run manual_backup_ui.py

---

##  Future Enhancements  

- *Background Notifications* – Currently, reminders only appear while the program is running. Future updates will allow notifications even when the program is not manually executed.  
- *Automated Backups* – Enable automatic backup execution when the reminder time arrives, instead of relying only on manual triggers.  
- *Cross-Platform Support* – Extend support for Mac/Linux in addition to Windows.  
- *Cloud Backup Integration* – Option to sync backups with Google Drive, OneDrive, or Dropbox.  

## Authors
-Kusumitha S
-Priyanka N
-Sowmya J
-Keerthana G

