# run_server_to_carla_api.py
from artery_tcp_server import ArteryTCPServer
from router import AttackRouter
from attacks import default_attacks
from carla_api_bridge import CarlaAPIBridge  # your API bridge

carla_api = CarlaAPIBridge()
router = AttackRouter(artery=None, carla=None, attacks=default_attacks())

def apply_to_carla(msg):
    # Example dispatch; implement your real handlers inside the bridge
    if msg.__class__.__name__ == "CAM":
        carla_api.handle_cam(msg)
    else:
        carla_api.handle_denm(msg)

def on_message(msg):
    apply_to_carla(msg)                 # real
    for fake in router._spoof(msg):     # spoofed
        apply_to_carla(fake)

srv = ArteryTCPServer(host="0.0.0.0", port=9000, on_message=on_message)
srv.start()

try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    srv.stop()
