import logging
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template_string, redirect

# ── Logging setup ──────────────────────────────────────────
logging.basicConfig(
    filename="honeypot.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

# ── Flask app ───────────────────────────────────────────────
app = Flask(__name__)

# ── Database ────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("honeypot.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS http_attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            username TEXT,
            password TEXT,
            user_agent TEXT,
            path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_attack(ip, username, password, user_agent, path):
    conn = sqlite3.connect("honeypot.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO http_attacks (timestamp, ip, username, password, user_agent, path)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip, username, password, user_agent, path))
    conn.commit()
    conn.close()
    logging.info(f"HTTP Attack - IP: {ip} | Username: {username} | Password: {password} | Path: {path} | Agent: {user_agent}")

# ── Fake login page HTML ─────────────────────────────────────
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #1a1a2e; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: Arial, sans-serif; }
        .login-box { background: #16213e; padding: 40px; border-radius: 8px; width: 350px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
        .login-box h2 { color: #e94560; text-align: center; margin-bottom: 30px; }
        .login-box input { width: 100%; padding: 12px; margin: 8px 0; background: #0f3460; border: none; border-radius: 4px; color: white; font-size: 14px; }
        .login-box button { width: 100%; padding: 12px; margin-top: 15px; background: #e94560; border: none; border-radius: 4px; color: white; font-size: 16px; cursor: pointer; }
        .login-box button:hover { background: #c73652; }
        .error { color: #e94560; text-align: center; margin-top: 10px; font-size: 13px; }
        .logo { text-align: center; color: #888; margin-bottom: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">⚙️ SYSTEM ADMINISTRATION</div>
        <h2>Admin Login</h2>
        <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" />
        <input type="password" name="password" placeholder="Password" />
        <button type="submit">Login</button>
        </form>
        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

# ── Routes ───────────────────────────────────────────────────
@app.route("/")
@app.route("/admin")
@app.route("/admin/login")
@app.route("/wp-admin")
@app.route("/login")
def login_page():
    error = request.args.get("error")
    msg = "Invalid credentials. Please try again." if error else None
    logging.info(f"HTTP Visit - IP: {request.remote_addr} | Path: {request.path} | Agent: {request.headers.get('User-Agent')}")
    return render_template_string(LOGIN_PAGE, error=msg)

@app.route("/login", methods=["POST"])
def handle_login():
    ip = request.remote_addr
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    user_agent = request.headers.get("User-Agent", "Unknown")
    path = request.path

    log_attack(ip, username, password, user_agent, path)

    return redirect("/admin?error=1")

# ── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("HTTP Honeypot running on port 8080...")
    app.run(host="0.0.0.0", port=8080, debug=False)