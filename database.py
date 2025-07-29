import sqlite3

# Create connection
conn = sqlite3.connect('plant_treasure.db')
cur = conn.cursor()

# Initialize tables
def init_db():
    cur.execute('''CREATE TABLE IF NOT EXISTS buy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_name TEXT,
        price REAL,
        quantity INTEGER,
        total REAL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS sell (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_name TEXT,
        price REAL,
        quantity INTEGER,
        total REAL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_name TEXT UNIQUE,
        quantity INTEGER)''')

    conn.commit()

# Export connection and cursor
def get_connection():
    return conn, cur
