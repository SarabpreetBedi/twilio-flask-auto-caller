import sqlite3

def init_db():
    conn = sqlite3.connect('calls.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS calls (
            sid TEXT PRIMARY KEY,
            number TEXT,
            call_id TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_call_start(sid, number, call_id):
    conn = sqlite3.connect('calls.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO calls (sid, number, call_id, status) VALUES (?, ?, ?, ?)", 
              (sid, number, call_id, 'initiated'))
    conn.commit()
    conn.close()

def update_status(sid, status):
    conn = sqlite3.connect('calls.db')
    c = conn.cursor()
    c.execute("UPDATE calls SET status=? WHERE sid=?", (status, sid))
    conn.commit()
    conn.close()

def get_all_calls():
    conn = sqlite3.connect('calls.db')
    c = conn.cursor()
    c.execute("SELECT * FROM calls")
    rows = c.fetchall()
    conn.close()
    return rows
