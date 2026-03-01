import sqlite3
import bcrypt

DB_FILE = "users.db"

def create_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    # Example table for mental health metrics
    c.execute('''
        CREATE TABLE IF NOT EXISTS mental_health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            stress_level INTEGER,
            mood INTEGER,
            anxiety_level INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, role='user'):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
              (username, hashed, role))
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT password, role FROM users WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    if result:
        hashed, role = result
        if bcrypt.checkpw(password.encode(), hashed):
            return True, role
    return False, None

def add_mental_health_entry(username, date, stress, mood, anxiety):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO mental_health (username, date, stress_level, mood, anxiety_level)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, date, stress, mood, anxiety))
    conn.commit()
    conn.close()

def get_user_entries(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT date, stress_level, mood, anxiety_level FROM mental_health WHERE username=? ORDER BY date', (username,))
    data = c.fetchall()
    conn.close()
    return data

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, username, role FROM users')
    users = c.fetchall()
    conn.close()
    return users
