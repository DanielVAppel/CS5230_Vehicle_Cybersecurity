# fake_artery_sender.py
"""
Tiny script that acts like Artery for demo/testing.
It connects to the Python server on localhost:9000 and sends a few CAM and DENM messages as JSON lines.
"""

import socket
import json
import time
import random

HOST = "127.0.0.1"
PORT = 9000

def make_cam(station_id: int, lat: float, lon: float):
    return {
        "msg_type": "CAM",
        "payload": {
            "station_id": station_id,
            "timestamp": time.time(),
            "lat": lat,
            "lon": lon,
            "speed": random.uniform(5.0, 25.0),
            "heading": random.uniform(0.0, 360.0),
        },
    }

def make_denm(station_id: int, lat: float, lon: float, event_type: str):
    return {
        "msg_type": "DENM",
        "payload": {
            "station_id": station_id,
            "timestamp": time.time(),
            "lat": lat,
            "lon": lon,
            "event_type": event_type,
            "severity": random.randint(1, 5),
        },
    }

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[fake_artery] Connected to {HOST}:{PORT}")

    # Send a few CAMs
    for i in range(3):
        msg = make_cam(station_id=1, lat=34.05 + i*0.0001, lon=-118.24)
        line = json.dumps(msg) + "\n"
        sock.sendall(line.encode("utf-8"))
        print(f"[fake_artery] Sent CAM {i+1}")
        time.sleep(0.5)

    # Send a few DENMs of different types
    for event in ["emergency_braking", "traffic_jam", "traction_loss"]:
        msg = make_denm(station_id=1, lat=34.05, lon=-118.24, event_type=event)
        line = json.dumps(msg) + "\n"
        sock.sendall(line.encode("utf-8"))
        print(f"[fake_artery] Sent DENM: {event}")
        time.sleep(0.5)

    print("[fake_artery] Done sending messages.")
    sock.close()

if __name__ == "__main__":
    main()
