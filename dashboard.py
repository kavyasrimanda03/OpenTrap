from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)
DB_PATH = "honeypot.db"

def get_ssh_attacks():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, ip, username, password, location FROM attacks ORDER BY timestamp DESC")
        attacks = cursor.fetchall()
        conn.close()
        return attacks
    except:
        return []

def get_http_attacks():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, ip, username, password, user_agent, path FROM http_attacks ORDER BY timestamp DESC")
        attacks = cursor.fetchall()
        conn.close()
        return attacks
    except:
        return []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OpenTrap Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: Arial, sans-serif; background: #0a0a0a; color: #00ff00; padding: 20px; }
        h1 { color: #00ff00; text-align: center; }
        h2 { color: #00ff00; margin-top: 40px; }
        .stats { display: flex; justify-content: center; gap: 40px; margin: 20px 0; }
        .stat-box { background: #111; border: 1px solid #00ff00; padding: 20px; text-align: center; border-radius: 8px; }
        .stat-box h2 { color: #00ff00; font-size: 2em; margin: 0; }
        .stat-box p { color: #888; margin: 5px 0 0 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { background: #111; color: #00ff00; padding: 12px; text-align: left; border-bottom: 1px solid #00ff00; }
        td { padding: 10px; border-bottom: 1px solid #222; color: #ccc; }
        tr:hover { background: #111; }
        .refresh { text-align: center; color: #444; font-size: 12px; margin-top: 10px; }
        .section-ssh { border-left: 3px solid #00ff00; padding-left: 10px; }
        .section-http { border-left: 3px solid #e94560; padding-left: 10px; }
        .badge-ssh { background: #00ff00; color: black; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
        .badge-http { background: #e94560; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
    </style>
</head>
<body>
    <h1>🍯 OpenTrap Honeypot Dashboard</h1>
    <p class="refresh">Auto-refreshes every 30 seconds</p>

    <div class="stats">
        <div class="stat-box">
            <h2>{{ total_ssh }}</h2>
            <p>SSH Attacks</p>
        </div>
        <div class="stat-box">
            <h2>{{ total_http }}</h2>
            <p>HTTP Attacks</p>
        </div>
        <div class="stat-box">
            <h2>{{ unique_ips }}</h2>
            <p>Unique Attackers</p>
        </div>
    </div>

    <h2 class="section-ssh">🔒 SSH Attacks <span class="badge-ssh">SSH</span></h2>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>IP Address</th>
            <th>Username</th>
            <th>Password</th>
            <th>Location</th>
        </tr>
        {% for attack in ssh_attacks %}
        <tr>
            <td>{{ attack[0] }}</td>
            <td>{{ attack[1] }}</td>
            <td>{{ attack[2] }}</td>
            <td>{{ attack[3] }}</td>
            <td>{{ attack[4] }}</td>
        </tr>
        {% endfor %}
    </table>

    <h2 class="section-http">🌐 HTTP Attacks <span class="badge-http">HTTP</span></h2>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>IP Address</th>
            <th>Username</th>
            <th>Password</th>
            <th>User Agent</th>
            <th>Path</th>
        </tr>
        {% for attack in http_attacks %}
        <tr>
            <td>{{ attack[0] }}</td>
            <td>{{ attack[1] }}</td>
            <td>{{ attack[2] }}</td>
            <td>{{ attack[3] }}</td>
            <td>{{ attack[4] }}</td>
            <td>{{ attack[5] }}</td>
        </tr>
        {% endfor %}
    </table>

</body>
</html>
"""

@app.route("/")
def index():
    ssh_attacks = get_ssh_attacks()
    http_attacks = get_http_attacks()
    total_ssh = len(ssh_attacks)
    total_http = len(http_attacks)
    all_ips = set(a[1] for a in ssh_attacks) | set(a[1] for a in http_attacks)
    unique_ips = len(all_ips)

    return render_template_string(HTML_TEMPLATE,
                                   ssh_attacks=ssh_attacks,
                                   http_attacks=http_attacks,
                                   total_ssh=total_ssh,
                                   total_http=total_http,
                                   unique_ips=unique_ips)

if __name__ == "__main__":
    app.run(debug=True, port=5000)