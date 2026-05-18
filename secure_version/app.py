from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    hashed_pw = generate_password_hash('admin123')
    c.execute("INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
              ('admin', hashed_pw))
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def logic():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        return "Username and password are required.", 400
    if len(username) > 50 or len(password) > 50:
        return "Input too long.", 400

    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    query = "SELECT username, password_hash FROM users WHERE username=?"
    c.execute(query, (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        return "Login successful!"
    else:
        return "Login failed. Invalid credentials.", 401
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')
