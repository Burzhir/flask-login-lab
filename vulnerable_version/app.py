from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def logic():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"Running query: {query}")
    c.execute(query)
    user = c.fetchone()
    conn.close()
    if user:
        return "Login successful!"
    else:
        return "Login failed. Invalid credentials."


@app.route('/api/users')
def api_users():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    rows = c.fetchall()
    conn.close()

    usernames = [row[0] for row in rows]
    return jsonify({"users": usernames})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
