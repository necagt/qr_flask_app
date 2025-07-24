import sqlite3
import uuid

def init_db():
    conn = sqlite3.connect("veritabani.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_entry(name, description):
    entry_id = str(uuid.uuid4())
    conn = sqlite3.connect("veritabani.db")
    c = conn.cursor()
    c.execute("INSERT INTO entries (id, name, description) VALUES (?, ?, ?)",
              (entry_id, name, description))
    conn.commit()
    conn.close()
    return entry_id

def get_entry(entry_id):
    conn = sqlite3.connect("veritabani.db")
    c = conn.cursor()
    c.execute("SELECT name, description FROM entries WHERE id=?", (entry_id,))
    row = c.fetchone()
    conn.close()
    return row
