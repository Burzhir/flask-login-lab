# Flask SQL Injection Lab

A deliberately vulnerable Flask login page built to demonstrate SQL injection
and secure coding practices. This project contains two versions:
- **Vulnerable** — exploitable login with multiple security issues
- **Secure** — the same app with all vulnerabilities fixed

---

## Vulnerabilities in the Vulnerable Version

### 1. SQL Injection (Critical)
The login query builds SQL using f-strings, allowing user input to become
part of the SQL command.

**Vulnerable code:**
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

**Exploit payloads:**
- `admin' --` — bypass password check
- `' OR 1=1 --` — login as first user
- `' UNION SELECT 1, username, password_hash FROM users --` — dump credentials

**Fix:** Parameterized queries using `?` placeholders

### 2. Plaintext Passwords (Critical)
Passwords stored as raw text in the database. An attacker who dumps the
database gets every user's real password.

**Fix:** Password hashing with Werkzeug's `generate_password_hash()` and
`check_password_hash()`

### 3. Username Enumeration via API (High)
The `/api/users` endpoint returns all usernames as JSON without authentication.
This gives attackers a valid user list for brute-force or targeted attacks.

**Fix:** Removed the endpoint entirely

### 4. Debug Mode Enabled (High)
`debug=True` exposes Python tracebacks and the Werkzeug debugger in the
browser. This leaks file paths, code snippets, and can lead to remote
code execution if the debug PIN is compromised.

**Fix:** Set `debug=False`

### 5. No Input Validation (Medium)
No checks on username/password length or content. Allows extremely long
inputs and potential denial-of-service.

**Fix:** Added length limits and empty input checks

---

## How to Run

### Vulnerable Version
cd vulnerable_version
pip install -r requirements.txt
python app.py
Visit http://127.0.0.1:5000

Try logging in with:
- Username: admin
- Password: admin123
- Then try: username: admin' --  password: anything

### Secure Version
cd secure_version
pip install -r requirements.txt
python app.py
Visit http://127.0.0.1:5000

The same SQL injection payloads will fail.

---

## Lessons Learned
- Never trust user input — always use parameterized queries
- Hash passwords; never store plaintext
- Disable debug mode in production
- Don't expose unnecessary API endpoints
- Validate all input before processing
- A simple f-string mistake can compromise an entire application

---

## Technologies
- Python 3
- Flask
- SQLite3
- Werkzeug (password hashing)
