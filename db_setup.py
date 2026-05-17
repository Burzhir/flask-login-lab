import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",('admin', 'admin123'))

conn.commit()
conn.close()
print("Database and test user created.")
