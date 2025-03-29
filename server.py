from flask import Flask, render_template
from flask_socketio import SocketIO
from pymavlink import mavutil
import threading
import atexit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Establish MAVLink connection
try:
    mav_connection = mavutil.mavlink_connection('udp:127.0.0.1:15559', reuse=True)
    print("MAVLink connected to UDP:15559")
except Exception as e:
    print(f"MAVLink failed: {e}")
    exit(1)

# Cleanup on exit
@atexit.register
def cleanup():
    mav_connection.close()
    print("MAVLink connection closed.")

# Background thread to read MAVLink messages
def read_mavlink():
    try:
        while True:
            msg = mav_connection.recv_match(blocking=True)
            if msg:
                data = process_mavlink_message(msg)
                if data:
                    socketio.emit("mavlink_data", data)
    except Exception as e:
        print(f"MAVLink thread crashed: {e}")

# Process MAVLink messages and extract relevant data
def process_mavlink_message(msg):
    data = {"mavpackettype": msg.get_type()}
    
    if msg.get_type() == "AHRS2" or msg.get_type() == "AHRS3":
        data["roll"] = msg.roll
        data["pitch"] = msg.pitch
        data["yaw"] = msg.yaw
    elif msg.get_type() == "VFR_HUD":
        data["airspeed"] = msg.airspeed
        data["groundspeed"] = msg.groundspeed
        data["alt"] = msg.alt
        data["heading"] = msg.heading
        data["climb"] = msg.climb
    elif msg.get_type() == "GLOBAL_POSITION_INT":
        data["lat"] = msg.lat / 1e7
        data["lng"] = msg.lon / 1e7
        data["alt"] = msg.alt / 1000

    return data

# Route for frontend
@app.route('/')
def index():
    return render_template('index.html')

# Start MAVLink reading thread
mav_thread = threading.Thread(target=read_mavlink)
mav_thread.daemon = True
mav_thread.start()

# Run the Flask server
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)
