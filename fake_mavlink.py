import socket
import time
import json
import random
import math

UDP_IP = "127.0.0.1"
UDP_PORT = 15559

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def generate_random_telemetry():
    """Generate realistic random drone telemetry data"""
    return {
        "mavpackettype": random.choice(["AHRS2", "AHRS3", "VFR_HUD", "GLOBAL_POSITION_INT"]),
        "roll": random.uniform(-15, 15),       # degrees (-15 to 15)
        "pitch": random.uniform(-10, 10),      # degrees (-10 to 10)
        "yaw": random.uniform(0, 360),         # degrees (0-360)
        "altitude": random.uniform(0, 100),     # meters
        "lat": 12.9716 + random.uniform(-0.01, 0.01),  # Small variations around Bangalore
        "lng": 77.5946 + random.uniform(-0.01, 0.01),
        "airspeed": random.uniform(0, 25),      # m/s
        "groundspeed": random.uniform(0, 23),   # m/s
        "heading": random.uniform(0, 360),      # degrees
        "climb": random.uniform(-2, 2)          # m/s
    }

while True:
    # Generate and send random data
    telemetry = generate_random_telemetry()
    sock.sendto(json.dumps(telemetry).encode(), (UDP_IP, UDP_PORT))
    
    # Print with color for better visibility
    print(f"\033[94mSent:\033[0m {json.dumps(telemetry, indent=2)}")
    
    # Random interval between 0.5-1.5 seconds
    time.sleep(random.uniform(0.5, 1.5))