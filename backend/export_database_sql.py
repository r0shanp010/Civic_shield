import sqlite3
import os

db_path = r"C:\Users\FIFA 2022\.gemini\antigravity\scratch\civicshield\backend\civicshield.db"
root_sql_path = r"C:\Users\FIFA 2022\.gemini\antigravity\scratch\civicshield\civicshield_database.sql"
backend_sql_path = r"C:\Users\FIFA 2022\.gemini\antigravity\scratch\civicshield\backend\civicshield_database.sql"
public_sql_path = r"C:\Users\FIFA 2022\.gemini\antigravity\scratch\civicshield\frontend\public\civicshield_database.sql"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables in order
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = [r[0] for r in cursor.fetchall()]

sql_lines = []
sql_lines.append("-- ==============================================================================")
sql_lines.append("-- CIVICSHIELD: AI-BASED ANONYMOUS CORRUPTION & BRIBERY COMPLAINT MANAGEMENT SYSTEM")
sql_lines.append("-- MCA Major Project Database Schema & Seed Data Export (.sql)")
sql_lines.append("-- Platform: Anti-Corruption Grievance Redressal & TF-IDF Machine Learning Triage")
sql_lines.append("-- ==============================================================================\n")
sql_lines.append("PRAGMA foreign_keys = ON;\n")

# Order tables logically (parent tables first)
ordered_tables = [
    'users', 
    'admin_users', 
    'complaints', 
    'evidence', 
    'ai_predictions', 
    'complaint_updates', 
    'assignments', 
    'audit_logs', 
    'case_actions'
]

# Add any additional tables found
for t in tables:
    if t not in ordered_tables:
        ordered_tables.append(t)

for table in ordered_tables:
    if table not in tables:
        continue
        
    sql_lines.append(f"-- ------------------------------------------------------------------------------")
    sql_lines.append(f"-- Table Structure for `{table}`")
    sql_lines.append(f"-- ------------------------------------------------------------------------------")
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';")
    res = cursor.fetchone()
    if res and res[0]:
        create_sql = res[0]
        sql_lines.append(f"{create_sql};\n")
    
    # Get table data
    cursor.execute(f"SELECT * FROM `{table}`;")
    rows = cursor.fetchall()
    
    if rows:
        cursor.execute(f"PRAGMA table_info(`{table}`);")
        columns = [col[1] for col in cursor.fetchall()]
        col_str = ", ".join([f"`{c}`" for c in columns])
        
        sql_lines.append(f"-- Dumping data for table `{table}` ({len(rows)} records)")
        for row in rows:
            val_strs = []
            for v in row:
                if v is None:
                    val_strs.append("NULL")
                elif isinstance(v, (int, float)):
                    val_strs.append(str(v))
                else:
                    escaped_v = str(v).replace("'", "''")
                    val_strs.append(f"'{escaped_v}'")
            val_str = ", ".join(val_strs)
            sql_lines.append(f"INSERT INTO `{table}` ({col_str}) VALUES ({val_str});")
        sql_lines.append("")

full_sql_content = "\n".join(sql_lines)

# Write to root project folder
with open(root_sql_path, "w", encoding="utf-8") as f:
    f.write(full_sql_content)

# Write to backend folder
with open(backend_sql_path, "w", encoding="utf-8") as f:
    f.write(full_sql_content)

# Write to frontend public folder
with open(public_sql_path, "w", encoding="utf-8") as f:
    f.write(full_sql_content)

print("SUCCESS: SQL Database file created successfully at:")
print(f"1. Project Root:   {root_sql_path}")
print(f"2. Backend Folder: {backend_sql_path}")
print(f"3. Public Assets:  {public_sql_path}")
