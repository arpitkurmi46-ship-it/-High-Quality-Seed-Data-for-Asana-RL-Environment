import sqlite3

DB_PATH = "output/asana_simulation.sqlite"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# print schema info
cursor.execute("PRAGMA table_info(task_events);")
cols = cursor.fetchall()

print("TASK_EVENTS COLUMNS:")
for col in cols:
    print(col)

conn.close()
