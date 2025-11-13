# run_client_to_carla_api.py
from artery_client import ArteryClient
from attacks import default_attacks
from router import AttackRouter
from carla_api_bridge import CarlaAPIBridge

artery = ArteryClient(host="127.0.0.1", port=9000)
carla_api = CarlaAPIBridge()
router = AttackRouter(artery=artery, carla=None, attacks=default_attacks())

def apply_to_carla(msg):
    if msg.__class__.__name__ == "CAM":
        carla_api.handle_cam(msg)
    else:
        carla_api.handle_denm(msg)

for msg in artery.message_stream():
    apply_to_carla(msg)                 # real
    for fake in router._spoof(msg):     # spoofed
        apply_to_carla(fake)
