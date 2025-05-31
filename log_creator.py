import os
import sqlite3
from datetime import datetime

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "lacziostr_logs.db")

LOGO = r"""
============================================================
  _                  _       ____  _             
 | |    __ _ _ __ __| | ___ / ___|| |_ ___  _ __ 
 | |   / _` | '__/ _` |/ _ \\___ \| __/ _ \| '__|
 | |__| (_| | | | (_| |  __/ ___) | || (_) | |   
 |_____\__,_|_|  \__,_|\___||____/ \__\___/|_|   
                                                 
                Laczi.ostr CLI Log
============================================================
"""

def create_table():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_time TEXT,
                user TEXT,
                session_id TEXT,
                description TEXT,
                command TEXT,
                status TEXT,
                additional_info TEXT
            )
        """)
    print("✅ Database and table ready.")

def insert_log_entry():
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    user = os.getenv("USER") or os.getenv("USERNAME") or "unknown_user"
    session_id = now.strftime("%Y%m%d%H%M%S")

    description = input("Description of the log entry: ")
    command = input("Command executed: ")
    status = input("Status (Success/Failure/Error): ")
    additional_info = input("Additional Info (optional): ")

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (date_time, user, session_id, description, command, status, additional_info)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (date_time, user, session_id, description, command, status, additional_info))
    print("✅ Log entry inserted into database.")

def export_log_entry_to_txt(log_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE id = ?", (log_id,))
        row = cursor.fetchone()
        if row:
            id, date_time, user, session_id, description, command, status, additional_info = row
            log_entry = f"""{LOGO}

Date: {date_time}
User: {user}
Session: {session_id}

------------------------------------------------------------
[INFO] Log Start
------------------------------------------------------------

[INFO] Description: {description}
[INFO] Command executed: {command}
[INFO] Status: {status}
[INFO] Additional Info: {additional_info}

------------------------------------------------------------
[INFO] Log End
------------------------------------------------------------

============================================================
"""
            filename = f"log_{id}_{session_id}.txt"
            with open(os.path.join(SCRIPT_DIR, filename), "w") as file:
                file.write(log_entry)
            print(f"✅ Log entry exported to {filename}")
        else:
            print("❌ Log entry not found.")

def main():
    create_table()
    while True:
        print("\n1. Add new log entry")
        print("2. Export log entry to TXT file")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            insert_log_entry()
        elif choice == "2":
            log_id = input("Enter the ID of the log entry to export: ")
            export_log_entry_to_txt(log_id)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
