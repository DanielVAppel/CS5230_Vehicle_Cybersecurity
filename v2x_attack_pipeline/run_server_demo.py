# run_server_demo.py
from artery_tcp_server import ArteryTCPServer
from router import AttackRouter
from attacks import default_attacks

# No CARLA involved — we just print output
def print_output(msg):
    print("\n=== REAL MESSAGE RECEIVED ===")
    print(msg)

def print_spoofed(msg):
    print("\n>>> SPOOFED MESSAGE GENERATED >>>")
    print(msg)

router = AttackRouter(artery=None, carla=None, attacks=default_attacks())

def on_message(msg):
    # print real message
    print_output(msg)

    # generate spoofed messages
    spoofed = router._spoof(msg)
    for fake in spoofed:
        print_spoofed(fake)

# Start a TCP listener that waits for fake_artery_sender.py
server = ArteryTCPServer(host="0.0.0.0", port=9000, on_message=on_message)

print("Server started on port 9000. Waiting for messages...")
server.start()

import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    server.stop()
