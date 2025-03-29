from flask import Flask, render_template
from flask_socketio import SocketIO
import socket
import threading
import atexit
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# UDP Socket setup for JSON data
UDP_IP = "127.0.0.1"
UDP_PORT = 15559

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

# Cleanup on exit
@atexit.register
def cleanup():
    udp_socket.close()
    print("UDP connection closed.")

# Background thread to read UDP messages
def read_udp():
    try:
        print(f"⚡ UDP server actively listening on 127.0.0.1:15559")
        while True:
            data, addr = udp_socket.recvfrom(1024)
            print(f"📦 Raw {len(data)}-byte packet from {addr}")
            try:
                json_data = json.loads(data.decode())
                print(f"📊 JSON received:", json.dumps(json_data, indent=2))
                processed_data = process_json_message(json_data)
                socketio.emit("mavlink_data", processed_data)
            except Exception as e:
                print(f"❌ Decoding error: {e}\nRaw data: {data[:50]}...")
    except Exception as e:
        print(f"💥 UDP thread crashed: {e}")

        
# Process JSON messages
def process_json_message(json_data):
    # Convert your JSON structure to match what your frontend expects
    processed = {
        "mavpackettype": json_data.get("mavpackettype", "UNKNOWN"),
        "roll": json_data.get("roll", 0),
        "pitch": json_data.get("pitch", 0),
        "yaw": json_data.get("yaw", 0),
        "alt": json_data.get("altitude", 0),
        "lat": json_data.get("lat", 0),
        "lng": json_data.get("lng", 0)
    }
    return processed

# Route for frontend
@app.route('/')
def index():
    return render_template('index.html')

# Start UDP reading thread
udp_thread = threading.Thread(target=read_udp)
udp_thread.daemon = True
udp_thread.start()

# Run the Flask server
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5001, debug=True, use_reloader=False)