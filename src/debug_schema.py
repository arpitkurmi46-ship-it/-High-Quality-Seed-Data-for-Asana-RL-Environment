import sqlite3

DB_PATH = "output/asana_simulation.sqlite"
conn = sqlite3.connect(DB_PATH)

tables = ["organizations", "projects", "sections", "users", "tasks"]

for t in tables:
    print(f"\n=== {t.upper()} SCHEMA ===")
    rows = conn.execute(f"PRAGMA table_info({t});").fetchall()
    for row in rows:
        print(row)

conn.close()
