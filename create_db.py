import sqlite3

# database file create / open
db = sqlite3.connect("database.db")

# cursor create
cur = db.cursor()

# users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT
)
""")

# tasks table
cur.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT,
    done INTEGER DEFAULT 0
)
""")

# save changes
db.commit()

# close database
db.close()

print("✅ Database created successfully")
