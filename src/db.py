import sqlite3

def get_connection(path):
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def execute_script(conn, script_path):
    with open(script_path, "r") as f:
        conn.executescript(f.read())
