import socket
import paramiko
import threading
import logging
import requests
import sqlite3
from datetime import datetime

logging.basicConfig(
    filename="honeypot.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)
HOST = "0.0.0.0"
PORT = 2222

SERVER_KEY = paramiko.RSAKey.generate(2048)

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        country = data.get("country", "Unknown")
        city = data.get("city", "Unknown")
        isp = data.get("isp", "Unknown")
        return f"{city}, {country} | ISP: {isp}"
    except:
        return "Location unavailable"
    
def init_db():
    conn = sqlite3.connect("honeypot.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            username TEXT,
            password TEXT,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_attack(ip, username, password, location):
    conn = sqlite3.connect("honeypot.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO attacks (timestamp, ip, username, password, location)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip, username, password, location))
    conn.commit()
    conn.close()

class SSHHoneypot(paramiko.ServerInterface):
    
    def check_auth_password(self, username, password):
        logging.info(f"Login attempt - Username: {username} Password: {password}")
        log_attack(self.client_ip, username, password, self.location)
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def handle_connection(client, addr):
    location = get_location(addr[0])
    logging.info(f"New connection from: {addr[0]} | Location: {location}")
    
    transport = paramiko.Transport(client)
    transport.add_server_key(SERVER_KEY)
    
    server = SSHHoneypot()
    server.client_ip = addr[0]
    server.location = location
    transport.start_server(server=server)

def start_honeypot():
    init_db()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(100)
    
    print(f"SSH Honeypot listening on port {PORT}...")
    logging.info(f"Honeypot started on port {PORT}")
    while True:
        client, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(client, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_honeypot()