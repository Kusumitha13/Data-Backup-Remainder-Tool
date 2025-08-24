import os
import mysql.connector
from dotenv import load_dotenv

# Step 1: Load environment variables
load_dotenv()

# Step 2: Get the variables
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# Step 3: Connect to MySQL
try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("✅ Connected to MySQL successfully!")
except mysql.connector.Error as err:
    print("❌ MySQL connection error:", err)