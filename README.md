# 🍯 OpenTrap — Open Source Honeypot Platform

A dual-protocol SSH and HTTP honeypot platform built from scratch in Python that traps, logs, and analyzes real-world attackers with a live auto-refreshing dashboard.

## 🌍 Real Attack Data
This honeypot was deployed on AWS EC2 and captured real attacks within hours of deployment — including SSH brute force attempts from automated bots across multiple countries.

## 🏗️ Architecture
- **SSH Honeypot** — Emulates an SSH server on port 2222, captures attacker IPs, credentials, and client fingerprints
- **HTTP Honeypot** — Serves a fake admin login page on port 8080, captures credentials and attacker browser fingerprints
- **Live Dashboard** — Flask web app showing all attacks in real time, auto-refreshes every 30 seconds
- **SQLite Database** — Stores all attack data persistently
- **Geolocation** — Maps attacker IPs to country, city, and ISP using ip-api.com

## 🛠️ Technologies Used
- Python 3
- Paramiko (SSH protocol emulation)
- Flask (HTTP honeypot + dashboard)
- SQLite3 (attack logging database)
- Requests (IP geolocation)
- AWS EC2 (cloud deployment)

## 📊 What Gets Captured
- Attacker IP address
- Geolocation (city, country, ISP)
- Usernames and passwords attempted
- SSH client fingerprint
- Browser user agent
- URLs/paths probed
- Timestamps of all events

## 🚀 How to Run Locally

### Prerequisites
- Python 3.x
- pip

### Installation
```bash
git clone https://github.com/kavyasrimanda03/OpenTrap.git
cd OpenTrap
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install paramiko flask requests
```

### Run the honeypots
```bash
# Terminal 1 - SSH Honeypot
python ssh_honeypot.py

# Terminal 2 - HTTP Honeypot
python http_honeypot.py

# Terminal 3 - Dashboard
python dashboard.py
```

### Access
- SSH Honeypot: port 2222
- HTTP Honeypot: http://localhost:8080/wp-admin
- Dashboard: http://localhost:5000

## ⚠️ Legal Disclaimer
This tool is intended for educational and research purposes only. Only deploy on infrastructure you own. Do not use to intercept unauthorized traffic.

## 📝 Author
Kavya Sri Reddy Manda — MS Cybersecurity, University of Delaware
