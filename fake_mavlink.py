import socket
import time
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 14552

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    fake_data = {
        "mavpackettype": "AHRS2",
        "roll": -0.1,
        "pitch": -0.02,
        "yaw": 2.1,
        "altitude": 5.0,
        "lat": 12.9716,
        "lng": 77.5946
    }
    sock.sendto(json.dumps(fake_data).encode(), (UDP_IP, UDP_PORT))
    print(f"Sent: {fake_data}")
    time.sleep(1)


