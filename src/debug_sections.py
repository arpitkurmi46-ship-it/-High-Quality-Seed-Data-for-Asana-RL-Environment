import sqlite3

DB_PATH = "output/asana_simulation.sqlite"

conn = sqlite3.connect(DB_PATH)

print("\n=== SECTIONS TABLE SCHEMA ===")
rows = conn.execute("PRAGMA table_info(sections);").fetchall()
for row in rows:
    print(row)

conn.close()
